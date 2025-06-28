import gradio as gr
import numpy as np

from TextToPDF import TextToPDF
from Model import ask_medical_llm

# 语音转文字
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
import tempfile
import soundfile as sf

# 禁用ModelScope的非Error日志
from modelscope.utils.logger import get_logger
logger = get_logger()
logger.setLevel(40)

# 用于处理正则
import re
def clean_text(raw_text):
    return re.sub(r"<\|.*?\|>", "", raw_text)

# 用于模型记录输出
medical_data = {}

# 换成了通义的SenseVoiceSmall，看看效果如何
asr_pipeline = pipeline(
    task=Tasks.auto_speech_recognition,
    model='iic/SenseVoiceSmall',
    model_revision="master",
    device="cuda:0",)

# 调用本地模型
def chat(user_input, history):
    print("--------------已开启新一轮调用--------------")
    result = ask_medical_llm(user_input)
    medical_data.update(result)

    history.append({"role": "user", "content": user_input})
    history.append({"role": "assistant", "content":
        "主诉：" + result["chief_complaint"] + "\n" +
        "辅助检查：" + result["examinations"] + "\n" +
        "诊断：" + result["diagnosis"] + "\n" +
        "处置意见：" + result["disposal"]})

    print("--------------history--------------")
    return "", history, result["chief_complaint"], result["examinations"], result["diagnosis"], result["disposal"]

# 生成PDF
def generate_pdf(this_name, this_gender, this_age, this_phone, chief, exam, diag, disp):
    print("正在准备保存为PDF...")
    pdf_path = TextToPDF(this_name, this_gender, this_age, this_phone,
                         chief_complaint=chief,
                         examinations=exam,
                         diagnosis=diag,
                         disposal=disp)
    return pdf_path

# 语音转文字
def transcribe(audio):
    if not audio or not isinstance(audio, (tuple, list)) or len(audio) != 2:
        return "无效的音频输入，请重新录音"

    sr, y = audio
    if y is None or len(y) == 0:
        return "音频数据为空，请重新录音"

    if y.ndim > 1:
        y = y.mean(axis=1)
    y = y.astype(np.float32)

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        sf.write(f.name, y, sr)
        result = asr_pipeline(f.name)

    try:
        return clean_text(result[0]["text"])
    except Exception as e:
        print("识别失败：", e)
        return "语音识别失败，请重试"


# 预设的css样式，可以应用到gradio程序中
custom_css ="""
/* 背景页面淡蓝色 */
.gradio-container {
    background-color: #f2f6fa;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* 页脚 */
#footer {
    text-align: center;
    font-size: 12px;
    color: #999;
    margin-top: 20px;
}

/* 清空按钮 */
#clear-btn {
    background-color: red;
    color: white;
}

/* Markdown 标题样式 */
h1 {
    text-align: center;
    color: #2c3e50;
    margin-bottom: 20px;
}

/* 卡片颜色 */
#card {
    background-color: #67E667;       /* 卡片背景色 */
    border-radius: 12px;             /* 圆角 */
    padding: 16px;                   /* 内边距 */
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);  /* 阴影 */
}

/* 普通文本框边框样式 */
textarea, input, .gradio-textbox {
    border: 1px solid #ccc !important;
    border-radius: 8px !important;
    padding: 8px !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

/* ChatBot文本框边框样式 */
.gradio-chatbot {
    border-radius: 8px !important;
    border: 1px solid #ccc !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}
"""

with gr.Blocks(title="智能医疗诊断系统", css=custom_css, theme='shivi/calm_seafoam') as demo:
    gr.Markdown("# 智能医疗诊断系统")

    # 顶部：病人信息填写
    with gr.Row():
        name = gr.Textbox(label="姓名")
        gender = gr.Radio(["男", "女"], label="性别")
        age = gr.Textbox(label="年龄")
        phone = gr.Textbox(label="电话")

    # 中间：左右布局
    with gr.Row():
        # 左侧：聊天界面
        with gr.Column(scale=1):
            chatbot = gr.Chatbot(label="诊疗对话", type="messages", height=300)
            msg = gr.Textbox(label="输入您的病情描述")
            with gr.Row():
                clear_btn = gr.ClearButton([msg, chatbot], value="清空对话",
                                           elem_id="clear-btn")
                send_btn = gr.Button("发送")
            with gr.Row():
                transcribe_btn = gr.Button("识别语音")
            with gr.Row():
                audio_input = gr.Audio(sources="microphone", label="语音输入")
            transcribe_btn.click(transcribe, inputs=audio_input, outputs=msg)

        # 右侧：可编辑框和PDF生成
        with gr.Column(scale=1):
            chief_complaint_box = gr.Textbox(label="主诉", lines=2)
            examinations_box = gr.Textbox(label="辅助检查", lines=2)
            diagnosis_box = gr.Textbox(label="诊断", lines=2)
            disposal_box = gr.Textbox(label="处置意见", lines=2)
            generate_btn = gr.Button("生成病历PDF")
            file_output = gr.File(label="下载PDF")

    # 绑定事件
    send_btn.click(
        chat,
        inputs=[msg, chatbot],
        outputs=[msg, chatbot, chief_complaint_box, examinations_box, diagnosis_box, disposal_box]
    )

    # PDF生成
    generate_btn.click(
        generate_pdf,
        inputs=[name, gender, age, phone, chief_complaint_box, examinations_box, diagnosis_box, disposal_box],
        outputs=file_output
    )

    gr.Markdown("© 2025 智能医疗诊断系统 | 版权所有", elem_id="footer")

# 通过share控制是否开启分享链接，实测开启的话Gradio启动会变慢
# 开发时暂时不开启
# demo.launch(share=True)

demo.launch(share=False)
