def get_target_dfa():
    from aalpy.automata import Dfa

    target_dfa = {
        'q0': (False, {'a': 'q0', 'b': 'q1'}),  # q0 是初始狀態，非接受
        'q1': (True, {'a': 'q2', 'b': 'q2'}),   # q1 是接受狀態
        'q2': (True, {'a': 'q2', 'b': 'q2'})    # q2 是接受狀態
    } 

    return Dfa.from_state_setup(target_dfa)