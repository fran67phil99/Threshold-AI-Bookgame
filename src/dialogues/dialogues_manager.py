from pathlib import Path
import json

class DialoguesManager:
    def __init__(self, dialogues_file):
        self.dialogues_file = dialogues_file
        self.dialogues = self.load_dialogues()

    def load_dialogues(self):
        if Path(self.dialogues_file).is_file():
            with open(self.dialogues_file, 'r', encoding='utf-8') as file:
                return json.load(file)
        return []

    def get_dialogue(self, scene_id):
        for dialogue in self.dialogues:
            if dialogue['scene_id'] == scene_id:
                return dialogue
        return None

    def get_choices(self, scene_id):
        dialogue = self.get_dialogue(scene_id)
        if dialogue:
            return dialogue.get('choices', [])
        return []

    def get_response(self, scene_id, choice_text):
        dialogue = self.get_dialogue(scene_id)
        if dialogue:
            for choice in dialogue.get('choices', []):
                if choice['text'] == choice_text:
                    return choice['response'], choice['effect'], choice['next_scene']
        return None, None, None

    def update_dialogue_effects(self, effects):
        # Logic to update the game state based on dialogue effects can be implemented here
        pass

    def get_intent(self, user_message):
        # Semplice esempio: restituisce uno "intent" fittizio
        # Sostituisci con la tua logica di NLP o matching
        if "pace" in user_message.lower():
            return "pace"
        elif "guerra" in user_message.lower():
            return "guerra"
        else:
            return "generico"

# Example usage
# dialogues_manager = DialoguesManager('src/data/dialogues.json')
# dialogue = dialogues_manager.get_dialogue('intro_syra')
# print(dialogue)