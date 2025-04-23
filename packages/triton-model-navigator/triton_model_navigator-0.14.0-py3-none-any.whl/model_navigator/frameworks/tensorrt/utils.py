# Copyright (c) 2021-2024, NVIDIA CORPORATION. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""TensorRT utils."""

import contextlib
import os
import pathlib
import signal
from functools import lru_cache
from typing import Callable, List, Optional, Tuple, TypeVar, Union

import numpy as np
from loguru import logger
from packaging.version import Version

from model_navigator.configuration import ShapeTuple, TensorRTProfile, TensorType
from model_navigator.core.tensor import TensorMetadata, get_tensor_type
from model_navigator.exceptions import ModelNavigatorNotFoundError
from model_navigator.utils import common as utils
from model_navigator.utils import module
from model_navigator.utils.common import (
    invoke_if_callable,
    numpy_to_torch_dtype,
    optimal_batch_size,
    torch_to_numpy_dtype,
)

trt = module.lazy_import("tensorrt")
torch = module.lazy_import("torch")

T = TypeVar("T")


def get_version():
    """Get TensorRT version."""
    trt_version = Version(trt.__version__)
    return trt_version


def search_for_optimized_profiles(config, model_configs):
    """Check if search for optimized TensorRT profiles can be performed."""
    search = config.batch_dim is not None
    for model_cfg in model_configs:
        search = search and not model_cfg.trt_profiles
    return search


def get_trt_profile_from_trt_dynamic_axes(trt_dynamic_axes):
    """Create TensorRT profile from dynamic axes."""
    trt_profile = TensorRTProfile()
    if trt_dynamic_axes is None:
        return trt_profile
    for name, axes in trt_dynamic_axes.items():
        if axes:
            trt_profile.add(name, *list(zip(*list(axes.values()))))
    return trt_profile


def cast_type(dtype: np.dtype) -> np.dtype:
    """Cast type and return new dtype."""
    type_casts = _types_casts()
    if dtype in type_casts:
        return type_casts[dtype]

    return dtype


def _types_casts():
    try:
        is_int64_supported = get_version() >= Version("9.0")
    except AttributeError:
        logger.warning("TensorRT not found. Using default type casts including int64 to int32.")
        is_int64_supported = False

    if is_int64_supported:
        return {
            np.dtype(np.float64): np.dtype(np.float32),
            np.dtype(np.uint64): np.dtype(np.uint32),
        }
    else:
        return {
            np.dtype(np.int64): np.dtype(np.int32),
            np.dtype(np.float64): np.dtype(np.float32),
            np.dtype(np.uint64): np.dtype(np.uint32),
        }


def _cast_torch_tensor(tensor, dtype):
    type_casts = _types_casts()
    target_dtype = dtype or type_casts.get(np.dtype(torch_to_numpy_dtype(tensor.dtype)))
    if target_dtype:
        logger.debug(f"Casting {dtype} tensor to {target_dtype}.")
        return tensor.to(numpy_to_torch_dtype(target_dtype))
    return tensor


def _cast_numpy_tensor(tensor, dtype):
    type_casts = _types_casts()
    target_dtype = dtype or type_casts.get(tensor.dtype)
    if target_dtype:
        logger.debug(f"Casting {dtype} tensor to {target_dtype}.")
        return tensor.astype(target_dtype.type, copy=False)
    return tensor


def cast_tensor(tensor: T, dtype: Optional[np.dtype] = None) -> T:
    """Cast type and return tensor with new dtype."""
    if dtype is not None:
        assert isinstance(dtype, np.dtype)

    tensor_type = get_tensor_type(tensor)
    if tensor_type == TensorType.TORCH:
        return _cast_torch_tensor(tensor, dtype)
    else:
        assert tensor_type == TensorType.NUMPY
        return _cast_numpy_tensor(tensor, dtype)


def get_new_profile_with_static_batch_size(
    trt_profile: TensorRTProfile, batch_size: int, batch_dim: int
) -> TensorRTProfile:
    """Create new TensorRT profile with maximum batch size.

    Args:
        trt_profile (TensorRTProfile): TensorRT Profile.
        batch_size (int): new maximum batch size.
        batch_dim (int): Batch dimension.

    Returns:
        Profile: New TensoRT Profile.
    """
    new_profile = TensorRTProfile()
    for input_name in trt_profile:
        max_shapes = list(trt_profile[input_name].max)
        opt_shapes = list(trt_profile[input_name].opt)
        min_shapes = list(trt_profile[input_name].min)

        max_shapes[batch_dim] = batch_size
        opt_shapes[batch_dim] = batch_size
        min_shapes[batch_dim] = batch_size

        new_profile[input_name] = ShapeTuple(tuple(min_shapes), tuple(opt_shapes), tuple(max_shapes))
    return new_profile


