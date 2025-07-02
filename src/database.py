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

    # 创建文件表 - 添加文件路径和唯一标识字段
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            file_name TEXT,
            file_path TEXT UNIQUE NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
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

def add_user_file(user_id, file_name):
    """添加用户文件到数据库和文件系统"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        # 生成唯一路径
        file_path = "SavedMedicalRecords/" + f"{file_name}"

        # 保存文件信息到数据库
        cursor.execute(
            "INSERT INTO files (user_id, file_name, file_path) VALUES (?, ?, ?)",
            (user_id, file_name, file_path)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"保存文件出错: {e}")
        return False
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