import gradio as gr
from Model import ask_medical_llm

# 声音转文字
from src.VoiceToText import transcribe

# 用于模型记录输出
medical_data = {}

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
from TextToPDF import TextToPDF
def generate_pdf(this_name, this_gender, this_age, this_phone, chief, exam, diag, disp):
    print("正在准备保存为PDF...")
    pdf_path = TextToPDF(this_name, this_gender, this_age, this_phone,
                         chief_complaint=chief,
                         examinations=exam,
                         diagnosis=diag,
                         disposal=disp)
    return pdf_path


# 支持用户上传图片（例如影像报告）
import shutil
import os
def save_uploaded_image(image_path):
    if image_path is None or not os.path.exists(image_path):
        return None

    save_dir = "UploadedImages"
    os.makedirs(save_dir, exist_ok=True)

    filename = os.path.basename(image_path)
    save_path = os.path.join(save_dir, filename)

    shutil.copy(image_path, save_path)
    print(f"图片已保存到：{save_path}")

    return save_path  # 用于在界面上显示


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

/* 取消点击输入框后的蓝色背景 */
textarea:focus, .gradio-textbox:focus {
    background-color: white !important;
    outline: none !important;
    box-shadow: none !important;
    border: 1px solid #999 !important;
}
"""

# 系统主体
with gr.Blocks(title="智能医疗诊断系统", css=custom_css, theme='shivi/calm_seafoam') as demo:
    gr.Markdown("# 智能医疗诊断系统")

    # 顶部：病人信息填写
    with gr.Row():
        name = gr.Textbox(label="姓名")
        gender = gr.Radio(["男", "女"], label="性别")
        age = gr.Textbox(label="年龄")
        phone = gr.Textbox(label="电话")

    with gr.Tabs():
        with gr.Tab("文本诊疗"):
    # 中间：左右布局
            with gr.Row():
                # 左侧：聊天界面
                with gr.Column(scale=1):
                    chatbot = gr.Chatbot(label="诊疗对话", type="messages", height=260)
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
                    file_output = gr.File(label="下载PDF", visible=False)

        with gr.Tab("图像处理"):
            # 上传图片, 自动保存, 显示
            image_input = gr.Image(type="filepath", label="上传图片")
            uploaded_image = gr.Image(label="显示上传图片")

            image_input.change(
                save_uploaded_image,
                inputs=image_input,
                outputs=uploaded_image
            )

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
    ).then(
        lambda x: gr.update(visible=True),
        outputs=file_output
    )

    gr.Markdown("© 2025 智能医疗诊断系统 | 版权所有", elem_id="footer")

# 通过share控制是否开启分享链接，实测开启的话Gradio启动会变慢
# 开发时暂时不开启
# demo.launch(share=True)

demo.launch(share=False)
