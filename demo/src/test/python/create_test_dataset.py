import time
import re

# 使 LLM 生成正反例
def create_test_sequence(client, query, params):
    positive_examples = []
    negative_examples = []
    response = ""
    
    while len(response) == 0:
        response = client.execute_query(query, **params)
        response = response.replace('\n', '').replace('**', '').replace('<', '').replace('>', '')
        time.sleep(2)
    positive_pattern = r"Positive examples[:\-]*\s*([\s\S]*)"
    negative_pattern = r"Negative examples[:\-]*\s*([\s\S]*)"

    # 取出正例
    match = re.search(positive_pattern, response)
    if match:
        positive_examples = extract_lists(match.group(1)) if match else []
        print("positive_examples : ", positive_examples)
        return positive_examples

    # 取出反例
    match = re.search(negative_pattern, response)
    if match:
        negative_examples = extract_lists(match.group(1)) if match else []
        print("negative_examples : ", negative_examples)
        return negative_examples

# 提取各項並轉為列表
def extract_lists(example_text):
    examples = []
    # 按行分割並清理空格
    lines = example_text.strip().split("\n")
    for line in lines:
        # 匹配方括號、單引號、雙引號的例子
        matches = re.findall(r"\[(.*?)\]|'([^']*)'|\"([^\"]*)\"", line)
        for match in matches:
            # 選擇非空的匹配部分
            content = match[0] or match[1] or match[2]
            # 移除外部引號
            content = content.strip("'\"")
            # 處理逗號分隔的列表
            if "," in content:
                examples.append([item.strip().strip("'\"") for item in content.split(",")])
            elif content:  # 非空字串，保留整體作為列表
                examples.append([content])
            else:  # 空例子
                examples.append([])
    return examples

