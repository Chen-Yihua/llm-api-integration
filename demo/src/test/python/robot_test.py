import Client
import sys
from tee import Tee
import create_test_dataset
from aalpy.learning_algs import (
        run_Lstar, run_KV, run_non_det_Lstar,
        run_stochastic_Lstar, run_abstracted_ONFSM_Lstar, run_Alergia,
        run_JAlergia, run_active_Alergia, run_RPNI, run_active_RPNI 
    )

def robot_test():
    """
    Example automaton from L∗LM paper.

    alphabet: 
    test_datasize_size: 
    test_data_size: 
    model_name: 
    automaton_type: 
    cex_processing: 
    selected_algorithm: 
    max_completion_tokens: 
    temperature: 
    question: 
    definition_problem: 

    :return: learned DFA
    """
    from LLMAutomatonSUL import LLMAutomatonSUL
    from ChatGPTEqOracle import ChatGPTEqOracle
    counterexample_processing_strategy = [None, 'rs', 'longest_prefix', 'linear_fwd', 'linear_bwd', 'exponential_fwd','exponential_bwd']
    api_dict = {
        "Lstar": run_Lstar,
        "KV": run_KV,
        "non_det_Lstar": run_non_det_Lstar,
        "stochastic_Lstar": run_stochastic_Lstar,
        "abstracted_ONFSM_Lstar": run_abstracted_ONFSM_Lstar,
        "Alergia": run_Alergia,
        "JAlergia": run_JAlergia,
        "active_Alergia": run_active_Alergia,
        "RPNI": run_RPNI,
        "active_RPNI": run_active_RPNI
    }

    # 打開檔案，覆蓋舊內容
    with open("run_active_RPNI_vpa.txt", "w", encoding="utf-8") as log_file:
        sys.stdout = Tee(sys.stdout, log_file) # 同時輸出到終端和檔案
        # 設定變數
        alphabet = ['red', 'yellow', 'blue', 'green']
        test_datasize_size = 10 # 資料集大小限制
        test_data_size = 5      # 單筆資料個數限制
        model_name = "o1-mini"  # 使用的 GPT 模型名稱
        automaton_type = 'vpa'  # 自動機類型
        cex_processing = 'rs'   # 反例處理策略
        selected_algorithm = "active_RPNI" # 選擇學習算法
        learner = api_dict[selected_algorithm]    

        # 設定 LLM 參數
        client = Client.ChatGPTClient(model_name = model_name)
        params = {
                    "max_completion_tokens": 1200,
                    "temperature": 1,
                }

        # 設定 prompt
        # 成員查詢問題
        question = (f"""
        Please briefly answer the following questions to show your work. 
        - Do not answer any other question. 
        - The empty sequence is denoted by '#'
        
        Question:
        - Is the following sequence a positive example? :  
        
        Output format:
        FINAL_ANSWER: <true, false>
        """)
        # 任務定義
        definition_problem = ("""
        A robot is operating in a grid world and can visit four types of tiles: {red, yellow, blue, green}.
        They correspond to lava (red), recharging (yellow), water (blue), and drying (green) tiles.
        The robot is to visit tiles according to some set of rules. This will be recorded as a sequence of colors.
        
        Rules:
        1. The sequence must contain at least one yellow tile, i.e., must recharge at some point..
        2. The sequence must not contain any red tiles, i.e., lava must be avoided at all costs.
        3. If the robot has visited blue and then needs to go to yellow, it must visit green immediately before yellow, i.e., the robot must dry off before recharging.
        A positive example must conform to all rules.
        
        Further note that repeated sequential colors can be replaced with a single instance.
        For example:
        - [yellow,yellow,blue] => [yellow, blue]
        - [red,red,blue,green,green,red] => [red,blue,green,red]
        """)
        # 測試生成問題
        example_types = ['Positive', 'Negative']
        example_results = {} # 儲存測試資料結果
        for example_type in example_types:
            test_data_prompt = (f"""
            Provide {test_datasize_size} {example_type} examples.
            - Each example has 1–{test_data_size} elements.

            Output format:
            {example_type} examples:
            - [color1]
            - [color1, color2]
            """)
            test_data_prompt = definition_problem + test_data_prompt
            example_results[example_type] = create_test_dataset.create_test_sequence(client, test_data_prompt, params)

        # 取出 positive 和 negative examples
        positive_examples = example_results['Positive']
        negative_examples = example_results['Negative']

        mq_prompt = definition_problem + question

        # 初始化 SUL 和等價查詢
        sul = LLMAutomatonSUL(None, client, mq_prompt, params) # 將 DFA 包裝為被學習系統（System Under Learning，SUL）
        eq_oracle = ChatGPTEqOracle(alphabet, sul, client, positive_examples, negative_examples, automaton_type)
        
        learned_dfa = learner(
            vpa_alphabet = alphabet, 
            sul = sul, 
            eq_oracle = eq_oracle, 
            automaton_type = automaton_type,
            cex_processing = cex_processing,
            )

        print(f"Using {selected_algorithm} algorithm.")
        print(f"Used model: {model_name}")
        sys.stdout = sys.__stdout__ # 恢復 stdout

    return(learned_dfa)

if __name__ == '__main__':
    learned_dfa = robot_test()
    print("Learned DFA:", learned_dfa)
