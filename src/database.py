import sqlite3
import os

DB_FILE = "app.db"
USER_FILES_DIR = "SavedMedicalRecords"  # 存储用户文件的目录

# 确保用户文件目录存在
os.makedirs(USER_FILES_DIR, exist_ok=True)


def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # 创建用户表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    # 创建病人信息表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            gender TEXT,
            age INTEGER,
            phone TEXT,
            condition_description TEXT,
            auxiliary_examination TEXT
        )
    ''')
    # 创建文件表 - 添加文件路径和唯一标识字段
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            patient_id INTEGER,
            file_name TEXT,
            file_path TEXT UNIQUE NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(patient_id) REFERENCES patients(id)
        )
    ''')

    
    conn.commit()
    conn.close()
    
def register_user(username, password):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True, "注册成功，即将跳转登录"
    except sqlite3.IntegrityError:
        return False, "注册失败，用户名已存在"
    finally:
        conn.close()

def authenticate_user(username, password):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def add_user_file(user_id, file_name, patient_id):
    """添加用户文件到数据库和文件系统"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        # 生成唯一路径
        file_path = "SavedMedicalRecords/" + f"{file_name}"

        # 保存文件信息到数据库
        cursor.execute(
            "INSERT INTO files (user_id, file_name, file_path, patient_id) VALUES (?, ?, ?, ?)",
            (user_id, file_name, file_path, patient_id)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"保存文件出错: {e}")
        return False
    finally:
        conn.close()

def export_patient_file(name, gender, age, phone, condition_description, auxiliary_examination):
    """
    将患者信息导入patients表。

    参数：
    - name: 患者姓名
    - gender: 性别
    - age: 年龄
    - phone: 电话
    - condition_description: 病情描述
    - auxiliary_examination: 辅助检查
    返回：
    - True, 新增记录的门诊号
    - False, 插入失败
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO patients (name, gender, age, phone, condition_description, auxiliary_examination)"
            " VALUES (?, ?, ?, ?, ?, ?)",
            (name, gender, age, phone, condition_description, auxiliary_examination)
        )
        conn.commit()
        outpatient_number = cursor.lastrowid
        return True, outpatient_number
    except Exception as e:
        print(f"导入患者信息出错: {e}")
        return False, None
    finally:
        conn.close()

def get_user_files(user_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT id, file_name, file_path
                   FROM files
                   WHERE user_id = ?
                   """, (user_id,))

    files = []
    for row in cursor.fetchall():
        files.append({
            "id": row[0],
            "name": row[1],
        })
    conn.close()
    return files

def get_file_by_filename(file_name):
    """根据filename获取文件路径"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT file_path FROM files WHERE file_name=?", (file_name,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None