import json
import os
import shutil
import subprocess
from pathlib import Path


def filecontent(path):
    """
    读取指定路径的文件并返回其内容字符串
    

    Args:
        path (str): 文件路径

    Returns:
        str: 文件内容字符串
    """
    try:
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return f"错误：文件 '{path}' 未找到。"
    except Exception as e:
        return f"读取文件时发生错误：{e}"


def read_json(file_path, default_value=None):
    """
    读取JSON文件并返回解析后的数据

    Args:
        file_path (str): JSON文件路径
        default_value: 当文件不存在或解析失败时返回的默认值

    Returns:
        dict/list: 解析后的JSON数据
    """
    try:
        # 检查文件是否存在
        if not os.path.exists(file_path):
            if default_value is not None:
                return default_value
            raise FileNotFoundError(f"文件不存在: {file_path}")

        # 读取并解析JSON文件
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data

    except json.JSONDecodeError as e:
        print(f"JSON格式错误: {e}")
        if default_value is not None:
            return default_value
        raise

    except Exception as e:
        print(f"读取文件时发生错误: {e}")
        if default_value is not None:
            return default_value
        raise


def write_json(data, file_path, indent=4):
    """导出数据为JSON文件"""
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=indent)
        return True
    except Exception as e:
        print(f"导出失败: {e}")
        return False


def p2(problem):
    template = """
    topic: {topic}
    
    P2:
    {p2}
    
    P3:
    {p3}
    """

    p3 = ""
    for idx, piece in enumerate(problem['p3']):
        p3 += f"{idx + 1}. {piece}\n"

    return template.format(
        topic=problem['topic'],
        p2=problem['p2'],
        p3=p3,
    )


def p2u(problem):
    template = """
    topic: {topic}
    """

    return template.format(topic=problem['topic'])


def p1(problem):
    template = """
    topic: {topic}
    
    题目:
    {p1}
    """

    p1 = ""
    for idx, piece in enumerate(problem['p1']):
        p1 += f"{idx + 1}. {piece}\n"

    return template.format(
        topic=problem['topic'],
        p1=p1,
    )


def write_file(content, output_file_path):
    """将答案写入文件"""
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(content)


def get_topics(path):
    topics = []

    # 遍历目录下的所有文件
    for filename in os.listdir(path):
        if filename.endswith('.json'):
            file_path = os.path.join(path, filename)
            try:
                data = read_json(file_path)
                # 提取topic字段
                if 'topic' in data:
                    topics.append(data['topic'])
            except Exception as e:
                print(f"读取文件 {filename} 时出错: {e}")
                continue

    return topics


# def md2pdf(path):
#     """
#     将Markdown文件转换为PDF
#
#     Args:
#         path (str): Markdown文件路径
#
#     Returns:
#         bool: 转换是否成功
#     """
#     css_path = "./data/theme.css"
#
#     try:
#         # 检查文件是否存在
#         if not os.path.exists(path):
#             print(f"错误：文件 '{path}' 未找到。")
#             return False
#
#         # 构建输出文件路径
#         html_output_path = path.replace(".md", ".html")
#
#         # 构建pandoc命令
#         cmd = [
#             "pandoc",
#             path,
#             "-o", html_output_path,
#             "--pdf-engine=wkhtmltopdf",  # 使用xelatex引擎支持中文
#             "--pdf-engine-opt=--enable-local-file-access",
#             "--standalone",
#             "--self-contained"
#         ]
#
#         # 如果提供了CSS路径，则添加CSS选项
#         if css_path and os.path.exists(css_path):
#             cmd.extend(["-c", css_path])
#
#         # 执行pandoc命令，指定编码为utf-8
#         result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
#
#         # 检查命令执行结果
#         if result.returncode == 0:
#             print(f"成功将 '{path}' 转换为 '{html_output_path}'")
#         else:
#             print(f"转换失败: {result.stderr}")
#             return False
#
#         # 构建输出文件路径
#         pdf_output_path = path.replace(".md", ".pdf")
#
#         # 构建pandoc命令
#         cmd = [
#             "wkhtmltopdf",
#             "--enable-local-file-access",
#             "--print-media-type",
#             "--disable-smart-shrinking",
#             html_output_path,
#             pdf_output_path
#         ]
#
#         # cmd = [
#         #     "weasyprint",
#         #     html_output_path,
#         #     pdf_output_path
#         # ]
#
#         # 执行pandoc命令，指定编码为utf-8
#         result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
#
#         # 检查命令执行结果
#         if result.returncode == 0:
#             print(f"成功将 '{html_output_path}' 转换为 '{pdf_output_path}'")
#             return True
#         else:
#             print(f"转换失败: {result.stderr}")
#             return False
#
#     except Exception as e:
#         print(f"转换过程中发生错误：{e}")
#         return False


