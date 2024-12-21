# 🎧🚀 Human Voice Extraction with Firebase Integration  

Welcome to the **Human Voice Extraction** project! This tool processes audio files to extract human voice segments, adjust amplitudes, and store the results in Firebase for easy access.  

---

## 🎤 Features  
- **Upload & Process Audio Files** – Easily upload your audio files and extract human voice content.  
- **Amplitude Adjustment** – Automatically adjusts the amplitude of the extracted segments.  
- **Firebase Integration** – Upload processed files to Firebase and download them effortlessly.  
- **User-Friendly Flask App** – An intuitive web interface for handling audio files.  

---

## 🔧 How It Works  
1. **Audio Upload** – Drag and drop or select an audio file.  
2. **Processing** – Behind the scenes, we:  
   - Split audio into segments.  
   - Detect the maximum amplitude time.  
   - Extract and normalize the human voice.  
3. **Firebase Magic** – Save processed audio to Firebase for safekeeping and access.  
4. **Download** – Grab your processed file and enjoy the results!  

---

## 🌐 Tech Stack  
- **Backend**: Flask 🌟  
- **Audio Processing**: pydub, librosa  
- **Storage**: Firebase 🔐  
- **Python Modules**: os, re, shutil, and more  

---

## 🔁 Setup Instructions  

### 1️⃣ Clone this repository:  
```bash
git clone https://github.com/yourusername/voice-extraction.git  
cd voice-extraction  
```
### 2️⃣ Install Dependencies:
Install the required Python libraries from the `requirements.txt` file:
```bash
pip install -r requirements.txt
```
### 3️⃣ Set up Firebase Credentials:
-Download your service account JSON file from Firebase.
-Place it in the root directory.
-Add this file to your '.gitignore' to keep it secure.
Install the
required Python libraries from the `requirements.txt` file:
```bash
pip install -r requirements.txt
```
### 4️⃣ Run the Flask App:
Start the Flask application:
```bash
python main.py
```

### 🎨 Future Enhancements
- **Multi-language Voice Support** 🌐  
- **Real-time Processing** ⏳  
- **Advanced Filters for Noise Reduction** 🔊  

### 🎶 Fun Fact  
*"Your voice is like your fingerprint – unique and irreplaceable. This tool helps bring out the best in yours!"* ✨




