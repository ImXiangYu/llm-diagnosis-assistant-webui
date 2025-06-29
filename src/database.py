import sqlite3
import os

DB_FILE = "app.db"
USER_FILES_DIR = "UserFiles"  # 存储用户文件的目录

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
            file_uuid TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
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
        return True, "注册成功"
    except sqlite3.IntegrityError:
        return False, "用户名已存在"
    finally:
        conn.close()

def authenticate_user(username, password):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None
