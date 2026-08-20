#!/usr/bin/env python3
"""
SBR AUTO TYPER - Project Validator
Checks if all required files are present and displays build information.
"""

import os
import sys

def colorize(text, color_code):
    """Add color to terminal output"""
    return f"\033[{color_code}m{text}\033[0m"

def check_file(filepath, description):
    """Check if a file exists and print status"""
    exists = os.path.exists(filepath)
    status = colorize("✓", "92") if exists else colorize("✗", "91")
    print(f"  {status} {description}: {filepath}")
    return exists

def main():
    print(colorize("\n" + "="*60, "96"))
    print(colorize("  SBR AUTO TYPER - Project Validation", "96;1"))
    print(colorize("="*60 + "\n", "96"))
    
    all_ok = True
    
    print(colorize("📋 Checking Core Files...", "94;1"))
    all_ok &= check_file("main.py", "Main application")
    all_ok &= check_file("buildozer.spec", "Build configuration")
    all_ok &= check_file("AndroidManifest.xml", "Android manifest")
    all_ok &= check_file("README.md", "Documentation")
    
    print(colorize("\n📋 Checking Java Source...", "94;1"))
    all_ok &= check_file("android/src/com/sbr/autotyper/AutoTyperService.java", 
                         "Accessibility Service")
    
    print(colorize("\n📋 Checking Android Resources...", "94;1"))
    all_ok &= check_file("android/res/xml/accessibilityservice_config.xml", 
                         "Accessibility config")
    all_ok &= check_file("android/res/values/strings.xml", 
                         "String resources")
    
    print("\n" + "="*60)
    if all_ok:
        print(colorize("✅ PROJECT VALIDATION SUCCESSFUL!", "92;1"))
        print(colorize("\nAll required files are present.", "92"))
    else:
        print(colorize("❌ PROJECT VALIDATION FAILED!", "91;1"))
        print(colorize("\nSome files are missing. Check above for details.", "91"))
    print("="*60 + "\n")
    
    print(colorize("📱 SBR AUTO TYPER - Build Information", "96;1"))
    print("="*60)
    print(colorize("\n⚠️  IMPORTANT:", "93;1"))
    print("This project CANNOT be built on Replit.")
    print("You must build the APK on one of these platforms:\n")
    
    print(colorize("1️⃣  Android Device (Termux) - RECOMMENDED", "92;1"))
    print("   • Install Termux from F-Droid")
    print("   • Install: pkg install python git openjdk-17")
    print("   • Install: pip install buildozer cython==0.29.33")
    print("   • Run: buildozer android debug")
    
    print(colorize("\n2️⃣  Linux PC (Ubuntu/Debian)", "92;1"))
    print("   • Install: sudo apt install python3 openjdk-11-jdk")
    print("   • Install: pip install buildozer cython==0.29.33")
    print("   • Run: buildozer android debug")
    
    print(colorize("\n3️⃣  Cloud Build (GitHub Actions)", "92;1"))
    print("   • Push to GitHub")
    print("   • Use provided GitHub Actions workflow")
    print("   • Download APK from Actions artifacts")
    
    print("\n" + "="*60)
    print(colorize("📖 Full Instructions:", "96;1"))
    print("   Read README.md for complete build instructions")
    print("="*60 + "\n")
    
    print(colorize("✨ Features:", "95;1"))
    print("   • Dark teal SBR-themed UI")
    print("   • Auto-type from .txt files (supports large files)")
    print("   • Configurable rows per send (1-5 lines)")
    print("   • Optional delay system (milliseconds)")
    print("   • Customizable watermark (default: 'SBR RULEX')")
    print("   • Wallpaper & gradient backgrounds")
    print("   • Accessibility service for auto-typing")
    
    print(colorize("\n🙏 Jai Shree Ram Jai Bhavani 🧡\n", "93;1"))
    
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())
