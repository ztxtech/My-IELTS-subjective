# merge.py
import os
import argparse

def merge_markdown_files(input_dir, output_path):
    """
    将输入目录中的所有 .md 文件按字母顺序合并到一个输出文件中。

    Args:
        input_dir (str): 包含 .md 文件的输入目录路径。
        output_path (str): 合并后输出文件的完整路径（包括文件名）。
    """
    # 检查输入路径是否存在且为目录
    if not os.path.isdir(input_dir):
        print(f"错误：输入路径 '{input_dir}' 不是一个有效的目录。")
        return

    # 1. 获取并按字母序排序所有.md文件
    try:
        file_list = os.listdir(input_dir)
        md_files = sorted([f for f in file_list if f.endswith('.md')])
    except FileNotFoundError:
        print(f"错误：找不到输入目录 '{input_dir}'。")
        return

    if not md_files:
        print(f"在 '{input_dir}' 目录中没有找到 .md 文件。")
        return

    # 确保输出目录存在
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"创建输出目录：'{output_dir}'")


    # 2. 从输出文件名创建一级标题
    # os.path.basename 获取路径中的文件名
    # os.path.splitext 分离文件名和扩展名
    output_filename = os.path.basename(output_path)
    title, _ = os.path.splitext(output_filename)
    main_title = f"# {title}\n\n"

    # 3. 合并文件
    try:
        with open(output_path, 'w', encoding='utf-8') as outfile:
            # 写入主标题
            outfile.write(main_title)

            # 遍历排序后的文件列表，读取内容并写入输出文件
            for i, filename in enumerate(md_files):
                filepath = os.path.join(input_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as infile:
                    outfile.write(infile.read())
                    # 在文件内容之间添加两个换行符以作分隔
                    if i < len(md_files) - 1:
                        outfile.write('\n\n')

        print(f"✅ 成功！已将 {len(md_files)} 个 .md 文件合并到 '{output_path}'")

    except IOError as e:
        print(f"写入文件时发生错误：{e}")


if __name__ == "__main__":
    # 设置命令行参数解析器
    parser = argparse.ArgumentParser(
        description="将一个目录中的所有 .md 文件按字母顺序合并成一个单一的 Markdown 文件。"
    )
    parser.add_argument(
        "--in",
        dest="input_dir",
        required=True,
        help="包含 .md 文件的输入目录路径。"
    )
    parser.add_argument(
        "--out",
        dest="output_file",
        required=True,
        help="合并后输出文件的路径和文件名 (例如：'./output/final.md')。"
    )

    args = parser.parse_args()

    # 调用主函数
    merge_markdown_files(args.input_dir, args.output_file)