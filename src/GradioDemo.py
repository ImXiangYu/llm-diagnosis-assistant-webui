import gradio as gr
from src.CustomCss import custom_css
from src.OperationFunc import handle_login, handle_register, handle_query_files, handle_file_selection, \
    save_uploaded_image, chat, generate_pdf

# 声音转文字
from src.VoiceToText import transcribe

# 初始化数据库
import database
database.init_db()

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
            logout_btn = gr.Button("🚪 退出登录", size="sm")

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
