import os
import time
import json
from openai import OpenAI
from typing import List

# 從 config.json 讀取 API Key
def get_API():
    current_dir = os.path.dirname(os.path.abspath(__file__))  # 取得目前檔案所在目錄
    project_path = os.path.dirname(current_dir) # 取得專案根目錄的路徑
    config_path = os.path.join(project_path, "main", "resources", "config.json") # 構建相對路徑

    with open(config_path, "r") as file:
        config = json.load(file)
    api_key = config.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Error: API Key not found in config.json")
    return api_key

def get_query(content):
    message = {
        "role": "user",
        "content": content,
    }
    return message

def execute_query(content, model):
    api_key = get_API()
    # 初始化 OpenAI 客戶端
    client = OpenAI(
        api_key = api_key
    )
    
    # 查詢模型
    start_time = time.time()
    chat_completion = client.chat.completions.create(
        messages = [
            get_query(content)
        ],
        model = model,
    )
    end_time = time.time()
    execute_time = end_time - start_time

    completion_tokens = chat_completion.usage.completion_tokens
    prompt_tokens = chat_completion.usage.prompt_tokens
    total_tokens = chat_completion.usage.total_tokens

    print("completion_tokens", completion_tokens)
    print("prompt_tokens", prompt_tokens)
    print("total_tokens", total_tokens)
    print(f"Query Time: {execute_time:.2f} seconds")

    return chat_completion.choices[0].message.content

def main():
    content = "say this is a test"
    model = "o1-mini"
    response = execute_query(content, model)
    print(response)


# "Stock Trading Rules:"
# "1. Today's price : The last number in each sequence represents today's price. Today's price is excluded from determining whether a value is a peak or trough."
# "2. Peak : It is the local maximum in the sequence before today, meaning it is greater than its immediate left and right neighbors at a specific position and appears only once at that position."
# "3. Trough : It is the local minimum in the sequence before today, meaning it is less than its immediate left and right neighbors at a specific position and appears only once at that position."
# "4. Buy Condition : Buy when today's price (the last number) is strictly greater than the peak(the unique maximum value in the sequence before today)."
# "5. Sell Condition : Sell when today's price (the last number) is strictly less than the through(the unique minimum value in the sequence before today)."
# "6. No Action Condition : Take no action when today's price (the last number) is equal to or between the peak and the trough, or if there is no peak or trough."
# "Instructions:"
# "Based on the prices preceding today (i.e., the numbers before the last one), determine the action for each period, and indicate the appropriate action."
# "Please briefly answer the following questions using step-by-step reasoning to show your work and explanation of the all process for finding a peak and a trough(according to the peak and trough rules). Do not answer any other question."
# "Question :"
# "Q1. 1, 1, 2, 1, 3, 3, 2, 5"
# "Q2. 3, 3, 2, 2, 3, 3, 1"
# "Q3. 1, 2, 3, 2, 5"
# "Q4. 1, 1, 1, 5"
# "Q5. 1, 2, 3, 4, 5"
# "Q6. 1, 2, 3, 4, 5, 5"
# "Q7. 2, 3, 4, 1"
# "Q8. 2, 1, 3, 5, 4, 2"
# "Q9. 2, 2, 2, 3, 2, 1"
# "Q10. 1.2, 1.0, 1.3, 0.5"
# "Q11. 1.2, 1, 1.3, 0.5",


def calculate_confusion_matrix(true_labels: List[int], predicted_labels: List[int]):
    """
    計算混淆矩陣
    
    Args:
        true_labels (List[int]): 真實標籤
        predicted_labels (List[int]): 預測標籤
    """
    from sklearn.metrics import confusion_matrix
    
    cm = confusion_matrix(true_labels, predicted_labels, labels=[1, 0])  # labels指定順序
    
    TP = cm[0, 0]
    FN = cm[0, 1]
    FP = cm[1, 0]
    TN = cm[1, 1]
    
    # 計算指標
    TPR = TP / (TP + FN) if (TP + FN) > 0 else 0  # True Positive Rate
    FPR = FP / (FP + TN) if (FP + TN) > 0 else 0  # False Positive Rate
    TNR = TN / (TN + FP) if (TN + FP) > 0 else 0  # True Negative Rate
    FNR = FN / (FN + TP) if (FN + TP) > 0 else 0  # False Negative Rate
    
    print(f"Confusion Matrix: TP={TP}, FP={FP}, TN={TN}, FN={FN}")
    print(f"Metrics: TPR={TPR:.2f}, FPR={FPR:.2f}, TNR={TNR:.2f}, FNR={FNR:.2f}")

if __name__ == "__main__":
    main()



# 提取所需字段
# finish_reason = chat_completion['choices'][0]['finish_reason']
# completion_tokens = chat_completion['usage']['completion_tokens']
# prompt_tokens = chat_completion['usage']['prompt_tokens']
# total_tokens = chat_completion['usage']['total_tokens']

# 提取花費信息（假設 OpenAI API 返回相應字段）
# cost_info = chat_completion.get("usage", {})
# tokens_used = cost_info.get("total_tokens", "N/A")

# 印出結果
# print(f"Tokens Used: {tokens_used}")