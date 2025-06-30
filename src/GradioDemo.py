import gradio as gr
from Model import ask_medical_llm

# 声音转文字
from src.VoiceToText import transcribe

# 初始化数据库
import database
database.init_db()

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
def generate_pdf(this_name, this_gender, this_age, this_phone,
                 chief, exam, diag, disp, this_current_user):
    print("正在准备保存为PDF...")
    saved_pdf = TextToPDF(this_name, this_gender, this_age, this_phone,
                         chief_complaint=chief,
                         examinations=exam,
                         diagnosis=diag,
                         disposal=disp)
    pdf_filename = saved_pdf[1]
    pdf_path = saved_pdf[0]
    user_id = this_current_user[0]
    database.add_user_file(user_id, pdf_filename)
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

# 登录逻辑
def handle_login(username, password):
    user_id = database.authenticate_user(username, password)
    if user_id:
        return (
            "",
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=True),
            (user_id, username)
        )
    else:
        return "❌ 用户名或密码错误", gr.update(), gr.update(), gr.update(visible=False), None, ""


# 注册逻辑
def handle_register(username, password):
    ok, this_msg = database.register_user(username, password)
    return this_msg, gr.update(visible=True) if ok else gr.update()

# 查询文件逻辑
def handle_query_files(user):
    if not user:
        return "❌ 请先登录", None

    files = database.get_user_files(user[0])
    file_data = [
        [f["name"], f"📥 下载"]
        for f in files
    ]

    if not file_data:
        # 如果没有文件，返回提示行
        return [["⚠️ 无历史病历", ""]]

    return file_data


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

/* Markdown 标题样式 */
h2 {
    color: #1e40af;
    margin-bottom: 20px;
}

/* 普通文本框边框样式 */
textarea, input, .gradio-textbox {
    border: 1px solid #ccc !important;
    border-radius: 8px !important;
    padding: 8px !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

/* 取消点击输入框后的蓝色背景 */
textarea:focus, input[type="password"]:focus, .gradio-textbox:focus {
    background-color: white !important;
    outline: none !important;
    box-shadow: none !important;
    border: 1px solid #999 !important;
}

/* ChatBot文本框边框样式 */
.gradio-chatbot {
    border-radius: 8px !important;
    border: 1px solid #ccc !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}
"""

# 系统主体
with gr.Blocks(title="智能医疗诊断系统", css=custom_css, theme='shivi/calm_seafoam') as demo:
    current_user = gr.State(value=None)  # (user_id, username)

    # 登录/注册界面
    with gr.Row():
        with gr.Column(visible=True) as login_panel:
            gr.Markdown("## 🔐 登录")
            login_username = gr.Textbox(label="用户名")
            login_password = gr.Textbox(label="密码", type="password")
            login_button = gr.Button("登录")
            login_info = gr.Markdown(value="")

        with gr.Column(visible=True) as register_panel:
            gr.Markdown("## 📝 注册")
            register_username = gr.Textbox(label="新用户名")
            register_password = gr.Textbox(label="新密码", type="password")
            register_button = gr.Button("注册")
            register_info = gr.Markdown(value="")

    # 主界面
    with gr.Column(visible=False) as main_panel:
        with gr.Row():
            gr.Markdown("")
            gr.Markdown("# 智能医疗诊断系统")
            user_label = gr.Markdown()

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
                            audio_input = gr.Audio(sources=["microphone"], label="语音输入")
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

            with gr.Tab("历史病历查询"):
                with gr.Column():
                    gr.Markdown("### 📂 历史病历")
                    with gr.Row():
                        query_btn = gr.Button("🔍 查询历史病历")

                    # 文件列表显示 - 使用DataFrame
                    file_table = gr.DataFrame(
                        headers=["文件名", "操作"],
                        datatype=["str", "str"],
                        interactive=False,
                        wrap=True
                    )
                # 隐藏文件下载组件
                file_download = gr.File(label="文件下载", visible=False)

    # 绑定事件
    send_btn.click(
        chat,
        inputs=[msg, chatbot],
        outputs=[msg, chatbot, chief_complaint_box, examinations_box, diagnosis_box, disposal_box]
    )

    # 登录
    login_button.click(
        fn=handle_login,
        inputs=[login_username, login_password],
        outputs=[login_info, login_panel, register_panel, main_panel, current_user]
    )

    # 注册
    register_button.click(
        fn=handle_register,
        inputs=[register_username, register_password],
        outputs=[register_info, login_panel]
    )

    # 用户名显示
    current_user.change(
        lambda u: f"## 👤 当前用户：**{u[1]}**" if u else "",
        inputs=current_user,
        outputs=user_label
    )

    # PDF生成
    generate_btn.click(
        generate_pdf,
        inputs=[name, gender, age, phone, chief_complaint_box,
                examinations_box, diagnosis_box, disposal_box, current_user],
        outputs=file_output
    ).then(
        lambda x: gr.update(visible=True),
        outputs=file_output
    )

    query_btn.click(
        fn=handle_query_files,
        inputs=current_user,
        outputs=file_table
    )

    # 文件下载逻辑
    def handle_file_selection(user, data, evt: gr.SelectData):
        """处理文件选择并显示下载组件"""
        try:
            # 检查用户是否登录
            if not user:
                return gr.File(visible=False)

            # 获取选中的行索引
            selected_idx = evt.index[0] if isinstance(evt.index, tuple) else evt.index
            row_index = selected_idx[0]

            # 获取选中的行数据
            # selected_data = data.iat[selected_idx[0], selected_idx[1]]
            selected_row = data.iloc[row_index]
            # print(selected_row)

            # 行数据分两个，[file_name, button]
            # 从行数据中提取file_name
            # 获取文件路径
            file_path = database.get_file_by_filename(selected_row[0])
            if file_path and os.path.exists(file_path):
                # 返回可见的文件下载组件
                return gr.File(
                    value=file_path,
                    visible=True,
                    label=f"下载文件: {selected_row[0]}"
                )

            return gr.File(visible=False)

        except Exception as e:
            print(f"文件选择错误: {e}")
            return gr.File(visible=False)


    # 当用户选择文件时触发下载
    file_table.select(
        fn=handle_file_selection,
        inputs=[current_user, file_table],
        outputs=file_download
    )

    gr.Markdown("© 2025 智能医疗诊断系统 | 版权所有", elem_id="footer")

# 通过share控制是否开启分享链接，实测开启的话Gradio启动会变慢
# 开发时暂时不开启
# demo.launch(share=True)

demo.launch(share=False)
