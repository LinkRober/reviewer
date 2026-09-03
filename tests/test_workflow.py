from contextlib import redirect_stdout
from io import StringIO
import json
from pathlib import Path
import secrets
from tempfile import TemporaryDirectory
import subprocess
import unittest
from unittest.mock import patch

from lcr.workflow import (
    NoReviewableFiles,
    ReviewError,
    collect_diff,
    generate_review_id,
    load_prompt,
    review_repository,
)


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

        parsed_result = json.loads(result)
        self.assertEqual(parsed_result["result"], 1)
        self.assertRegex(
            parsed_result["reviewId"],
            r"^LCR-\d{13}-[0-9A-F]{12}$",
        )
        self.assertEqual(len(fake_llm.messages), 3)
        self.assertEqual(fake_llm.messages[0][1]["role"], "user")
        self.assertIn("diff --git", fake_llm.messages[0][1]["content"])
        judge_input = json.loads(fake_llm.messages[2][1]["content"])
        self.assertIn("STYLE-001", judge_input["rule"])
        self.assertIn("ARCH-001", judge_input["arch"])

        review_id = parsed_result["reviewId"]
        self.assertIn(review_id, fake_llm.messages[0][0]["content"])
        self.assertIn(review_id, fake_llm.messages[1][0]["content"])

    def test_generate_review_id_uses_milliseconds_and_random_suffix(self):
        with patch("lcr.workflow.time.time", return_value=1788391234.567):
            with patch.object(secrets, "token_hex", return_value="4f9a2c7e81d0"):
                review_id = generate_review_id()

        self.assertEqual(review_id, "LCR-1788391234567-4F9A2C7E81D0")
        self.assertRegex(review_id, r"^LCR-\d{13}-[0-9A-F]{12}$")

    def test_each_review_generates_a_new_id(self):
        first = generate_review_id()
        second = generate_review_id()
        self.assertNotEqual(first, second)

    def test_diff_command_filters_to_ios_extensions(self):
        outputs = ["true", "base", "head", "merge", "diff --git a/file.m b/file.m"]
        with TemporaryDirectory() as directory:
            with patch("lcr.workflow.run_git", side_effect=outputs) as run_git_mock:
                collect_diff(Path(directory), "main", "feature", ".", "repo")

        self.assertEqual(
            run_git_mock.call_args_list[-1].args,
            (
                Path(directory),
                "diff",
                "merge..head",
                "--",
                "*.h",
                "*.m",
                "*.mm",
            ),
        )

    def test_review_range_declares_filtered_extensions(self):
        outputs = ["true", "base", "head", "merge", "diff --git a/file.h b/file.h"]
        with TemporaryDirectory() as directory:
            with patch("lcr.workflow.run_git", side_effect=outputs):
                _, review_range = collect_diff(
                    Path(directory), "main", "feature", "../", "LKFont"
                )

        self.assertEqual(review_range["fileExtensions"], [".h", ".m", ".mm"])
        self.assertRegex(review_range["reviewId"], r"^LCR-\d{13}-[0-9A-F]{12}$")

    def test_review_range_contains_review_id_when_provided(self):
        outputs = ["true", "base", "head", "merge", "diff --git a/file.h b/file.h"]
        with TemporaryDirectory() as directory:
            with patch("lcr.workflow.run_git", side_effect=outputs):
                _, review_range = collect_diff(
                    Path(directory),
                    "main",
                    "feature",
                    "../",
                    "LKFont",
                    "LCR-1788391234567-4F9A2C7E81D0",
                )

        self.assertEqual(
            review_range["reviewId"],
            "LCR-1788391234567-4F9A2C7E81D0",
        )

    def test_missing_repository_is_reported(self):
        with self.assertRaisesRegex(ReviewError, "仓库路径不存在"):
            collect_diff(
                Path("/path/that/does/not/exist"),
                "main",
                "feature",
                ".",
                "missing",
            )

    def test_empty_filtered_diff_is_reported_as_non_error(self):
        outputs = ["true", "base", "head", "merge", ""]
        with TemporaryDirectory() as directory:
            with patch("lcr.workflow.run_git", side_effect=outputs):
                with self.assertRaisesRegex(NoReviewableFiles, "没有可审核的 iOS 文件"):
                    collect_diff(
                        Path(directory),
                        "main",
                        "feature",
                        ".",
                        "repo",
                    )

    def test_git_diff_includes_only_ios_files_and_supports_spaces(self):
        with TemporaryDirectory() as directory:
            repo = Path(directory)

            def git(*args):
                return subprocess.run(
                    ["git", *args],
                    cwd=repo,
                    check=True,
                    capture_output=True,
                    text=True,
                ).stdout.strip()

            git("init", "-q")
            git("config", "user.email", "test@example.com")
            git("config", "user.name", "Test User")
            (repo / "README.md").write_text("base\n", encoding="utf-8")
            git("add", ".")
            git("commit", "-qm", "base")
            base_sha = git("rev-parse", "HEAD")

            for name in ("Header.h", "Implementation.m", "Bridge.mm"):
                (repo / name).write_text("changed\n", encoding="utf-8")
            (repo / "Other.swift").write_text("changed\n", encoding="utf-8")
            (repo / "Settings.json").write_text("{}\n", encoding="utf-8")
            (repo / "File With Spaces.m").write_text("changed\n", encoding="utf-8")
            git("add", ".")
            git("commit", "-qm", "feature")
            head_sha = git("rev-parse", "HEAD")
            git("update-ref", "refs/remotes/origin/base", base_sha)
            git("update-ref", "refs/remotes/origin/head", head_sha)

            code_diff, review_range = collect_diff(
                repo,
                "base",
                "head",
                "../",
                "LKFont",
            )

        self.assertIn("Header.h", code_diff)
        self.assertIn("Implementation.m", code_diff)
        self.assertIn("Bridge.mm", code_diff)
        self.assertIn("File With Spaces.m", code_diff)
        self.assertNotIn("Other.swift", code_diff)
        self.assertNotIn("Settings.json", code_diff)
        self.assertEqual(review_range["fileExtensions"], [".h", ".m", ".mm"])


if __name__ == "__main__":
    unittest.main()
