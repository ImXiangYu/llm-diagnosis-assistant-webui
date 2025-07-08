# 登录逻辑
import gradio as gr

from src.ImageModel import ask_image_model
from src.Model import ask_medical_llm
from src.database import *
from src.TextToPDF import TextToPDF
from src.ImageToPDF import ImageToPDF


def handle_login(username, password):
    user_id = authenticate_user(username, password)
    if user_id:
        return "", True, (user_id, username)
    else:
        return "❌ 用户名或密码错误", False, None


# 注册逻辑
def handle_register(username, password):
    ok, this_msg = register_user(username, password)
    return ok, this_msg


# 登录逻辑
def on_login(username, password):
    if not username:
        gr.Warning(message="用户名不能为空", duration=2, title="登录页")
        return (
            "用户名不能为空",
            gr.update(visible=True),
            gr.update(visible=False),
            gr.update(visible=True),
            gr.update(visible=False),
            None,
        )
    if not password:
        gr.Warning(message="密码不能为空", duration=2, title="登录页")
        return (
            "密码不能为空",
            gr.update(visible=True),
            gr.update(visible=False),
            gr.update(visible=True),
            gr.update(visible=False),
            None,
        )
    msg, success, current_user = handle_login(username, password)
    return (
        msg,
        gr.update(visible=not success),
        gr.update(visible=False),
        gr.update(visible=not success),
        gr.update(visible=success),
        current_user,
    )


# 注册逻辑
def on_register(username, password):
    if not username:
        gr.Warning(message="用户名不能为空", duration=2, title="注册页")
        return (
            "用户名不能为空",
            gr.update(visible=False),
            gr.update(visible=True),
            gr.update(visible=False),
            None,
        )
    if not password:
        gr.Warning(message="密码不能为空", duration=2, title="注册页")
        return (
            "密码不能为空",
            gr.update(visible=False),
            gr.update(visible=True),
            gr.update(visible=False),
            None,
        )
    success, msg = handle_register(username, password)
    if success:
        gr.Success(message="注册成功，已跳转至主页面！", duration=2,  title="注册")
        _, _, current_user = handle_login(username, password)
        return (
            msg,
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=True),
            current_user,
        )
    return (
        msg,
        gr.update(visible=False),
        gr.update(visible=True),
        gr.update(visible=False),
        None,
    )


def handle_create_case(name, gender, age, phone):
    """处理创建病例"""
    outpatient_number = create_patient_case(name, gender, age, phone)
    if outpatient_number:
        gr.Success(message="创建病例成功!", duration=1, title="病例创建")
        return outpatient_number

    gr.Error(message="创建病例失败!", duration=1, title="病例创建")

    return "❌ 创建病例失败"

def handle_clear_chat():
    """清除聊天记录"""
    return "", [], "", "", "", ""

def handle_clear_image_chat():
    """清除影像聊天记录"""
    print("清除影像聊天记录")
    return "", [], None,"", ""
# 查询文件逻辑
def handle_query_files():
    files = get_patient_cases()
    file_data = [
        [
            f"门诊号：{f['id']}，姓名：{f['name']}",
            f"📥 下载病历",
            f"📥 下载影像报告",
            f"⤵️ 导入信息",
            f"🗑️ 删除"
        ]
        for f in files
    ]

    if not file_data:
        # 如果没有文件，返回提示行
        return [["⚠️ 无历史病历", ""]]

    return file_data


