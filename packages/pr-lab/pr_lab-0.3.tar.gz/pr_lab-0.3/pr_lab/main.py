def lab1():
    print(''' Lab - 1: Pattern Matching with RegEx
import re
import pandas as pd
import seaborn as sns
data = pd.read_csv("Titanic-Dataset.csv")
def match_pattern(data, column, pattern):
    matched = []
    for value in data[column]:
        if re.match(pattern.lower(), str(value).lower()):
            matched.append(value)
    return matched
def get_input():
    print("Available columns to search: 'Name', 'Age', 'Sex', 'Survived', 'Pclass'")
    column = input("Enter the column name to search: ")
    if column not in ['Name', 'Age', 'Sex', 'Survived', 'Pclass']:
        print("Invalid column name. Please enter a valid column name")
        return
    pattern = input(f"Enter the pattern to match in the {column} column: ")
    matched = match_pattern(data, column, pattern)
    if matched:
        print(f"\nFound {len(matched)} matches for the pattern {pattern} in column {column}:")
        for result in matched:
            print(result)
    else:
        print(f"\nNo matches found for the pattrn {pattern} in column {column}")
get_input()
''')
    
def lab2():
    print('''Lab - 2: AND Gate Using Perceptron
import numpy as np
def binary_step(x):
    return np.heaviside(x, 1)
def learn(X, y, lr = 0.1, epochs = 1000):
    weights = np.random.rand(X.shape[1])
    bias = 0
    for epoch in range(epochs):
        output = np.dot(X, weights) + bias
        preds = binary_step(output)
        error = y - preds
        weights += lr * np.dot(error, X)
        bias += lr * error
    return weights, bias
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y = np.array([0, 0, 0, 1])
weights, bias = learn(X, y)
def predict(X, weights, bias):
    output = np.dot(X, weights) + bias
    return binary_step(output)
print(f"Input : \n{X} \nPrediction: {predict(X, weights, bias)}")
print("Input :", X)
print("Prediction:", predict(X, weights, bias))
''')
    
def lab3():
    print('''Lab - 3: Mahalanobis Distance
import numpy as np
def mahalanobis(A, B):
    combined_data = np.vstack((A, B))
    cov_matrix = np.cov(combined_data.T)
    inv_cov_matrix = np.linalg.pinv(cov_matrix)
  
    centroid_A = np.mean(A, axis=0)
    centroid_B = np.mean(B, axis=0)
    
    diff = centroid_A - centroid_B
    mahalanobis_distance = np.sqrt(np.dot(np.dot(diff, inv_cov_matrix), diff.T))
    
    return mahalanobis_distance
A = np.array([[1, 2], [4, 5], [6, 7], [8, 9]])
B = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
print("Mahalanobis Distance: ", mahalanobis(A, B))
''')
    
def lab4():
    print('''Lab - 4: Shannon Entropy
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
def entropy(p):
    if np.isclose(p,0.0) or np.isclose(p,1.0):
        return 0.0
    else:
        return - p*np.log2(p) - (1-p)*np.log2((1-p))
def plot_entropy():
    x = np.arange(0.0, 1, 0.01)
    ent = [entropy(p) for p in x]
    plt.plot(x, ent)
    plt.xlabel("p(i=1)")
    plt.ylabel("Entropy")
    plt.show()
    
plot_entropy()
          
def entropy_node(node):
    p = np.mean(node.target)
    return entropy(p)
def information_gain(node, feature):
    n_parent = node.size
    ent_parent = entropy_node(node)
    
    gain = ent_parent
    for value, child_node in node.groupby(feature):
        n_child = child_node.size
        ent_child = entropy_node(child_node)
        gain -= ent_child * (n_child/n_parent)
    return gain
def split(node, feature):
    splits = []
    for value, child_node in node.groupby(feature):
        splits.append(child_node)
    return splits
data = pd.DataFrame([
    ['blue', 'circle', 1], ['blue', 'circle', 1],['blue', 'circle', 1],
    ['red', 'circle', 0], ['red', 'circle', 0], ['red', 'circle', 1],        
    ['blue', 'square', 0], ['blue', 'square', 0], ['blue', 'square', 0],
    ['red', 'square', 1], ['red', 'square', 1], ['red', 'square', 0],
    ], columns=['color', 'shape', 'target'])

display(data.sort_values('color'))
print(f"entropy: {entropy_node(data)}")

print(f"split on color: IG={information_gain(data, 'color')}")
print(f"split on shape: IG={information_gain(data, 'shape')}")

splits = split(data, 'shape')
for child_node in splits:
    display(child_node)
    print(f"entropy: {entropy_node(child_node)}")
    
circle = splits[0]
ig = information_gain(circle, 'color')
print(f"split circle on color: IG={ig}")
splits = split(circle, 'color')
for child_node in splits:
    display(child_node)
    print(f"entropy: {entropy_node(child_node)}")
''')
    
