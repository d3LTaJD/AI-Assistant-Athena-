"""
Build script for creating Windows installer
"""
import os
import subprocess
import sys
from pathlib import Path

def create_pyinstaller_spec():
    """Create PyInstaller spec file"""
    spec_content = '''
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets', 'assets'),
    ],
    hiddenimports=[
        'customtkinter',
        'PIL._tkinter_finder',
        'pyttsx3.drivers',
        'pyttsx3.drivers.sapi5',
        'speech_recognition',
        'sqlite3',
        'bcrypt',
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
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    cofile_version=None,
    version='version_info.txt',
    icon='assets/icon.ico',
)
'''
    
    with open('ai_assistant.spec', 'w') as f:
        f.write(spec_content)

def create_version_info():
    """Create version info file"""
    version_content = '''
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'AI Assistant'),
        StringStruct(u'FileDescription', u'Personal AI Assistant'),
        StringStruct(u'FileVersion', u'1.0.0.0'),
        StringStruct(u'InternalName', u'AI_Assistant'),
        StringStruct(u'LegalCopyright', u'Copyright (C) 2024'),
        StringStruct(u'OriginalFilename', u'AI_Assistant.exe'),
        StringStruct(u'ProductName', u'AI Assistant'),
        StringStruct(u'ProductVersion', u'1.0.0.0')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
'''
    
    with open('version_info.txt', 'w') as f:
        f.write(version_content)

def create_inno_setup_script():
    """Create Inno Setup script"""
    inno_script = '''
[Setup]
AppName=AI Assistant
AppVersion=1.0
AppPublisher=AI Assistant
AppPublisherURL=https://github.com/yourusername/ai-assistant
AppSupportURL=https://github.com/yourusername/ai-assistant
AppUpdatesURL=https://github.com/yourusername/ai-assistant
DefaultDirName={autopf}\\AI Assistant
DefaultGroupName=AI Assistant
AllowNoIcons=yes
LicenseFile=LICENSE.txt
OutputDir=installer
OutputBaseFilename=AI_Assistant_Setup
SetupIconFile=assets\\icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\\AI_Assistant.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "assets\\*"; DestDir: "{app}\\assets"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\\AI Assistant"; Filename: "{app}\\AI_Assistant.exe"
Name: "{group}\\{cm:UninstallProgram,AI Assistant}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\\AI Assistant"; Filename: "{app}\\AI_Assistant.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\\AI_Assistant.exe"; Description: "{cm:LaunchProgram,AI Assistant}"; Flags: nowait postinstall skipifsilent

[Code]
procedure InitializeWizard;
begin
  WizardForm.LicenseAcceptedRadio.Checked := True;
end;

function InitializeSetup(): Boolean;
begin
  Result := True;
  MsgBox('This AI assistant works offline, but some features (e.g., YouTube, news, weather) require internet connection.', mbInformation, MB_OK);
end;
'''
    
    with open('ai_assistant_setup.iss', 'w') as f:
        f.write(inno_script)

def create_license():
    """Create license file"""
    license_content = '''
AI ASSISTANT LICENSE

Copyright (c) 2024 AI Assistant

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

DISCLAIMER:
This AI assistant works primarily offline, but some features (such as YouTube search,
news updates, and weather information) require an internet connection to function properly.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
    
    with open('LICENSE.txt', 'w') as f:
        f.write(license_content)

def create_assets():
    """Create assets directory and placeholder files"""
    assets_dir = Path('assets')
    assets_dir.mkdir(exist_ok=True)
    
    # Create a simple icon placeholder (you should replace with actual icon)
    icon_content = '''
# This is a placeholder for the application icon
# Replace assets/icon.ico with your actual application icon
# You can create an icon from an image using online converters
'''
    
    with open(assets_dir / 'icon_placeholder.txt', 'w') as f:
        f.write(icon_content)

def build_executable():
    """Build the executable using PyInstaller"""
    print("Creating PyInstaller spec file...")
    create_pyinstaller_spec()
    
    print("Creating version info...")
    create_version_info()
    
    print("Creating assets...")
    create_assets()
    
    print("Building executable with PyInstaller...")
    try:
        subprocess.run([
            sys.executable, '-m', 'PyInstaller',
            '--clean',
            'ai_assistant.spec'
        ], check=True)
        print("✅ Executable built successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error building executable: {e}")
        return False

def build_installer():
    """Build the Windows installer using Inno Setup"""
    print("Creating Inno Setup script...")
    create_inno_setup_script()
    
    print("Creating license file...")
    create_license()
    
    # Check if Inno Setup is installed
    inno_setup_path = r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
    if not os.path.exists(inno_setup_path):
        print("❌ Inno Setup not found. Please install Inno Setup 6 from https://jrsoftware.org/isinfo.php")
        print("After installation, run this script again to create the installer.")
        return False
    
    try:
        subprocess.run([inno_setup_path, 'ai_assistant_setup.iss'], check=True)
        print("✅ Installer created successfully!")
        print("📦 Installer location: installer/AI_Assistant_Setup.exe")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creating installer: {e}")
        return False

def main():
    """Main build process"""
    print("🚀 Building AI Assistant...")
    print("=" * 50)
    
    # Step 1: Build executable
    if not build_executable():
        print("❌ Build failed at executable creation step")
        return
    
    # Step 2: Build installer
    print("\n" + "=" * 50)
    print("📦 Creating Windows installer...")
    
    if build_installer():
        print("\n✅ Build process completed successfully!")
        print("\n📋 Next steps:")
        print("1. Test the executable: dist/AI_Assistant.exe")
        print("2. Test the installer: installer/AI_Assistant_Setup.exe")
        print("3. Distribute the installer to users")
    else:
        print("\n⚠️ Executable created but installer creation failed")
        print("You can still distribute: dist/AI_Assistant.exe")

if __name__ == "__main__":
    main()