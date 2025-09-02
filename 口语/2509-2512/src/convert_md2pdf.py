import os

from utils import md2pdf


def convert_all_md_to_pdf(path="./answer"):
    # 检查answer目录是否存在
    if not os.path.exists(path):
        print(f"错误：目录 '{path}' 不存在。")
        return

    # 遍历answer目录及其子目录
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            # 检查是否为md文件
            if filename.endswith(".md"):
                md_path = os.path.join(dirpath, filename)
                pdf_path = md_path.replace(".md", ".pdf")

                if os.path.exists(pdf_path):
                    print(f"{pdf_path} 已经存在，跳过转换。")
                    continue
                print(f"正在处理: {md_path}")

                # 调用md2pdf函数转换PDF
                success = md2pdf(md_path)
                if success:
                    print(f"成功生成: {pdf_path}")
                else:
                    print(f"生成失败: {md_path}")


if __name__ == "__main__":
    # 调用函数转换所有md文件
    convert_all_md_to_pdf()
