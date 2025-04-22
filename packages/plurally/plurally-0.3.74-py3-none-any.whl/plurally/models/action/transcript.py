import io
import os

import requests
from loguru import logger
from openai import NotGiven
from pydantic import Field, field_validator

from plurally.models.env_vars import BaseEnvVars, OpenAiApiKeyRequired
from plurally.models.misc import AudioFile
from plurally.models.node import Node


class Transcript(Node):
    ICON = "openai"

    class EnvVars(BaseEnvVars):
        OPENAI_API_KEY: str = OpenAiApiKeyRequired

    class InitSchema(Node.InitSchema):
        language: str = Field("", max_length=2, title="Language", description="The language of the audio file")
        model: str = Field("whisper-v3-turbo")

        @field_validator("language", mode="before")
        def language_uppercase(cls, value):
            return value.strip().lower()

    class InputSchema(Node.InputSchema):
        audio: AudioFile = Field(
            title="Audio",
            description="The audio file",
            json_schema_extra={
                "type-friendly": "Audio",
            },
        )
        # FIXME: Prompt is buggy as hell and completely messes up the transcription
        # do not use it
        # prompt: str = Field(
        #     "",
        #     title="Prompt",
        #     description="The prompt to use for the transcription",
        #     json_schema_extra={
        #         "uiSchema": {"ui:widget": "textarea", "ui:options": {"rows": 10}}
        #     },
        # )

    class OutputSchema(Node.OutputSchema):
        transcript: str = Field(
            description="The extracted transcript from the audio file.",
        )

    def __init__(self, init_inputs: Node.InitSchema):
        self._client = None
        self.model = init_inputs.model
        self.language = init_inputs.language
        super().__init__(init_inputs)

    @property
    def client(self):
        global OpenAI
        from openai import OpenAI

        if self._client is None:
            self._client = OpenAI()
        return self._client

    def forward(self, node_inputs: InputSchema, **kwargs):
        model = kwargs.get("model", self.model)
        logger.debug(f"Transcribing audio {node_inputs.audio.filename} with model {model}")

        try:
            if model == "whisper-1":
                transcription = self.client.audio.transcriptions.create(
                    model=model,
                    file=(node_inputs.audio.filename, node_inputs.audio.content),
                    language=self.language or NotGiven(),
                    temperature=0,
                )
                self.outputs = {"transcript": transcription.text}
            elif model == "whisper-v3-turbo":
                assert os.environ.get("FIREWORKSAI_API_KEY"), "FIREWORKSAI_API_KEY is not set"
                bio = io.BytesIO(node_inputs.audio.content)
                bio.seek(0)
                data = {"model": model, "temperature": "0", "vad_model": "silero"}
                if self.language:
                    data["language"] = self.language

                response = requests.post(
                    "https://audio-turbo.us-virginia-1.direct.fireworks.ai/v1/audio/transcriptions",
                    headers={"Authorization": f"Bearer {os.environ['FIREWORKSAI_API_KEY']}"},
                    files={"file": bio},
                    data=data,
                )
                self.outputs = {"transcript": response.json()["text"]}
            else:
                raise ValueError(f"Unknown transcription model {model}")
        except Exception as e:
            logger.exception(e)
            if model == "whisper-1":
                raise ValueError("Transcription failed") from e

            logger.debug(f"Transcription failed, falling back to whisper-1")
            return self.forward(node_inputs, model="whisper-1")

    def serialize(self):
        return super().serialize() | {"language": self.language, "model": self.model}
