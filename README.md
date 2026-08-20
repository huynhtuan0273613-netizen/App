# SBR AUTO TYPER

**Version:** 1.0  
**Branding:** SBR RULEX  
**Purpose:** Fun & Educational

An Android auto-typing application built with Kivy (Python) and Java AccessibilityService that allows you to automatically send text from .txt files to other apps.

---

## ✨ Features

### 🎨 Branding & UI
- **App Name:** SBR AUTO TYPER
- **Theme:** Dark teal UI with SBR branding
- **Default Watermark:** "SBR RULEX" (customizable)
- **Disclaimer:** "This keyboard is made only for fun purpose. Jai Shree Ram Jai Bhavani🧡"

### ⌨️ Auto-Typing Features
- ✅ Load large .txt files (supports 2000+ lines)
- ✅ Send text line-by-line automatically
- ✅ Configurable rows per send: 1, 2, 3, 4, or 5 lines
- ✅ Optional delay system between sends (milliseconds)
- ✅ Automatic watermark appending to each message
- ✅ Preview first 10 lines of loaded file

### 🎨 Visual Customization
- ✅ Choose custom wallpaper from device
- ✅ Gradient background option (black → violet #9400D3 at 135°)
- ✅ Start/Stop controls

### 🔐 Permissions
- **Accessibility Service** - Required for auto-typing in other apps
- **Storage Access** - Read .txt files and wallpapers
- **Internet** - (Optional, for future features)
- **Offline Operation** - Everything runs on device

---

## 📁 Project Structure

```
sbr-auto-typer/
├── main.py                          # Main Kivy application
├── buildozer.spec                   # Build configuration
├── AndroidManifest.xml              # Android manifest template
├── android/
│   ├── src/com/sbr/autotyper/
│   │   └── AutoTyperService.java   # Java accessibility service
│   └── res/
│       ├── xml/
│       │   └── accessibilityservice_config.xml
│       └── values/
│           └── strings.xml
└── README.md                        # This file
```

---

## 🚀 Building the APK

**IMPORTANT:** This project **CANNOT** be built on Replit. You must use one of the following methods:

### Method 1: Build on Android Device (Termux) ⭐ RECOMMENDED

1. **Install Termux** from [F-Droid](https://f-droid.org/packages/com.termux/)

2. **Update Termux packages:**
   ```bash
   pkg update && pkg upgrade
   ```

3. **Install required dependencies:**
   ```bash
   pkg install python git wget build-essential libffi openssl -y
   pkg install clang make autoconf automake libtool pkg-config -y
   pkg install libgmp libmpc libmpfr -y
   ```

4. **Install Java (OpenJDK):**
   ```bash
   pkg install openjdk-17 -y
   ```

5. **Install Python dependencies:**
   ```bash
   pip install --upgrade pip setuptools wheel
   pip install buildozer cython==0.29.33
   ```

6. **Clone/Download this project to Termux:**
   ```bash
   # If on Replit, download as ZIP and extract to Termux storage
   cd ~/storage/downloads/sbr-auto-typer/
   ```

7. **Build the APK:**
   ```bash
   buildozer android debug
   ```

8. **Find your APK:**
   ```bash
   ls bin/*.apk
   ```
   The APK will be in `bin/sbr_autotyper-1.0-debug.apk`

**Note:** First build takes 30-60 minutes as it downloads Android SDK/NDK.

---

### Method 2: Build on Linux PC

1. **Install dependencies (Ubuntu/Debian):**
   ```bash
   sudo apt update
   sudo apt install -y python3-pip python3-venv git wget unzip
   sudo apt install -y build-essential libssl-dev libffi-dev
   sudo apt install -y libgmp-dev libmpfr-dev libmpc-dev
   sudo apt install -y openjdk-11-jdk
   ```

2. **Create virtual environment:**
   ```bash
   python3 -m venv buildenv
   source buildenv/bin/activate
   ```

3. **Install Buildozer:**
   ```bash
   pip install --upgrade pip setuptools wheel
   pip install buildozer cython==0.29.33
   ```

4. **Navigate to project and build:**
   ```bash
   cd sbr-auto-typer/
   buildozer android debug
   ```

5. **APK location:**
   ```bash
   ls bin/*.apk
   ```

---

### Method 3: Cloud Build (GitHub Actions)

1. **Create `.github/workflows/build-apk.yml`:**

```yaml
name: Build Android APK

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        sudo apt update
        sudo apt install -y openjdk-11-jdk
        pip install buildozer cython==0.29.33
    
    - name: Build APK
      run: buildozer android debug
    
    - name: Upload APK
      uses: actions/upload-artifact@v3
      with:
        name: sbr-autotyper-apk
        path: bin/*.apk
```

2. Push to GitHub and download APK from Actions tab

---

## 📱 Installation & Setup

### 1. Install the APK
```bash
adb install bin/sbr_autotyper-1.0-debug.apk
# OR transfer APK to phone and install manually
```

### 2. Enable Accessibility Service
1. Open **Settings** → **Accessibility**
2. Find **SBR Auto Typer** service
3. Toggle it **ON**
4. Grant permission when prompted

### 3. Grant Storage Permissions
1. Open **SBR AUTO TYPER** app
2. Grant file access when prompted

---

## 🎯 How to Use

1. **Launch SBR AUTO TYPER** app
2. **Tap "Choose .txt file"** and select your text file
3. **Configure settings:**
   - Rows per send: 1-5 lines
   - Delay: Set milliseconds between sends
   - Enable delay checkbox if needed
   - Edit watermark text (or uncheck to disable)
4. **Optional:** Choose wallpaper or use gradient
5. **Tap "Start AutoType"**
6. **Switch to target app** (WhatsApp, Telegram, etc.)
7. **Focus on text input field**
8. Text will automatically type and send!
9. **Tap "Stop"** in SBR app to stop typing

---

## ⚠️ Important Notes

### Accessibility Service
- The app **MUST** have Accessibility Service enabled to work
- Without it, auto-typing will not function
- The service can read screen content to find input fields

### Compatibility
- **Minimum Android:** 5.0 (API 21)
- **Target Android:** 11 (API 30)
- Works with most messaging apps (WhatsApp, Telegram, Instagram, etc.)

### Limitations
- Some apps may block accessibility services
- Send button detection is app-specific (may need manual send)
- Large delays may cause the app to pause

### File Format
- Only **.txt files** supported
- UTF-8 encoding recommended
- Each line = one row (configure rows per send accordingly)

---

## 🛠️ Troubleshooting

### Build Errors

**"Command failed: buildozer"**
- Ensure all dependencies are installed
- Check Java is installed: `java -version`
- Clear cache: `buildozer android clean`

**"NDK not found"**
- First build downloads NDK automatically (be patient)
- Stable internet required for first build

**"Permission denied" errors**
- Check file permissions: `chmod +x buildozer`
- Don't run as root user

### App Errors

**"AutoType not working"**
- ✅ Check Accessibility Service is enabled
- ✅ Ensure file is loaded
- ✅ Focus on input field in target app

**"File not loading"**
- ✅ Check storage permissions granted
- ✅ Ensure file is .txt format
- ✅ Check file encoding is UTF-8

**"App crashes on start"**
- Check Android version (min API 21)
- Clear app data and restart

---

## 📄 License & Disclaimer

**Purpose:** Educational and fun use only  
**Disclaimer:** "This keyboard is made only for fun purpose. Jai Shree Ram Jai Bhavani🧡"

Use responsibly and in accordance with app terms of service.

---

## 🔧 Development

### Requirements
- Python 3.7+
- Kivy 2.0+
- pyjnius
- Buildozer
- Android SDK/NDK

### Testing on Desktop
```bash
pip install kivy pillow
python main.py
```
(Auto-typing features only work on Android)

---

## 📞 Support

For build issues:
- Check Buildozer documentation: https://buildozer.readthedocs.io/
- Kivy documentation: https://kivy.org/doc/stable/

---

**Made with ❤️ by SBR**  
**Jai Shree Ram Jai Bhavani 🧡**
