from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from lcr.workflow import NoReviewableFiles, collect_diff


class FilteringTests(unittest.TestCase):
    def test_non_ios_only_diff_does_not_reach_model(self):
        outputs = ["true", "base", "head", "merge", ""]
        with TemporaryDirectory() as directory:
            with patch("lcr.workflow.run_git", side_effect=outputs):
                with self.assertRaises(NoReviewableFiles):
                    collect_diff(
                        Path(directory),
                        "main",
                        "feature",
                        ".",
                        "repo",
                    )


if __name__ == "__main__":
    unittest.main()
