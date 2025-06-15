# toc.py (树状目录版)
import os
import argparse


def generate_tree_toc(input_dir, output_path):
    """
    递归扫描输入目录中的所有 .md 文件，并生成一个树状结构的 Markdown 目录。

    Args:
        input_dir (str): 需要扫描的输入目录路径。
        output_path (str): 生成的目录文件的完整路径（包括文件名）。
    """
    # 检查输入路径是否存在且为目录
    if not os.path.isdir(input_dir):
        print(f"错误：输入路径 '{input_dir}' 不是一个有效的目录。")
        return

    # 1. 递归获取所有.md文件的相对路径
    all_md_paths = []
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".md"):
                full_path = os.path.join(root, file)
                # 计算相对路径
                relative_path = os.path.relpath(full_path, input_dir)
                all_md_paths.append(relative_path)

    if not all_md_paths:
        print(f"在 '{input_dir}' 及其子目录中没有找到 .md 文件。")
        return

    # 2. 对路径进行字母排序，这是生成正确树结构的关键
    all_md_paths.sort()

    output_lines = ["# Table of Contents"]
    last_path_parts = []

    # 3. 遍历排序后的路径，生成树状结构
    for path in all_md_paths:
        # 将Windows路径分隔符'\'替换为'/'，以保证兼容性和后续处理
        link_path = path.replace(os.path.sep, "/")
        path_parts = link_path.split("/")

        # 找出与上一个路径的共同父目录深度
        common_parts_len = 0
        for i in range(min(len(last_path_parts), len(path_parts) - 1)):
            if last_path_parts[i] == path_parts[i]:
                common_parts_len += 1
            else:
                break

        # 打印新的目录层级
        for i in range(common_parts_len, len(path_parts) - 1):
            indent = "  " * i  # 两个空格用于缩进
            output_lines.append(f"{indent}* {path_parts[i]}/")

        # 打印文件链接
        filename = path_parts[-1]
        file_indent_level = len(path_parts) - 1
        indent = "  " * file_indent_level
        output_lines.append(f"{indent}* [{filename}]({link_path})")

        # 更新上一个路径的目录部分，用于下一次比较
        last_path_parts = path_parts[:-1]

    # 4. 确保输出目录存在并写入文件
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"创建输出目录：'{output_dir}'")

    try:
        with open(output_path, "w", encoding="utf-8") as outfile:
            outfile.write("\n".join(output_lines))

        print(f"✅ 成功！已在 '{output_path}' 生成了树状目录。")

    except IOError as e:
        print(f"写入文件时发生错误：{e}")


if __name__ == "__main__":
    # 命令行参数部分保持不变
    parser = argparse.ArgumentParser(
        description="递归扫描目录中的 .md 文件，并生成一个树状结构的 Markdown 目录。"
    )
    parser.add_argument(
        "--in", dest="input_dir", required=True, help="需要递归扫描的输入目录路径。"
    )
    parser.add_argument(
        "--out",
        dest="output_file",
        required=True,
        help="输出的 Markdown 目录文件的路径和文件名。",
    )

    args = parser.parse_args()
    generate_tree_toc(args.input_dir, args.output_file)