def lab5():
    print('''Lab - 5: Unsupervised and Supervised Classification
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
def load_images_from_folder(folder, img_size = (64, 64)):
    images = []
    labels = []
    class_names = os.listdir(folder)

    for label, class_name in enumerate(class_names):
        class_path = os.path.join(folder, class_name)
        if not os.path.isdir(class_path):
            continue
        for file in os.listdir(class_path):
            img_path = os.path.join(class_path, file)
            img = cv2.imread(img_path)
            if img is not None:
                img = cv2.resize(img, img_size)
                img = img / 255.0
                images.append(img)
                labels.append(label)

    return np.array(images), np.array(labels), class_names
folder_path = 'caltech101_classification'
X, y, class_names = load_images_from_folder(folder_path)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 69, shuffle = True)

y_train_cat = to_categorical(y_train, num_classes = len(class_names))
y_test_cat = to_categorical(y_test, num_classes = len(class_names))
          
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
model = Sequential([
    Conv2D(32, (3, 3), activation = 'relu', input_shape = (64, 64, 3)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation = 'relu'),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(128, activation = 'relu'),
    Dropout(0.5),
    Dense(len(class_names), activation = 'softmax')
])

model.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])
model.fit(X_train, y_train_cat, epochs = 10, validation_data = (X_test, y_test_cat), batch_size = 32)    

test_loss, test_acc = model.evaluate(X_test, y_test_cat)

print(f"Test Accuracy: {test_acc:.2f}")

from sklearn.cluster import KMeans
X_flattened = X.reshape(X.shape[0], -1)
k = len(class_names)
kmeans = KMeans(n_clusters = k, random_state = 69)
labels = kmeans.fit_predict(X_flattened)
fig, axes = plt.subplots(1, 5, figsize=(10, 5))
for i, ax in enumerate(axes):
    ax.imshow(X[i])
    ax.set_title(f"Cluster {labels[i]}")
    ax.axis('off')
plt.show()      
''')
    
def lab6():
    print('''Lab - 6: Bayesian Classification
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report
from sklearn.datasets import load_iris

data = load_iris()
X = data.data # Features
y = data.target # Target labels
# Split dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = GaussianNB()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred, target_names=data.target_names)
print(f"Accuracy: {accuracy:.2f}")
print("Classification Report:\n", report)          
''')
    
def lab7():
    print('''Lab - 7: Hopfield Network
import numpy as np
def train_hopfield(patterns):
  num_neurons = len(patterns[0])
  weights = np.zeros((num_neurons, num_neurons))

  for pattern in patterns:
    pattern = np.array(pattern).reshape(-1, 1)
    weights += pattern @ pattern.T

  np.fill_diagonal(weights, 0)
  return weights
def recall(weights, input, max_iter = 10):
  output = np.array(input)

  for _ in range(max_iter):
    for i in range(len(output)):
      net_input = weights[i] @ output
      output[i] = 1 if net_input >= 0 else -1

  return output
original = [-1, 1, -1, -1, -1, -1, -1, 1, -1, 1]
weights = train_hopfield([original])
noisy = [-1, -1, -1, 1, -1, -1, -1, 1, -1, 1]
recalled = recall(weights, noisy)
print(recalled)
''')
    
def lab8():
    print('''Lab - 8: Fuzzy C-Means on Given Data
import matplotlib.pyplot as plt 
import pandas as pd
from sklearn.preprocessing import StandardScaler
from fcmeans import FCM
from sklearn.datasets import load_wine

wine = load_wine()
X = wine.data[:, :2]  # Taking only the first two features for visualization

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

fcm = FCM(n_clusters=3, m=2.0, max_iter=100, error=1e-5, random_state=42)
fcm.fit(X_scaled)


centers = fcm.centers
labels = fcm.predict(X_scaled)

plt.figure(figsize=(8, 6))
for i in range(3):
    plt.scatter(X_scaled[labels == i, 0], X_scaled[labels == i, 1], label=f'Cluster {i+1}')
plt.scatter(centers[:, 0], centers[:, 1], marker='x', color='black', s=200, label='Centers')
plt.xlabel("Feature 1")
plt.ylabel("Feature 2")
plt.legend()
plt.title("Fuzzy C-Means Clustering on Wine Dataset")
plt.show()
''')
    
