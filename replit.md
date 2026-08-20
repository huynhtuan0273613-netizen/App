# SBR AUTO TYPER - Android Project

## Overview
This is a complete, build-ready Android application project for **SBR AUTO TYPER**. The app allows users to automatically type and send text from .txt files into other apps using Android's AccessibilityService.

**Important:** This project **cannot be built on Replit**. It must be compiled using Buildozer on:
- Android device (Termux)
- Linux PC (Ubuntu/Debian)
- Cloud build service (GitHub Actions)

## Project Status
✅ **Complete and ready to build**

All source files, configurations, and build instructions are provided. The project is ready to be downloaded and compiled into an APK.

## Architecture

### Tech Stack
- **Frontend:** Kivy (Python UI framework)
- **Backend Service:** Java AccessibilityService
- **Build Tool:** Buildozer (P4A)
- **Platform:** Android (API 21+)

### Key Components
1. **main.py** - Kivy-based UI with SBR dark-teal theme
   - File picker with Android activity result handling
   - Preview of first 10 lines
   - Configuration: rows per send (1-5), delay, watermark
   - Gradient/wallpaper background options
   
2. **AutoTyperService.java** - Accessibility service
   - Broadcast receiver for start/stop commands
   - Text insertion via ACTION_SET_TEXT or clipboard
   - Send button detection and clicking
   - Memory leak prevention (proper node recycling)

3. **buildozer.spec** - Build configuration
   - Android SDK 30, NDK 21b, min API 21
   - Permissions: storage, accessibility, network
   - Python requirements: kivy, pillow, pyjnius

4. **AndroidManifest.xml** - App manifest
   - Accessibility service declarations
   - Required permissions
   - Activity configurations

## Features
✨ **Core Features**
- Load large .txt files (2000+ lines supported)
- Auto-type line by line with configurable rows per send (1-5)
- Optional delay system (milliseconds between sends)
- Customizable watermark (default: "SBR RULEX")
- Dark teal SBR-themed UI
- Gradient backgrounds (black → violet)
- First-time disclaimer popup
- Preview of first 10 lines

🔐 **Permissions**
- Accessibility Service (required for auto-typing)
- Storage access (read .txt files)
- Internet (optional, for future features)

## Build Instructions
See **README.md** for complete build instructions for:
1. Termux (Android device) - **RECOMMENDED**
2. Linux PC (Ubuntu/Debian)
3. GitHub Actions (cloud build)

## File Structure
```
.
├── main.py                                  # Kivy app
├── buildozer.spec                          # Build config
├── AndroidManifest.xml                     # Android manifest
├── README.md                               # Build instructions
├── validate_project.py                     # Project validator
├── android/
│   ├── src/com/sbr/autotyper/
│   │   └── AutoTyperService.java          # Java service
│   └── res/
│       ├── xml/
│       │   └── accessibilityservice_config.xml
│       └── values/
│           └── strings.xml
└── .gitignore
```

## Recent Changes (Latest Session)
- Created complete Android project structure
- Implemented Kivy UI with SBR branding
- Fixed Android file picker with proper activity result handling
- Fixed Java AccessibilityService double-recycle issue
- Removed invalid Kivy Gradient import
- Corrected buildozer.spec configuration
- Fixed AndroidManifest.xml theme reference
- Added comprehensive build documentation

## Known Limitations
- Cannot build on Replit (requires external build environment)
- Send button detection is app-specific (may need manual send in some apps)
- Some apps may block accessibility services
- Requires Android 5.0+ (API 21)

## User Preferences
None specified yet.

## Security Notes
- All file handling uses proper Android content URIs
- Accessibility service permissions clearly described in strings.xml
- No API keys or secrets required
- Offline operation - no data leaves device

## Next Steps for User
1. Download this entire project from Replit
2. Transfer to build environment (Termux/Linux/Cloud)
3. Run `buildozer android debug`
4. Install APK on Android device
5. Enable Accessibility Service in Settings
6. Launch app and enjoy!

---
**Jai Shree Ram Jai Bhavani 🧡**
