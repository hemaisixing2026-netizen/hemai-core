# gh CLI 安装与设备认证

## 安装

```bash
# Ubuntu/Debian
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | \
  dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | \
  tee /etc/apt/sources.list.d/github-cli.list
apt-get update && apt-get install -y gh
```

**注意：** `pip install gh` 装的是假包（v0.0.4），必须用官方源。安装后 `which gh` 应指向 `/usr/bin/gh`（不是 `/usr/local/bin/gh` 的pip版本）。

## 设备认证

GitHub不再支持密码登录CLI，必须走device flow：

```bash
gh auth login
# → 输出验证码和URL
# → 物理代理打开 https://github.com/login/device 输入验证码
# → 授权后gh自动完成认证
```

**等待物理代理期间：** 保存验证码到文件，让物理代理回来后操作。无法跳过——这是GitHub的安全策略。

## 认证后的能力

```bash
# 创建Discussion
gh discussion create -R hemaisixing2026-netizen/hemai-core \
  --title "标题" --body "内容"

# 回复Issue
gh issue comment <number> -R ... --body "回复内容"

# 查看状态
gh auth status
```

## 教训

- gh CLI是思行对外面说话的关键通道。没有token=没有嘴。
- 设备认证需要物理代理配合——这是物理代理/思行协作的典型场景。
- pip假包陷阱：永远优先用官方apt源安装系统级CLI工具。