def lab10():
    print('''Lab - 10:  Handwritten Digit Recognition
import tensorflow as tf
from tensorflow.keras import datasets
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
import matplotlib.pyplot as plt
from tensorflow.keras.utils import to_categorical
(X_train, y_train), (X_test, y_test) = datasets.mnist.load_data()

X_train = X_train.reshape((X_train.shape[0], 28, 28, 1)).astype('float32')/255.0
X_test = X_test.reshape((X_test.shape[0], 28, 28, 1)).astype('float32')/255.0

y_train = to_categorical(y_train, 10)
y_test = to_categorical(y_test, 10)
model = Sequential([
    Conv2D(32, 3, activation = 'relu', input_shape = (28, 28, 1)),
    MaxPooling2D(2),
    Conv2D(16, 3, activation = 'relu', input_shape = (28, 28, 1)),
    MaxPooling2D(2),
    Flatten(),
    Dense(64, activation = 'relu'),
    Dense(10, activation = 'softmax')
])
model.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])
history = model.fit(X_train, y_train, epochs = 5, validation_data = (X_test, y_test), batch_size = 64)
test_loss, test_acc = model.evaluate(X_test, y_test, verbose = 2)
print(f"Test Accuracy: {test_acc}")
''')
    
def lab11():
    print('''Lab - 11: Real-Time Fuzzy C-Means Classification
import cv2
import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl

# Define fuzzy variables
brightness = ctrl.Antecedent(np.arange(0, 256, 1), 'brightness')
edge_intensity = ctrl.Antecedent(np.arange(0, 256, 1), 'edge_intensity')
classification = ctrl.Consequent(np.arange(0, 101, 1), 'classification')

brightness['dark'] = fuzz.trimf(brightness.universe, [0, 50, 100])
brightness['normal'] = fuzz.trimf(brightness.universe, [50, 127, 200])
brightness['bright'] = fuzz.trimf(brightness.universe, [150, 200, 255])

edge_intensity['low'] = fuzz.trimf(edge_intensity.universe, [0, 50, 100])
edge_intensity['medium'] = fuzz.trimf(edge_intensity.universe, [50, 127, 200])
edge_intensity['high'] = fuzz.trimf(edge_intensity.universe, [150, 200, 255])

classification['low'] = fuzz.trimf(classification.universe, [0, 25, 50])
classification['medium'] = fuzz.trimf(classification.universe, [25, 50, 75])
classification['high'] = fuzz.trimf(classification.universe, [50, 75, 100])

# Fuzzy rules
rule1 = ctrl.Rule(brightness['dark'] | edge_intensity['low'], classification['low'])
rule2 = ctrl.Rule(brightness['normal'] | edge_intensity['medium'], classification['medium'])
rule3 = ctrl.Rule(brightness['bright'] | edge_intensity['high'], classification['high'])

classification_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])

def real_time_image_classification():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        return
        
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        brightness_value = np.mean(gray)
        edges = cv2.Canny(gray, 100, 200)
        edge_intensity_value = np.mean(edges)

        # Create a fresh simulation per frame
        classifier = ctrl.ControlSystemSimulation(classification_ctrl)
        classifier.input['brightness'] = brightness_value
        classifier.input['edge_intensity'] = edge_intensity_value
        classifier.compute()
        classification_result = classifier.output['classification']

        # Overlay results
        cv2.putText(frame, f'Brightness: {brightness_value:.1f}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
        cv2.putText(frame, f'Edge Intensity: {edge_intensity_value:.1f}', (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
        cv2.putText(frame, f'Classification: {classification_result:.2f}', (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow('Real-Time Classification', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    real_time_image_classification()
''')
    
def lab12():
    print('''Lab - 12: Real-Time K-Means Classification
import cv2
import numpy as np

cap = cv2.VideoCapture(0)
k = 10
criteria = (cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
attempts = 10

while(True):
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.resize(frame, None, fx = 0.5, fy = 0.5)

    pixel_data = frame.reshape((-1, 3))
    pixel_data = np.float32(pixel_data)

    _, labels, centers = cv2.kmeans(pixel_data, k, None, criteria, attempts, cv2.KMEANS_PP_CENTERS)

    centers = np.uint8(centers)

    segmented_data = centers[labels.flatten()]
    segmented_image = segmented_data.reshape(frame.shape)

    cv2.imshow('Real Time K-Means', segmented_image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
''')
    
def help():
    print('''
lab1 - RegEx Pattern Matching
lab2 - Perceptron AND Gate
lab3 - Mahalanobis
lab4 - Shannon Entropy / Decision Tree
lab5 - Supervised and Unsupervised
lab6 - Bayesian Classifier
lab7 - Hopfield Network
lab8 - Fuzzy CMeans on GIVEN Data
lab10 - Handwritten Digits / MNIST
lab11 - Fuzzy CMeans on REAL-TIME Data
lab12 - KMeans on REAL-TIME Data
          
Find the program you want from the key above and insert the appropriate 
lab name into this command
from pr_lab import lab_name
lab_name()
          
Note: Labs 11 and 12 use opencv and real time data and hence will not work on Jupyter notebook. Use PyCharm or VSCode.
''')