def get_trt_profile_with_new_max_batch_size(
    trt_profile: TensorRTProfile, max_batch_size: int, batch_dim: int
) -> TensorRTProfile:
    """Create new TensorRT profile with maximum batch size.

    Args:
        trt_profile (TensorRTProfile): TensorRT Profile.
        max_batch_size (int): new maximum batch size.
        batch_dim (int): Batch dimension.

    Returns:
        Profile: New TensoRT Profile.
    """
    new_profile = TensorRTProfile()
    for input_name in trt_profile:
        max_shapes = list(trt_profile[input_name].max)
        opt_shapes = list(trt_profile[input_name].opt)

        max_shapes[batch_dim] = max_batch_size
        opt_shapes[batch_dim] = optimal_batch_size(max_batch_size)

        new_profile[input_name] = ShapeTuple(trt_profile[input_name].min, tuple(opt_shapes), tuple(max_shapes))
    return new_profile


def _should_use_v3_api():
    return Version(trt.__version__) > Version("8.5.0.9")


def get_bindings_per_profile(engine):
    """Return bindings per profile."""
    if _should_use_v3_api():
        logger.error("This function should not be called when using the V3 API")

    return engine.num_bindings // engine.num_optimization_profiles


def is_dimension_dynamic(dim) -> bool:
    """Return True if dimension is dynamic."""
    is_dim_str = not isinstance(dim, int)
    return dim is None or is_dim_str or dim < 0


def num_dynamic_dimensions(shape) -> int:
    """Return number of dynamic dimensions in shape."""
    return len([dim for dim in shape if is_dimension_dynamic(dim)])


def is_shape_dynamic(shape) -> bool:
    """Return True if shape is dynamic."""
    return num_dynamic_dimensions(shape) > 0


TRT_LOGGER = None


def get_trt_logger() -> "trt.Logger":
    """Get the global TensorRT logger.

    Returns:
        The TensorRT logger.
    """
    global TRT_LOGGER

    logger_type = trt.Logger
    if Version(trt.__version__) >= Version("8.0"):

        @lru_cache
        def get_log_level(severity):
            """Translates trt log level into loguru log level.

            Returns level only if it is WARNING or above to reduce TRT spam.

            Note:
            - loguru uses str levels.
            - when logging the log function cannot throw, so `critical` should not be mapped here!
            """
            log_level = {
                trt.Logger.INTERNAL_ERROR: "ERROR",
                trt.Logger.ERROR: "ERROR",
                trt.Logger.WARNING: "WARNING",
                trt.Logger.INFO: "INFO",
                trt.Logger.VERBOSE: "DEBUG",
            }.get(severity, "INFO")

            # emit log level only if the severity is WARNING or above, use int levels to compare
            if logger.level(log_level).no >= logger.level("WARNING").no:
                return log_level
            else:
                return None

        class CustomTrtLogger(trt.ILogger):
            def __init__(self):
                trt.ILogger.__init__(self)

            def log(self, severity, msg):
                try:
                    if log_level := get_log_level(severity):
                        logger.log(log_level, msg)
                except KeyboardInterrupt:
                    # `log()` is `noexcept` so we need to convert exceptions to signals so that
                    # ctrl-C will work as expected.
                    os.kill(os.getpid(), signal.SIGTERM)

        logger_type = CustomTrtLogger

    if TRT_LOGGER is None:
        TRT_LOGGER = logger_type()
    return TRT_LOGGER


class EngineFromBytes:
    """Functor that deserializes an engine from a buffer."""

    def __init__(self, serialized_engine: Union[Union[str, bytes], Callable]):
        """Deserializes an engine from a buffer.

        Args:
            serialized_engine: The serialized engine bytes  or a callable that returns them.
        """
        self._serialized_engine = serialized_engine

    def __call__(self, *args, **kwargs):
        """Invokes the loader by forwarding arguments to ``call_impl``.

        Note: ``call_impl`` should *not* be called directly - use this function instead.
        """
        return self.call_impl()

    def call_impl(self) -> "trt.ICudaEngine":
        """Implementation of ``__call__``.

        Returns: The deserialized engine.
        """
        buffer, owns_buffer = invoke_if_callable(self._serialized_engine)

        trt_logger = get_trt_logger()
        trt.init_libnvinfer_plugins(trt_logger, "")
        with contextlib.ExitStack() as stack, trt.Runtime(trt_logger) as runtime:
            if owns_buffer:
                try:
                    buffer.__enter__  # noqa: B018 IHostMemory is freed only in __exit__
                except AttributeError:
                    pass
                else:
                    stack.enter_context(buffer)

            engine = runtime.deserialize_cuda_engine(buffer)
            if not engine:
                raise ModelNavigatorNotFoundError("Could not deserialize engine. See log for details.")
            return engine


def np_dtype_from_trt(trt_dtype):
    """Convert a TensorRT dtype to a numpy dtype."""
    return np.dtype(trt.nptype(trt_dtype))


def add_binding_to_metadata(engine, binding, metadata, name_binding):
    """Add a binding to metadata."""
    if _should_use_v3_api():
        logger.error("This function should not be called when using the V3 API")

    # name_binding always comes from profile 0, since that's where we
    # get all binding names in the runner
    metadata.add(
        name=engine[name_binding],
        dtype=np_dtype_from_trt(engine.get_binding_dtype(binding)),
        shape=list(engine.get_binding_shape(binding)),
    )


