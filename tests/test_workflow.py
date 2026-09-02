from contextlib import redirect_stdout
from io import StringIO
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from lcr.workflow import ReviewError, collect_diff, load_prompt, review_repository


class FakeLLM:
    model = "fake-model"

    def __init__(self):
        self.messages = []

    def think(self, messages):
        self.messages.append(messages)
        if len(self.messages) == 1:
            return '{"issues": [{"id": "STYLE-001"}]}'
        if len(self.messages) == 2:
            return '{"issues": [{"id": "ARCH-001"}]}'
        return '{"result": 1, "details": [], "reason": []}'


class WorkflowTests(unittest.TestCase):
    def test_bundled_prompt_is_readable(self):
        self.assertIn("编码规范审核专员", load_prompt("rule_role.md"))

    def test_review_chain_sends_diff_and_json_summary(self):
        outputs = [
            "true",
            "base-sha",
            "head-sha",
            "merge-base-sha",
            "diff --git a/file.m b/file.m\n+added line",
        ]
        fake_llm = FakeLLM()

        with TemporaryDirectory() as directory:
            with patch("lcr.workflow.run_git", side_effect=outputs):
                with redirect_stdout(StringIO()):
                    result = review_repository(
                        repo_path=Path(directory),
                        from_branch="release/1.7.0",
                        to_branch="feature/xm/my_7",
                        component_path="../",
                        component_name="LKFont",
                        llm=fake_llm,
                    )

        self.assertEqual(result, '{"result": 1, "details": [], "reason": []}')
        self.assertEqual(len(fake_llm.messages), 3)
        self.assertEqual(fake_llm.messages[0][1]["role"], "user")
        self.assertIn("diff --git", fake_llm.messages[0][1]["content"])
        judge_input = json.loads(fake_llm.messages[2][1]["content"])
        self.assertIn("STYLE-001", judge_input["rule"])
        self.assertIn("ARCH-001", judge_input["arch"])

    def test_missing_repository_is_reported(self):
        with self.assertRaisesRegex(ReviewError, "仓库路径不存在"):
            collect_diff(
                Path("/path/that/does/not/exist"),
                "main",
                "feature",
                ".",
                "missing",
            )

    def test_empty_diff_is_reported(self):
        outputs = ["true", "base", "head", "merge", ""]
        with TemporaryDirectory() as directory:
            with patch("lcr.workflow.run_git", side_effect=outputs):
                with self.assertRaisesRegex(ReviewError, "没有代码差异"):
                    collect_diff(
                        Path(directory),
                        "main",
                        "feature",
                        ".",
                        "repo",
                    )


if __name__ == "__main__":
    unittest.main()
