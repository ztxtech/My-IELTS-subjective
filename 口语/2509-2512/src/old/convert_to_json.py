import json
import re

# 定义文件路径
file_path = "./口语/2509-2512/data/保留题库.txt"
output_path = "./口语/2509-2512/data/保留题库.json"

# 读取文件内容
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 初始化结果列表
result = {}
result["p1"] = []
result["p2_p3"] = []

# 分割内容为部分
parts = re.split(r"Part 2&3\n", content, 1)
p1_content = parts[0]
p2_p3_content = parts[1] if len(parts) > 1 else ""

# 解析P1部分
p1_pattern = r"(\d+)\s+P1\s+([^\n]+)\n([\s\S]*?)(?=\n\n\d+\s+P1|\Z)"
p1_matches = re.finditer(p1_pattern, p1_content)

for match in p1_matches:
    topic = match.group(2).strip()
    questions_text = match.group(3)
    # 提取问题列表
    questions = [q.strip() for q in questions_text.split("\n") if q.strip()]
    # 添加到结果
    result["p1"].append({"type": "p1", "topic": topic, "problems": questions})

# 解析P2和P3部分
p2_p3_pattern = (
    r"(\d+)\s+P2\s*\n([\s\S]*?)(?=\nP3\n)(?:\nP3\n)([\s\S]*?)(?=\n\n\d+\s+P2|\Z)"
)
p2_p3_matches = re.finditer(p2_p3_pattern, p2_p3_content)

for match in p2_p3_matches:
    p2_text = match.group(2).strip().replace("\n", " ")
    p3_text = match.group(3).strip()
    # 提取P3问题列表
    p3_questions = [q.strip() for q in p3_text.split("\n") if q.strip()]
    # 添加到结果
    result["p2_p3"].append(
        {
            "type": "p2_p3",
            "topic": "",  # 按照用户要求，topic字段放空字符串
            "p2": p2_text,
            "p3": p3_questions,
        }
    )

# 保存为JSON文件
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"转换完成！JSON文件已保存至：{output_path}")
