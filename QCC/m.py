class NFAtoDFA:
    def __init__(self, nfa_transitions, nfa_start_state, nfa_final_states, alphabet):
        # NFA transitions in the form: {state: {symbol: [states]}}
        self.nfa_transitions = nfa_transitions
        self.nfa_start_state = nfa_start_state
        self.nfa_final_states = nfa_final_states
        self.alphabet = alphabet
        self.dfa_transitions = {}
        self.dfa_start_state = frozenset([self.nfa_start_state])
        self.dfa_final_states = set()
        self.dfa_states = {self.dfa_start_state}
    
    def epsilon_closure(self, state):
        """Find the epsilon closure of a state."""
        closure = frozenset([state])  # Use frozenset to make it hashable
        if state in self.nfa_transitions and 'ε' in self.nfa_transitions[state]:
            for next_state in self.nfa_transitions[state]['ε']:
                closure = closure.union(self.epsilon_closure(next_state))
        return closure
    
    def move(self, states, symbol):
        """Return the set of states the NFA can move to on a symbol."""
        next_states = set()
        for state in states:
            if state in self.nfa_transitions and symbol in self.nfa_transitions[state]:
                next_states.update(self.nfa_transitions[state][symbol])
        return next_states
    
    def convert(self):
        """Convert the NFA to a DFA."""
        unprocessed = [self.dfa_start_state]
        while unprocessed:
            current_dfa_state = unprocessed.pop()
            # If the current state is a final state, add it to the DFA final states
            if any(state in self.nfa_final_states for state in current_dfa_state):
                self.dfa_final_states.add(current_dfa_state)
            
            # For each symbol in the alphabet, move to new states
            for symbol in self.alphabet:
                # Find the epsilon closure of the move
                next_state = self.epsilon_closure(self.move(current_dfa_state, symbol))
                if next_state and next_state not in self.dfa_states:
                    self.dfa_states.add(next_state)
                    unprocessed.append(next_state)
                
                if current_dfa_state not in self.dfa_transitions:
                    self.dfa_transitions[current_dfa_state] = {}
                self.dfa_transitions[current_dfa_state][symbol] = next_state
    
    def get_dfa(self):
        """Return the DFA states, start state, final states, and transitions."""
        return {
            'start_state': self.dfa_start_state,
            'final_states': self.dfa_final_states,
            'transitions': self.dfa_transitions
        }


# Example NFA: 
# NFA transitions: state -> {symbol: [states]}
nfa_transitions = {
    0: {'a': [0, 1], 'b': [0], 'ε': [2]},
    1: {'a': [1], 'b': [1]},
    2: {'a': [2], 'b': [3]},
    3: {'b': [3]}
}

nfa_start_state = 0
nfa_final_states = {1, 3}
alphabet = ['a', 'b']

# Create NFA to DFA converter
nfa_to_dfa = NFAtoDFA(nfa_transitions, nfa_start_state, nfa_final_states, alphabet)

# Convert NFA to DFA
nfa_to_dfa.convert()

# Get the DFA
dfa = nfa_to_dfa.get_dfa()

# Output the DFA
print("DFA Start State:", dfa['start_state'])
print("DFA Final States:", dfa['final_states'])
print("DFA Transitions:")
for state, transitions in dfa['transitions'].items():
    for symbol, next_state in transitions.items():
        print(f"  {state} --{symbol}--> {next_state}")
