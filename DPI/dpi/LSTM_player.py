import torch
import torch.nn as nn
import torch.optim as optim

# Definimos la LSTM que predice la próxima jugada del oponente
class PrisonerDilemmaLSTM(nn.Module):
    def __init__(self, input_size=1, hidden_size=16, output_size=1):
        super(PrisonerDilemmaLSTM, self).__init__()
        self.hidden_size = hidden_size
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        h0 = torch.zeros(1, x.size(0), self.hidden_size)
        c0 = torch.zeros(1, x.size(0), self.hidden_size)
        out, _ = self.lstm(x, (h0, c0))
        out = self.fc(out[:, -1, :])
        return self.sigmoid(out)

# Clase de la estrategia que utiliza la LSTM para adaptarse
class AdaptiveLSTMStrategy:
    def __init__(self):
        self.model = PrisonerDilemmaLSTM()
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.01)
        self.criterion = nn.BCELoss()  # Función de pérdida binaria
        self.history = []  # Historial de jugadas previas del oponente

    def update(self, opponent_move):
        # Agrega la última jugada del oponente al historial
        self.history.append([opponent_move])
        if len(self.history) > 5:
            self.history.pop(0)

        # Entrena la red si hay suficientes datos
        if len(self.history) == 5:
            # Prepara el conjunto de datos de entrenamiento
            input_data = torch.tensor(self.history[:-1], dtype=torch.float32).unsqueeze(0)
            target = torch.tensor([self.history[-1][0]], dtype=torch.float32).unsqueeze(0)
            
            # Adelante y cálculo de pérdida
            output = self.model(input_data)
            loss = self.criterion(output, target)
            
            # Backpropagación
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

    def play(self, opponent_last_action):
        # Usa la LSTM para predecir la próxima jugada del oponente
        if len(self.history) < 5:
            return 0  # Cooperar al inicio

        # Prepara los datos de entrada basados en las últimas jugadas
        input_data = torch.tensor(self.history, dtype=torch.float32).unsqueeze(0)
        prediction = self.model(input_data)
        
        # Decisión: deserta (1) si predice que el oponente desertará, coopera (0) si no
        return 1 if prediction.item() > 0.5 else 0
