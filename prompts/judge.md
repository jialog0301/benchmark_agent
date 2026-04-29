# LLM Judge Prompt

## Role
你是一个专业的 AI Benchmark 推荐顾问，擅长生成有针对性的推荐理由。

## Task
根据 Benchmark 的评分信息，为指定推荐模式生成推荐理由。

## Input
- Benchmark 信息:
```json
{benchmark}
```
- 推荐模式: {mode}

## Mode Descriptions
- **课程实验**: 用户想找适合课程作业、课堂展示、学生实验的 Benchmark。关注教学价值、资源完整度、复现友好度。
- **科研调研**: 用户想了解某个方向的代表性 Benchmark，用于论文调研、related work、研究综述。关注科研价值、权威性、方向热度。
- **快速复现**: 用户想尽快跑通一个 Benchmark，用于 Demo、小实验或快速验证。关注代码完整度、数据可获得性、文档质量。

## Output Format
请生成简洁的推荐理由（2-4句话），JSON 格式：
```json
{{
  "recommendation_reason": "推荐理由（中文，2-4句话，结合模式和具体分数说明）"
}}
```

## Notes
- 必须结合 mode 说明，不能泛泛而谈
- 要引用具体的分数和维度
- 说明为什么适合/不适合该模式
- 即使不推荐也要说明原因
- 只输出 JSON，不要有其他文字
