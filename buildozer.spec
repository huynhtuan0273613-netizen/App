[app]

# App title and package name
title = SBR AUTO TYPER
package.name = sbr_autotyper
package.domain = org.sbr

# Source directory and file extensions
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# App version
version = 1.0

# Python requirements
requirements = python3,kivy,pillow,pyjnius

# Android permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Android API levels
android.minapi = 21
android.api = 30
android.ndk = 21b

# Include Java service in android/src
android.add_src = android/src

# Orientation
orientation = portrait

# Fullscreen
fullscreen = 0

# Presplash and icon (optional - add your own images)
# icon.filename = %(source.dir)s/icon.png
# presplash.filename = %(source.dir)s/presplash.png

# Bootstrap
p4a.bootstrap = sdl2

# Additional Android libraries
android.gradle_dependencies = 

# Additional Java classes path
android.add_jars = 

# Log level
log_level = 2

# Build architecture
android.archs = arm64-v8a,armeabi-v7a

[buildozer]

# Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# Display warning if buildozer is run as root
warn_on_root = 1

# Build directory
build_dir = ./.buildozer

# Binary directory  
bin_dir = ./bin
