import gradio as gr
from TextToPDF import TextToPDF
from Model import ask_medical_llm

# 语音转文字
from transformers import pipeline
import numpy as np

medical_data = {}

# 调用Openai的whisper模型，支持多语言
# 这里暂时使用pipeline，后续部署到本地
# 并且这个模型中文效果很差，后续应该要更换
transcriber = pipeline("automatic-speech-recognition", model="openai/whisper-base")

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
    sr, y = audio
    if y.ndim > 1:
        y = y.mean(axis=1)
    y = y.astype(np.float32)
    y /= np.max(np.abs(y))
    return transcriber({"sampling_rate": sr, "raw": y})["text"]

# 预设的css样式，可以应用到gradio程序中
custom_css ="""
#clear-btn {
    background-color: red;
    color: white;
}
"""

with gr.Blocks(title="智能医疗诊断系统", css=custom_css) as demo:
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

# 通过share控制是否开启分享链接，实测开启的话Gradio启动会变慢
# 开发时暂时不开启
demo.launch(share=False)
