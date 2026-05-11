"""
MarketMind — 多 Agent 协作市场研究系统
运行前请设置环境变量: export ANTHROPIC_API_KEY="your-api-key"
"""

import anthropic
import datetime
import sys

client = anthropic.Anthropic()

def log(agent_name: str, emoji: str, message: str):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {emoji} {agent_name} — {message}")


def call_claude(system_prompt: str, user_message: str) -> str:
    """调用 Claude API"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1500,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}]
    )
    return response.content[0].text


# ──────────────────────────────────────────────
# Agent 1: Search Agent
# 负责将研究主题拆解为关键词，并模拟多源信息检索
# ──────────────────────────────────────────────
def search_agent(topic: str) -> str:
    log("Search Agent", "🔍", f"启动 — 研究主题: {topic}")

    # Step 1: 拆解关键词
    keywords_raw = call_claude(
        system_prompt="你是一个市场研究关键词分析专家。用户给你一个研究主题，你需要将其拆解为4个最重要的搜索关键词。直接输出关键词列表，格式为Python列表，例如：['关键词1', '关键词2', '关键词3', '关键词4']，不要输出任何其他内容。",
        user_message=f"研究主题：{topic}"
    )
    log("Search Agent", "🔍", f"拆解关键词: {keywords_raw.strip()}")

    # Step 2: 模拟检索并生成摘要
    summaries = call_claude(
        system_prompt="你是一个市场信息检索专家。根据给定的关键词列表，为每个关键词生成一段真实、具体、有数据的市场信息摘要（2-3句话）。用编号列表格式输出。",
        user_message=f"研究主题：{topic}\n关键词列表：{keywords_raw}\n\n请为每个关键词生成对应的市场信息摘要。"
    )

    log("Search Agent", "🔍", "完成资料收集，共 4 条摘要")
    return summaries


# ──────────────────────────────────────────────
# Agent 2: Analysis Agent
# 负责多步推理分析，提炼趋势与洞察
# ──────────────────────────────────────────────
def analysis_agent(topic: str, raw_data: str) -> str:
    log("Analysis Agent", "🧠", "启动 — 开始多步推理分析")

    analysis = call_claude(
        system_prompt="""你是一个资深市场分析师，擅长从原始资料中进行多步推理，提炼核心洞察。
请按以下结构输出分析结果：
1. 核心市场趋势（3条）
2. 主要机会点（2条）
3. 潜在风险（2条）
4. 综合判断（1段）
语言简洁有力，每条附具体数据或例证。""",
        user_message=f"研究主题：{topic}\n\n原始资料：\n{raw_data}"
    )

    log("Analysis Agent", "🧠", "分析完成")
    return analysis


# ──────────────────────────────────────────────
# Agent 3: Report Agent
# 负责将分析结果整合为完整研究报告
# ──────────────────────────────────────────────
def report_agent(topic: str, analysis: str) -> str:
    log("Report Agent", "📝", "启动 — 开始生成报告")

    report = call_claude(
        system_prompt="""你是一个专业报告撰写专家。根据提供的分析结果，生成一份结构清晰、语言专业的市场研究报告。
报告格式：
# 市场研究报告：[主题]
## 执行摘要
## 市场趋势分析
## 机会与风险评估
## 战略建议
## 结论

语言专业、数据有支撑、结论明确。""",
        user_message=f"研究主题：{topic}\n\n分析结果：\n{analysis}"
    )

    log("Report Agent", "📝", "报告生成完成")
    return report


# ──────────────────────────────────────────────
# 主流程：三个 Agent 顺序协作
# ──────────────────────────────────────────────
def run_market_research(topic: str):
    print("\n" + "="*60)
    print(f"🚀 MarketMind 多Agent市场研究系统启动")
    print(f"📌 研究主题：{topic}")
    print("="*60 + "\n")

    # Agent 1: 检索
    raw_data = search_agent(topic)
    print()

    # Agent 2: 分析
    analysis = analysis_agent(topic, raw_data)
    print()

    # Agent 3: 报告
    report = report_agent(topic, analysis)
    print()

    # 输出最终报告
    print("="*60)
    print(f"📊 市场研究报告：{topic}")
    print("="*60)
    print(report)
    print("="*60 + "\n")

    return report


if __name__ == "__main__":
    # 默认研究主题，可通过命令行参数修改
    topic = sys.argv[1] if len(sys.argv) > 1 else "国内新能源汽车市场"
    run_market_research(topic)
