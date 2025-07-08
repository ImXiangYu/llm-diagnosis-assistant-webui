import requests
import re


def ask_medical_llm(user_input: str, model_enhancement) -> dict:
    network_information = ""
    if "🌐联网搜索" in model_enhancement:
        print("现在启动联网搜索")
        network_url="http://localhost:6666/mcp/chat"
        search=True
        network_messages = [
            {"role": "system", "content": ""},
            {"role": "user", "content": user_input}
        ]
        payload = {"messages": network_messages, "stream": False, "search": search}
        network_response = requests.post(network_url, json=payload)

        # 安全获取第一个结果
        network_information = network_response.json()[2]["content"]
        print(network_information)

    url = "http://localhost:11434/api/generate"
    system_prompt = (
        "你作为临床医生，需严格按SOAP框架（四部分）整理患者病历。"
        "你的回答一定要严格遵守每一部分的标题，例如第四部分一定要以'诊疗计划:'开头"
        "第一部分，主观信息。首先从患者病情陈述中提取关键主观信息，简洁列出患者的主要症状与持续时间，不要在本项内出现换行或列举，用一句话或一段话表述。"
        "第二部分，客观信息。除了第一部分的主观信息外，还需要整合患者提供的客观信息（医生或其他医疗专业人员通过观察、体格检查或使用仪器设备测量得到的信息），如果患者没有提供，则可以根据患者病情给出检查建议。"
        "第三部分，鉴别诊断。需要依据第一第二部分的主客观信息来推测生成Top-5可能诊断结果，按置信度从高到低排列，按照如下格式：[诊断名称] 置信度：[高/中/低] → 依据：（关键S/O证据链，限30字）。"
        "（例：1. 急性阑尾炎 置信度：高 → 依据：转移性右下腹痛+麦氏点压痛+WBC升高。2. 骨囊肿 置信度：中 → 依据：单发溶骨性病变）每个诊断要有小标号且之间一定要以句号结尾，严格符合上述格式"
        "第四部分，诊疗计划。分为两方面，一是随访方案，依据前三部分个性化设计，推荐包括时间（具体时间点），目的（评估XX/监测XX）以及内容（复查项目/症状追踪）等。二是检查建议，需明确关联目标诊断，推荐检查项目与目的（确诊/排除/监测[具体诊断或并发症）"
        "注意这四部分是由浅入深，层层深入的。你的回复一定要立足实际，严谨准确，专业细致！"
        "此外请格外注意你的回复，每一部分之间不换行不加粗，每一部分之中可保持层次清晰。"
    )
    payload = {
        "model": "qwen3:4b",
        "system": system_prompt,
        "prompt": network_information + user_input,
        "stream": False,
    }
    response = requests.post(url, json=payload)
    raw_text = response.json()["response"]
    print(raw_text)

    # 移除 <think> 标签及其内容
    cleaned_text = re.sub(r"<think>.*?</think>\s*", "", raw_text, flags=re.DOTALL)
    # 可选：去掉前后空行或多余空格
    cleaned_text = cleaned_text.strip()

    result = {
        "chief_complaint": "",
        "examinations": "",
        "diagnosis": "",
        "disposal": "",
        "original": cleaned_text,
    }

    # 正则提取主观信息、客观信息、鉴别诊断、诊疗计划
    patterns = {
        "chief_complaint": r"主观信息[:：]\s*(.*?)(?=客观信息[:：])",
        "examinations": r"客观信息[:：]\s*(.*?)(?=鉴别诊断[:：])",
        "diagnosis_full": r"鉴别诊断[:：]\s*(.*?)(?=诊疗计划[:：])",
        "disposal": r"诊疗计划[:：]\s*(.*)$",
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, raw_text, re.DOTALL)
        if match:
            result[key] = match.group(1).strip()

    # 提取第一条诊断作为 diagnosis 字段
    diagnosis_text = result.get("diagnosis_full", "")
    match_diagnosis = re.search(
        r"1[.、]?\s*(.*?)\s+置信度：.*?→\s*依据：(.*?)。", diagnosis_text
    )
    if match_diagnosis:
        diagnosis_name = match_diagnosis.group(1).strip()
        diagnosis_basis = match_diagnosis.group(2).strip()
        result["diagnosis"] = f"{diagnosis_name}（依据：{diagnosis_basis}）"
    else:
        result["diagnosis"] = ""

    # 移除中间变量
    result.pop("diagnosis_full", None)

    return result
