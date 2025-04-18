class StateManager:
    def save_state(state, file_path):
        with open(file_path, 'w') as file:
            json.dump(state, file)

    def load_state(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)

    def update_state(state, key, value):
        state[key] = value
        return state

    def reset_state():
        return {}