"""Streamlit app for BenchmarkRadarAgent."""

from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

import streamlit as st

from src.pipeline import run_benchmark_radar
from src.cache import get_all_cached_topics

st.set_page_config(page_title="BenchmarkRadarAgent", page_icon="📡")

st.title("📡 BenchmarkRadarAgent")

st.markdown("""
BenchmarkRadarAgent 是一个面向 AI Benchmark 调研的智能体系统。
输入研究主题和推荐模式，自动完成搜索、抽取、评分和报告生成。
""")

# ---- Input section ----
col1, col2 = st.columns(2)

with col1:
    topic = st.text_input(
        "调研主题",
        value="AI Agent Evaluation Benchmark",
        placeholder="例如: AI Agent Evaluation Benchmark"
    )

with col2:
    mode = st.selectbox(
        "推荐模式",
        options=["课程实验", "科研调研", "快速复现"],
        index=0
    )

use_cache = st.checkbox("使用缓存", value=True)

# ---- Run pipeline ----
if st.button("🚀 开始分析", type="primary"):
    if not topic:
        st.error("请输入调研主题")
    else:
        st.session_state.result = None

        # UI placeholders for each step
        plan_placeholder = st.empty()
        search_placeholder = st.empty()
        extract_placeholder = st.empty()
        score_placeholder = st.empty()
        judge_placeholder = st.empty()
        report_placeholder = st.empty()

        def on_progress(step: str, data: dict):
            """Update Streamlit UI based on pipeline progress."""
            status = data.get("status", "")

            # --- Planner ---
            if step == "planner":
                if status == "running":
                    plan_placeholder.info("🔍 **Planner** — 正在生成搜索计划...")
                elif status == "done":
                    plan_data = data.get("plan", {})
                    goals = plan_data.get("search_goals", [])
                    queries = plan_data.get("search_queries", [])
                    lines = ["✅ **Planner** — 搜索计划已生成\n"]
                    lines.append("**搜索目标:**")
                    for g in goals[:5]:
                        lines.append(f"- {g}")
                    lines.append(f"\n**搜索查询:**")
                    for q in queries[:5]:
                        lines.append(f"- `{q}`")
                    plan_placeholder.markdown("\n".join(lines))

            # --- Searcher ---
            elif step == "search":
                if status == "running":
                    search_placeholder.info("🌐 **Searcher** — 正在多源检索资料 (Tavily/arXiv/GitHub/DDG)...")
                elif status == "done":
                    count = data.get("candidate_count", 0)
                    search_placeholder.success(f"✅ **Searcher** — 检索完成，发现 **{count}** 个候选 Benchmark")

            # --- Extractor ---
            elif step == "extract":
                if status == "running":
                    extract_placeholder.info("📄 **Extractor** — LLM 正在从报告中抽取结构化 Benchmark...")
                elif status == "done":
                    names = data.get("benchmark_names", [])
                    count = data.get("benchmark_count", 0)
                    lines = [f"✅ **Extractor** — 抽取完成，获得 **{count}** 个 Benchmark:\n"]
                    for i, name in enumerate(names, 1):
                        lines.append(f"| {i} | **{name}** |")
                    if lines:
                        header = lines[0]
                        table = "\n".join(lines[1:])
                        extract_placeholder.markdown(f"{header}\n\n| # | 名称 |\n|---|------|\n{table}")
                    else:
                        extract_placeholder.success(f"✅ **Extractor** — 抽取完成")

            # --- Scorer ---
            elif step == "score":
                if status == "running":
                    score_placeholder.info("📊 **Scorer** — 正在计算 Task-Fit Score...")
                elif status == "done":
                    top3 = data.get("top3", [])
                    lines = [f"✅ **Scorer** — 评分排序完成 (共 {data.get('ranked_count', 0)} 个)\n"]
                    lines.append("**Top 3:**")
                    for item in top3:
                        lines.append(f"- **{item['name']}**: {item['score']:.2f}")
                    score_placeholder.markdown("\n".join(lines))

            # --- Judge ---
            elif step == "judge":
                total = data.get("total", 0)
                current = data.get("current", 0)
                name = data.get("name", "")
                if status == "running":
                    judge_placeholder.info(f"⚖️ **Judge** — 即将为 {total} 个 Benchmark 生成推荐理由...")
                elif status == "progress":
                    judge_placeholder.info(f"⚖️ **Judge** — 正在分析 [{current}/{total}] **{name}** ...")
                elif status == "item_done":
                    thinking_text = data.get("thinking", "")
                    thinking_html = ""
                    if thinking_text:
                        thinking_html = f'<details><summary>💭 模型思考过程</summary><pre style="white-space:pre-wrap;font-size:0.85em;background:#f5f5f5;padding:8px;border-radius:4px;">{thinking_text[:800]}</pre></details>'
                    judge_placeholder.markdown(
                        f"⚖️ **Judge** — [{current}/{total}] **{name}** (Score: {data.get('score', 0):.2f})  ✅\n{thinking_html}",
                        unsafe_allow_html=True,
                    )
                elif status == "done":
                    pass  # Let the last item_done message stay visible

            # --- Reporter ---
            elif step == "report":
                if status == "running":
                    report_placeholder.info("📝 **Reporter** — LLM 正在生成最终报告...")
                elif status == "done":
                    thinking_text = data.get("thinking", "")
                    thinking_html = ""
                    if thinking_text:
                        thinking_html = f'<details open><summary>💭 模型思考过程</summary><pre style="white-space:pre-wrap;font-size:0.85em;background:#f5f5f5;padding:8px;border-radius:4px;">{thinking_text[:1000]}</pre></details>'
                    report_placeholder.markdown(
                        f"✅ **Reporter** — 最终报告已生成\n{thinking_html}",
                        unsafe_allow_html=True,
                    )

        try:
            result = run_benchmark_radar(topic, mode, use_cache, progress_callback=on_progress)
            st.session_state.result = result
        except Exception as e:
            st.error(f"执行过程中发生错误: {e}")
            st.stop()

        st.success("🎉 全流程完成！")

