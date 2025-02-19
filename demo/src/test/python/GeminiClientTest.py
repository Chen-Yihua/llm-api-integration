import os
import json
import time
import google.generativeai as genai
# from vertexai.generative_models import GenerativeModel
# from google.oauth2 import service_account

def get_API(model_name):
    # 從 config.json 讀取 API Key
    current_working_directory = os.getcwd() 
    config_path = os.path.join(current_working_directory, "demo", "src", "main", "resources", "config.json") # 構建相對路徑

    with open(config_path, "r") as file:
        config = json.load(file)
    api_key = config.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Error: API Key not found in config.json")

    genai.configure(api_key = api_key) # 初始化客戶端
    model = genai.GenerativeModel(model_name)
    return model

def execute_query(model_name, prompt, max_output_tokens, temperature):
    model = get_API(model_name)
    start_time = time.time()
    response = model.generate_content(
        prompt,
        generation_config = genai.GenerationConfig(
            max_output_tokens = max_output_tokens,
            temperature = temperature
        )
    )
    end_time = time.time()
    print(f"Query Time: {end_time - start_time:.2f} seconds")
    print("Total Tokens:", response.usage_metadata.total_token_count)
    return response.text


def main():
    prompt = (
    "Stock Trading Rules:"
    "1. Today's price : The last number in each sequence represents today's price. Today's price is excluded from determining whether a value is a peak or trough."
    "2. Peak : It is the local maximum in the sequence before today, meaning it is greater than its immediate left and right neighbors at a specific position and appears only once at that position."
    "3. Trough : It is the local minimum in the sequence before today, meaning it is less than its immediate left and right neighbors at a specific position and appears only once at that position."
    "4. Buy Condition : Buy when today's price (the last number) is strictly greater than the peak(the unique maximum value in the sequence before today)."
    "5. Sell Condition : Sell when today's price (the last number) is strictly less than the through(the unique minimum value in the sequence before today)."
    "6. No Action Condition : Take no action when today's price (the last number) is equal to or between the peak and the trough, or if there is no peak or trough."
    "Instructions:"
    "Based on the prices preceding today (i.e., the numbers before the last one), determine the action for each period, and indicate the appropriate action."
    "Please briefly answer the following questions using step-by-step reasoning to show your work and explanation of the all process for finding a peak and a trough(according to the peak and trough rules). Do not answer any other question."
    "Question :"
    "Q1. 1, 1, 2, 1, 3, 3, 2, 5"
    "Q2. 3, 3, 2, 2, 3, 3, 1"
    "Q3. 1, 2, 3, 2, 5"
    "Q4. 1, 1, 1, 5"
    "Q5. 1, 2, 3, 4, 5"
    "Q6. 1, 2, 3, 4, 5, 5"
    "Q7. 2, 3, 4, 1"
    "Q8. 2, 1, 3, 5, 4, 2"
    "Q9. 2, 2, 2, 3, 2, 1"
    "Q10. 1.2, 1.0, 1.3, 0.5"
    "Q11. 1.2, 1, 1.3, 0.5")
    result = execute_query("gemini-1.5-pro", prompt, 1000, 0.1)
    print(result)

if __name__ == "__main__":
    main()