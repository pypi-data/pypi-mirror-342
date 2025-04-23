# Copyright (c) 2023-2024, NVIDIA CORPORATION. All rights reserved.
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
"""Find Max Batch size pipelines builders."""

from typing import Dict, List

from model_navigator.configuration import DeviceKind, Format
from model_navigator.configuration.common_config import CommonConfig
from model_navigator.configuration.model.model_config import (
    ModelConfig,
)
from model_navigator.core.logger import LOGGER


def do_find_device_max_batch_size(config: CommonConfig, models_config: Dict[Format, List[ModelConfig]]) -> bool:
    """Verify find max batch size is required.

    Args:
        config: A configuration for pipelines
        models_config: List of model configs per format

    Returns:
        True if search is required, false, otherwise
    """
    model_formats = models_config.keys()
    adaptive_formats = {Format.TORCH_TRT, Format.TENSORRT, Format.TF_TRT, Format.TORCH_EXPORTEDPROGRAM}

    matching_formats = adaptive_formats.intersection(set(model_formats))
    if len(matching_formats) == 0 or config.target_device != DeviceKind.CUDA:
        LOGGER.debug("No matching formats found")
        return False

    run_search = config.batch_dim is not None

    if not run_search:
        LOGGER.debug("Run search disabled.")
        return False

    return True
