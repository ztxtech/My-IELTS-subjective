import json
import os


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
