# Model selection / 模型选择

Reviewed 2026-11-24. This is a provisional routing decision based on the refreshed local catalog and official model/cost documentation, not a benchmark of this user's completed tasks.

检查日期：2026-11-24。以下是根据刷新后的客户端模型目录与官方资料制定的初始分工，不是用户真实任务的模型对照实验。

## Evidence / 依据

The local selectable catalog lists ten general models: `gpt-6.2-sol`, `gpt-6.2-astra`, `gpt-6.1-terra`, `gpt-6.1-sol`, `gpt-6-astra`, `gpt-6-sol`, `gpt-6-luna`, `gpt-5.6-sol`, `gpt-5.6-terra`, `gpt-5.6-luna`. Hidden reserve/approval models are not general worker candidates. Catalog presence establishes selectable metadata, not guaranteed quota or successful execution of every model. Do not publish the raw catalog: it contains internal prompt material unnecessary for this package.

目录中有上述十个可选通用模型；隐藏的备用和审批模型不纳入分工。目录可见不代表已验证所有模型的运行及额度。不要公开包含无关内部提示材料的原始目录。

Official Standard-speed **credits per million tokens** (input / cached input / output):

| Model | Input | Cached | Output | Decision / 分工 |
| --- | ---: | ---: | ---: | --- |
| GPT-6.2 Sol | 50 | 2.5 | 250 | Default orchestration/execution, medium; hard planning, high / 默认编排执行 medium，困难规划 high |
| GPT-6.1 Sol | 50 | 2.5 | 250 | Previous-generation explicit fallback / 旧版显式备选 |
| GPT-6.2 Astra | 200 | 10 | 1,000 | Independent reviewers, high / 独立审核 high |
| GPT-6 Astra | 250 | 25 | 1,250 | Previous-generation explicit fallback / 旧版显式备选 |
| GPT-6.1 Terra | 25 | 1.25 | 125 | Visual/computer-use specialist, medium / 视觉操作专项 medium |
| GPT-6 Luna | 2.5 | 0.25 | 12.5 | Clear low-risk tasks only, medium / 明确低风险任务 medium |

These are credit rates, not USD API rates or an estimate of included subscription task counts. With equal token mix, 6.2 Sol has the same rate as 6.1 Sol; 6.2 Astra's uncached-input and output rates are 20% lower than old Astra, and cached-input rate 60% lower. Different token usage, retries, tools and reasoning may change actual task cost. Astra costs 4x Sol per token at these rates; Terra 0.5x Sol; Luna's uncached input/output 0.05x Sol. None of these ratios establish cost per correct task.

这是积分单价，不是 API 美元价格，也不能换算订阅内可完成任务数。相同 token 组合下，新 Sol 与旧 Sol 同价；新 Astra 普通输入及输出便宜 20%，缓存输入便宜 60%。实际任务的 token、重试、工具和推理开销会变化；单价比例不等于每个正确完成任务的成本比例。

## Quality and escalation / 质量与升级

Official positioning favors 6.2 Sol for everyday coding/cost balance and 6.2 Astra for the hardest professional work. Retain medium effort for ordinary orchestration: evaluating dependencies and deciding delegation merit real reasoning. Keep high for frontier review instead of weakening acceptance to save tokens. Luna is restricted to mechanically clear low-risk work; failed checks or ambiguity escalate to Sol. Terra is a specialization, not a replacement for general reasoning or frontier acceptance. Legacy models remain available as explicit alternatives rather than automatic fallbacks; temporary promotions do not justify a permanent default.

根据官方定位，6.2 Sol 适合日常编程与成本平衡，6.2 Astra 用于困难专业工作。编排保留 medium，避免削弱复杂度和依赖判断；审核保留 high，不能为省 token 放松验收。Luna 只处理明确低风险任务，歧义或验证失败升级到 Sol。Terra 用于专项视觉操作，不替代通用推理和独立验收。旧模型仅作显式备选，临时优惠不作为长期默认理由。

Do not automatically enable Fast/Ultrafast or max/ultra. Keep the user's existing speed setting unchanged; speed multipliers may raise usage. Preserve standard one-review and enhanced three-review modes. Escalation changes model/effort only when justified; material scope/resource changes still follow human approval rules.

不自动启用加速档或 max/ultra，保留已有速度设置；加速可能增加消耗。标准单审、增强三审不变。有依据时才升级模型与推理；实质范围或资源变化仍遵守人工审批规则。

There is no measured user-specific quality, latency, token-efficiency or ROI comparison yet. Track trusted outcome labels, escaped defects, completion, retries, reasoning/output tokens, elapsed time and human effort by task class. Choose the least costly configuration meeting validated quality requirements; do not claim achieved numeric reliability from model age, price or reviewer agreement.

尚无用户真实任务的质量、延迟、token 效率或 ROI 对照数据。后续按任务类别记录可信结果、漏检、完成率、重试、推理与输出 token、耗时及人工投入；在满足已验证质量要求的配置中选总成本最低者。

## Official sources / 官方来源

- [Models](https://learn.chatgpt.com/docs/models)
- [Codex / Work pricing](https://learn.chatgpt.com/docs/pricing)
- [GPT-6.2 Sol](https://developers.openai.com/api/docs/models/gpt-6.2-sol)
- [GPT-6.2 Astra](https://developers.openai.com/api/docs/models/gpt-6.2-astra)
