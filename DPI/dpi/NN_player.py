
import torch
import torch.nn as nn
import torch.optim as optim

from player import Player

# Definimos la red neuronal que predice la próxima jugada del oponente
class PrisonerDilemmaNN(nn.Module, Player):
    def __init__(self, input_size=4, hidden_size=16, output_size=1):
        super(PrisonerDilemmaNN, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, output_size)
        self.sigmoid = nn.Sigmoid()  # Para obtener la probabilidad de deserción

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.sigmoid(self.fc2(x))
        return x

# Clase de la estrategia que utiliza la red neuronal para adaptarse
class AdaptiveNNStrategy:
    def __init__(self):
        self.model = PrisonerDilemmaNN()
        self.optimizer = optim.SGD(self.model.parameters(), lr=0.01)
        self.criterion = nn.BCELoss()  # Función de pérdida binaria
        self.history = []  # Historial de jugadas previas [mi_jugada, su_jugada]

    def update(self, my_move, opponent_move):
        # Agrega la última jugada al historial
        self.history.append([my_move, opponent_move])
        if len(self.history) > 4:
            self.history.pop(0)

        # Entrena la red si hay suficientes datos
        if len(self.history) == 4:
            # Prepara el conjunto de datos de entrenamiento
            input_data = torch.tensor([x[1] for x in self.history[:-1]], dtype=torch.float32).unsqueeze(0)
            target = torch.tensor([self.history[-1][1]], dtype=torch.float32).unsqueeze(0)
            
            # Adelante y cálculo de pérdida
            output = self.model(input_data)
            loss = self.criterion(output, target)
            
            # Backpropagación
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

    def play(self, opponent_last_action):
        # Usa la red para predecir la próxima jugada del oponente
        if len(self.history) < 4:
            return 0  # Cooperar al inicio

        # Prepara los datos de entrada basados en las últimas jugadas
        input_data = torch.tensor([x[1] for x in self.history], dtype=torch.float32).unsqueeze(0)
        prediction = self.model(input_data)
        
        # Decisión: deserta (1) si predice que el oponente desertará, coopera (0) si no
        return 1 if prediction.item() > 0.5 else 0
