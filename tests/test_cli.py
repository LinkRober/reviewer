from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from lcr.cli import build_parser, main


class CliTests(unittest.TestCase):
    def test_review_arguments_are_parsed(self):
        args = build_parser().parse_args([
            "review",
            "--from",
            "release/1.7.0",
            "--to",
            "feature/xm/my_7",
            "--path",
            "../",
            "--name",
            "LKFont",
        ])

        self.assertEqual(args.from_branch, "release/1.7.0")
        self.assertEqual(args.to_branch, "feature/xm/my_7")
        self.assertEqual(args.path, Path("../"))
        self.assertEqual(args.name, "LKFont")

    def test_missing_review_arguments_exit_with_code_two(self):
        with redirect_stderr(StringIO()):
            with self.assertRaises(SystemExit) as context:
                main(["review"])

        self.assertEqual(context.exception.code, 2)

    def test_path_with_or_without_trailing_slash_resolves_equally(self):
        with TemporaryDirectory() as directory:
            parent = Path(directory) / "parent"
            repository = parent / "LKFont"
            repository.mkdir(parents=True)
            resolved_paths = []

            def fake_review_repository(**kwargs):
                resolved_paths.append(kwargs["repo_path"])
                return "{}"

            with patch("lcr.cli.review_repository", side_effect=fake_review_repository):
                with redirect_stdout(StringIO()):
                    first = main([
                        "review", "--from", "main", "--to", "feature",
                        "--path", str(parent), "--name", "LKFont",
                    ])
                    second = main([
                        "review", "--from", "main", "--to", "feature",
                        "--path", f"{parent}/", "--name", "LKFont",
                    ])

        self.assertEqual(first, 0)
        self.assertEqual(second, 0)
        self.assertEqual(resolved_paths, [repository.resolve(), repository.resolve()])

    def test_review_error_returns_code_one(self):
        with patch("lcr.cli.review_repository", side_effect=ValueError("bad review")):
            stderr = StringIO()
            with redirect_stdout(StringIO()), redirect_stderr(stderr):
                exit_code = main([
                    "review", "--from", "main", "--to", "feature",
                    "--path", ".", "--name", "LKFont",
                ])

        self.assertEqual(exit_code, 1)
        self.assertIn("错误: bad review", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
