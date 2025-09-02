import os

from src.agent import p2_generate
from utils import read_json, write_file


def generate_p2_answers(input_dir, output_dir):
    """批量生成part1的答案"""

    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 遍历输入目录中的所有JSON文件
    for filename in os.listdir(input_dir):
        if filename.endswith(".json"):
            # 构造完整的文件路径
            input_file_path = os.path.join(input_dir, filename)

            # 读取JSON文件
            problem = read_json(input_file_path)

            # 构造输出文件路径
            output_filename = filename.replace(".json", ".md")
            label_path = os.path.join(output_dir, problem["label"])
            os.makedirs(label_path, exist_ok=True)
            output_file_path = os.path.join(label_path, output_filename)

            # 检查输出文件是否已存在
            if os.path.exists(output_file_path):
                print(f"Answer for {filename} already exists, skipping...")
                continue

            # 生成答案
            answer = p2_generate(problem)

            if answer:
                # 将答案写入文件
                write_file(answer, output_file_path)
                print(f"Generated answer for {filename} and saved to {output_file_path}")
            else:
                print(f"Failed to generate answer for {filename}")

    print("All answers generated.")


if __name__ == "__main__":
    input_dir = "data/jsons/p2/"
    output_dir = "answer/p2/"
    generate_p2_answers(input_dir, output_dir)
