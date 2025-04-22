from pathlib import Path

from onnx_asr.asr import Asr


class Whisper(Asr):
    def __init__(self, model_parts: dict[str, Path]):
        super().__init__("whisper", model_parts["vocab"])

    @staticmethod
    def _get_model_files(version: str | None = None) -> dict[str, str]:
        return {"vocab": "vocab.txt"}
