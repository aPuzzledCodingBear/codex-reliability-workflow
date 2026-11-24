# Codex 可靠性工作流

[English](README.md)

面向复杂多步骤任务的可移植个人配置：按风险选择流程，结合计划审查、人工批准、过程验证和独立验收，在合理总成本下减少重大错误。目前不声称达到任何数值错误率。

## 工作流程

1. 主代理评估复杂度、失败影响、不确定性和可验证性。简单可逆任务直接执行；复杂任务先推荐标准或增强流程，由用户选择。
2. 计划写明范围、任务依赖、模型分工、资源预期及验收条件。独立 frontier 代理检查计划和验收方法，再由用户批准具体版本。
3. 执行批准的子任务并保存证据。高影响中间结果先验证，再供后续步骤使用。独立任务可并行，相互依赖或写入冲突的任务串行。
4. 最终验收使用批准的方法和阈值，逐项提供证据。同时独立检查验收方法是否充分覆盖原始需求。
5. 标准模式使用一个全新 frontier 验收代理；增强模式使用三个先互相隔离的审计代理，分别侧重需求覆盖、独立复现和反例。按证据裁决，不按多数投票。
6. 修复后复核；实质变化需要重新审查或批准计划。关键项目没有证据时保持 UNVERIFIED，不能算通过。

## 安装

需要 Python 3.11+，以及支持当前自定义代理配置格式的本地 Codex 客户端。安装前请检查源码。

```sh
git clone https://github.com/aPuzzledCodingBear/codex-reliability-workflow.git
cd codex-reliability-workflow
python3 install.py --dry-run
python3 install.py
```

通过 `--target PATH` 指定 Codex home；默认读取 `CODEX_HOME`，未设置时使用 `~/.codex`。安装后新建会话或重启客户端；已有会话可能仍保留旧指令。

安装器在全局 `AGENTS.md` 及已有的 `AGENTS.override.md` 中合并带标记规则，安装九个角色及 `reliability/WORKFLOW.md`，允许最多三个子代理，并将主模型和默认子代理设为 `gpt-6.2-sol`、medium 推理。保留其他指令和权限、认证、供应商、MCP、插件等设置。写入前备份原文件，重复安装不会重复添加规则。

对整个 TOML 解析结果核对，只允许预定的设置变化；不支持的布局在写入前停止，避免误改字符串中的内容。

## 模型分工

| 角色 | 请求模型 | 推理强度 |
| --- | --- | --- |
| 主编排、普通执行代理 | `gpt-6.2-sol` | medium |
| 困难任务规划代理 | `gpt-6.2-sol` | high |
| 计划审查、验收及增强审计 | `gpt-6.2-astra` | high |
| 明确、低风险的轻量代理 | `gpt-6-luna` | medium |
| 视觉理解、电脑操作专项代理 | `gpt-6.1-terra` | medium |

这些是请求配置，不代表已验证模型可用。若没有对应模型，请明确选择可用替代，修改 `POLICY.md` 和角色 TOML 后重新安装。若更换主模型或默认子代理模型，还需修改 `install.py` 中的设置及语义保留校验预期。不能静默降低审核模型。模型名称与配置支持可能随客户端版本变化。

## 多设备

在**每个独立执行任务的设备**上安装。远程控制已配置主机的客户端使用该主机配置。本包不自动同步设备，也不配置远程访问。规则更新后，各主机拉取并重新安装。

托管的 ChatGPT Work／网页会话不读取本地文件。受管理的规则、项目指令和显式覆盖可能影响实际行为。

## 证据、隐私与恢复

`WORKFLOW.md` 定义任务记录：需求 → 验收条件 → 方法 → 阈值 → 证据 → PASS／FAIL／UNVERIFIED。没有授权时不公开运行记录。

`<Codex home>/reliability/backups/<timestamp>/` 中的备份可能包含原有私密配置，**不要提交或上传**。原始提示诊断、本地验证报告、缓存和任务证据均不属于发布内容。发布前检查了源码中的凭据、个人路径、联系方式及设备记录；检查有范围限制，不能保证发现一切秘密。

```sh
python3 -m unittest discover -s tests -v
python3 install.py --dry-run
```

客户端支持时可用 `codex debug prompt-input` 检查指令加载。输出可能含私人上下文，不要公开。部分诊断子命令不接受 `--strict-config`。

恢复时查看备份中的 `manifest.json`：还原原有文件，仅移除其中记录的新建文件。安装后若修改过其他设置，先保留这些变化，不要直接覆盖为旧配置。

## 可靠性边界

这是行为指令，不是强制 CI 门禁、独立只读沙箱或统计证明。三名审核者一致通过不能证明错误概率很小。数值可靠性需要可信结果标签、明确任务类别的完整流程留出集评估、置信区间及分布漂移检查；同时记录完成率、未完成／拒绝交付与漏检错误。

## 参考资料

- [Codex 子代理](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [全局 AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [设置与环境边界](https://learn.chatgpt.com/docs/developer-settings)
- [Conformal Risk Control](https://arxiv.org/abs/2208.02814)
- [Towards a Science of Scaling Agent Systems](https://arxiv.org/abs/2512.08296)

初次发布尚未选择许可证；公开仓库本身不等于授予开源许可。

模型选择与带日期的定价依据：[English / 中文](MODEL-SELECTION.md)。
