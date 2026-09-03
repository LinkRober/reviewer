from importlib import resources
import json
from pathlib import Path
import subprocess

from .llm import LLMAdaptor
from .reviewer import Reviewer


class ReviewError(RuntimeError):
    """Raised when a repository cannot be reviewed."""


class NoReviewableFiles(ReviewError):
    """Raised when a diff contains no supported Objective-C files."""


IOS_FILE_EXTENSIONS = (".h", ".m", ".mm")


def load_prompt(name: str) -> str:
    prompt = resources.files("lcr.prompt").joinpath(name)
    return prompt.read_text(encoding="utf-8")


def make_prompt(role: str, common: str, content: str, review_range: str) -> str:
    return (
        role.replace("{rule}", content)
        .replace("{range}", review_range)
        .replace("{common_rule}", common)
    )


def make_judge_prompt(role: str, common: str) -> str:
    return role.replace("{common_rule}", common)


def run_git(repo_path: Path, *git_args: str) -> str:
    try:
        result = subprocess.run(
            ["git", *git_args],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True,
        )
    except FileNotFoundError as error:
        raise ReviewError("未找到 git 命令") from error
    except subprocess.CalledProcessError as error:
        detail = (error.stderr or error.stdout or "").strip()
        command = " ".join(["git", *git_args])
        raise ReviewError(f"Git 命令失败 ({command}): {detail or error}") from error
    return result.stdout.strip()


def collect_diff(
    repo_path: Path,
    from_branch: str,
    to_branch: str,
    component_path: str,
    component_name: str,
) -> tuple[str, dict[str, object]]:
    if not repo_path.is_dir():
        raise ReviewError(f"仓库路径不存在或不是目录: {repo_path}")
    if run_git(repo_path, "rev-parse", "--is-inside-work-tree") != "true":
        raise ReviewError(f"路径不是 Git 仓库: {repo_path}")

    from_revision = f"origin/{from_branch}^{{commit}}"
    to_revision = f"origin/{to_branch}^{{commit}}"
    from_commit_hash = run_git(repo_path, "rev-parse", from_revision)
    to_commit_hash = run_git(repo_path, "rev-parse", to_revision)
    merge_base_hash = run_git(
        repo_path,
        "merge-base",
        from_commit_hash,
        to_commit_hash,
    )
    diff_spec = f"{merge_base_hash}..{to_commit_hash}"
    code_diff = run_git(
        repo_path,
        "diff",
        diff_spec,
        "--",
        "*.h",
        "*.m",
        "*.mm",
    )
    if not code_diff:
        raise NoReviewableFiles(
            "提交范围内没有可审核的 iOS 文件（仅支持 .h、.m、.mm）"
        )

    review_range = {
        "componentPath": component_path,
        "componentName": component_name,
        "baseSha": from_commit_hash,
        "headSha": to_commit_hash,
        "mergeBaseSha": merge_base_hash,
        "diffSpec": diff_spec,
        "fileExtensions": list(IOS_FILE_EXTENSIONS),
    }
    return code_diff, review_range


def review_repository(
    *,
    repo_path: Path,
    from_branch: str,
    to_branch: str,
    component_path: str,
    component_name: str,
    llm: LLMAdaptor | None = None,
) -> str:
    code_diff, review_range = collect_diff(
        repo_path,
        from_branch,
        to_branch,
        component_path,
        component_name,
    )
    range_prompt = json.dumps(review_range, ensure_ascii=False, indent=2)

    common_prompt = load_prompt("common.md")
    rule_prompt = make_prompt(
        load_prompt("rule_role.md"),
        common_prompt,
        load_prompt("ios_coding_rule.md"),
        range_prompt,
    )
    arch_prompt = make_prompt(
        load_prompt("arch_role.md"),
        common_prompt,
        load_prompt("arch_prompt.md"),
        range_prompt,
    )
    judge_prompt = make_judge_prompt(load_prompt("judger_role.md"), common_prompt)

    model = llm or LLMAdaptor()
    print("================编码规范审核================")
    rule_result = Reviewer(
        "rule_reviewer",
        model,
        system_prompt=rule_prompt,
    ).run(code_diff)
    print("================架构审核================")
    arch_result = Reviewer(
        "arch_reviewer",
        model,
        system_prompt=arch_prompt,
    ).run(code_diff)

    judge_input = json.dumps(
        {"rule": rule_result, "arch": arch_result},
        ensure_ascii=False,
        indent=2,
    )
    print("================总结================")
    return Reviewer(
        "judge_reviewer",
        model,
        system_prompt=judge_prompt,
    ).run(judge_input)
