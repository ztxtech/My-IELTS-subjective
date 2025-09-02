import json
import os


def convert_txt_to_json(input_file, output_dir):
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 读取输入文件
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 处理每一行
    for line in lines:
        line = line.strip()
        if not line:  # 跳过空行
            continue

        # 创建 JSON 数据
        json_data = {
            "type": "p2u",
            "topic": line
        }

        # 生成输出文件名
        filename = line + ".json"
        filepath = os.path.join(output_dir, filename)

        # 如果文件已存在则跳过
        if os.path.exists(filepath):
            print(f"文件 {filename} 已存在，跳过。")
            continue

        # 写入 JSON 文件
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)

        print(f"已创建文件: {filename}")


if __name__ == "__main__":
    input_file = "data/p2u.txt"
    output_dir = "data/jsons/p2u"
    convert_txt_to_json(input_file, output_dir)
