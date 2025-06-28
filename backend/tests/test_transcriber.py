import unittest
from pathlib import Path
from modules import transcriber
from modules.config_loader import load_config
import json

class TestTranscriber(unittest.TestCase):
    def test_transcription_output(self):
        config = load_config()
        test_audio = Path("tests/resources/test_audio.wav")
        transcriber.transcribe(test_audio, config)

        output_path = Path("transcripts") / (test_audio.stem + ".json")
        self.assertTrue(output_path.exists(), "Transcript file was not created")

        with open(output_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.assertIn("text", data)

if __name__ == "__main__":
    unittest.main()
