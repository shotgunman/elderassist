---

# WebUI 安装教程

## 手动安装

### 1. 安装 Python
- 下载并安装 [Python 3.11.11](https://www.python.org/downloads/release/python-31111/)。
- 确保在安装过程中将 Python 添加到系统环境变量（勾选“Add Python to PATH”选项）。

### 2. 创建虚拟环境（可选）
- 打开命令提示符（CMD）或 PowerShell。
- 创建虚拟环境：
  ```bash
  python -m venv webui_env
  ```
- 激活虚拟环境：
  ```bash
  webui_env\Scripts\activate
  ```

### 3. 安装依赖
- 在项目目录下，运行以下命令安装依赖：
  ```bash
  pip install -r requirements.txt
  ```

### 4. 启动服务器
- 安装完成后，运行以下命令启动服务器：
  ```bash
  python manage.py runserver
  ```
- 访问 [http://127.0.0.1:8000/chat](http://127.0.0.1:8000/chat) 查看 WebUI。

---

## 自动安装

### 1. 安装 Python
- 下载并安装 [Python 3.11.11](https://www.python.org/downloads/release/python-31111/)。
- 确保在安装过程中将 Python 添加到系统环境变量（勾选“Add Python to PATH”选项）。

### 2. 运行安装脚本
- 下载项目代码到本地。
- 打开命令提示符（CMD）或 PowerShell。
- 运行以下命令：
  ```bash
  setup.bat
  ```

### 3. 启动 WebUI
- 安装完成后，运行以下命令启动 WebUI：
  ```bash
  webui.bat
  ```
- 访问 [http://127.0.0.1:8000/chat](http://127.0.0.1:8000/chat) 查看 WebUI。

---

## 注意事项

- 确保安装过程中网络畅通，避免因网络问题导致依赖安装失败。
- 如果在安装过程中遇到问题，请检查 Python 版本是否正确，以及是否正确激活了虚拟环境。
- 如果需要自定义服务器端口，可以在 `manage.py` 文件中修改相关配置。
