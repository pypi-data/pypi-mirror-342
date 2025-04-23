# Copyright (c) 2021-2023, NVIDIA CORPORATION. All rights reserved.
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
"""JAX optimize API."""

import pathlib
from typing import Any, Callable, Optional, Sequence, Tuple, Type, Union

from model_navigator.configuration import (
    DEFAULT_JAX_TARGET_FORMATS,
    CustomConfig,
    DeviceKind,
    Format,
    OptimizationProfile,
    SizedDataLoader,
    VerifyFunction,
    map_custom_configs,
)
from model_navigator.configuration.common_config import CommonConfig
from model_navigator.configuration.constants import DEFAULT_SAMPLE_COUNT
from model_navigator.configuration.model.model_config_builder import ModelConfigBuilder
from model_navigator.exceptions import ModelNavigatorConfigurationError
from model_navigator.frameworks import (
    Framework,
    is_tf_available,  # noqa: F401
)
from model_navigator.package.package import Package
from model_navigator.pipelines.builders import (
    correctness_builder,
    performance_builder,
    preprocessing_builder,
    verify_builder,
)
from model_navigator.pipelines.builders.find_device_max_batch_size import find_device_max_batch_size_builder
from model_navigator.pipelines.wrappers.optimize import optimize_pipeline
from model_navigator.runners.base import NavigatorRunner
from model_navigator.runners.utils import default_runners, filter_runners
from model_navigator.utils import enums

from .builders import jax_export_builder
from .model import JaxModel


def optimize(
    model: Callable,
    model_params: Any,
    dataloader: SizedDataLoader,
    sample_count: int = DEFAULT_SAMPLE_COUNT,
    batching: Optional[bool] = True,
    target_formats: Optional[Tuple[Union[str, Format], ...]] = None,
    target_device: Optional[DeviceKind] = DeviceKind.CUDA,
    runners: Optional[Tuple[Union[str, Type[NavigatorRunner]], ...]] = None,
    optimization_profile: Optional[OptimizationProfile] = None,
    workspace: Optional[pathlib.Path] = None,
    verbose: bool = False,
    debug: bool = False,
    verify_func: Optional[VerifyFunction] = None,
    custom_configs: Optional[Sequence[CustomConfig]] = None,
) -> Package:
    """Entry point for JAX optimize.

    Perform export, conversion, correctness testing, profiling and model verification.

    Args:
        model: JAX forward function
        model_params: JAX model parameters (weights)
        dataloader: Sized iterable with data that will be feed to the model
        sample_count: Limits how many samples will be used from dataloader
        batching: Enable or disable batching on first (index 0) dimension of the model
        target_formats: Target model formats for optimize process
        target_device: Target device for optimize process, default is CUDA
        runners: Use only runners provided as parameter
        optimization_profile: Optimization profile for conversion and profiling
        workspace: Workspace where packages will be extracted
        verbose: Enable verbose logging
        debug: Enable debug logging from commands
        verify_func: Function for additional model verification
        custom_configs: Sequence of CustomConfigs used to control produced artifacts

    Returns:
        Package descriptor representing created package.
    """
    if is_tf_available():
        import tensorflow  # pytype: disable=import-error

        if target_device == DeviceKind.CPU and any(
            device.device_type == "GPU" for device in tensorflow.config.get_visible_devices()
        ):
            raise ModelNavigatorConfigurationError(
                "\n"
                "    'target_device == nav.DeviceKind.CPU' is not supported for TensorFlow2 "
                "(exported from JAX) when GPU is available.\n"
                "    To optimize model for CPU, disable GPU with: "
                "'tf.config.set_visible_devices([], 'GPU')' directly after importing TensorFlow.\n"
            )
    if isinstance(model, str):
        model = pathlib.Path(model)

    if target_formats is None:
        target_formats = DEFAULT_JAX_TARGET_FORMATS

    if runners is None:
        runners = default_runners(device_kind=target_device)
    else:
        runners = filter_runners(runners, device_kind=target_device)

    if optimization_profile is None:
        optimization_profile = OptimizationProfile()

    target_formats_enums = enums.parse(target_formats, Format)
    runner_names = enums.parse(runners, lambda runner: runner if isinstance(runner, str) else runner.name())

    if Format.JAX not in target_formats_enums:
        target_formats_enums = (Format.JAX,) + target_formats_enums

    config = CommonConfig(
        Framework.JAX,
        model=JaxModel(model=model, params=model_params),
        dataloader=dataloader,
        target_formats=target_formats_enums,
        target_device=target_device,
        sample_count=sample_count,
        batch_dim=0 if batching else None,
        runner_names=runner_names,
        optimization_profile=optimization_profile,
        verbose=verbose,
        debug=debug,
        verify_func=verify_func,
        custom_configs=map_custom_configs(custom_configs=custom_configs),
    )

    models_config = ModelConfigBuilder.generate_model_config(
        framework=Framework.JAX,
        target_formats=target_formats_enums,
        custom_configs=custom_configs,
    )

    builders = [
        preprocessing_builder,
    ]

    if is_tf_available():
        from model_navigator.pipelines.builders import (
            tensorflow_conversion_builder,
            tensorflow_tensorrt_conversion_builder,
            tensorrt_conversion_builder,
        )

        builders += [
            jax_export_builder,
            find_device_max_batch_size_builder,
            tensorflow_conversion_builder,
            tensorflow_tensorrt_conversion_builder,
            tensorrt_conversion_builder,
        ]

    builders += [
        correctness_builder,
        performance_builder,
        verify_builder,
    ]
    package = optimize_pipeline(
        model=model,
        workspace=workspace,
        builders=builders,
        config=config,
        models_config=models_config,
    )

    return package
