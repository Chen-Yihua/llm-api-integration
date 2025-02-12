from aalpy.base import Automaton
from aalpy.base.CacheTree import CacheDict
from aalpy.base import SUL
import re
import time

class LLMAutomatonSUL(SUL):
    def __init__(self, automaton: Automaton, client, mq_prompt, params):
        super().__init__()
        self.client = client # LLM 客戶端
        self.params = params # LLM 參數
        self.current_sequence = [] # 當前序列
        self.mq_prompt = mq_prompt # 成員查詢問題
        self.cache = CacheDict()

    def add_cache(self, input_sequence, output_result):
        self.cache.cache_dict[input_sequence] = output_result

    def in_cache(self, input_seq: tuple):
        if input_seq in self.cache.cache_dict.keys():
            return (self.cache.cache_dict[input_seq])
        return None

    def pre(self): # 重置
        self.current_sequence = []

    def step(self, letter = None): # 向 LLM 發送序列並獲取回應 (membership query)
        # 暫存字母
        if letter is None:
            letter = '""'
        else:
            self.current_sequence.append(letter)

        cached_query = self.in_cache(tuple(self.current_sequence)) # 查看序列是否被問過
        if cached_query != None:
            return cached_query
        
        # 詢問 LLM
        full_seq = ','.join(self.current_sequence) 
        if not full_seq:  # 處理空字串
            full_seq = '#'
        query = self.mq_prompt + full_seq
        print("-----------------------------")
        print("ask LLM the following sequence : ", full_seq)

        full_response = ""
        while len(full_response) == 0:
            full_response = self.client.execute_query(query, **self.params)
            time.sleep(2)

        # 取出回答
        response_cleaned = full_response.replace('\n', '').replace('**', '').replace('<', '').replace('>', '').replace('\_', '_')
        pattern = r"FINAL_ANSWER\s*:\s*(.*?)[\s.]*$"
        print("LLM response : ",response_cleaned)
        match = re.search(pattern, response_cleaned)
        if match:
            response = match.group(1).lower()
        else:
            raise ValueError(f"No match: {response}")
        
        # 確認回答是否符合格式
        if response not in {"true","false"}:
            raise ValueError(f"Unexpected LLM response: {response}")
        if response == "true":
            self.add_cache(tuple(self.current_sequence), True)
            return True
        else:
            self.add_cache(tuple(self.current_sequence), False)
            return False
        
    def post(self): # 清理
        pass

MealySUL = OnfsmSUL = StochasticMealySUL = DfaSUL = MooreSUL = MdpSUL = McSUL = SevpaSUL = LLMAutomatonSUL
