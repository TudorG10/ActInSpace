import pandas as pd
import numpy as np

dataset = pd.read_csv("commercial.txt")
print(dataset.head())


mask = np.random.rand(len(dataset)) < 0.9

training_set = dataset[mask]
test_set = dataset[~mask]

print len(dataset), len(training_set), len(test_set)

