import os
import random
import time
import traceback

from src.llm.gemini import Gemini as Client
from src.utils import filecontent, p1, read_json, write_file, p2


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


def p1_generate(problem):
    # 设置重试参数
    MAX_RETRIES = 3
    BASE_DELAY = 1  # 基础延迟秒数

    system_prompts = [filecontent('data/prompt/个人信息.md'),
                      filecontent('data/prompt/雅思口语答案示范.md'),
                      filecontent('data/prompt/p1.md')]
    client = Client(system_prompts=system_prompts)
    res = None

    retries = 0
    while retries < MAX_RETRIES:
        try:
            res = client.generate_content([p1(problem)])
            client.wait()
            break  # 成功则跳出重试循环
        except:
            retries += 1
            if retries >= MAX_RETRIES:
                print(traceback.format_exc())
            else:
                # 指数退避 + 随机抖动
                client.fail()
                delay = BASE_DELAY * (2 ** (retries - 1)) + random.uniform(0, 1)
                print(f"第{retries}次重试，{delay:.2f}秒后重试...")
                time.sleep(delay)

    return res


def p2_classify(problem):
    # 设置重试参数
    MAX_RETRIES = 3
    BASE_DELAY = 1  # 基础延迟秒数

    system_prompts = [
        filecontent('data/prompt/雅思口语答案示范.md'),
        filecontent('data/prompt/p2分类.md'), ]
    client = Client(system_prompts=system_prompts)
    res = None

    retries = 0
    while retries < MAX_RETRIES:
        try:
            res = client.generate_content([p2(problem)]).replace(" ", "").replace("\n", "")
            if res not in ['人物', '经历', '事物', '地点']:
                raise ValueError(f'Invalid answer for {problem}: {res}')
            client.wait()
            break  # 成功则跳出重试循环
        except:
            retries += 1
            if retries >= MAX_RETRIES:
                print(traceback.format_exc())
            else:
                # 指数退避 + 随机抖动
                client.fail()
                delay = BASE_DELAY * (2 ** (retries - 1)) + random.uniform(0, 1)
                print(f"第{retries}次重试，{delay:.2f}秒后重试...")
                time.sleep(delay)

    return res


def p2_prototype(p2_path, prompt_path):
    # 设置重试参数
    MAX_RETRIES = 3
    BASE_DELAY = 1  # 基础延迟秒数

    system_prompts = [
        filecontent('data/prompt/雅思口语答案示范.md'),
        filecontent('./data/prompt/个人信息.md'),
        filecontent('data/prompt/p2原型生成.md'), ]
    client = Client(system_prompts=system_prompts)

    topics = get_topics(p2_path)
    prompt = "下面是part2, part3的话题"
    for topic in topics:
        prompt += f"\n- {topic}"

    res = None

    retries = 0
    while retries < MAX_RETRIES:
        try:
            res = client.generate_content([prompt])
            client.wait()
            write_file(res, prompt_path)
            break  # 成功则跳出重试循环
        except:
            retries += 1
            if retries >= MAX_RETRIES:
                print(traceback.format_exc())
            else:
                # 指数退避 + 随机抖动
                client.fail()
                delay = BASE_DELAY * (2 ** (retries - 1)) + random.uniform(0, 1)
                print(f"第{retries}次重试，{delay:.2f}秒后重试...")
                time.sleep(delay)

    return res


def p2_generate(problem):
    # 设置重试参数
    MAX_RETRIES = 3
    BASE_DELAY = 1  # 基础延迟秒数

    system_prompts = [filecontent('data/prompt/雅思口语答案示范.md'),
                      filecontent('./data/prompt/个人信息.md'),
                      filecontent('data/prompt/p2原型.md'),
                      filecontent('data/prompt/p2.md')]
    client = Client(system_prompts=system_prompts)
    res = None

    retries = 0
    while retries < MAX_RETRIES:
        try:
            res = client.generate_content([p2(problem)])
            client.wait()
            break  # 成功则跳出重试循环
        except:
            retries += 1
            if retries >= MAX_RETRIES:
                print(traceback.format_exc())
            else:
                print(traceback.format_exc())
                # 指数退避 + 随机抖动
                client.fail()
                delay = BASE_DELAY * (2 ** (retries + 2)) + random.uniform(0, 1)
                print(f"第{retries}次重试，{delay:.2f}秒后重试...")
                time.sleep(delay)

    return res
