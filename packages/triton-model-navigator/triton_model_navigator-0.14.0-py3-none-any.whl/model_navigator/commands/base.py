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
"""Base module for commands common classes and helpers."""

import abc
import dataclasses
from enum import Enum
from inspect import getfullargspec
from typing import Any, Callable, Dict, List, Optional, Type

from model_navigator.configuration.model.model_config import ModelConfig
from model_navigator.configuration.runner.runner_config import RunnerConfig
from model_navigator.exceptions import ModelNavigatorWrongParameterError
from model_navigator.runners.base import NavigatorRunner
from model_navigator.utils.common import DataObject


class CommandStatus(str, Enum):
    """Status for commands."""

    OK = "OK"
    FAIL = "FAIL"
    NOOP = "NOOP"
    INITIALIZED = "INITIALIZED"
    SKIPPED = "SKIPPED"


@dataclasses.dataclass
class CommandOutput(DataObject):
    """Command output dataclass structure."""

    status: CommandStatus
    output: Optional[Dict[str, Any]] = None
    execution_time: Optional[float] = None

    @classmethod
    def from_dict(cls, data_dict: Dict) -> "CommandOutput":
        """Create CommandOutput from the dictionary.

        Args:
            data_dict (Dict): dictionary with command output data.

        Returns:
            CommandOutput
        """
        return cls(
            status=CommandStatus(data_dict["status"]),
            output=data_dict["output"],
            execution_time=data_dict.get("execution_time"),
        )


class CommandMeta(abc.ABCMeta):  # noqa: B024
    """Metaclass for command."""

    @property
    def name(cls):
        """Return name of the command.

        Return:
            Name of command as a string
        """
        return cls.__name__

    def __repr__(cls) -> str:
        """Return a string representation of the command."""
        return cls.name


class Command(metaclass=CommandMeta):
    """Base class for command definition."""

    _is_required: bool = False
    _requires: Optional[List[str]] = None

    def __init_subclass__(cls, is_required: bool = False, requires: Optional[List[str]] = None, **kwargs):
        """Initialization of a command subclass."""
        super().__init_subclass__(**kwargs)
        cls._is_required = is_required
        cls._requires = requires if requires is not None else []

    @classmethod
    def is_required(cls):
        """Indicates if Command should be considered as required.

        Returns:
            True if required, False otherwise
        """
        return cls._is_required

    @classmethod
    def requires(cls):
        """Return required commands to execute current command.

        Returns:
            List of required commands
        """
        return cls._requires

    def run(self, *args, **kwargs) -> CommandOutput:
        """Run command execution.

        Args:
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Output with command result
        """

        def _filter_dict_for_func(data_dict: Dict[str, Any], func: Callable):
            return {k: v for k, v in data_dict.items() if k in getfullargspec(func).args}

        do_execute = self._pre_run(*args, **_filter_dict_for_func(kwargs, self._pre_run))
        if do_execute:
            output = self._run(*args, **_filter_dict_for_func(kwargs, self._run))
        else:
            output = CommandOutput(CommandStatus.SKIPPED)
        self._post_run(output, *args, **_filter_dict_for_func(kwargs, self._post_run))
        return output

    def _pre_run(self, *args, **kwargs) -> bool:
        """Pre-run command execution.

        Args:
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            True if command should be executed, False otherwise
        """
        return True

    @abc.abstractmethod
    def _run(self, *args, **kwargs) -> CommandOutput:
        """Run command execution.

        Args:
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Output with command result
        """
        raise NotImplementedError

    def _post_run(self, output: CommandOutput, *args, **kwargs) -> None:  # noqa: B027
        """Post-run command execution.

        Args:
            output: Command output
            *args: Positional arguments
            **kwargs: Keyword arguments
        """
        pass


class ExecutionUnit:
    """Command along with configuration and runner."""

    def __init__(
        self,
        *,
        command: Type[Command],
        model_config: Optional[ModelConfig] = None,
        runner_cls: Optional[Type[NavigatorRunner]] = None,
        runner_config: Optional[RunnerConfig] = None,
        results_lookup_runner_cls: Optional[Type[NavigatorRunner]] = None,
        **kwargs,
    ) -> None:
        """Initialize object.

        Args:
            command: A command to execute
            config: Global configuration provide by user
            model_config: Optional configuration of model that has to be produced by command
            runner_cls: Optional runner for correctness or performance evaluation
            runner_config: Additional runner arguments
            results_lookup_runner_cls: Optional runner for results lookup
            kwargs: Additional arguments for command
        """
        self.command = command
        self.model_config = model_config
        self.runner_cls = runner_cls
        self.runner_config = runner_config
        self.results_lookup_runner_cls = results_lookup_runner_cls
        self.kwargs = kwargs

        if self.runner_cls and self.results_lookup_runner_cls:
            raise ModelNavigatorWrongParameterError("runner_cls and results_lookup_runner_cls cannot be set at once.")

    def __repr__(self) -> str:
        """Return a string representation of the execution unit."""
        runner_name = "None" if self.runner_cls is None else self.runner_cls.name()
        config = "None" if self.model_config is None else self.model_config.key
        return f"Cmd:{self.command}, Config:{config}, Runner:{runner_name}"
