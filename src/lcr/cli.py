import argparse
from pathlib import Path
import sys
from typing import Sequence

from .config import ConfigurationError
from .llm import LLMError
from .workflow import ReviewError, review_repository


def build_parser() -> argparse.ArgumentParser:
    # 工具名称
    parser = argparse.ArgumentParser(
        prog="lcr",
        description="乐刻代码审核命令行工具",
    )
    # 命令
    subparsers = parser.add_subparsers(dest="command", required=True)
    review_parser = subparsers.add_parser("review", help="审核两个远程分支之间的差异")
    # 参数
    review_parser.add_argument(
        "--from",
        dest="from_branch",
        required=True,
        help="基线分支",
    )
    review_parser.add_argument(
        "--to",
        dest="to_branch",
        required=True,
        help="开发分支",
    )
    review_parser.add_argument(
        "--path",
        type=Path,
        required=True,
        help="仓库父目录",
    )
    review_parser.add_argument("--name", required=True, help="仓库目录名")
    review_parser.set_defaults(handler=run_review)
    return parser


def run_review(args: argparse.Namespace) -> int:
    repo_path = (args.path.expanduser() / args.name).resolve()
    print(f"path:{repo_path}")
    review_repository(
        repo_path=repo_path,
        from_branch=args.from_branch,
        to_branch=args.to_branch,
        component_path=str(args.path),
        component_name=args.name,
    )
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.handler(args)
    except (ConfigurationError, LLMError, ReviewError, ValueError) as error:
        print(f"错误: {error}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("审核已取消", file=sys.stderr)
        return 130
