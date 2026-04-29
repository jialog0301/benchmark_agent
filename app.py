"""Streamlit app for BenchmarkRadarAgent."""

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
        with st.spinner("分析中..."):
            result = run_benchmark_radar(topic, mode, use_cache)

        # Display results
        st.success("分析完成！")

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
            st.dataframe(df[display_cols], use_container_width=True)

            # Top recommendation
            st.subheader("🏆 Top 推荐")
            top = result["ranked_benchmarks"][0]
            st.markdown(f"**{top['name']}** (Score: {top['task_fit_score']:.2f})")
            if top.get("recommendation_reason"):
                st.markdown(top["recommendation_reason"])

        # Final report
        if result.get("final_report"):
            st.subheader("📝 最终报告")
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
