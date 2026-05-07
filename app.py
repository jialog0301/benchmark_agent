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

# Input section
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

if st.button("🚀 开始分析", type="primary"):
    if not topic:
        st.error("请输入调研主题")
    else:
        st.session_state.result = None
        with st.status("Agent 执行过程...", expanded=True) as status:
            try:
                st.write("⏳ 启动 Planner Agent 生成搜索计划...")
                st.write("⏳ 唤醒 Search Agent 检索资料 (接口/缓存)...")
                st.write("⏳ 唤醒 Extractor Agent 抽取 Benchmark 信息...")
                st.write("⏳ 唤醒 Scorer Agent 计算 Task-Fit Score...")
                st.write("⏳ 唤醒 Judge Agent 生成推荐理由...")
                st.write("⏳ 唤醒 Report Agent 生成 Markdown 报告...")
                result = run_benchmark_radar(topic, mode, use_cache)
                st.session_state.result = result
                status.update(label="✅ 数据分析完成！", state="complete", expanded=False)
            except Exception as e:
                status.update(label="❌ 数据分析失败", state="error", expanded=False)
                st.error(f"执行过程中发生错误: {e}")

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
        
        # 使用 column_config 优化可视化
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