if st.session_state.get("result"):
    result = st.session_state.result

    # Plan
    if result.get("plan"):
        st.subheader("📋 搜索规划")
        st.json(result["plan"])

    # Benchmarks table
    if result.get("ranked_benchmarks"):
        st.subheader("📊 Benchmark 对比表")
        import pandas as pd
        df = pd.DataFrame(result["ranked_benchmarks"])
        display_cols = ["rank", "name", "task_fit_score", "teaching_value",
                       "research_value", "resource_completeness", "reproduction_difficulty"]
        display_cols = [c for c in display_cols if c in df.columns]

        st.dataframe(
            df[display_cols],
            width="stretch",
            column_config={
                "rank": st.column_config.NumberColumn("排名"),
                "name": st.column_config.TextColumn("Benchmark 名称", width="medium"),
                "task_fit_score": st.column_config.NumberColumn("Task-Fit Score", format="%.2f"),
                "teaching_value": st.column_config.ProgressColumn("教学价值", min_value=0, max_value=5, format="%d"),
                "research_value": st.column_config.ProgressColumn("科研价值", min_value=0, max_value=5, format="%d"),
                "resource_completeness": st.column_config.ProgressColumn("资源完整度", min_value=0, max_value=5, format="%d"),
                "reproduction_difficulty": st.column_config.ProgressColumn("复现难度", min_value=0, max_value=5, format="%d"),
            }
        )

        # Top recommendation
        st.subheader("🏆 Top 推荐")
        top = result["ranked_benchmarks"][0]
        st.markdown(f"**{top['name']}** (Score: {top['task_fit_score']:.2f})")
        if top.get("recommendation_reason"):
            st.markdown(top["recommendation_reason"])

    # Final report
    if result.get("final_report"):
        rep_col1, rep_col2 = st.columns([0.8, 0.2])
        with rep_col1:
            st.subheader("📝 最终报告")
        with rep_col2:
            st.download_button(
                label="📥 下载报告",
                data=result["final_report"],
                file_name=f"{topic.replace(' ', '_')}_{mode}_report.md",
                mime="text/markdown"
            )

        st.markdown(result["final_report"])

# Sidebar - cached topics
st.sidebar.title("📁 缓存数据")
cached = get_all_cached_topics()
if cached:
    st.sidebar.write("已缓存主题:")
    for t in cached:
        st.sidebar.write(f"- {t}")
else:
    st.sidebar.info("暂无缓存数据")
