import os
import openai
from shipyard_openai_chatgpt.cli.chatgpt_translation import main as translation_main
from pathlib import Path


class DummyMessage:
    def __init__(self, content):
        self.content = content


class DummyChoice:
    def __init__(self, content):
        self.message = DummyMessage(content)


def dummy_create(*args, **kwargs):
    return type("DummyCompletion", (), {"choices": [DummyChoice("dummy translated text")]})


def test_chatgpt_translation(monkeypatch, tmp_path):
    source_file = tmp_path / "original.txt"
    source_file.write_text("Hello world!")

    monkeypatch.setenv("CHATGPT_API_KEY", "dummy_key")
    monkeypatch.setenv("CHATGPT_TEXT_FILE", str(source_file))
    monkeypatch.setenv("CHATGPT_LANGUAGE", "Spanish")
    output_file = tmp_path / "translated.txt"
    monkeypatch.setenv("CHATGPT_DESTINATION_FILE_NAME", str(output_file))

    monkeypatch.setattr(openai.ChatCompletion, "create", dummy_create)

    translation_main()

    content = output_file.read_text()
    assert "dummy translated text" in content
