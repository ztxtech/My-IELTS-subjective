# merge.py
import os
import argparse

def merge_markdown_files(input_dir, output_path):
    """
    将输入目录及其所有子目录中的 .md 文件按字母顺序合并到一个输出文件中。

    Args:
        input_dir (str): 包含 .md 文件的输入目录路径。
        output_path (str): 合并后输出文件的完整路径（包括文件名）。
    """
    # 检查输入路径是否存在且为目录
    if not os.path.isdir(input_dir):
        print(f"错误：输入路径 '{input_dir}' 不是一个有效的目录。")
        return

    # 1. 【修改】使用 os.walk() 递归获取并排序所有.md文件的完整路径
    md_files_paths = []
    try:
        # os.walk() 会遍历目录树
        # root 是当前正在遍历的目录路径
        # dirs 是该目录下的子目录列表
        # files 是该目录下的文件列表
        for root, dirs, files in os.walk(input_dir):
            for filename in files:
                if filename.endswith('.md') and 'ztxtech' not in filename:
                    # 将找到的.md文件的完整路径添加到列表中
                    full_path = os.path.join(root, filename)
                    md_files_paths.append(full_path)
        
        # 按完整路径的字母顺序排序
        md_files_paths.sort()

    except FileNotFoundError:
        print(f"错误：找不到输入目录 '{input_dir}'。")
        return

    if not md_files_paths:
        print(f"在 '{input_dir}' 及其子目录中没有找到 .md 文件。")
        return

    # 确保输出目录存在
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"创建输出目录：'{output_dir}'")


    # 2. 从输出文件名创建一级标题
    output_filename = os.path.basename(output_path)
    title, _ = os.path.splitext(output_filename)
    main_title = f"# {title}\n\n"

    # 3. 合并文件
    try:
        with open(output_path, 'w', encoding='utf-8') as outfile:
            # 写入主标题
            outfile.write(main_title)

            # 【修改】遍历排序后的文件【路径】列表
            for i, filepath in enumerate(md_files_paths):
                # 直接使用完整的 `filepath` 读取文件
                with open(filepath, 'r', encoding='utf-8') as infile:
                    # （可选）可以添加一个二级标题来指明源文件
                    relative_path = os.path.relpath(filepath, input_dir)
                    outfile.write(f"## {relative_path}\n\n")
                    
                    outfile.write(infile.read().replace(r'../../','./'))
                    # 在文件内容之间添加两个换行符以作分隔
                    if i < len(md_files_paths) - 1:
                        outfile.write('\n\n---\n\n') # 使用更明显的分隔符

    
        print(f"✅ 成功！已将 {len(md_files_paths)} 个 .md 文件合并到 '{output_path}'")

    except IOError as e:
        print(f"写入文件时发生错误：{e}")


if __name__ == "__main__":
    # 设置命令行参数解析器
    parser = argparse.ArgumentParser(
        description="将一个目录及其所有子目录中的 .md 文件按字母顺序合并成一个单一的 Markdown 文件。"
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