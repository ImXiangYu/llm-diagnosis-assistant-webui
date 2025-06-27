import gradio as gr
from TextToPDF import TextToPDF
from Qwen3_Model import ask_medical_llm

medical_data = {}

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

def generate_pdf(this_name, this_gender, this_age, this_phone, chief, exam, diag, disp):
    print("正在准备保存为PDF...")
    pdf_path = TextToPDF(this_name, this_gender, this_age, this_phone,
                         chief_complaint=chief,
                         examinations=exam,
                         diagnosis=diag,
                         disposal=disp)
    return pdf_path

with gr.Blocks(title="智能医疗诊断系统") as demo:
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
                send_btn = gr.Button("发送")
                clear_btn = gr.ClearButton([msg, chatbot], value="清空对话")

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

    generate_btn.click(
        generate_pdf,
        inputs=[name, gender, age, phone, chief_complaint_box, examinations_box, diagnosis_box, disposal_box],
        outputs=file_output
    )

demo.launch(share=True)
