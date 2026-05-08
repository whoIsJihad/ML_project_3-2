import torch
import torch.nn as nn
import torch.optim as optim

# -------------------------------
# Hyperparameters
# -------------------------------
INPUT_SIZE = 10      # number of features
HIDDEN1 = 32         # first hidden layer neurons
HIDDEN2 = 16         # second hidden layer neurons
OUTPUT_SIZE = 1      # output dimension
LR = 0.01            # learning rate
EPOCHS = 20          # number of training epochs

# -------------------------------
# Sample Data (replace with your own)
# -------------------------------
x = torch.randn(64, INPUT_SIZE)  # batch of 64 samples
y = torch.randn(64, OUTPUT_SIZE) # target values

# -------------------------------
# Model Definition
# -------------------------------
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(INPUT_SIZE, HIDDEN1)
        self.fc2 = nn.Linear(HIDDEN1, HIDDEN2)
        self.fc3 = nn.Linear(HIDDEN2, OUTPUT_SIZE)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x

model = Net()

# -------------------------------
# Loss and Optimizer
# -------------------------------
criterion = nn.MSELoss()           # for regression
# criterion = nn.CrossEntropyLoss() # for classification
optimizer = optim.SGD(model.parameters(), lr=LR)
# optimizer = optim.Adam(model.parameters(), lr=LR)

# -------------------------------
# Training Loop
# -------------------------------
for epoch in range(EPOCHS):
    optimizer.zero_grad()           # reset gradients

    output = model(x)               # forward pass
    loss = criterion(output, y)    # compute loss

    loss.backward()                 # backward pass
    optimizer.step()                # update weights

    # Print progress
    print(f"Epoch {epoch+1}/{EPOCHS} | Loss: {loss.item():.4f}")
    
    # Print predicted output (first 5 samples)
    print(f"Predicted: {output[:5].detach().numpy().flatten()}")
    
    # Print actual output (first 5 samples)
    print(f"Actual: {y[:5].numpy().flatten()}")
    
    # Print weights (first layer weights, first 3 rows)
    print(f"FC1 Weights (first 3 rows): {model.fc1.weight[:3].detach().numpy()}")
    print("---")
