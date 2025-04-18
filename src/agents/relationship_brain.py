from sklearn.neural_network import MLPRegressor
import numpy as np

class RelationshipBrain:
    def __init__(self):
        # Stato iniziale delle relazioni: valori tra -1 (ostilità) e 1 (alleanza)
        self.state = {
            ("Gaia", "Prometheus"): 0.0,
            ("Prometheus", "Gaia"): 0.0,
            ("Gaia", "Syra"): 0.0,
            ("Syra", "Gaia"): 0.0,
            ("Prometheus", "Syra"): 0.0,
            ("Syra", "Prometheus"): 0.0
        }
        self.model = MLPRegressor(hidden_layer_sizes=(8,), max_iter=500)
        # Dati di esempio iniziali (puoi espandere)
        self.X = []
        self.y = []

    def update(self, agent1, agent2, interaction_value):
        # interaction_value: -1 (conflitto), 0 (neutrale), 1 (collaborazione)
        self.X.append([self.state[(agent1, agent2)]])
        self.y.append(interaction_value)
        if len(self.X) > 3:  # Addestra solo se hai almeno 3 esempi
            self.model.fit(self.X, self.y)
            pred = self.model.predict([[self.state[(agent1, agent2)]]])[0]
            self.state[(agent1, agent2)] = np.clip(pred, -1, 1)
        else:
            # Aggiorna direttamente se pochi dati
            self.state[(agent1, agent2)] += 0.1 * interaction_value
            self.state[(agent1, agent2)] = np.clip(self.state[(agent1, agent2)], -1, 1)

    def get_relationship(self, agent1, agent2):
        return self.state.get((agent1, agent2), 0.0)