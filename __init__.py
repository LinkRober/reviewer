#!/usr/bin/env python3

from pathlib import Path
import json

from dotenv import load_dotenv
import argparse,subprocess

from reviewer import RuleReviewer
from llm import LLMAdaptor

def load_text(file:str) -> str:
    base_dir = Path(__file__).resolve().parent
    prompt_template = (base_dir / file).read_text(encoding="utf-8")
    return prompt_template

def make_prompt(role:str,common:str,content:str,range:str) -> str:
    prompt = role.replace("{rule}", content)
    prompt = prompt.replace("{range}", range)
    prompt = prompt.replace("{common_rule}",common)
    return prompt

def make_judge_prompt(role:str,common:str) -> str:
    prompt = role.replace("{common_rule}",common)
    return prompt

"""公共规则prompt"""
common_prompt = load_text("./prompt/common.md")

"""角色prompt"""
rule_role = load_text("./prompt/rule_role.md")
arch_role = load_text("./prompt/arch_role.md")
judge_role = load_text("./prompt/judger_role.md")

"""coding规则prompt"""
rule_prompt = load_text("./prompt/ios_coding_rule.md")
arch_prompt = load_text("./prompt/arch_prompt.md")

"""范围"""
range = {}
parser = argparse.ArgumentParser()
parser.add_argument("--from", required=True) # 基线分支
parser.add_argument("--to", required=True) # 开发分支
parser.add_argument("--path", required=True) # 库的本地地址
parser.add_argument("--name", required=True) # 库名称
args = parser.parse_args()

range['componentPath'] = args.path
range['componentName'] = args.name

repo_path = Path(
    f"{range['componentPath']}{range['componentName']}"
).expanduser().resolve()
print(f"path:{repo_path}")
if not repo_path.is_dir():
    parser.error(f"仓库路径不存在或不是目录: {repo_path}")

def run_git(*git_args):
    return subprocess.run(
        ["git", *git_args],
        cwd=repo_path,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()

from_revision = f"origin/{getattr(args, 'from')}^{{commit}}"
from_commit_hash = run_git("rev-parse", from_revision)

to_revision = f"origin/{args.to}^{{commit}}"
to_commit_hash = run_git("rev-parse", to_revision)

mergebase_hash = run_git("merge-base", from_commit_hash, to_commit_hash)

diffSpec = f"{mergebase_hash}..{to_commit_hash}"
code_diff = run_git("diff", diffSpec)


range['baseSha'] = from_commit_hash # 对比分支当前对应的固定提交
range['headSha'] = to_commit_hash # 开发分支当前对应的固定提交
range['mergeBaseSha'] = mergebase_hash # 两个分支最近的共同祖先
range['diffSpec'] = diffSpec # 真正交给 Agent 审核的提交范围
range_prompt = json.dumps(range, ensure_ascii=False, indent=2)

rule_prompt = make_prompt(rule_role,common_prompt,rule_prompt,range_prompt)
arch_prompt = make_prompt(arch_role,common_prompt,arch_prompt,range_prompt)
judger_prompt = make_judge_prompt(judge_role,common_prompt)

llm = LLMAdaptor()
rule_reviewer = RuleReviewer("rule_reviewer", llm, system_prompt=rule_prompt)
rule_result = rule_reviewer.run(code_diff)
arch_reviewer = RuleReviewer("arch_reviewer", llm, system_prompt=arch_prompt)
arch_result = arch_reviewer.run(code_diff)
preResult = {}
preResult["rule"] = rule_result
preResult["arch"] = arch_result
judger = RuleReviewer('judge_reviewer',llm,system_prompt=judger_prompt)
print(f"================开始总结==============\n")
judge_input = json.dumps(preResult, ensure_ascii=False, indent=2)
result = judger.run(judge_input)

