# Copyright (c) 2023, NVIDIA CORPORATION. All rights reserved.
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

"""This module contains classes representing runner configurations."""

from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional

from model_navigator.utils.common import DataObject


class RunnerConfig(ABC, DataObject):
    """Abstract runner configuration class."""

    @classmethod
    @abstractmethod
    def from_dict(cls, data_dict: Dict):
        """Creates RunnerConfig from dictionary.

        Takes dictionary and use it to create appropriate RunnerConfig subclass.

        Args:
            data_dict: Dictionary with runner configuration data

        Returns:
            RunnerConfig
        """
        pass

    @abstractmethod
    def to_dict(self, parse: bool = False, *_, **__) -> dict:
        """Returns dictionary representation of the object.

        Args:
            parse: if True, converts parsable fields to string representation

        Returns:
            Dictionary representation of RunnerConfig
        """
        pass

    def get_config_dict_for_command(self) -> dict:
        """Returns dictionary with RunnerConfig data required for Command execution.

        Returns:
            Dictionary representation of RunnerConfig with unpacked params
        """
        return {**self.__dict__}

    @staticmethod
    def _parse_string(parse_func: Callable, val: Optional[str] = None):
        """Parses string with parse_func or returns None if val not provided."""
        if val:
            return parse_func(val)
        else:
            return None

    def _get_path_params_as_array_of_strings(self) -> List[str]:
        return []


class TorchRunnerConfig(RunnerConfig):
    """Torch runner configuration class."""

    def __init__(
        self,
        autocast: bool,
        inference_mode: bool,
        device: Optional[str],
        autocast_dtype: Optional[str] = None,
        custom_args: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initializes Torch runner configuration class.

        Args:
            autocast: Enable Automatic Mixed Precision in runner
            inference_mode: Enable inference mode in runner
            device: The target device on which mode has to be loaded
            autocast_dtype: The dtype to use for autocast
            custom_args: Additional keyword arguments used for model export and conversions
        """
        super().__init__()
        self.autocast = autocast
        self.inference_mode = inference_mode
        self.device = device
        self.autocast_dtype = autocast_dtype
        self.custom_args = custom_args

    @classmethod
    def from_dict(cls, data_dict: Dict) -> "TorchRunnerConfig":
        """Initializes Torch runner from dictionary.

        Args:
            data_dict: dictionary data

        Returns:
            TorchRunnerConfig object
        """
        return cls(
            autocast=cls._parse_string(bool, data_dict.get("autocast")),
            inference_mode=cls._parse_string(bool, data_dict.get("inference_mode")),
            autocast_dtype=data_dict.get("autocast_dtype"),
            device=data_dict.get("device"),
            custom_args=data_dict.get("custom_args"),  # TODO(kn): parse_string int ?
        )

    def to_dict(self, parse: bool = False, *_, **__) -> Dict:
        """Returns dictionary representation of the object.

        Args:
            parse: if True, converts parsable fields to string representation

        Returns:
            Dictionary representation of TorchRunnerConfig
        """
        return {
            "autocast": self.autocast,
            "inference_mode": self.inference_mode,
            "device": self.device,
            "autocast_dtype": self.autocast_dtype,
            "custom_args": self.custom_args,
        }


class DeviceRunnerConfig(RunnerConfig):
    """Device supported runner configuration class."""

    def __init__(self, device: Optional[str]) -> None:
        """Initializes device based runner configuration class.

        Args:
            device: The target device on which mode has to be loaded
        """
        super().__init__()
        self.device = device

    @classmethod
    def from_dict(cls, data_dict: Dict):
        """Initializes device based runner."""
        return cls(
            device=data_dict.get("device"),
        )

    def to_dict(self, *_, **__) -> Dict:
        """Returns dictionary representation of the object.

        Returns:
            Dictionary representation of DeviceRunnerConfig
        """
        return {
            "device": self.device,
        }
