import requests
import re
def ask_medical_llm(user_input: str) -> dict:
    # 调用本地 Ollama 服务上的 Qwen3 模型，返回结构化的医疗辅助建议。
    url = "http://localhost:11434/api/generate"
    system_prompt = (
        "你现在是一套医疗辅助决策支持系统（CDSS），专为医生在临床诊疗过程中提供参考信息。"
        "请根据用户提供的症状信息，按以下结构化格式输出内容："
        "主诉: [简洁列出患者的主要症状与持续时间，不要在本项内出现换行或列举，用一句话或一段话表述]\n"
        "辅助检查: [列出有助于鉴别诊断和病情评估的实验室或影像学检查，不要在本项内出现换行或列举，用一句话或一段话表述]\n"
        "诊断:[列出可能性最高的疾病或健康问题和简要支持依据，不要在本项内出现换行或列举，用一句话或一段话表述]\n"
        "处置意见: [建议医生考虑的初步干预方向，如生活方式调整、药物观察、专科会诊等，不要在本项内出现换行或列举，用一句话或一段话表述]"
        "请务必注意："
        "1. 输出应体现医学专业性，避免绝对化表述；"
        "2. 若涉及危急症状（如胸痛、呼吸困难、意识障碍等），需明确提示病人高度重视并优先排查严重疾病；"
        "3. 保持客观中立，不得出现“你可以自行用药”、“你患了XXX病”等表述；"
    )
    payload = {
        "model": "qwen3:4b",  # 或者你在 Ollama 中导入时设置的模型名
        "system": system_prompt,
        "prompt": user_input,
        "stream": False
    }
    # 发送请求
    response = requests.post(url, json=payload)
    text = response.json()["response"]
    print(text)
    # 解析结构化内容
    result = {
        "chief_complaint": "",
        "examinations": "",
        "diagnosis": "",
        "disposal": ""
    }
    patterns = {
        "chief_complaint": r"主诉[:：]\s*(.*?)\n",
        "examinations": r"辅助检查[:：]\s*(.*?)\n",
        "diagnosis": r"诊断[:：]\s*(.*?)\n",
        "disposal": r"处置意见[:：]\s*(.*?)($|\n)"
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.DOTALL)
        if match:
            result[key] = match.group(1).strip()

    return result
