import os

from src.agent import p2_classify
from utils import read_json, write_json


def generate_p1_answers(input_dir):
    """批量生成part1的答案"""

    # 遍历输入目录中的所有JSON文件
    for filename in os.listdir(input_dir):
        if filename.endswith('.json'):
            # 构造完整的文件路径
            input_file_path = os.path.join(input_dir, filename)
            problem = read_json(input_file_path)

            if 'label' in problem:
                if not problem['label']:
                    continue

            problem['label'] = p2_classify(problem)

            # 将答案写入文件
            write_json(problem, input_file_path)

            print(f'Generated answer for {filename} and saved to {input_file_path}')

    print('All answers generated.')


if __name__ == '__main__':
    input_dir = 'data/jsons/p2'
    generate_p1_answers(input_dir)