# 文件下载逻辑
def handle_record_download(user, data, evt: gr.SelectData):
    """处理文件选择并显示下载组件"""
    try:
        # 检查用户是否登录
        if not user:
            return gr.File(visible=False)

        # 获取选中的行索引
        selected_idx = evt.index[0] if isinstance(evt.index, tuple) else evt.index
        row_index = selected_idx[0]
        col_index = selected_idx[1]

        selected_row = data.iloc[row_index]
        try:
            id_str = selected_row[0].split("，")[0]  # "门诊号：123"
            patient_id = int(id_str.split("：")[1])
        except Exception as e:
            print(f"解析门诊号失败: {e}")
            return gr.File(visible=False)
        # 只允许点击第二列（索引为1）时触发下载
        if col_index != 1 and col_index != 2:
            return gr.File(visible=False)
        if col_index == 1:
            file_path = get_record_by_id(patient_id)
            if not file_path:
                print(f"未找到门诊号 {patient_id} 的病历文件")
                gr.Warning(message=f"未找到门诊号 {patient_id} 的病历文件", duration=3, title="报告下载")
                # 加一个前端提示在此处
                return gr.File(visible=False)
        elif col_index == 2:
            file_path = get_image_report_by_id(patient_id)
            if not file_path:
                print(f"未找到门诊号 {patient_id} 的影像报告文件")
                gr.Warning(message=f"未找到门诊号 {patient_id} 的影像报告文件", duration=3, title="报告下载")
                # 加一个前端提示在此处
                return gr.File(visible=False)
        print(file_path)
        if os.path.exists(file_path):
            # 返回可见的文件下载组件
            return gr.File(
                value=file_path, visible=True, label=f"下载文件: {selected_row[0]}"
            )
        return gr.File(visible=False)

    except Exception as e:
        print(f"文件选择错误: {e}")
        return gr.File(visible=False)


def handle_case_load(data, evt: gr.SelectData):
    """处理载入病例信息"""
    # 获取选中的行索引
    selected_idx = evt.index[0] if isinstance(evt.index, tuple) else evt.index
    row_index = selected_idx[0]
    col_index = selected_idx[1]
    selected_row = data.iloc[row_index]
    id_str = selected_row[0].split("，")[0]
    patient_id = int(id_str.split("：")[1])
    if col_index == 3:
        print("正在载入病例信息...")
        case_info = get_case_by_id(patient_id)
        # 把信息填入各个空里
        name = case_info["name"]
        gender = case_info["gender"]
        age = case_info["age"]
        phone = case_info["phone"]
        chief = case_info["chief"] if case_info["chief"] else "无"
        auxiliary_examination = case_info["auxiliary_examination"] if case_info["auxiliary_examination"] else "无"
        msg = (
            chief + "\n辅助检查：" + auxiliary_examination
        )
        print(
            f"加载病例信息：门诊号={patient_id}，姓名={name}，性别={gender}，年龄={age}，电话={phone}，病情描述={msg}"
        )
        return patient_id, name, gender, age, phone, msg, [], "", "", "", "",[], chief, "", ""
    else:
        return (
            gr.update(),
            gr.update(),
            gr.update(),
            gr.update(),
            gr.update(),
            gr.update(),
            gr.update(),
            gr.update(),
            gr.update(),
            gr.update(),
            gr.update(),
            gr.update(),
            gr.update(),
            gr.update(),
            gr.update()
        )

def handle_case_delete(data, evt: gr.SelectData):
    """处理删除病例信息"""
    # 获取选中的行索引
    selected_idx = evt.index[0] if isinstance(evt.index, tuple) else evt.index
    row_index = selected_idx[0]
    col_index = selected_idx[1]
    selected_row = data.iloc[row_index]
    id_str = selected_row[0].split("，")[0]
    patient_id = int(id_str.split("：")[1])
    if col_index == 4:
        print(f"正在删除门诊号 {patient_id} 的病例信息...")
        success = delete_patient_case(patient_id)
        if success:
            print(f"门诊号 {patient_id} 的病例信息已成功删除")
            return gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), handle_query_files()
        else:
            print(f"删除门诊号 {patient_id} 的病例信息失败")
            return gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), handle_query_files()
    else:
        return gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), handle_query_files()

# 调用本地模型
def chat(user_input, history, model_enhancement):
    print(f"模型增强: {model_enhancement}")
    print("--------------已开启新一轮调用--------------")
    result = ask_medical_llm(user_input, model_enhancement)

    print("--------------result--------------")
    print(result)

    # 用于模型记录输出
    medical_data = {}
    medical_data.update(result)

    history.append({"role": "user", "content": user_input})
    history.append({"role": "assistant", "content": result["original"]})

    print("--------------history--------------")
    print(history)
    return (
        "",
        history,
        result["chief_complaint"],
        result["examinations"],
        result["diagnosis"],
        result["disposal"],
    )


