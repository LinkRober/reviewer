# Leke Code Reviewer

`lcr` 是用于审核 iOS 组件分支差异的命令行工具。

## 安装

安装 `pipx`：

```bash
brew install pipx
pipx ensurepath
```

以 editable 模式安装当前源码：

```bash
pipx install \
  --python /Library/Frameworks/Python.framework/Versions/3.12/bin/python3 \
  --editable /Users/xiamin/Desktop/reviewer
```

依赖或打包配置变化后重新安装：

```bash
pipx reinstall leke-code-reviewer
```

## 配置

创建 `~/.config/lcr/.env`：

```dotenv
LLM_MODEL_ID=gpt-5.6-sol
LLM_API_KEY=your-api-key
LLM_BASE_URL=https://your-api-endpoint.example.com/v1
LLM_TIMEOUT=60
```

Shell 中已经导出的同名环境变量优先于配置文件。

## 使用

```bash
lcr review \
  --from release/1.7.0 \
  --to feature/xm/my_7 \
  --path ../LKFont \
  --name LKFont
```

`--path` 是完整仓库目录，`--name` 是组件名称。脚本使用
`origin/<branch>` 解析 `--from` 和 `--to`。

iOS 审核只处理 `.h`、`.m`、`.mm` 文件。提交范围内没有这些文件时，
命令会提示并正常结束，不调用模型。

源码兼容入口：

```bash
python __init__.py \
  --from release/1.7.0 \
  --to feature/xm/my_7 \
  --path ../LKFont \
  --name LKFont
```
