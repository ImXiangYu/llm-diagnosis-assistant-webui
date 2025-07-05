# 预设的css样式，可以应用到gradio程序中
custom_css ="""
/* 背景页面淡蓝色 */
.gradio-container {
    display: flex;
    flex-direction: column;
    min-height: 100vh;

    background-image: url('https://www.cqu.edu.cn/images/23/10/11/1ucry5xfsw/%E8%99%8E%E6%BA%AA%E4%BA%91%E6%B9%96%E6%B0%B4%E5%BD%B1.jpg'); /* 替换为你的背景图片URL */
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-color: #f2f6fa;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* 主体内容自动占据剩余空间 */
#main-content {
    flex: 1;
    min-height: 670px;
}


/* 添加一个半透明遮罩层 */
.gradio-container::before {
    content: "";
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background-color: rgba(255, 255, 255, 0.5); /* 白色半透明遮罩，透明度可调 */
    z-index: 0;
}

/* 确保容器内其他内容在遮罩上方 */
.gradio-container > * {
    position: relative;
    z-index: 1;
}

/* 清空按钮 */
#clear-btn {
    background-color: red;
    color: white;
}

#normal-btn {
    background-color: #90EE90;
    color: #1D4ED8;
}

/* Markdown 标题样式 */
h1 {
    text-align: center;
    color: #2c3e50;
    margin-bottom: 20px;
}

/* Markdown 标题样式 */
h2 {
    text-align: center;
    color: #1e40af;
    margin-bottom: 20px;
}

/* Markdown 标题样式 */
h3 {
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

#card {
    position: fixed;         /* 脱离文档流，基于窗口定位 */
    top: 50%;                /* 顶部 50% */
    left: 50%;               /* 左边 50% */
    transform: translate(-50%, -50%);  /* 向左上反移自身一半，实现完美居中 */

    background-color: white;
    padding: 2rem;
    border-radius: 12px;
    width: 360px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

/* 页脚样式 */
#footer {
    text-align: center;
    font-size: 12px;
    color: #999;
    padding: 10px 0;
    border-top: 1px solid #ddd;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    width: 100%;
}


/* PDF生成 */
#PDF-File {
    height: 70px; /* 自定义高度 */
    overflow-y: auto;
    border: 1px solid #ccc;
    padding: 10px;
}

/* 医学影像上传 */
#image-upload {
    height: 188px; /* 自定义高度 */
    overflow-y: auto;
    border: 1px solid #ccc;
    padding: 10px;
}
"""