def _get_input_metadata_from_engine(engine, start_binding, end_binding):
    """Returns input metadata from engine."""
    if _should_use_v3_api():
        logger.error("This function should not be called when using the V3 API")

    inputs = TensorMetadata()
    for index, binding in enumerate(range(start_binding, end_binding)):
        if engine.binding_is_input(binding):
            add_binding_to_metadata(engine, binding, inputs, name_binding=index)
    return inputs


def _get_output_metadata_from_engine(engine, start_binding, end_binding):
    """Returns input metadata from engine."""
    if _should_use_v3_api():
        logger.error("This function should not be called when using the V3 API")

    inputs = TensorMetadata()
    for index, binding in enumerate(range(start_binding, end_binding)):
        if engine.binding_is_output(binding):
            add_binding_to_metadata(engine, binding, inputs, name_binding=index)
    return inputs


def _get_metadata_from_engine(engine, mode):
    """Returns metadata from engine."""
    meta = TensorMetadata()
    for idx in range(engine.num_io_tensors):
        name = engine.get_tensor_name(idx)
        if engine.get_tensor_mode(name) != mode:
            continue
        # TODO: remove bfloat16 special case once torch.bfloat16 is supported
        dtype = engine.get_tensor_dtype(name)
        if dtype.name == "BF16":
            dtype = torch.bfloat16
        else:
            dtype = np_dtype_from_trt(engine.get_tensor_dtype(name))
        # meta.add(name=name, dtype=np_dtype_from_trt(engine.get_tensor_dtype(name)), shape=engine.get_tensor_shape(name))
        # meta.add(name=name, dtype=engine.get_tensor_dtype(name), shape=engine.get_tensor_shape(name))
        meta.add(name=name, dtype=dtype, shape=engine.get_tensor_shape(name))
    return meta


def get_active_profile_bindings(context):
    """Gets the start and end binding indices for the active optimization profile.

    Args:
        engine (trt.ICudaEngine): The engine in question.
        context (trt.IExecutionContext): The context where the profile is currently set.

    Returns:
        Tuple[int, int]: The start and end bindings indices, in that order
    """
    if _should_use_v3_api():
        logger.error("This function should not be called when using the V3 API")

    active_profile = context.active_optimization_profile
    if active_profile < 0:
        raise ModelNavigatorNotFoundError(
            f"Cannot determine profile bindings since the optimization profile for this context is set to: {active_profile}"
        )

    bindings_per_profile = get_bindings_per_profile(context.engine)

    start_binding = bindings_per_profile * active_profile
    end_binding = start_binding + bindings_per_profile

    logger.info(
        f"Total # of Profiles: {context.engine.num_optimization_profiles}, Bindings Per Profile: {bindings_per_profile}, "
        f"Active Profile: {active_profile}, Start Binding: {start_binding}, End Binding: {end_binding}"
    )
    return start_binding, end_binding


def get_input_metadata_impl(engine, context=None):
    """Implementation of get_input_metadata method.

    Returns:
        TensorMetadata: Input metadata.
    """
    if _should_use_v3_api():
        return _get_metadata_from_engine(engine, mode=trt.TensorIOMode.INPUT)
    else:
        start_binding, end_binding = get_active_profile_bindings(context)
        # This function always uses binding names of the 0th profile.
        return _get_input_metadata_from_engine(engine, start_binding, end_binding)


def get_output_metadate_impl(engine, context=None):
    """Implementation of get_output_metadata method.

    Returns:
        TensorMetadata: Output metadata.
    """
    if _should_use_v3_api():
        return _get_metadata_from_engine(engine, mode=trt.TensorIOMode.OUTPUT)
    else:
        start_binding, end_binding = get_active_profile_bindings(context)
        # This function always uses binding names of the 0th profile.
        return _get_output_metadata_from_engine(engine, start_binding, end_binding)


def get_tensorrt_io_names(model: pathlib.Path) -> Tuple[List, List]:
    """Collect inputs and outputs names from TensorRT model.

    Args:
        model: path to TensorRT model

    Returns:
        Tuple with lists of inputs and outputs names
    """
    engine_or_context = EngineFromBytes(utils.BytesFromPath(model.as_posix()))
    engine_or_context, owning = utils.invoke_if_callable(engine_or_context)

    if isinstance(engine_or_context, trt.ICudaEngine):
        engine = engine_or_context
        context = engine.create_execution_context()
        owns_engine = owning
        owns_context = True
        if not context:
            raise RuntimeError("Failed to create execution context")
    elif isinstance(engine_or_context, trt.IExecutionContext):
        context = engine_or_context
        engine = context.engine
        owns_context = owning
        owns_engine = False
    else:
        raise RuntimeError(
            "Invalid Engine or Context. Please ensure the engine was built correctly. See error log for details."
        )

    input_metadata = get_input_metadata_impl(engine, context)
    output_metadata = get_output_metadate_impl(engine, context)

    with contextlib.ExitStack() as stack:
        if owns_engine:
            stack.enter_context(engine)
        if owns_context:
            stack.enter_context(context)

    del (
        engine,
        owns_engine,
        context,
        owns_context,
    )

    return list(input_metadata.keys()), list(output_metadata.keys())
