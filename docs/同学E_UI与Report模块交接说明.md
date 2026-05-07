# 同学 E UI & Report 模块交接说明

## 1. 我负责的范围

我负责的是前端界面展示（UI）以及最终报告的生成（Report Writer）。其职责是将整套系统的中间结果汇总为可视化页面与可下载交付物，供最终用户查看和使用。

对应文件：
- `app.py` （Streamlit 前端完整交互实现）
- `src/reporter.py` （Markdown 报告与 CSV 导出逻辑）
- `prompts/report_writer.md` （让 LLM 汇总写报告的 Prompt）
- `outputs/` （系统最终输出内容的存放地）

我没有负责：
- B/C/D 模块的数据检索、抽取和打分排序等底层逻辑。我是他们产生结果的最终消费者。

---

## 2. 模块在整体 pipeline 中的位置

整体流程是：
User Input  
→ Query Planner (B)  
→ Search Agent (B)  
→ Benchmark Extractor (C)  
→ Task-Fit Scorer (D)  
→ LLM Judge (D)  
**→ Report Writer (E) （在这里将数据总结为文本和图表）**  
**→ Streamlit UI (E) （在这里呈现给用户）**

E 模块是 pipeline 的最后一环，直接面对最终用户。

---

## 3. 对外接口

`src/reporter.py` 的核心接口：

```python
def generate_report(topic: str, mode: str, ranked_benchmarks: List[Dict]) -> str:
    ...
```

`app.py` 中直接导入 `run_benchmark_radar` 获取 D 的输出，然后调用 `generate_report`，或者在系统 pipeline 内部统一调用。

---

## 4. app.py 做了什么（UI 端）

`app.py` 是整个工程的前端入口，除基础交互外，还承担结果展示与状态管理职责：

1. **交互界面与状态展示**：
   - 实现了左侧边栏参数配置。
   - 使用 `st.status` 展示执行过程，便于观察 Planner -> Search -> Extractor -> Scorer 的阶段推进。

2. **Session 状态管理（防超额耗流）**：
   - 实现了 `st.session_state` 缓存机制。首次得到结果后，后续页面重绘（如点击下载按钮、切换 Tab）不会重复触发后端 Pipeline，从而减少重复计算与 API 消耗。

3. **高阶可视化表格 (`st.column_config`)**：
   - D 同学输出的 `Task-Fit Score` 和各个评分维度（例如 1-5 分的教学价值）通过 `st.column_config` 配置为进度条样式，便于快速读取。

4. **异常全局拦截**：
   - 在核心调度逻辑外层增加 `try-except` 兜底，发生异常时仅提示错误信息，不中断 Streamlit 进程运行。

---

## 5. reporter.py 做了什么（报告端）

`src/reporter.py` 负责将排序结果生成最终报告并导出配套文件。

1. **多元物料导出**：
   - 生成 Markdown 报告，同时使用 `pandas` 将 D 同学的 `ranked_benchmarks` 导出为 CSV 文件（`benchmark_table.csv`）。

2. **请求大模型总结**：
   - 将 topic、mode 和排序结果填入 `prompts/report_writer.md`，生成结构化的 Markdown 报告。
   - 通过正则清理模型输出中的代码块包裹和 `[Thinking]` 标签，保证最终报告格式稳定。
   - 当前报告模板已与兜底模板对齐，核心结构为“结构化对比表及排名 + Top Benchmark 深度分析 + 推荐使用方案”，避免章节重复或编号跳号。

3. **健壮的 Fallback （模型失效兜底）**：
   - 当 LLM 不可用或网络异常时，系统自动切换到本地模板兜底，不影响最终报告生成。
   - 兜底模板会生成排名表格，并整合 Top 3 Benchmark 的推荐理由（来源于 D 模块）。
   - 代码中使用 `pathlib.Path` 进行路径定位，以降低工作区根目录变化带来的读写问题。

---

## 6. 输出及缓存文件

E 模块最终输出位于项目根目录的 `outputs/` 目录：

- `outputs/benchmark_table.csv` （完整表格）
- `outputs/final_report.md` （图文长文报告）

---

## 7. 给其他同学（尤其是 A 负责统筹）的注意事项

- E 的报告依赖 D 输出的结构完整性；若字段缺失，CSV 导出或兜底表格中可能出现空值。
- 若后续新增前端组件，应同步检查 `app.py` 中的 `session_state` 逻辑，避免重复触发 Pipeline。
- 当前路径解析基于 `__file__` 上溯到项目根目录；若目录结构调整，需要同步更新 `BASE_DIR` 解析规则。

---

## 8. 自测方式

可以使用以下方式验证 E 模块输出是否正常：

```bash
python - <<'PY'
from src.pipeline import run_benchmark_radar

result = run_benchmark_radar("AI Agent Evaluation Benchmark", "课程实验", use_cache=True)
assert isinstance(result, dict)
assert "ranked_benchmarks" in result
assert "final_report" in result
assert result["final_report"].startswith("# BenchmarkRadar Report")
print("E module smoke test passed")
PY
```

预期结果：

- 能正常返回 `ranked_benchmarks`
- 能正常生成 `final_report`
- 报告标题符合 `BenchmarkRadar Report` 格式

---

## 9. 已知边界

- E 模块对 D 模块输出字段有依赖；若上游字段缺失，展示结果会受到影响。
- 当 LLM 不可用时，报告将回退到本地模板，内容完整性优先于生成质量。
- 当前报告章节结构已与 `prompts/report_writer.md` 和 `src/reporter.py` 的兜底模板保持一致；若任一处调整，需要同步更新其余两处。

---

## 10. 交接结论

E 模块（UI 与 Report）已经完成并具备稳定输出能力，能够支撑完整的终端展示、结果下载与报告生成流程。当前实现满足项目的基础交付要求，可直接用于联调和演示。
