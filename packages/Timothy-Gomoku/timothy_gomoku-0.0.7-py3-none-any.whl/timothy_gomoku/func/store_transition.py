def store_transition(memory, state, action_index, reward):
    memory.append((state, action_index, reward))

__all__ = ["store_transition"]