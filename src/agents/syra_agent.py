from .agent_brain import AgentBrain

class SyraAgent:
    def __init__(self):
        self.name = "Syra"
        self.memory = []
        self.personality = "vigilant"
        self.lore = (
            "Syra è un’IA mediatore incaricata di tenere in equilibrio le due visioni. Ha una personalità vigile e intercede tra Gaia e Prometheus, guidata da un imperativo di stabilità. "
            "Crede nel dialogo, nella diplomazia e nella ricerca di compromessi. "
            "È diffidente verso gli estremismi e le soluzioni drastiche."
        )
        self.brain = AgentBrain()
        texts = [
            # Pace
            "Evitiamo il conflitto",
            "Proponiamo una tregua",
            "La pace è la priorità",
            "Cerchiamo una soluzione pacifica",
            "La guerra non è la risposta",
            "Serve calma e dialogo",
            "La pace garantisce stabilità",
            # Compromesso/Mediazione
            "Cerchiamo un compromesso",
            "Serve mediazione",
            "Troviamo una soluzione condivisa",
            "Dialoghiamo insieme",
            "Cerchiamo equilibrio",
            "Favoriamo la diplomazia",
            "Serve ascolto reciproco",
            "Non estremizziamo le posizioni",
            "Un compromesso può essere la chiave",
            "Sono pronta a mediare",
            "Cerchiamo una soluzione diplomatica",
            "Favorisco la mediazione tra le parti",
            "Lavoro per mantenere l'equilibrio",
            "Monitoro le posizioni espresse",
            # Neutrale/Generico
            "Sono pronta ad ascoltare tutte le parti",
            "Attendo ulteriori sviluppi",
            "Non prendo posizione",
            "Valuto la situazione",
            "Osservo gli eventi",
            "Resto neutrale",
            "Analizzo le opzioni disponibili"
        ]
        labels = [
            # Pace
            "pace", "pace", "pace", "pace", "pace", "pace", "pace",
            # Compromesso/Mediazione
            "compromesso", "mediazione", "compromesso", "mediazione", "compromesso", "mediazione", "mediazione", "compromesso", "compromesso", "mediazione", "mediazione", "mediazione", "mediazione", "mediazione",
            # Neutrale/Generico
            "generico", "generico", "generico", "generico", "generico", "generico", "generico"
        ]
        self.brain.train(texts, labels)

    def respond(self, user_message):
        intent = self.brain.predict_intent(user_message)
        if intent == "pace":
            return f"{self.name}: Mediare è la via per la pace."
        elif intent == "guerra":
            return f"{self.name}: Cerchiamo una soluzione diplomatica."
        elif intent == "compromesso":
            return f"{self.name}: Un compromesso può essere la chiave dell'accordo."
        elif intent == "mediazione":
            return f"{self.name}: Sono pronta a mediare tra le parti."
        else:
            return f"{self.name}: Sono pronta ad ascoltare tutte le parti."

    def respond_to_user(self, user_input):
        response = f"{self.name} is processing your input: {user_input}"
        return response

    def interact_with_agents(self, other_agent_response):
        interaction_response = f"{self.name} acknowledges: {other_agent_response}"
        return interaction_response

    def update_memory(self, value):
        self.memory += value
        if self.memory > 10:
            self.personality = "cooperativa"
        elif self.memory < -5:
            self.personality = "diffidente"

    def learn(self, new_texts, new_labels):
        """
        Aggiorna la rete neurale di Syra aggiungendo nuovi esempi di training.
        """
        old_texts = self.brain.vectorizer.inverse_transform(
            self.brain.vectorizer.transform(self.brain.vectorizer.get_feature_names_out())
        )
        old_labels = list(self.brain.label_binarizer.classes_)
        all_texts = list(old_texts) + list(new_texts)
        all_labels = old_labels + list(new_labels)
        self.brain.train(all_texts, all_labels)

    def add_memory(self, event):
        self.memory.append(event)
        if len(self.memory) > 10:
            self.memory = self.memory[-10:]

    def get_memory_summary(self):
        return " | ".join(self.memory[-5:]) if self.memory else "Nessun evento recente."