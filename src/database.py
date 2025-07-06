import sqlite3
import os

DB_FILE = "app.db"
USER_FILES_DIR = "../SavedMedicalRecords"  # 存储用户文件的目录

# 确保用户文件目录存在
os.makedirs(USER_FILES_DIR, exist_ok=True)


def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # 创建用户表
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """
    )
    # 创建病人信息表
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            gender TEXT,
            age INTEGER,
            phone TEXT,
            chief TEXT,
            auxiliary_examination TEXT
        )
    """
    )
    # 创建文件表 - 添加文件路径和唯一标识字段
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            patient_id INTEGER,
            file_name TEXT,
            file_path TEXT UNIQUE NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(patient_id) REFERENCES patients(id)
        )
    """
    )

    conn.commit()
    conn.close()


def register_user(username, password):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)", (username, password)
        )
        conn.commit()
        return True, "注册成功，即将跳转登录"
    except sqlite3.IntegrityError:
        return False, "注册失败，用户名已存在"
    finally:
        conn.close()


def authenticate_user(username, password):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM users WHERE username=? AND password=?", (username, password)
    )
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


def add_file(user_id, file_name, patient_id, file_type):
    """添加病历到数据库和文件系统"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        # 生成唯一路径
        if file_type == "record":
            file_path = "SavedMedicalRecords/" + f"{file_name}"
        elif file_type == "image_report":
            file_path = "SavedImageRecords/" + f"{file_name}"
        # 保存文件信息到数据库
        cursor.execute(
            "INSERT INTO files (user_id, file_name, file_path, patient_id) VALUES (?, ?, ?, ?)",
            (user_id, file_name, file_path, patient_id),
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"保存文件出错: {e}")
        return False
    finally:
        conn.close()


def create_patient_case(
    name, gender, age, phone
):
    """创建患者信息记录"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO patients (name, gender, age, phone)"
        " VALUES (?, ?, ?, ?)",
        (name, gender, age, phone),
    )
    conn.commit()
    outpatient_number = cursor.lastrowid
    conn.close()
    return outpatient_number

def update_patient_case(
    patient_id, chief, auxiliary_examination
):
    """更新患者信息记录"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    print("============更新中===============")
    try:
        if chief:
            print(chief)
            cursor.execute(
                "UPDATE patients SET chief=? WHERE id=?",
                (chief, patient_id),
            )
        if auxiliary_examination:
            cursor.execute(
                "UPDATE patients SET auxiliary_examination=? WHERE id=?",
                (auxiliary_examination, patient_id),
            )
        conn.commit()
        return True
    except Exception as e:
        print(f"更新患者信息失败: {e}")
        return False
    finally:
        conn.close()
    

def get_patient_cases():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        """
                   SELECT * FROM patients
                   """
    )

    files = []
    for row in cursor.fetchall():
        files.append(
            {
                "id": row[0],
                "name": row[1],
            }
        )
    conn.close()
    return files


def get_record_by_id(patient_id):
    """根据患者ID获取患者病历"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT file_path FROM files WHERE patient_id=? AND file_name LIKE ?",
        (patient_id, "病历%"),
    )
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


def get_image_report_by_id(patient_id):
    """根据患者ID获取影像报告"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT file_path FROM files WHERE patient_id=? AND file_name LIKE ?",
        (patient_id, "医学影像报告%"),
    )
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


def get_case_by_id(patient_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    print("patient_id:", patient_id)
    cursor.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
    row = cursor.fetchone()
    if row:
        files = {
            "id": row[0],
            "name": row[1],
            "gender": row[2],
            "age": row[3],
            "phone": row[4],
            "chief": row[5],
            "auxiliary_examination": row[6],
        }
    else:
        files = {}
    conn.close()
    return files
