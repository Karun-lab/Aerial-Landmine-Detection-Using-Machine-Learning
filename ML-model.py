import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from glob import glob

import librosa
import librosa.display
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

sns.set_theme(style="white", palette=None)
color_pal = plt.rcParams["axes.prop_cycle"].by_key()["color"]

# Update the path to your MP3 files
audio_files = glob('path_to_your_mp3_files/*.mp3')

# Load the first MP3 file
y, sr = librosa.load(audio_files[0], sr=None)

# Feature extraction - extracting MFCCs
mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
mfccs_mean = np.mean(mfccs.T, axis=0)

# Prepare data for training
X = []
y = []

# Assuming we have more audio files for training and testing
# Let's simulate with the same audio file but you should use different files
for file in audio_files:
    y_audio, sr_audio = librosa.load(file, sr=None)
    mfccs_audio = librosa.feature.mfcc(y=y_audio, sr=sr_audio, n_mfcc=13)
    mfccs_audio_mean = np.mean(mfccs_audio.T, axis=0)
    X.append(mfccs_audio_mean)
    y.append(1)  # Assuming all belong to the same class for simplicity

# Convert to numpy arrays
X = np.array(X)
y = np.array(y)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train a logistic regression model
model = LogisticRegression()
model.fit(X_train_scaled, y_train)

# Predict on the test set
y_pred = model.predict(X_test_scaled)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy}')

# Predict on the original audio file
mfccs_original = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
mfccs_original_mean = np.mean(mfccs_original.T, axis=0).reshape(1, -1)
mfccs_original_scaled = scaler.transform(mfccs_original_mean)

# Predict the class of the original audio file
prediction = model.predict(mfccs_original_scaled)
print(f'Prediction for the original audio file: {prediction[0]}')

# Visualization (optional)
plt.figure(figsize=(10, 4))
librosa.display.specshow(mfccs, x_axis='time')
plt.colorbar()
plt.title('MFCC')
plt.tight_layout()
plt.show()
