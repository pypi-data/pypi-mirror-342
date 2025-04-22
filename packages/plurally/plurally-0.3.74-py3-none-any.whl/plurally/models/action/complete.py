import os
import re
from typing import Any, Dict, List

import tenacity
from litellm import completion
from loguru import logger
from pydantic import ConfigDict, Field, create_model, model_validator

from plurally.json_utils import load_from_json_dict, replace_refs
from plurally.llm.llm_utils import build_messages
from plurally.models.action.instruct import InstructField
from plurally.models.env_vars import BaseEnvVars, OpenAiApiKey
from plurally.models.fields import (
    HANDLE_TYPE_FRIENDLY,
    HANDLE_TYPE_MAP,
    NameableHandle,
    get_nameable_fields,
)
from plurally.models.jinja_template import get_undeclared_vars
from plurally.models.node import Node


class Complete(Node):
    ICON = "openai"
    PLURALLY_VERSION = 1

    class OutputSchema(Node.OutputSchema):
        output: Any = Field()
        output_raw: str = Field()

    class EnvVars(BaseEnvVars):
        OPENAI_API_KEY: str = OpenAiApiKey

    class InputSchema(Node.InputSchema):
        model_config = ConfigDict(json_schema_extra={"can-add-fields": True})

    class InitSchema(Node.InitSchema):
        model: str = "mistral/mistral-tiny"
        source: str = Field("", json_schema_extra={"uiSchema": {"ui:widget": "textarea", "ui:options": {"rows": 10}}})
        input_fields: List[NameableHandle] = get_nameable_fields(
            title="Inputs",
            description="The different inputs of the AI model. For instance if you want to write an automatic support email, your inputs might be: like 'Question asked', 'Name of person asking'. Be sure to mention them in your instructions (see examples).",
            examples=["Question asked", "Name of person asking"],
            placeholder="Enter input name, example: Question asked",
            default_factory=list,
            json_schema_extra_extra={"is_input": True, "name_singular": "Input"},
        )
        instruct: str = InstructField
        examples: str = Field(
            "",
            description="Examples in JSON format (list of dicts)",
            json_schema_extra={"uiSchema": {"ui:widget": "textarea", "ui:options": {"rows": 10}}},
        )
        general_info: str = Field(
            "",
            description="General information in JSON format (list of strings)",
            json_schema_extra={"uiSchema": {"ui:widget": "textarea", "ui:options": {"rows": 10}}},
        )

        @model_validator(mode="after")
        def ckeck_model(cls, values):
            if len(set(field._clean for field in values.input_fields)) != len(values.input_fields):
                raise ValueError("Input fields must be unique")
            return values

    InitSchema.__doc__ = """Instruct an AI model to perform a task."""
    DESC = InitSchema.__doc__

    def __init__(
        self,
        init_inputs: InitSchema,
    ) -> None:
        self._input_fields = init_inputs.input_fields
        self.model = init_inputs.model
        self.source = init_inputs.source
        self.instruct = init_inputs.instruct
        self.examples = init_inputs.examples
        self.general_info = init_inputs.general_info

        super().__init__(init_inputs)

    def _set_schemas(self) -> None:
        # create pydantic model from input_fields
        in_fields_map = {}
        for field in self.input_fields:
            field_type = HANDLE_TYPE_MAP[field.type]
            json_schema_extra = {"handle_id": field.handle_id}
            type_friendly = HANDLE_TYPE_FRIENDLY.get(field.type)
            if type_friendly:
                json_schema_extra["type-friendly"] = type_friendly
            in_fields_map[field._clean] = (
                field_type,
                Field(
                    ...,
                    title=field.free,
                    json_schema_extra=json_schema_extra,
                ),
            )
        self.InputSchema = create_model(
            "InputSchema",
            **in_fields_map,
            __base__=Complete.InputSchema,
        )
        assert self.InputSchema.model_json_schema()["can-add-fields"]

    @property
    def input_fields(self):
        return self._input_fields

    @input_fields.setter
    def input_fields(self, value):
        value = [v if isinstance(v, NameableHandle) else NameableHandle(**v) for v in value]
        assert len(set(field._clean for field in value)) == len(value), f"Input fields must be unique {value}"
        self._input_fields = value
        self._set_schemas()
        self.tgt_handles = self._get_handles(self.InputSchema, None)

    def create(self, messages: List[Dict[str, str]]) -> Any:
        model_override = os.environ.get("OPENAI_MODEL")
        model = self.model
        if model_override:
            logger.info(f"Found override for OPENAI_MODEL: {model_override}, using it.")
            model = model_override

        response_model = self.instruct_schema

        output = self.client.chat.completions.create(
            model=model,
            messages=messages,
            response_model=response_model,
            max_retries=3,
            temperature=0,
            top_p=0,
            seed=1234,
        )
        return output

    @tenacity.retry(stop=tenacity.stop_after_attempt(3))
    def forward(self, node_input) -> Any:
        messages = build_messages(self.instruct, node_input, self.examples, self.general_info)
        content = (
            completion(
                model=self.model,
                messages=messages,
            )
            .choices[0]
            .message.content
        )
        self.outputs["output_raw"] = content
        self.outputs["output"] = self.post_process(content)

    def post_process(self, content: str) -> dict:
        if not self.source:
            return content
        loc = {}
        exec(self.source, {**globals(), **locals(), "content": content}, loc)
        return loc["__plurally_output"]

    def serialize(self) -> dict:
        return {
            **super().serialize(),
            "instruct": self.instruct,
            "input_fields": [i.model_dump() for i in self.input_fields],
            "input_schema": replace_refs(self.InputSchema.model_json_schema()),
            "model": self.model,
            "examples": self.examples,
            "general_info": self.general_info,
            "source": self.source,
        }

    @classmethod
    def _parse(cls, **kwargs):
        kwargs = load_from_json_dict(kwargs)
        kwargs["input_fields"] = [NameableHandle(**i) for i in kwargs["input_fields"]]
        return cls(cls.InitSchema(**kwargs))

    def add_target_handle(self, src_handle):
        """
        src_handle is the handle that one wants to connect to the node while adding a tgt_handle
        """
        new_tgt_handle = NameableHandle(free=src_handle)
        ix = 1
        while new_tgt_handle._clean in [i._clean for i in self.input_fields]:
            new_tgt_handle = NameableHandle(free=new_tgt_handle.free + f" {ix}")
        self.input_fields = [*self.input_fields, new_tgt_handle]
        return new_tgt_handle._clean

    def get_necessary_env_vars(self):
        necessary_env_vars = set()
        if self.model.startswith("mistral/"):
            necessary_env_vars.add("MISTRAL_API_KEY")
        ignore = {field.free for field in self.input_fields}
        return necessary_env_vars.union(get_undeclared_vars(self.instruct, ignore=ignore))
