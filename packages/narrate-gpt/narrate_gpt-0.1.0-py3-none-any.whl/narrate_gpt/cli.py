import argparse
import asyncio
import sys
from pathlib import Path
from typing import Optional

import pyperclip

from narrate_gpt.openai import AudioFormat, OpenAITTS


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="narrate-gpt",
        description="Convert text to speech using OpenAI's TTS API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Add arguments
    parser.add_argument(
        "text",
        nargs="?",
        help="Text to convert to speech. If not provided, will read from clipboard if -c is set",
    )
    parser.add_argument(
        "-c",
        "--clipboard",
        action="store_true",
        help="Read text from clipboard instead of command line",
    )
    parser.add_argument(
        "-m",
        "--model",
        type=str,
        help="TTS model to use",
        default=None,
    )
    parser.add_argument(
        "-v",
        "--voice",
        type=str,
        help="Voice to use for speech",
        default=None,
    )
    parser.add_argument(
        "-f",
        "--format",
        type=AudioFormat,
        help="Audio output format",
        choices=[f.value for f in AudioFormat],
        default=None,
    )
    parser.add_argument(
        "-i",
        "--instructions",
        type=str,
        help="Optional speaking instructions (tone, emotion, etc.)",
        default=None,
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output file path. If not provided, will play audio directly",
        type=Path,
        default=None,
    )

    return parser


async def generate_audio(
    text: Optional[str] = None,
    clipboard: bool = False,
    model: Optional[str] = None,
    voice: Optional[str] = None,
    format: Optional[AudioFormat] = None,
    instructions: Optional[str] = None,
    output: Optional[Path] = None,
) -> None:
    # Get text from clipboard if requested
    if clipboard:
        text = pyperclip.paste()
        if not text:
            raise ValueError("Clipboard is empty")

    # Create TTS client
    tts = OpenAITTS()

    if output:
        await tts.save(
            text=text,
            path=str(output),
            model=model,
            voice=voice,
            format=format,
            instructions=instructions,
        )
        print(f"Audio saved to: {output}")
    else:
        await tts.play(
            text=text,
            model=model,
            voice=voice,
            response_format=format,
            instructions=instructions,
        )


def main():
    parser = make_parser()
    args = parser.parse_args()

    if (
        (args.text and args.clipboard)  # both provided
        or (not args.text and not args.clipboard)  # neither provided
    ):
        parser.print_help()
        sys.exit(1)

    try:
        asyncio.run(generate_audio(**vars(args)))
        sys.exit(0)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
