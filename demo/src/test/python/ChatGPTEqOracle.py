from aalpy.base.Oracle import Oracle
from aalpy.base import SUL
from typing import Optional, List

class ChatGPTEqOracle(Oracle):
    def __init__(self, alphabet: List[str], sul: SUL, client, positive_examples, negative_examples, automaton_type):
        super().__init__(alphabet, sul)
        self.client = client
        self.automaton_type = automaton_type
        self.positive_examples = positive_examples
        self.negative_examples = negative_examples

    # 判斷假設模型 hypothesis 是否接受給定的輸入字串
    def accept_dfa_vpa(self, hypothesis, word, is_positive):
        hypothesis.reset_to_initial()
        temp_state = hypothesis.current_state
        for letter in word:
            temp_state = temp_state.transitions[letter]
        if temp_state.is_accepting != is_positive: # 若有 element 不被自動機接受就回傳
            return False
        return True
    
    def accept_moore(self, hypothesis, word, is_positive):
        hypothesis.reset_to_initial()
        temp_state = hypothesis.current_state
        for letter in word:
            temp_state = temp_state.transitions[letter]
        if temp_state.output != is_positive: # 若有 element 不被自動機接受就回傳
            return False
        return True
    
    def accept_mealy_smm(self, hypothesis, word, expected_output):
        hypothesis.reset_to_initial()
        current_state = hypothesis.initial_state
        for letter in word:
            # 取得對應的輸出和下一個狀態
            output = current_state.output_fun[letter]
            current_state = current_state.transitions[letter]
        if output != expected_output:
            return False
        return True
    
    def accept_stochastic(self, automaton, sequence, is_positive):
        probability = self.calculate_probability(automaton, sequence)
        threshold = 0.5 if is_positive else 0.1
        return probability >= threshold
    
    def accept_onfsm(self, automaton, sequence, is_positive):
        return any(self.accept_dfa_moore(automaton, seq, is_positive) for seq in self.get_all_possible_paths(automaton, sequence))


    # 測試正反例
    def find_cex(self, hypothesis) -> Optional[List[str]]: # 檢查假設模型是否等價於目標系統，若不等價，返回一個反例 
        hypothesis.visualize()

        print("****************************")
        print("測試正反例")
        
        for sequence in reversed(self.positive_examples):
            print("test positive example: ", sequence)
            if self.automaton_type in ["mealy", "smm"]:
                if not self.accept_mealy_smm(hypothesis, sequence, expected_output = True):
                    return list(sequence)
            elif self.automaton_type in ["dfa", "vpa"]:
                if not self.accept_dfa_vpa(hypothesis, sequence, is_positive = True):
                    return list(sequence)
            elif self.automaton_type in ["moore"]:
                if not self.accept_moore(hypothesis, sequence, is_positive = True):
                    return list(sequence)
            elif self.automaton_type in ["mc", "mdp"]:
                if not self.accept_stochastic(hypothesis, sequence, is_positive = True):
                    return list(sequence)
            elif self.automaton_type == "onfsm":
                if not self.accept_onfsm(hypothesis, sequence, is_positive = True):
                    return list(sequence)
            self.positive_examples.pop()

        for sequence in reversed(self.negative_examples):
            print("test negative example: ", sequence)
            if self.automaton_type in ["mealy", "smm"]:
                if not self.accept_mealy_smm(hypothesis, sequence, expected_output = False):
                    return list(sequence)
            elif self.automaton_type in ["dfa", "vpa"]:
                if not self.accept_dfa_vpa(hypothesis, sequence, is_positive = False):
                    return list(sequence)
            elif self.automaton_type in ["moore"]:
                if not self.accept_moore(hypothesis, sequence, is_positive = False):
                    return list(sequence)
            elif self.automaton_type in ["mc", "mdp"]:
                if not self.accept_stochastic(hypothesis, sequence, is_positive = False):
                    return list(sequence)
            elif self.automaton_type == "onfsm":
                if not self.accept_onfsm(hypothesis, sequence, is_positive = False):
                    return list(sequence)
            self.negative_examples.pop()
        
        
        print("****************************")
        return None # 未發現反例
             
