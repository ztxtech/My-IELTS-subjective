# toc.py
import os
import argparse


def generate_toc(input_dir, output_path):
    """
    递归扫描输入目录中的所有 .md 文件，并生成一个 Markdown 格式的目录文件。

    Args:
        input_dir (str): 需要扫描的输入目录路径。
        output_path (str): 生成的目录文件的完整路径（包括文件名）。
    """
    # 检查输入路径是否存在且为目录
    if not os.path.isdir(input_dir):
        print(f"错误：输入路径 '{input_dir}' 不是一个有效的目录。")
        return

    markdown_files = []
    # 1. 使用 os.walk() 递归遍历目录
    for root, dirs, files in os.walk(input_dir):
        # 对文件和目录列表进行排序，确保输出顺序一致
        dirs.sort()
        files.sort()

        for file in files:
            if file.endswith(".md"):
                # 2. 计算文件相对于输入目录的相对路径
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, input_dir)

                # 3. 将Windows路径分隔符'\'替换为'/'，以确保Markdown链接的兼容性
                link_path = relative_path.replace(os.path.sep, "/")

                # 4. 创建Markdown格式的列表项
                markdown_files.append(f"* [{link_path}]({link_path})")

    if not markdown_files:
        print(f"在 '{input_dir}' 及其子目录中没有找到 .md 文件。")
        return

    # 确保输出目录存在
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"创建输出目录：'{output_dir}'")

    # 5. 将目录写入输出文件
    try:
        with open(output_path, "w", encoding="utf-8") as outfile:
            outfile.write("# Table of Contents\n\n")
            outfile.write("\n".join(markdown_files))

        print(
            f"✅ 成功！已在 '{output_path}' 生成了包含 {len(markdown_files)} 个文件的目录。"
        )

    except IOError as e:
        print(f"写入文件时发生错误：{e}")


if __name__ == "__main__":
    # 设置命令行参数解析器
    parser = argparse.ArgumentParser(
        description="递归扫描目录中的 .md 文件，并生成一个 Markdown 格式的目录。"
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

    # 调用主函数
    generate_toc(args.input_dir, args.output_file)
