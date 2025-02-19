from aalpy.learning_algs import run_Lstar
from get_target_dfa import get_target_dfa
from LLMAutomatonSUL import LLMAutomatonSUL
from ChatGPTEqOracle import ChatGPTEqOracle
import Client

target_dfa = get_target_dfa() # 目標自動機

alphabet = target_dfa.get_input_alphabet() # 返回 DFA 所接受的所有輸入符號的集合

# 設定 LLM 參數
client = Client.ChatGPTClient(model_name = "o1-mini")
params = {
            "max_completion_tokens": 1500,
            "temperature": 1,
        }
problem = "'ba*b'" # 欲解決的問題
definition_problem = (f"""
        Instructions:
        - {problem} is the set of all possible finite-length sequences that start and end with the letter 'b', with one or more occurrences of the letter 'a' between the two 'b's. 
        """)

question = (f"""
            Rules:
            - The empty sequence is denoted by '#'
            - Please clean the following text by removing all LaTeX-related symbols (e.g., \\(, \\), \\#, \\ldots) and return the simplified content.
            - Do not answer any other question.
            
            Output format:
            - FINAL_ANSWER:<true, false>.

            Question:
            - Is the following sequence belongs to {problem}:
            """)

test_data_prompt = (f"""
                - By examining demonstrations of the task, please provide me some positive and negative example sequences containing only 'a' or 'b' to test {problem}. 
                - If there are empty strings, represent them with ''.

                Output format:
                Positive examples:
                - [letter1]
                - [letter1, letter2]
                Negative examples:
                - [letter1]
                - [letter1, letter2]
                """)

# 是否有測試資料
test_data_prompt = definition_problem + test_data_prompt
sul = LLMAutomatonSUL(target_dfa, client, definition_problem, question, params) # 將 DFA 包裝為被學習系統（System Under Learning，SUL）
eq_oracle = ChatGPTEqOracle(alphabet, sul, client, test_data_prompt, params)

learned_dfa = run_Lstar(alphabet, sul, eq_oracle, automaton_type='dfa',
                        cache_and_non_det_check = True, cex_processing = None , print_level = 3)

print("learned_dfa : ", learned_dfa)
print("target_dfa : ", target_dfa)

assert learned_dfa == target_dfa # 驗證學習到的 DFA 是否與目標 DFA 相同
print(learned_dfa)

