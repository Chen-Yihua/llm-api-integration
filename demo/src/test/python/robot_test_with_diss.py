import Client
import sys
from tee import Tee
import create_test_dataset
from aalpy.learning_algs import (
        run_Lstar, run_KV, run_non_det_Lstar,
        run_stochastic_Lstar, run_abstracted_ONFSM_Lstar, run_Alergia,
        run_JAlergia, run_active_Alergia, run_RPNI, run_active_RPNI 
    )
from diss.experiment.planner import GridWorldPlanner
from diss import diss, LabeledExamples
import robot_test
import diss_test

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
    # counterexample_processing_strategy = [None, 'rs', 'longest_prefix', 'linear_fwd', 'linear_bwd', 'exponential_fwd','exponential_bwd']
    # api_dict = {
    #     "Lstar": run_Lstar,
    #     "KV": run_KV,
    #     "non_det_Lstar": run_non_det_Lstar,
    #     "stochastic_Lstar": run_stochastic_Lstar,
    #     "abstracted_ONFSM_Lstar": run_abstracted_ONFSM_Lstar,
    #     "Alergia": run_Alergia,
    #     "JAlergia": run_JAlergia,
    #     "active_Alergia": run_active_Alergia,
    #     "RPNI": run_RPNI,
    #     "active_RPNI": run_active_RPNI
    # }

    # 打開檔案，覆蓋舊內容
    with open("run_active_RPNI_vpa.txt", "w", encoding="utf-8") as log_file:
        sys.stdout = Tee(sys.stdout, log_file) # 同時輸出到終端和檔案

        # planner = GridWorldPlanner.from_string(
        #     buff="""y....g..
        #     ........
        #     .b.b...r
        #     .b.b...r
        #     .b.b....
        #     .b.b....
        #     rrrrrr.r
        #     g.y.....""",
        #     start=(3, 5),
        #     slip_prob=1/32,
        #     horizon=15,
        #     policy_cache='diss_experiment.shelve',
        # )

        # to_demo = planner.to_demo

        # def to_chain(c, t, psat):
        #     return planner.plan(c, t, psat, monolithic=True, use_rationality=True)


        # # 範例集
        # TRC4 = [
        #     (3, 5),
        #     {'a': '↑', 'c': 0},
        #     {'a': '↑', 'c': 1},
        #     {'a': '↑', 'c': 1},
        #     {'a': '→', 'c': 1},
        #     {'a': '↑', 'c': 1},
        #     {'a': '↑', 'c': 1},
        #     {'a': '→', 'c': 1},
        #     {'a': '→', 'c': 1},
        #     {'a': '→', 'c': 1},
        #     {'a': '←', 'c': 1},
        #     {'a': '←', 'c': 1},
        #     {'a': '←', 'c': 1},
        #     {'a': '←', 'c': 1},
        #     {'a': '←', 'c': 1, 'EOE_ego': 1},
        # ]

        # TRC5 = [
        #     (3, 5),
        #     {'a': '↑', 'c': 1},
        #     {'a': '↑', 'c': 1},
        #     {'a': '↑', 'c': 1},
        #     {'a': '←', 'c': 1},
        #     {'a': '←', 'c': 1, 'EOE_ego': 1},
        # ]


        # # Binary encode demonstrations for BDD based planner.
        # demos = [to_demo(TRC4), to_demo(TRC5)] # 初始學習範例
        # path_to_colors = planner.lift_path
        demos = diss_test.get_demos()
        to_chain = diss_test.get_to_chain
        path_to_colors = diss_test.get_path_to_colors()

        diss_params={
            "sgs_temp": 2**-7,
            "surprise_weight": 1,
            "reset_period": 30,
            "size_weight": 1/80,
            "example_drop_prob": 1/20,
            "synth_timeout": 0,
            "lift_path": path_to_colors,
        }

        # %%
        def analyze(search):
            concept2energy = {}    # Explored concepts + associated energy

            # Run Search and collect concepts, energy, and POI.
            for data, concept, metadata in search:
                concept2energy[concept] = metadata['energy']

            return sorted(list(concept2energy), key=concept2energy.get)
        
        learned_dfa = robot_test.robot_test()

        max_diss_iters = 3

        diss_params = {
            "demos": demos,
            "sgs_temp": 0.01, # 用於控制樣本生成的多樣性
            "n_iters": max_diss_iters, 
            "surprise_weight": 1, # 控制樣本的驚喜程度，影響探索的優先順序
            "reset_period": 30, # 每 30 次迭代會重設內部狀態，防止過度偏向某些樣本
            "size_weight": 1/80,
            "example_drop_prob": 1/20, # 有 1/20 機率隨機丟棄範例，以提升模型的穩健性
            "synth_timeout": 0,
            "competency": lambda *_: 10,
            "to_chain": to_chain,
            "to_concept": learned_dfa,
        } | diss_params

        sys.stdout = sys.__stdout__ # 恢復 stdout
        result = analyze(diss(**diss_params))

    return(result)

if __name__ == '__main__':
    learned_dfa = robot_test()
    print("Learned DFA:", learned_dfa)
