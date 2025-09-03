import random
import time
import traceback
from functools import wraps

from src.llm.gemini import Gemini
from src.llm.modelscope import ModelScope
from src.utils import filecontent, p1, write_file, p2, p2u, get_topics


def retry(max_retries=3, base_delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    if retries >= max_retries:
                        print(traceback.format_exc())
                        raise
                    else:
                        # 指数退避 + 随机抖动
                        delay = base_delay * (2 ** (retries + 1)) + random.uniform(0, 1)
                        print(f"第{retries}次重试，{delay:.2f}秒后重试...")
                        time.sleep(delay)

        return wrapper

    return decorator


@retry(max_retries=3, base_delay=1)
def p1_generate(problem):
    system_prompts = [
        filecontent("data/prompt/个人信息.md"),
        filecontent("data/prompt/雅思口语答案示范.md"),
        filecontent("data/prompt/p1.md"),
    ]
    client = Gemini(system_prompts=system_prompts)
    res = client.generate_content([p1(problem)])
    client.wait()
    return res


@retry(max_retries=3, base_delay=1)
def p2_classify(problem):
    system_prompts = [
        filecontent("data/prompt/雅思口语答案示范.md"),
        filecontent("data/prompt/p2分类.md"),
    ]
    client = ModelScope(system_prompts=system_prompts)
    res = client.generate_content([p2(problem)]).replace(" ", "").replace("\n", "")
    if res not in ["人物", "经历", "事物", "地点"]:
        raise ValueError(f"Invalid answer for {problem}: {res}")
    client.wait()
    return res


@retry(max_retries=3, base_delay=1)
def p2u_classify(problem):
    system_prompts = [
        filecontent("data/prompt/雅思口语答案示范.md"),
        filecontent("data/prompt/p2分类.md"),
    ]
    client = Gemini(system_prompts=system_prompts)
    res = client.generate_content([p2u(problem)]).replace(" ", "").replace("\n", "")
    if res not in ["人物", "经历", "事物", "地点"]:
        raise ValueError(f"Invalid answer for {problem}: {res}")
    client.wait()
    return res


@retry(max_retries=3, base_delay=1)
def p2_prototype(p2_path, prompt_path):
    system_prompts = [
        filecontent("data/prompt/雅思口语答案示范.md"),
        filecontent("./data/prompt/个人信息.md"),
        filecontent("data/prompt/p2原型生成.md"),
    ]
    client = Gemini(system_prompts=system_prompts)

    topics = get_topics(p2_path)
    prompt = "下面是part2, part3的话题"
    for topic in topics:
        prompt += f"\n- {topic}"

    res = client.generate_content([prompt])
    client.wait()
    write_file(res, prompt_path)
    return res


@retry(max_retries=3, base_delay=1)
def p2_generate(problem):
    system_prompts = [
        filecontent("data/prompt/雅思口语答案示范.md"),
        filecontent("./data/prompt/个人信息.md"),
        filecontent("data/prompt/p2原型.md"),
        filecontent("./data/prompt/p3思路.md"),
        filecontent("data/prompt/p2.md"),
    ]
    client = ModelScope(system_prompts=system_prompts)
    res = client.generate_content([p2(problem)])
    client.wait()
    return res


@retry(max_retries=3, base_delay=1)
def p2u_generate(problem):
    system_prompts = [
        filecontent("data/prompt/雅思口语答案示范.md"),
        filecontent("./data/prompt/个人信息.md"),
        filecontent("data/prompt/p2原型.md"),
        filecontent("data/prompt/p2u.md"),
    ]
    client = Gemini(system_prompts=system_prompts)
    res = client.generate_content([p2u(problem)])
    client.wait()
    return res
