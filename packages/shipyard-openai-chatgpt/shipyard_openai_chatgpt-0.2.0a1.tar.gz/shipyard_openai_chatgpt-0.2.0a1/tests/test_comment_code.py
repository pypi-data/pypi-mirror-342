import os
import openai
from shipyard_openai_chatgpt.cli.comment_code import main as comment_code_main
from pathlib import Path
import pytest

class DummyMessage:
    def __init__(self, content):
        self.content = content


class DummyChoice:
    def __init__(self, content):
        self.message = DummyMessage(content)


def dummy_create(*args, **kwargs):
    return type("DummyCompletion", (), {"choices": [DummyChoice("dummy commented code")]})


def test_comment_code(monkeypatch, tmp_path):
    monkeypatch.setenv("CHATGPT_API_KEY", "dummy_key")
    monkeypatch.setenv("CHATGPT_SCRIPT", str(tmp_path / "non_existent.py"))
    monkeypatch.setenv("CHATGPT_SCRIPT_TYPED", "print('Hello world')")
    export_file = tmp_path / "exported_script.py"
    monkeypatch.setenv("CHATGPT_EXPORTED_FILE_NAME", str(export_file))

    monkeypatch.setattr(openai.ChatCompletion, "create", dummy_create)

    comment_code_main()


    content = export_file.read_text()
    assert "dummy commented code" in content


@pytest.mark.integration
def test_comment_code_integration_success(tmp_path):

    if not os.environ.get("CHATGPT_API_KEY"):
        pytest.skip("Skipping integration test: CHATGPT_API_KEY is not set")

    os.environ["CHATGPT_SCRIPT"] = str(tmp_path / "nonexistent.py")
    os.environ["CHATGPT_SCRIPT_TYPED"] = "print('Hello world')"
    export_file = tmp_path / "exported_script.py"
    os.environ["CHATGPT_EXPORTED_FILE_NAME"] = str(export_file)

    try:
        comment_code_main()
    except Exception as e:
        pytest.fail(f"comment_code integration test failed with exception: {e}")

    # Verify the exported file is created and non-empty.
    assert export_file.exists(), "Exported script file not created"
    content = export_file.read_text().strip()
    assert content, "Exported script file is empty"


@pytest.mark.integration
def test_comment_code_integration_failure(tmp_path):
    os.environ["CHATGPT_API_KEY"] = "invalid_key"
    os.environ["CHATGPT_SCRIPT"] = str(tmp_path / "nonexistent.py")
    os.environ["CHATGPT_SCRIPT_TYPED"] = "print('Hello world')"
    export_file = tmp_path / "exported_script.py"
    os.environ["CHATGPT_EXPORTED_FILE_NAME"] = str(export_file)

    with pytest.raises(Exception):
        comment_code_main()