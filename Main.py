import torch
from Model.TestModel import TestModel

model = TestModel()

inputOutputs = []

for smoker in range(0, 2):
	for male in range(0, 2):
		expectedAge = (83.3 * male - 3.9) - 10 * smoker
		for age in range(0, 130, 10):
			output = 0.0
			if age > expectedAge:
				output = 1.0

			expectedInput = torch.tensor([float(age), float(male), float(smoker)])
			expectedOutput = torch.tensor(float(output))
			inputOutputs.append([expectedInput, expectedOutput])

inputs = torch.stack([item[0] for item in inputOutputs])
targets = torch.stack([item[1] for item in inputOutputs])

print(f"Inputs shape: {inputs.shape}")
print(f"Targets shape: {targets.shape}")

optimizer = torch.optim.AdamW(
    model.parameters(),
    lr=1e-3
)

print("Starting")
for i in range(2000):
	optimizer.zero_grad()

	outputs = model(inputs).squeeze(1)
	loss = ((outputs - targets) ** 2).mean()

	loss.backward()
	optimizer.step()

	if i % 20 == 0:
		print(loss.item())


print(outputs.shape)
