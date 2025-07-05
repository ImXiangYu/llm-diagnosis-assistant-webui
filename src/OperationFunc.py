# 登录逻辑
import gradio as gr

from Model import ask_medical_llm
import database


def handle_login(username, password):
    user_id = database.authenticate_user(username, password)
    if user_id:
        return "", True, (user_id, username)
    else:
        return "❌ 用户名或密码错误", False, None

# 注册逻辑
def handle_register(username, password):
    ok, this_msg = database.register_user(username, password)
    return ok, this_msg

# 登录逻辑
def on_login(username, password):
    if not username:
        return "用户名不能为空", gr.update(visible=True), gr.update(visible=False), gr.update(visible=False), None
    if not password:
        return "密码不能为空", gr.update(visible=True), gr.update(visible=False), gr.update(visible=False), None
    msg, success, current_user = handle_login(username, password)
    return msg, gr.update(visible=not success), gr.update(visible=False), gr.update(visible=success), current_user

# 注册逻辑
def on_register(username, password):
    if not username:
        return "用户名不能为空", gr.update(visible=False), gr.update(visible=True), gr.update(visible=False), None
    if not password:
        return "密码不能为空", gr.update(visible=False), gr.update(visible=True), gr.update(visible=False), None
    success, msg = handle_register(username, password)
    if success:
        _, _, current_user = handle_login(username, password)
        return msg, gr.update(visible=False), gr.update(visible=False), gr.update(visible=True), current_user
    return msg, gr.update(visible=False), gr.update(visible=True), gr.update(visible=False), None

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


# 调用本地模型
def chat(user_input, history):
    print("--------------已开启新一轮调用--------------")
    result = ask_medical_llm(user_input)

    print("--------------result--------------")
    print(result)

    # 用于模型记录输出
    medical_data = {}
    medical_data.update(result)

    history.append({"role": "user", "content": user_input})
    history.append({"role": "assistant", "content": result["original"]})

    print("--------------history--------------")
    print(history)
    return "", history, result["chief_complaint"], result["examinations"], result["diagnosis"], result["disposal"]

# 生成PDF
from TextToPDF import TextToPDF
def generate_pdf(this_name, this_gender, this_age, this_phone, condition_description,
                 chief, exam, diag, disp, this_current_user):
    if not this_current_user:
        print("当前用户信息为空，无法生成PDF")
        return None
    # this_current_user: [user_id, username]
    print("正在准备保存为PDF...")
    saved_pdf = TextToPDF(this_name, this_gender, this_age, this_phone,
                         chief_complaint=chief,
                         examinations=exam,
                         diagnosis=diag,
                         disposal=disp, username=this_current_user[1])
    pdf_filename = saved_pdf[1]
    pdf_path = saved_pdf[0]
    user_id = this_current_user[0]
    success, patient_id = database.export_patient_file(
        this_name, this_gender, this_age, this_phone, condition_description, auxiliary_examination=None
    )
    if not success:
        print("导入患者信息失败，无法关联文件")
        return None
    saved = database.add_user_file(user_id, pdf_filename, patient_id)
    if not saved:
        print("保存文件记录失败")
    else:
        print(f"PDF {pdf_filename} 已保存并关联到患者 {patient_id}")
    return pdf_path


from ImageToPDF import ImageToPDF
def image_report_generate(this_name, this_gender, this_age, this_phone, this_current_user):
    print("正在保存影像报告...")
    saved_image_report = ImageToPDF(this_name, this_gender, this_age, this_phone, username=this_current_user[1])
    image_report_filename = saved_image_report[1]
    image_report_path = saved_image_report[0]
    user_id = this_current_user[0]
    database.add_user_file(user_id, image_report_filename)
    return image_report_path

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

# 退出登录逻辑
def handle_logout():
    # 返回值顺序应对应下面 outputs 的顺序
    return None, gr.update(visible=True), gr.update(visible=False), gr.update(visible=False), "", [], "", "", "", "", ""