def _find_chrome_executable():
    """在 Windows 的常见位置查找 Chrome 或 Edge 的可执行文件。"""
    # 检查环境变量中是否有 CHROME_PATH
    if "CHROME_PATH" in os.environ:
        path = Path(os.environ["CHROME_PATH"])
        if path.is_file():
            return str(path)

    # 常见安装路径列表
    potential_paths = [
        Path(os.environ.get("ProgramFiles", "C:/Program Files")) / "Google/Chrome/Application/chrome.exe",
        Path(os.environ.get("ProgramFiles(x86)", "C:/Program Files (x86)")) / "Google/Chrome/Application/chrome.exe",
        Path(os.environ.get("LOCALAPPDATA")) / "Google/Chrome/Application/chrome.exe",
        Path(os.environ.get("ProgramFiles", "C:/Program Files")) / "Microsoft/Edge/Application/msedge.exe",
        Path(os.environ.get("ProgramFiles(x86)", "C:/Program Files (x86)")) / "Microsoft/Edge/Application/msedge.exe",
    ]

    for path in potential_paths:
        if path.is_file():
            print(f"✅ 自动找到浏览器: {path}")
            return str(path)

    # 如果找不到，检查 shutil.which
    path = shutil.which("chrome") or shutil.which("msedge")
    if path:
        print(f"✅ 在系统 PATH 中找到浏览器: {path}")
        return path

    return None


def md2pdf(md_path, keep_html=False):
    # --- 1, 2, 3 步骤保持不变 ---
    md_file = Path(md_path)
    html_file = md_file.with_suffix('.html')
    pdf_file = md_file.with_suffix('.pdf')
    css_file = Path("./data/theme.css")
    if not md_file.is_file():
        print(f"❌ 错误：Markdown文件 '{md_file}' 未找到。")
        return False
    print(f"⚙️ 步骤 1/2: 正在将 '{md_file.name}' 转换为 HTML...")
    try:
        pandoc_cmd = ["pandoc", str(md_file), "-o", str(html_file), "--standalone", "--self-contained"]
        if css_file.is_file():
            pandoc_cmd.extend(["-c", str(css_file)])
        else:
            print(f"⚠️ 警告：CSS文件 '{css_file}' 未找到，将不应用样式。")
        subprocess.run(pandoc_cmd, capture_output=True, text=True, encoding='utf-8', check=True)
        print(f"✅ 成功生成HTML文件: '{html_file.name}'")
    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        print(f"❌ Pandoc 转换失败: {e.stderr if hasattr(e, 'stderr') else e}")
        return False

    # --- 4. 步骤二：HTML -> PDF (使用增强的Chrome引擎) ---
    print(f"⚙️ 步骤 2/2: 正在使用 Chrome 引擎将 HTML 转换为 PDF...")
    try:
        chrome_path = _find_chrome_executable()
        if not chrome_path:
            print("❌ 错误：找不到 Chrome 或 Edge 浏览器。")
            return False

        # 使用绝对路径来避免歧义
        abs_html_path = str(html_file.resolve())
        abs_pdf_path = str(pdf_file.resolve())

        pdf_cmd = [
            chrome_path,
            "--headless",
            "--disable-gpu",
            "--no-sandbox",
            # "--no-pdf-header-footer",  # <-- 就是加上这一行！
            f"--print-to-pdf={abs_pdf_path}",
            abs_html_path
        ]

        print(f"▶️  正在尝试执行命令: {' '.join(pdf_cmd)}")
        result = subprocess.run(pdf_cmd, capture_output=True, text=True, encoding='utf-8')

        # 无论成功与否，都打印标准输出和标准错误，以获取更多信息
        if result.stdout:
            print(f"ℹ️  Chrome 标准输出:\n{result.stdout}")
        if result.stderr:
            print(f"⚠️  Chrome 标准错误:\n{result.stderr}")

        # 再次检查PDF文件是否真的被创建了
        if pdf_file.is_file() and pdf_file.stat().st_size > 0:
            print(f"✅ 成功生成PDF文件: '{pdf_file.name}'")
            return True
        else:
            print(f"❌ 转换失败: 命令执行完毕，但未生成有效的 PDF 文件 '{pdf_file.name}'。")
            print(f"   (返回码: {result.returncode})")
            return False

    finally:
        # --- 5. 清理中间文件 ---
        if not keep_html and html_file.exists():
            html_file.unlink()
            print(f"🗑️ 已删除中间文件 '{html_file.name}'")
