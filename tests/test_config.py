from pathlib import Path
from tempfile import TemporaryDirectory
import os
import unittest
from unittest.mock import patch

from lcr.config import ConfigurationError, load_llm_config


CONFIG_NAMES = (
    "LLM_MODEL_ID",
    "LLM_API_KEY",
    "LLM_BASE_URL",
    "LLM_TIMEOUT",
)


class ConfigTests(unittest.TestCase):
    def test_loads_user_config_file(self):
        with TemporaryDirectory() as directory:
            env_path = Path(directory) / ".env"
            env_path.write_text(
                "LLM_MODEL_ID=test-model\n"
                "LLM_API_KEY=test-key\n"
                "LLM_BASE_URL=https://example.test/v1\n"
                "LLM_TIMEOUT=30\n",
                encoding="utf-8",
            )
            with patch.dict(os.environ, {}, clear=True):
                config = load_llm_config(env_path=env_path)

        self.assertEqual(config.model, "test-model")
        self.assertEqual(config.api_key, "test-key")
        self.assertEqual(config.base_url, "https://example.test/v1")
        self.assertEqual(config.timeout, 30)

    def test_shell_environment_overrides_config_file(self):
        with TemporaryDirectory() as directory:
            env_path = Path(directory) / ".env"
            env_path.write_text(
                "LLM_MODEL_ID=file-model\n"
                "LLM_API_KEY=file-key\n"
                "LLM_BASE_URL=https://file.test/v1\n",
                encoding="utf-8",
            )
            environment = {
                "LLM_MODEL_ID": "shell-model",
                "LLM_API_KEY": "shell-key",
                "LLM_BASE_URL": "https://shell.test/v1",
            }
            with patch.dict(os.environ, environment, clear=True):
                config = load_llm_config(env_path=env_path)

        self.assertEqual(config.model, "shell-model")
        self.assertEqual(config.api_key, "shell-key")
        self.assertEqual(config.base_url, "https://shell.test/v1")

    def test_reports_all_missing_required_settings(self):
        with TemporaryDirectory() as directory:
            env_path = Path(directory) / "missing.env"
            with patch.dict(os.environ, {}, clear=True):
                with self.assertRaises(ConfigurationError) as context:
                    load_llm_config(env_path=env_path)

        message = str(context.exception)
        for name in CONFIG_NAMES[:3]:
            self.assertIn(name, message)


if __name__ == "__main__":
    unittest.main()
