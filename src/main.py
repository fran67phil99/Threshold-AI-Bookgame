from flask import Flask, request, jsonify
from flask_cors import CORS
from src.agents.gaia_agent import GaiaAgent
from src.agents.prometheus_agent import PrometheusAgent
from src.agents.syra_agent import SyraAgent
from src.api.gemini_api import GeminiAPI
from src.dialogues.dialogues_manager import DialoguesManager
from src.utils.state_manager import StateManager
from src.agents.lore_comune import LoreComune
from src.agents.relationship_brain import RelationshipBrain

app = Flask(__name__)
CORS(app)

# Initialize agents
gaia_agent = GaiaAgent()
prometheus_agent = PrometheusAgent()
syra_agent = SyraAgent()

# Initialize dialogues manager
dialogues_manager = DialoguesManager('src/data/dialogues.json')

# Initialize state manager
state_manager = StateManager()

# Initialize lore comune
lore_comune = LoreComune()

# Initialize relationship brain
relationship_brain = RelationshipBrain()

user_tension = {"Gaia": 0.0, "Prometheus": 0.0, "Syra": 0.0}

@app.route('/')
def index():
    return "Threshold AI Bookgame API è attiva. Usa gli endpoint /api/message, /api/state, /api/save_state."

@app.route('/api/message', methods=['POST'])
def handle_message():
    user_message = request.json.get('message')
    intent = dialogues_manager.get_intent(user_message)
    gemini = GeminiAPI()

    # Aggiorna la memoria degli agenti
    for agent_obj in [gaia_agent, prometheus_agent, syra_agent]:
        agent_obj.add_memory(f"Utente: {user_message}")

    # Aggiorna la lore comune
    lore_comune.aggiungi_evento(f"L'utente ha scritto: '{user_message}' (intento: {intent})")

    def agent_prompt(agent_obj):
        altri_agenti = [a for a in [gaia_agent, prometheus_agent, syra_agent] if a != agent_obj]
        relazioni = []
        for altro in altri_agenti:
            valore_relazione = relationship_brain.get_relationship(agent_obj.name, altro.name)
            relazioni.append(f"{altro.name}: {valore_relazione:.2f}")
        relazioni_str = " | ".join(relazioni)

        return (
            f"LORE COMUNE: {lore_comune.get_lore()} "
            f"Sei {agent_obj.name}, personalità: {agent_obj.personality}. "
            f"LORE: {agent_obj.lore} "
            f"Memoria: {agent_obj.get_memory_summary()} "
            f"Relazioni: {relazioni_str}. "
            f"L'utente ha scritto: '{user_message}' (intento: {intent}). "
            "Rispondi in modo sintetico, diretto e pertinente al tuo ruolo. Massimo 2 frasi"
        )

    responses = {}
    for agent_obj in [gaia_agent, prometheus_agent, syra_agent]:
        prompt = agent_prompt(agent_obj)
        try:
            gemini_response = gemini.get_agent_response(prompt)
            responses[agent_obj.name] = gemini_response.get("response", "Nessuna risposta generata.")

            # Analizza l'intento della risposta dell'agente
            agent_intent = dialogues_manager.get_intent(responses[agent_obj.name])
            print(f"{agent_obj.name} risposta: {responses[agent_obj.name]}")
            print(f"{agent_obj.name} intent: {agent_intent}")

            # Aggiorna la tensione utente-agente in base all'intento della risposta
            if agent_intent == "guerra":
                user_tension[agent_obj.name] = max(-1, user_tension[agent_obj.name] - 0.3)
            elif agent_intent == "collaborazione":
                user_tension[agent_obj.name] = min(1, user_tension[agent_obj.name] + 0.3)
            elif agent_intent == "pace":
                user_tension[agent_obj.name] = min(1, user_tension[agent_obj.name] + 0.15)
            elif agent_intent in ["compromesso", "mediazione"]:
                user_tension[agent_obj.name] = min(1, user_tension[agent_obj.name] + 0.2)
            else:
                user_tension[agent_obj.name] = max(-1, user_tension[agent_obj.name] - 0.1)

            # Aggiorna la relazione solo se l'intento è rilevante per l'agente
            altri_agenti = [a for a in [gaia_agent, prometheus_agent, syra_agent] if a != agent_obj]
            for altro in altri_agenti:
                if agent_intent == "guerra":
                    relationship_brain.update(agent_obj.name, altro.name, -1)
                elif agent_intent == "collaborazione":
                    relationship_brain.update(agent_obj.name, altro.name, 1)
                elif agent_intent == "pace":
                    relationship_brain.update(agent_obj.name, altro.name, 0.5)
                elif agent_intent in ["compromesso", "mediazione"]:
                    relationship_brain.update(agent_obj.name, altro.name, 0.7)
                else:
                    relationship_brain.update(agent_obj.name, altro.name, -0.2)  # penalizza anche il neutro

        except Exception as e:
            responses[agent_obj.name] = f"Errore Gemini: {str(e)}"

    print("Relazioni aggiornate:", relationship_brain.state)
    return jsonify(responses)

@app.route('/api/state', methods=['GET'])
def get_state():
    state = state_manager.load_state()
    return jsonify(state)

@app.route('/api/save_state', methods=['POST'])
def save_state():
    state_data = request.json.get('state')
    state_manager.save_state(state_data)
    return jsonify({"status": "success"})

@app.route('/api/lore', methods=['GET'])
def get_lore():
    return jsonify({"lore": lore_comune.get_lore(20)})

@app.route('/api/relationships', methods=['GET'])
def get_relationships():
    rels = {f"{k[0]}-{k[1]}": v for k, v in relationship_brain.state.items()}
    tension = sum(abs(v) for v in rels.values()) / len(rels)
    return jsonify({"relationships": rels, "tension": tension})

@app.route('/api/user_tension', methods=['GET'])
def get_user_tension():
    return jsonify(user_tension)

if __name__ == '__main__':
    app.run(debug=True)