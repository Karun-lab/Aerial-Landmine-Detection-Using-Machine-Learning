import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import seaborn as sns

from glob import glob

import librosa
import librosa.display
import IPython.display as ipd

from itertools import cycle

sns.set_theme(style="white", palette=None)
color_pal = plt.rcParams["axes.prop_cycle"].by_key()["color"]
color_cycle = cycle(plt.rcParams["axes.prop_cycle"].by_key()["color"])

# Update the path to your MP3 files
audio_files = glob('path_to_your_mp3_files/*.mp3')

# Load the first MP3 file
y, sr = librosa.load(audio_files[0], sr=None)
print(f'y: {y[:10]}')
print(f'shape y: {y.shape}')
print(f'sr: {sr}')

# Plot the raw audio waveform
fig1, ax1 = plt.subplots(figsize=(10, 5))
pd.Series(y).plot(ax=ax1, lw=1, title='Raw Audio Example', color=color_pal[0])
plt.show(block=False)

# Trimming leading/lagging silence
y_trimmed, _ = librosa.effects.trim(y, top_db=20)
fig2, ax2 = plt.subplots(figsize=(10, 5))
pd.Series(y_trimmed).plot(ax=ax2, lw=1, title='Raw Audio Trimmed Example', color=color_pal[1])
plt.show(block=False)

# Zoomed-in raw audio
fig3, ax3 = plt.subplots(figsize=(10, 5))
pd.Series(y[30000:30500]).plot(ax=ax3, lw=1, title='Raw Audio Zoomed In Example', color=color_pal[2])
plt.show(block=False)

# Short-time Fourier transform
D = librosa.stft(y)
S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
print(S_db.shape)

# Plot the spectrogram
fig4, ax4 = plt.subplots(figsize=(10, 5))
img = librosa.display.specshow(S_db, x_axis='time', y_axis='log', ax=ax4)
ax4.set_title('Spectrogram Example', fontsize=20)
fig4.colorbar(img, ax=ax4, format='%0.2f')
plt.show(block=False)

# Keep the plots open
plt.show()
