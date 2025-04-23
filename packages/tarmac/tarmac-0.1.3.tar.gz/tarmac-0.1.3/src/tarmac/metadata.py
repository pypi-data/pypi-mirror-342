import re
from typing import Any, Iterator, Self, TypeAlias, Literal

import yaml
from pydantic import BaseModel, Field

REGEX = r"(?m)^# /// (?P<type>[a-zA-Z0-9-]+)$\s(?P<content>(^#(| .*)$\s)+)^# ///$"


def _metadata_stream(script: str) -> Iterator[tuple[str, str]]:
    for match in re.finditer(REGEX, script):
        yield (
            match.group("type"),
            "".join(
                line[2:] if line.startswith("# ") else line[1:]
                for line in match.group("content").splitlines(keepends=True)
            ),
        )


IOTypeString: TypeAlias = Literal["str", "int", "float", "bool", "list", "dict"]
IOType: TypeAlias = str | int | float | bool | list[Any] | dict[str, Any] | None
ValueMapping: TypeAlias = dict[str, IOType]


class Input(BaseModel):
    """
    Describes an input for a job step.
    """

    name: str = ""
    """
    The name of the input.
    """

    type: IOTypeString = "str"
    """
    The type of the input.
    Can be one of: str, int, float, bool, list, dict.
    """

    description: str = ""
    """
    A description of the input.
    """

    default: IOType = None
    """
    The default value of the input.
    Not required if the input is required.
    """

    required: bool = True
    """
    Whether the input is required.
    If True, the input must be provided.
    If False, the default value will be used if not provided.
    """

    example: Any = None
    """
    An example value for the input.
    This is used for documentation purposes only.
    """


class Output(BaseModel):
    """
    Describes an output for a job step.
    """

    name: str = ""
    """
    The name of the output.
    """

    type: IOTypeString = "str"
    """
    The type of the output.
    Can be one of: str, int, float, bool, list, dict.
    The type is not validated at runtime.
    """

    description: str = ""
    """
    A description of the output.
    """

    example: Any = None
    """
    An example value for the output.
    This is used for documentation purposes only.
    """


class Metadata(BaseModel):
    """
    Common metadata for all operations.
    """

    description: str = ""
    """
    A description of the operation.
    """

    inputs: dict[str, Input] = {}
    """
    A dictionary of inputs for the operation.
    The keys are the names of the inputs.
    The values are Input objects.
    """

    outputs: dict[str, Output] = {}
    """
    A dictionary of outputs for the operation.
    The keys are the names of the outputs.
    The values are Output objects.
    """

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        for name, input in self.inputs.items():
            input.name = name
        for name, output in self.outputs.items():
            output.name = name

    def validate_inputs(self, inputs: ValueMapping) -> ValueMapping:
        res = {}
        for input in self.inputs.values():
            if input.name not in inputs:
                if input.required:
                    raise ValueError(f"Missing required input: {input.name}")
                value = input.default
            else:
                value = inputs[input.name]
            res[input.name] = self.validate_type(input.name, value, input.type)
        for unknown_key in set(inputs) - set(self.inputs):
            raise ValueError(f"Unknown input: {unknown_key}")
        return res

    def validate_type(self, name: str, value: IOType, type_: IOTypeString) -> Any:
        if type_ == "str":
            return str(value)
        if type_ == "int":
            if isinstance(value, str):
                return int(value)
            if not isinstance(value, int):
                raise ValueError(f"Input {name} must be an integer")
            return value
        if type_ == "float":
            if not isinstance(value, (float, int)):
                raise ValueError(f"Input {name} must be a float")
            return float(value)
        if type_ == "bool":
            if isinstance(value, str):
                return value.lower() in ("true", "1")
            if not isinstance(value, bool):
                raise ValueError(f"Input {name} must be a boolean")
            return value
        if type_ == "list":
            if not isinstance(value, list):
                raise ValueError(f"Input {name} must be a list")
            return value
        if type_ == "dict":
            if not isinstance(value, dict):
                raise ValueError(f"Input {name} must be a dict")
            return value
        raise ValueError(f"Invalid input type: {type_}")


class ScriptMetadata(Metadata):
    """
    Metadata for a Python script.
    """

    dependencies: list[str] = []
    """
    A list of dependencies for the script.
    The dependencies are installed in the environment before the script is run.
    You can specify versions in PEP 508 format.
    """

    additional_uv_args: list[str] = []
    """
    A list of additional arguments to pass to the script runner (the uv command).
    """

    @classmethod
    def load(cls, script: str) -> Self:
        metadata = None
        for type_, content in _metadata_stream(script):
            if type_ == "tarmac":
                metadata = yaml.safe_load(content)
                break
        if metadata is None:
            raise ValueError("No metadata found")
        return cls(**metadata)


JobType: TypeAlias = Literal["script", "job", "shell"]


class JobStep(BaseModel):
    """
    Describes a job step.
    """

    id: str | None = None
    """
    The ID of the job step.
    If not provided, the ID will be set to the name of the job step.
    """

    type: JobType | None = None
    """
    The type of the job step.
    Can be one of: script, job, shell.
    If not provided, the type will be set based on the presence of the `do`, `run`, or `job` fields.
    """

    name: str = ""
    """
    The human-readable name of the job step.
    """

    do: str | None = None
    """
    The script to run.
    If provided, the type will be set to "script".
    """

    run: str | None = None
    """
    The shell command to run.
    If provided, the type will be set to "shell".
    """

    job: str | None = None
    """
    The job to run.
    If provided, the type will be set to "job".
    """

    params: ValueMapping = Field(alias="with", default_factory=dict)
    """
    The inputs to pass to the job step.
    """

    condition: Any = Field(alias="if", default=None)
    """
    The condition to run the job step.
    If provided, the job step will only run if the condition is true.
    """

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        if not self.id:
            self.id = self.name

    def validate_job_type(self):
        if self.do is not None:
            if self.run is not None:
                raise ValueError("Cannot use `run` with `do`")
            if self.job is not None:
                raise ValueError("Cannot use `job` with `do`")
            self.type = "script"
        elif self.run is not None:
            if self.job is not None:
                raise ValueError("Cannot use `job` with `run`")
            self.type = "shell"
        elif self.job is not None:
            self.type = "job"
        else:
            raise ValueError("Must have either `do` or `run` or `job`")


class JobMetadata(Metadata):
    """
    Metadata for a job.
    """

    steps: list[JobStep]
    """
    A list of job steps.
    The steps are executed in order.
    """

    @classmethod
    def load(cls, file: str) -> Self:
        metadata = yaml.safe_load(file)
        return cls(**metadata)
