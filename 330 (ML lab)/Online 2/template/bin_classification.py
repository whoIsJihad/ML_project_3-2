import torch
import torch.nn as nn
import torch.optim as optim

# -------------------------------
# Tiny Data
# -------------------------------
x_binary = torch.tensor([
    [0.0, 1.0, 2.0],
    [1.0, 2.0, 3.0],
    [2.0, 3.0, 4.0],
    [3.0, 4.0, 5.0],
    [4.0, 5.0, 6.0]
])
y_binary = torch.tensor([[0],[0],[1],[1],[1]]).float()  # target 0 or 1

# -------------------------------
# Small Binary Neural Net
# -------------------------------
class BinaryNet(nn.Module):
    def __init__(self):
        super(BinaryNet, self).__init__()
        self.fc1 = nn.Linear(3, 2)   # 3 inputs → 2 hidden
        self.fc2 = nn.Linear(2, 1)   # 2 hidden → 1 output

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.sigmoid(self.fc2(x))  # outputs 0-1 probability
        return x

model = BinaryNet()

# -------------------------------
# Loss and Optimizer
# -------------------------------
criterion = nn.BCELoss()
optimizer = optim.SGD(model.parameters(), lr=0.1)

# -------------------------------
# Training Loop (Step by Step)
# -------------------------------
for epoch in range(20):
    optimizer.zero_grad()

    output = model(x_binary)
    loss = criterion(output, y_binary)

    loss.backward()
    optimizer.step()

    # Print step-by-step info
    w1 = model.fc1.weight.data
    b1 = model.fc1.bias.data
    w2 = model.fc2.weight.data
    b2 = model.fc2.bias.data

    print(f"Epoch {epoch+1}")
    print("  Output:", output.squeeze().tolist())
    print("  Target:", y_binary.squeeze().tolist())
    print("  Loss:", round(loss.item(),4))
    print("  fc1 weights:\n", w1)
    print("  fc1 bias:", b1)
    print("  fc2 weights:", w2)
    print("  fc2 bias:", b2)
    print("-----------------------------")
