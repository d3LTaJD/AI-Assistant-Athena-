"""
Setup script for AI Assistant
Creates a Windows installer that bundles all dependencies
"""
import sys
import os
import subprocess
import shutil
from pathlib import Path
import PyInstaller.__main__

def create_installer():
    """Create Windows installer for AI Assistant"""
    print("🚀 Creating AI Assistant Installer")
    print("=" * 60)
    
    # Step 1: Install required packages for building
    print("\n📦 Installing build dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller", "pywin32", "pillow"])
    
    # Step 2: Create spec file
    print("\n📝 Creating PyInstaller spec file...")
    spec_content = """# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'pyttsx3.drivers',
        'pyttsx3.drivers.sapi5',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AI_Assistant',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico',
)
"""
    
    with open("ai_assistant.spec", "w") as f:
        f.write(spec_content)
    
    # Step 3: Create a simple icon file if it doesn't exist
    if not os.path.exists("icon.ico"):
        print("\n🖼️ Creating icon file...")
        from PIL import Image, ImageDraw
        
        # Create a simple icon
        img = Image.new('RGB', (256, 256), color=(53, 102, 187))
        d = ImageDraw.Draw(img)
        d.ellipse((50, 50, 206, 206), fill=(255, 255, 255))
        d.rectangle((90, 90, 166, 166), fill=(53, 102, 187))
        
        img.save("temp_icon.png")
        
        # Convert to ICO (requires pillow)
        img.save("icon.ico", format="ICO")
    
    # Step 4: Create installer script
    print("\n📝 Creating installer script...")
    nsis_script = """
; AI Assistant Installer Script
!include "MUI2.nsh"

; General
Name "AI Assistant"
OutFile "AI_Assistant_Setup.exe"
InstallDir "$PROGRAMFILES\\AI Assistant"
InstallDirRegKey HKCU "Software\\AI Assistant" ""

; Interface Settings
!define MUI_ABORTWARNING
!define MUI_ICON "icon.ico"

; Pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

; Languages
!insertmacro MUI_LANGUAGE "English"

; Installer Sections
Section "Install"
    SetOutPath "$INSTDIR"
    
    ; Add files
    File "dist\\AI_Assistant.exe"
    File "icon.ico"
    File "README.md"
    
    ; Create uninstaller
    WriteUninstaller "$INSTDIR\\Uninstall.exe"
    
    ; Create shortcuts
    CreateDirectory "$SMPROGRAMS\\AI Assistant"
    CreateShortcut "$SMPROGRAMS\\AI Assistant\\AI Assistant.lnk" "$INSTDIR\\AI_Assistant.exe" "" "$INSTDIR\\icon.ico"
    CreateShortcut "$SMPROGRAMS\\AI Assistant\\Uninstall.lnk" "$INSTDIR\\Uninstall.exe"
    CreateShortcut "$DESKTOP\\AI Assistant.lnk" "$INSTDIR\\AI_Assistant.exe" "" "$INSTDIR\\icon.ico"
    
    ; Write registry keys
    WriteRegStr HKCU "Software\\AI Assistant" "" $INSTDIR
    WriteRegStr HKCU "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\AI Assistant" "DisplayName" "AI Assistant"
    WriteRegStr HKCU "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\AI Assistant" "UninstallString" "$INSTDIR\\Uninstall.exe"
    WriteRegStr HKCU "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\AI Assistant" "DisplayIcon" "$INSTDIR\\icon.ico"
    WriteRegStr HKCU "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\AI Assistant" "Publisher" "AI Assistant"
    WriteRegStr HKCU "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\AI Assistant" "DisplayVersion" "1.0.0"
SectionEnd

; Uninstaller Section
Section "Uninstall"
    ; Remove files
    Delete "$INSTDIR\\AI_Assistant.exe"
    Delete "$INSTDIR\\icon.ico"
    Delete "$INSTDIR\\README.md"
    Delete "$INSTDIR\\Uninstall.exe"
    
    ; Remove shortcuts
    Delete "$SMPROGRAMS\\AI Assistant\\AI Assistant.lnk"
    Delete "$SMPROGRAMS\\AI Assistant\\Uninstall.lnk"
    Delete "$DESKTOP\\AI Assistant.lnk"
    
    ; Remove directories
    RMDir "$SMPROGRAMS\\AI Assistant"
    RMDir "$INSTDIR"
    
    ; Remove registry keys
    DeleteRegKey HKCU "Software\\AI Assistant"
    DeleteRegKey HKCU "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\AI Assistant"
SectionEnd
"""
    
    with open("installer.nsi", "w") as f:
        f.write(nsis_script)
    
    # Step 5: Build executable with PyInstaller
    print("\n🔨 Building executable with PyInstaller...")
    PyInstaller.__main__.run([
        'ai_assistant.spec',
        '--clean',
    ])
    
    # Step 6: Create installer with NSIS (if available)
    print("\n📦 Creating installer with NSIS...")
    try:
        # Try to find NSIS in common locations
        nsis_paths = [
            r"C:\Program Files (x86)\NSIS\makensis.exe",
            r"C:\Program Files\NSIS\makensis.exe"
        ]
        
        nsis_found = False
        for nsis_path in nsis_paths:
            if os.path.exists(nsis_path):
                subprocess.call([nsis_path, "installer.nsi"])
                nsis_found = True
                break
        
        if not nsis_found:
            print("\n⚠️ NSIS not found. Please install NSIS and run:")
            print("makensis installer.nsi")
    except Exception as e:
        print(f"\n⚠️ Error creating installer: {e}")
        print("You can manually create the installer by installing NSIS and running:")
        print("makensis installer.nsi")
    
    # Step 7: Create a simple setup batch file as fallback
    print("\n📝 Creating simple setup batch file...")
    batch_content = """@echo off
echo Installing AI Assistant...
echo.

REM Check if Python is installed
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed! Please install Python 3.8 or higher.
    echo Visit https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Install dependencies
echo Installing dependencies...
python -m pip install -r requirements.txt

echo.
echo Installation complete!
echo Run the assistant with: python main.py
echo.
pause
"""
    
    with open("setup.bat", "w") as f:
        f.write(batch_content)
    
    print("\n✅ Setup files created successfully!")
    print("\n📋 Distribution options:")
    print("1. Windows Installer: AI_Assistant_Setup.exe (if NSIS was available)")
    print("2. Simple Setup: setup.bat + all source files")
    print("3. Standalone Executable: dist\\AI_Assistant.exe")
    
    print("\n💡 To share with others:")
    print("- Option 1: Share the installer (easiest for users)")
    print("- Option 2: Share all files + setup.bat (most compatible)")
    print("- Option 3: Share just the executable (minimal, but may miss dependencies)")

if __name__ == "__main__":
    create_installer()