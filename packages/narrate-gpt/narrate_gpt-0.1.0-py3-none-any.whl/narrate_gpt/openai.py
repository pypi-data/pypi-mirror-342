"""OpenAI Text-to-Speech module for converting text to streaming audio.

This module provides an extremely high-level interface to OpenAI's TTS API,
with support for streaming audio playback using LocalAudioPlayer.
"""

from contextlib import asynccontextmanager
from enum import Enum
from typing import Optional

import openai
from openai import NOT_GIVEN
from openai.helpers import LocalAudioPlayer
from pydantic import BaseModel, Field


class AudioFormat(str, Enum):
    """Supported audio output formats."""

    MP3 = "mp3"  # Default format for general use
    OPUS = "opus"  # For internet streaming, low latency
    AAC = "aac"  # Digital audio compression (YouTube, iOS, Android)
    FLAC = "flac"  # Lossless audio compression
    WAV = "wav"  # Uncompressed audio, low latency
    PCM = "pcm"  # Raw 24kHz 16-bit samples


class TTSConfig(BaseModel):
    """Configuration for text-to-speech conversion."""

    model: str = Field(default="gpt-4o-mini-tts", description="The TTS model to use")
    voice: str = Field(default="ash", description="The voice to use for speech")
    response_format: AudioFormat = Field(
        default=AudioFormat.MP3, description="The audio format to return"
    )
    instructions: Optional[str] = Field(
        default=None, description="Optional speaking instructions (tone, emotion, etc.)"
    )


class OpenAITTS:
    """Args:
    config: TTSConfig object with TTS settings.
    """

    def __init__(self, config: Optional[TTSConfig] = None) -> None:
        self.config = config or TTSConfig()

    @asynccontextmanager
    async def request(
        self,
        text: str,
        model: str | None = None,
        voice: str | None = None,
        format: AudioFormat | None = None,
        instructions: str | None = None,
    ):
        async with openai.AsyncOpenAI().audio.speech.with_streaming_response.create(
            input=text,
            model=model or self.config.model,
            voice=voice or self.config.voice,
            response_format=format or self.config.response_format.value,
            instructions=instructions or self.config.instructions or NOT_GIVEN,
        ) as response:
            yield response

    async def save(
        self,
        text: str,
        path: str,
        model: str | None = None,
        voice: str | None = None,
        format: AudioFormat | None = None,
        instructions: str | None = None,
    ) -> None:
        """Convert text to speech and save it to a file.

        Args:
            text: The text to convert to speech
            path: The path to save the audio file
        """
        async with self.request(
            text=text,
            model=model,
            voice=voice,
            format=format,
            instructions=instructions,
        ) as response:
            with open(path, "wb") as f:
                f.write(response.read())

    async def play(
        self,
        text: str,
        model: str | None = None,
        voice: str | None = None,
        response_format: AudioFormat | None = None,
        instructions: str | None = None,
    ) -> None:
        """Convert text to speech and play it using LocalAudioPlayer.

        Args:
            text: The text to convert to speech and play
        """
        async with self.request(
            text=text,
            model=model,
            voice=voice,
            format=AudioFormat.PCM,
            instructions=instructions,
        ) as response:
            await LocalAudioPlayer().play(response)


if __name__ == "__main__":
    import asyncio

    tts = OpenAITTS()
    asyncio.run(
        tts.save("Hello! This is a test of the OpenAI TTS system.", "./test.mp3")
    )
