"""Report Writer module."""

import os
import json
import re
import pandas as pd
from pathlib import Path
from typing import List, Dict

try:
    from src.llm_client import call_llm
except ImportError:
    call_llm = None

BASE_DIR = Path(__file__).resolve().parent.parent

def generate_report(topic: str, mode: str, ranked_benchmarks: List[Dict]) -> str:
    """
    Generate final Markdown report and save output files.

    Args:
        topic: Research topic
        mode: Recommendation mode
        ranked_benchmarks: List of ranked benchmarks

    Returns:
        Markdown report string
    """
    # 确保输出目录存在
    outputs_dir = BASE_DIR / "outputs"
    outputs_dir.mkdir(exist_ok=True)
    
    # 1. 导出 CSV 文件
    try:
        df = pd.DataFrame(ranked_benchmarks)
        df.to_csv(outputs_dir / "benchmark_table.csv", index=False, encoding="utf-8-sig")
    except Exception as e:
        print(f"Failed to export CSV: {e}")

    report = None
    
    # 2. 尝试调用 LLM 生成报告
    if call_llm is not None:
        try:
            prompt_path = BASE_DIR / "prompts" / "report_writer.md"
            with open(prompt_path, "r", encoding="utf-8") as f:
                prompt_template = f.read()
                
            benchmarks_str = json.dumps(ranked_benchmarks, ensure_ascii=False, indent=2)
            prompt = prompt_template.replace("{topic}", topic).replace("{mode}", mode).replace("{ranked_benchmarks}", benchmarks_str)
            
            system_msg = "你是一个专业的技术报告撰写助手，擅长生成结构清晰、内容详实的调研报告。"
            report = call_llm(prompt=prompt, system=system_msg)
            
            # 清理 MiniMax 的 thinking tag
            if "[Thinking]:" in report:
                report = "\n".join([line for line in report.split("\n") if not line.startswith("[Thinking]:")])
                report = report.strip()
                
            # 清理 Markdown 代码块包裹
            report = re.sub(r"^```(?:markdown)?\s*", "", report, flags=re.IGNORECASE)
            report = re.sub(r"```\s*$", "", report)
            report = report.strip()
                
        except Exception as e:
            print(f"LLM Generation failed, fallback to template: {e}")
            report = None

    # 3. 如果大模型调用失败，或是没有配置，走一个默认模板兜底
    if not report:
        # 组装 Benchmark 简单表格
        summary_table = "| 排名 | Benchmark 名称 | 任务类型 | Task-Fit Score |\n|---|---|---|---|\n"
        for idx, bm in enumerate(ranked_benchmarks):
            bm_name = str(bm.get('name', 'N/A')).replace('\n', ' ')
            bm_type = str(bm.get('task_type', 'N/A')).replace('\n', ' ')
            summary_table += f"| {idx+1} | **{bm_name}** | {bm_type} | {bm.get('task_fit_score', 0):.2f} |\n"

        # Top Benchmark 分析组装
        top_analysis = ""
        for idx, bm in enumerate(ranked_benchmarks[:3]):
            bm_name = str(bm.get('name', 'N/A')).replace('\n', ' ')
            reason = str(bm.get('recommendation_reason', '暂无')).replace('\n', ' ')
            top_analysis += f"### Top {idx+1}: {bm_name}\n"
            top_analysis += f"- **Task-Fit Score**: {bm.get('task_fit_score', 0):.2f}\n"
            top_analysis += f"- **推荐理由**: {reason}\n"
            top_analysis += f"- **开源情况**: {'开源' if bm.get('open_source') else '闭源/未知'}\n"
            top_analysis += f"- **代码链接**: {bm.get('code_url', '暂无')}\n\n"

        report = f"""# BenchmarkRadar Report: {topic}

## 1. 调研主题
**{topic}**

## 2. 推荐模式
**{mode}**

## 3. 背景与动机
本报告围绕 {topic} 进行定向自动调研，并根据“{mode}”模式的要求，对调研得到的一系列 Benchmark 进行了过滤与结构化评价抽取，旨在为您提供最符合当前场景的最佳基准测试推荐。

## 4. Benchmark 总览
总计调研出 **{len(ranked_benchmarks)}** 个相关 Benchmark。整体均具备一定的相关性。

## 5. Benchmark 结构化对比表及排名
以下是根据 Task-Fit Score 排序的推荐列表：

{summary_table}

## 6. Top Benchmark 深度分析

{top_analysis}

## 7. 推荐使用方案
考虑到你选择的模式为“**{mode}**”，优先考虑排名靠前的 Benchmark 作为首选。

## 8. 局限性
本文档为基于自动化检索与结构化总结自动生成的版本，具体复现请参考原网站。

## 9. 参考资料
"""
        for bm in ranked_benchmarks:
            urls = [bm.get('paper_url'), bm.get('code_url'), bm.get('dataset_url'), bm.get('leaderboard_url')]
            urls = [u for u in urls if u]
            if urls:
                report += f"- **{bm.get('name', 'N/A')}**: {', '.join(urls)}\n"
            if bm.get('evidence'):
                for ev in bm['evidence']:
                   report += f"  - Evidence: {ev}\n"

    # 4. 生成最终 .md 文件到 outputs/
    try:
        with open(outputs_dir / "final_report.md", "w", encoding="utf-8") as f:
            f.write(report)
    except Exception as e:
        print(f"Failed to write markdown report to file: {e}")

    return report