def image_chat(user_input, image_history, image_input):
    print("--------------已开启新一轮调用--------------")
    result = ask_image_model(user_input, image_input)

    print("--------------result--------------")
    print(result)

    # 用于模型记录输出
    medical_data = {}
    medical_data.update(result)

    image_history.append({"role": "user", "content": user_input})
    image_history.append({"role": "assistant", "content": result["original"]})

    print("--------------history--------------")
    print(image_history)
    return (
        "",
        image_history,
        result["description"],
        result["imaging_diagnosis"],
    )


# 生成PDF
def record_generate(
    patient_id,
    this_name,
    this_gender,
    this_age,
    this_phone,
    chief,
    exam,
    diag,
    disp,
    this_current_user,
):
    if not this_current_user:
        print("当前用户信息为空，无法生成PDF")
        return None
    # this_current_user: [user_id, username]
    print("正在准备保存为PDF...")
    print("病情描述：" + chief)
    saved_pdf = TextToPDF(
        this_name,
        this_gender,
        this_age,
        this_phone,
        chief_complaint=chief,
        examinations=exam,
        diagnosis=diag,
        disposal=disp,
        username=this_current_user[1],
    )
    pdf_filename = saved_pdf[1]
    pdf_path = saved_pdf[0]
    user_id = this_current_user[0]
    success = update_patient_case(
        patient_id,
        chief,
        exam,
    )
    if not success:
        print("导入患者信息失败，无法关联文件")
        return None
    saved = add_file(user_id, pdf_filename, patient_id, "record")
    if not saved:
        print("保存文件记录失败")
    else:
        print(f"PDF {pdf_filename} 已保存并关联到患者 {patient_id}")
    return pdf_path


def image_report_generate(
    patient_id,
    this_name,
    this_gender,
    this_age,
    this_phone,
    this_current_user,
    this_clinical_diagnosis="无",
    this_image="无",
    this_description="无",
    this_imaging_diagnosis="无",
):
    print("正在保存影像报告...")
    saved_image_report = ImageToPDF(
        this_name,
        this_gender,
        this_age,
        this_phone,
        this_clinical_diagnosis,
        this_image,
        this_description,
        this_imaging_diagnosis,
    )
    image_report_filename = saved_image_report[1]
    image_report_path = saved_image_report[0]
    user_id = this_current_user[0]
    success = update_patient_case(
        patient_id,
        None,
        this_imaging_diagnosis,
    )
    if not success:
        print("导入患者信息失败，无法关联文件")
        return None
    saved = add_file(user_id, image_report_filename, patient_id, "image_report")
    if not saved:
        print("保存文件记录失败")
    else:
        print(f"PDF {image_report_filename} 已保存并关联到患者 {patient_id}")
    return image_report_path


# 支持用户上传图片（例如影像报告）
import shutil
import os


def save_uploaded_image(image_path):
    if image_path is None or not os.path.exists(image_path):
        return None,None

    save_dir = "UploadedImages"
    os.makedirs(save_dir, exist_ok=True)

    filename = "影像图片_" + os.path.basename(image_path)
    save_path = os.path.join(save_dir, filename)

    shutil.copy(image_path, save_path)
    print(f"图片已保存到：{save_path}")

    return [save_path, save_path]  # 用于在界面上显示

# 上传知识库文件
def save_uploaded_file(file):
    upload_file_dir = "UploadedFiles"
    os.makedirs(upload_file_dir, exist_ok=True)
    if not file:
        gr.Warning(message="未选择任何文件 上传失败！", duration=3, title="文件上传")
    else:
        file_path = os.path.join(
            upload_file_dir, "知识库文件_" + os.path.basename(file.name)
        )
        shutil.copy(file.name, file_path)
        print(f"{file.name}, 上传成功")
        gr.Success(message=os.path.basename(file.name) + ",上传成功！", duration=3, title="文件上传")


def list_uploaded_files():
    upload_file_dir = "UploadedFiles"
    os.makedirs(upload_file_dir, exist_ok=True)
    files = [
        os.path.join(upload_file_dir, f)
        for f in os.listdir(upload_file_dir)
        if os.path.isfile(os.path.join(upload_file_dir, f)) and f != "README.md"
    ]
    print("已列出所有文件")
    return files
