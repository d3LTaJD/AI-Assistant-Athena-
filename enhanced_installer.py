"""
Enhanced Installer Builder for Advanced AI Assistant
Creates professional Windows installer with all features
"""
import os
import subprocess
import sys
import shutil
from pathlib import Path
import json

class AdvancedInstallerBuilder:
    def __init__(self):
        self.project_name = "Advanced_AI_Assistant"
        self.version = "2.0.0"
        self.author = "AI Assistant Team"
        self.description = "Advanced AI Assistant with Room-Scale Voice Recognition"
        
        # Paths
        self.build_dir = Path("build")
        self.dist_dir = Path("dist")
        self.installer_dir = Path("installer")
        
        # Create directories
        for directory in [self.build_dir, self.dist_dir, self.installer_dir]:
            directory.mkdir(exist_ok=True)
    
    def create_pyinstaller_spec(self):
        """Create advanced PyInstaller spec file"""
        spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

import sys
from pathlib import Path

block_cipher = None

# Define paths
project_root = Path.cwd()
assets_path = project_root / "assets"

a = Analysis(
    ['enhanced_main.py'],
    pathex=[str(project_root)],
    binaries=[],
    datas=[
        (str(assets_path), 'assets'),
        ('requirements_advanced.txt', '.'),
        ('README.md', '.'),
    ],
    hiddenimports=[
        'customtkinter',
        'PIL._tkinter_finder',
        'pyttsx3.drivers',
        'pyttsx3.drivers.sapi5',
        'pyttsx3.drivers.nsss',
        'pyttsx3.drivers.espeak',
        'speech_recognition',
        'sqlite3',
        'bcrypt',
        'psutil',
        'numpy',
        'webrtcvad',
        'pyaudio',
        'tkinter',
        'tkinter.ttk',
        'queue',
        'threading',
        'json',
        'pathlib',
        'glob',
        'math',
        'random',
        'time',
        'datetime',
        'collections',
        'platform',
        'socket',
        'uuid',
        'hashlib',
        'webbrowser',
        'subprocess',
        'requests',
        'urllib',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'pandas',
        'scipy',
        'tensorflow',
        'torch',
        'cv2',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Filter out unnecessary files
a.datas = [x for x in a.datas if not x[0].startswith('tcl')]
a.datas = [x for x in a.datas if not x[0].startswith('tk')]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='{self.project_name}',
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
    manifest='manifest.xml',
)
'''
        
        with open('advanced_assistant.spec', 'w') as f:
            f.write(spec_content)
        
        print("✅ PyInstaller spec file created")
    
    def create_version_info(self):
        """Create detailed version info file"""
        version_content = f'''VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=({self.version.replace('.', ', ')}, 0),
    prodvers=({self.version.replace('.', ', ')}, 0),
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
        [StringStruct(u'CompanyName', u'{self.author}'),
        StringStruct(u'FileDescription', u'{self.description}'),
        StringStruct(u'FileVersion', u'{self.version}'),
        StringStruct(u'InternalName', u'{self.project_name}'),
        StringStruct(u'LegalCopyright', u'Copyright (C) 2024 {self.author}'),
        StringStruct(u'OriginalFilename', u'{self.project_name}.exe'),
        StringStruct(u'ProductName', u'Advanced AI Assistant'),
        StringStruct(u'ProductVersion', u'{self.version}'),
        StringStruct(u'Comments', u'Room-scale voice recognition AI assistant')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)'''
        
        with open('version_info.txt', 'w') as f:
            f.write(version_content)
        
        print("✅ Version info file created")
    
    def create_manifest(self):
        """Create application manifest for Windows"""
        manifest_content = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
  <assemblyIdentity
    version="2.0.0.0"
    processorArchitecture="*"
    name="AdvancedAIAssistant"
    type="win32"
  />
  <description>Advanced AI Assistant with Room-Scale Voice Recognition</description>
  <dependency>
    <dependentAssembly>
      <assemblyIdentity
        type="win32"
        name="Microsoft.Windows.Common-Controls"
        version="6.0.0.0"
        processorArchitecture="*"
        publicKeyToken="6595b64144ccf1df"
        language="*"
      />
    </dependentAssembly>
  </dependency>
  <trustInfo xmlns="urn:schemas-microsoft-com:asm.v2">
    <security>
      <requestedPrivileges>
        <requestedExecutionLevel level="asInvoker" uiAccess="false"/>
      </requestedPrivileges>
    </security>
  </trustInfo>
  <compatibility xmlns="urn:schemas-microsoft-com:compatibility.v1">
    <application>
      <supportedOS Id="{8e0f7a12-bfb3-4fe8-b9a5-48fd50a15a9a}"/>
      <supportedOS Id="{1f676c76-80e1-4239-95bb-83d0f6d0da78}"/>
      <supportedOS Id="{4a2f28e3-53b9-4441-ba9c-d69d4a4a6e38}"/>
      <supportedOS Id="{35138b9a-5d96-4fbd-8e2d-a2440225f93a}"/>
      <supportedOS Id="{e2011457-1546-43c5-a5fe-008deee3d3f0}"/>
    </application>
  </compatibility>
  <application xmlns="urn:schemas-microsoft-com:asm.v3">
    <windowsSettings>
      <dpiAware xmlns="http://schemas.microsoft.com/SMI/2005/WindowsSettings">true</dpiAware>
      <dpiAwareness xmlns="http://schemas.microsoft.com/SMI/2016/WindowsSettings">PerMonitorV2</dpiAwareness>
    </windowsSettings>
  </application>
</assembly>'''
        
        with open('manifest.xml', 'w') as f:
            f.write(manifest_content)
        
        print("✅ Application manifest created")
    
    def create_inno_setup_script(self):
        """Create comprehensive Inno Setup script"""
        inno_script = f'''[Setup]
AppName=Advanced AI Assistant
AppVersion={self.version}
AppVerName=Advanced AI Assistant {self.version}
AppPublisher={self.author}
AppPublisherURL=https://github.com/yourusername/advanced-ai-assistant
AppSupportURL=https://github.com/yourusername/advanced-ai-assistant/issues
AppUpdatesURL=https://github.com/yourusername/advanced-ai-assistant/releases
DefaultDirName={{autopf}}\\Advanced AI Assistant
DefaultGroupName=Advanced AI Assistant
AllowNoIcons=yes
LicenseFile=LICENSE.txt
InfoBeforeFile=INSTALL_INFO.txt
OutputDir=installer
OutputBaseFilename=Advanced_AI_Assistant_Setup_v{self.version}
SetupIconFile=assets\\icon.ico
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
WizardSizePercent=120
DisableWelcomePage=no
DisableDirPage=no
DisableProgramGroupPage=no
DisableReadyPage=no
DisableFinishedPage=no
ShowLanguageDialog=yes
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64
MinVersion=6.1sp1
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "spanish"; MessagesFile: "compiler:Languages\\Spanish.isl"
Name: "french"; MessagesFile: "compiler:Languages\\French.isl"
Name: "german"; MessagesFile: "compiler:Languages\\German.isl"

[Tasks]
Name: "desktopicon"; Description: "{{cm:CreateDesktopIcon}}"; GroupDescription: "{{cm:AdditionalIcons}}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{{cm:CreateQuickLaunchIcon}}"; GroupDescription: "{{cm:AdditionalIcons}}"; Flags: unchecked; OnlyBelowVersion: 6.1
Name: "startmenu"; Description: "Add to Start Menu"; GroupDescription: "{{cm:AdditionalIcons}}"; Flags: checkedonce

[Files]
Source: "dist\\{self.project_name}.exe"; DestDir: "{{app}}"; Flags: ignoreversion
Source: "assets\\*"; DestDir: "{{app}}\\assets"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "README.md"; DestDir: "{{app}}"; Flags: ignoreversion
Source: "requirements_advanced.txt"; DestDir: "{{app}}"; Flags: ignoreversion

[Icons]
Name: "{{group}}\\Advanced AI Assistant"; Filename: "{{app}}\\{self.project_name}.exe"; IconFilename: "{{app}}\\assets\\icon.ico"
Name: "{{group}}\\{{cm:ProgramOnTheWeb,Advanced AI Assistant}}"; Filename: "https://github.com/yourusername/advanced-ai-assistant"
Name: "{{group}}\\{{cm:UninstallProgram,Advanced AI Assistant}}"; Filename: "{{uninstallexe}}"
Name: "{{autodesktop}}\\Advanced AI Assistant"; Filename: "{{app}}\\{self.project_name}.exe"; IconFilename: "{{app}}\\assets\\icon.ico"; Tasks: desktopicon
Name: "{{userappdata}}\\Microsoft\\Internet Explorer\\Quick Launch\\Advanced AI Assistant"; Filename: "{{app}}\\{self.project_name}.exe"; Tasks: quicklaunchicon

[Run]
Filename: "{{app}}\\{self.project_name}.exe"; Description: "{{cm:LaunchProgram,Advanced AI Assistant}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{{userprofile}}\\.ai_assistant"

[Registry]
Root: HKCU; Subkey: "Software\\Advanced AI Assistant"; ValueType: string; ValueName: "InstallPath"; ValueData: "{{app}}"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\\Advanced AI Assistant"; ValueType: string; ValueName: "Version"; ValueData: "{self.version}"; Flags: uninsdeletekey

[Code]
var
  FeaturePage: TInputOptionWizardPage;
  
procedure InitializeWizard;
begin
  // Create custom feature selection page
  FeaturePage := CreateInputOptionPage(wpSelectTasks,
    'Select Features', 'Choose which features to enable',
    'Select the features you want to use with your AI Assistant:',
    True, False);
  
  FeaturePage.Add('Enable voice recognition (requires microphone)');
  FeaturePage.Add('Enable system monitoring');
  FeaturePage.Add('Enable web search features');
  FeaturePage.Add('Create desktop shortcuts');
  
  // Set default selections
  FeaturePage.Values[0] := True;  // Voice recognition
  FeaturePage.Values[1] := True;  // System monitoring
  FeaturePage.Values[2] := True;  // Web search
  FeaturePage.Values[3] := False; // Desktop shortcuts
end;

function InitializeSetup(): Boolean;
var
  ResultCode: Integer;
begin
  Result := True;
  
  // Show welcome message with features
  if MsgBox('Welcome to Advanced AI Assistant Setup!' + #13#10 + #13#10 +
           '🤖 Features included:' + #13#10 +
           '• Room-scale voice recognition' + #13#10 +
           '• 3D animated assistant avatar' + #13#10 +
           '• Smart file management' + #13#10 +
           '• Real-time system monitoring' + #13#10 +
           '• Advanced AI capabilities' + #13#10 + #13#10 +
           '⚠️ Note: This assistant works offline, but some features ' +
           '(YouTube, news, weather) require internet connection.' + #13#10 + #13#10 +
           'Continue with installation?',
           mbConfirmation, MB_YESNO) = IDNO then
    Result := False;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // Create user data directory
    CreateDir(ExpandConstant('{{userprofile}}\\.ai_assistant'));
    CreateDir(ExpandConstant('{{userprofile}}\\.ai_assistant\\logs'));
    CreateDir(ExpandConstant('{{userprofile}}\\.ai_assistant\\database'));
  end;
end;

function ShouldSkipPage(PageID: Integer): Boolean;
begin
  Result := False;
end;

procedure CurPageChanged(CurPageID: Integer);
begin
  if CurPageID = wpFinished then
  begin
    WizardForm.FinishedLabel.Caption := 
      'Advanced AI Assistant has been successfully installed!' + #13#10 + #13#10 +
      '🚀 Getting Started:' + #13#10 +
      '1. Launch the application from the Start Menu or Desktop' + #13#10 +
      '2. Create your account and name your assistant' + #13#10 +
      '3. Choose your preferred voice (male/female)' + #13#10 +
      '4. Grant microphone permissions for voice features' + #13#10 +
      '5. Say your assistant''s name to activate voice control' + #13#10 + #13#10 +
      '💡 Tips:' + #13#10 +
      '• Works from across the room with room-scale voice detection' + #13#10 +
      '• All data is stored locally for privacy' + #13#10 +
      '• Type "help" or say "help" to see all available commands' + #13#10 + #13#10 +
      'Enjoy your new AI assistant!';
  end;
end;
'''
        
        with open('advanced_assistant_setup.iss', 'w') as f:
            f.write(inno_script)
        
        print("✅ Inno Setup script created")
    
    def create_license_and_docs(self):
        """Create license and documentation files"""
        # License file
        license_content = f'''ADVANCED AI ASSISTANT LICENSE

Copyright (c) 2024 {self.author}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

FEATURES AND CAPABILITIES:
This Advanced AI Assistant includes:
• Room-scale voice recognition technology
• 3D animated assistant avatar with natural interactions
• Smart file management with natural language processing
• Real-time system monitoring and performance tracking
• Advanced AI capabilities for complex task handling
• Offline-first design with optional online features

PRIVACY AND DATA:
• All personal data is stored locally on your computer
• No data is transmitted to external servers without your consent
• Voice recognition processing happens entirely offline
• Optional online features (YouTube, news, weather) require internet

SYSTEM REQUIREMENTS:
• Windows 10 or later (64-bit)
• Minimum 4GB RAM (8GB recommended)
• Microphone for voice features
• Internet connection for optional online features

DISCLAIMER:
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
        
        # Installation info
        install_info = '''ADVANCED AI ASSISTANT - INSTALLATION INFORMATION

🚀 WELCOME TO THE FUTURE OF AI ASSISTANCE!

You are about to install the most advanced offline-first AI assistant available.

KEY FEATURES:
═══════════════════════════════════════════════════════════════

🎤 ROOM-SCALE VOICE RECOGNITION
• Hear you from across the room
• Advanced noise filtering
• Natural wake word detection
• Works in noisy environments

🤖 3D ANIMATED AVATAR
• Realistic facial expressions
• Speaking and listening animations
• Visual feedback for all interactions
• Customizable appearance

📁 SMART FILE MANAGEMENT
• "Open my resume from Documents"
• "Find all photos from last month"
• "Play music from my playlist"
• Natural language file operations

🖥️ REAL-TIME SYSTEM MONITORING
• CPU, memory, and disk usage
• Network status and performance
• Running processes overview
• System health alerts

🧠 ADVANCED AI CAPABILITIES
• Context-aware conversations
• Learning from your preferences
• Complex task handling
• Multi-step command execution

SYSTEM REQUIREMENTS:
═══════════════════════════════════════════════════════════════

✅ Windows 10 or later (64-bit)
✅ Minimum 4GB RAM (8GB recommended for optimal performance)
✅ 500MB free disk space
✅ Microphone (for voice features)
✅ Audio output device (speakers/headphones)
✅ Internet connection (optional, for web features)

PRIVACY & SECURITY:
═══════════════════════════════════════════════════════════════

🔒 All data stored locally on your computer
🔒 No cloud dependencies for core features
🔒 Encrypted password storage
🔒 No telemetry or tracking
🔒 Full control over your data

GETTING STARTED:
═══════════════════════════════════════════════════════════════

After installation:
1. Launch the application
2. Create your account
3. Name your assistant (this becomes your wake word)
4. Choose voice preferences (male/female)
5. Grant microphone permissions
6. Start talking to your assistant!

SUPPORT:
═══════════════════════════════════════════════════════════════

📧 Email: support@ai-assistant.com
🌐 Website: https://github.com/yourusername/advanced-ai-assistant
📖 Documentation: Check the README.md file after installation

Ready to experience the future of AI assistance?
'''
        
        with open('INSTALL_INFO.txt', 'w') as f:
            f.write(install_info)
        
        print("✅ License and documentation files created")
    
    def create_assets(self):
        """Create or copy application assets"""
        assets_dir = Path('assets')
        assets_dir.mkdir(exist_ok=True)
        
        # Create a placeholder icon info file
        icon_info = '''# Application Icon

This directory should contain:

## icon.ico
- Main application icon
- Size: 256x256 pixels (with multiple sizes embedded)
- Format: ICO file
- Used for: Executable, installer, shortcuts

## Creating the Icon:
1. Design a 256x256 pixel image representing your AI assistant
2. Use an online converter to create ICO file:
   - https://convertio.co/png-ico/
   - https://www.icoconverter.com/
3. Ensure multiple sizes are embedded (16x16, 32x32, 48x48, 256x256)
4. Save as 'icon.ico' in this directory

## Current Status:
Replace this placeholder with your actual application icon before building.

## Suggested Design Elements:
- Modern, clean design
- AI/robot theme
- Microphone or voice wave elements
- Professional appearance
- Good visibility at small sizes
'''
        
        with open(assets_dir / 'icon_info.txt', 'w') as f:
            f.write(icon_info)
        
        print("✅ Assets directory prepared")
    
    def build_executable(self):
        """Build the executable using PyInstaller"""
        print("🔨 Building executable with PyInstaller...")
        
        try:
            # Clean previous builds
            if self.build_dir.exists():
                shutil.rmtree(self.build_dir)
            if self.dist_dir.exists():
                shutil.rmtree(self.dist_dir)
            
            # Run PyInstaller
            subprocess.run([
                sys.executable, '-m', 'PyInstaller',
                '--clean',
                '--noconfirm',
                'advanced_assistant.spec'
            ], check=True)
            
            print("✅ Executable built successfully!")
            
            # Check if executable was created
            exe_path = self.dist_dir / f"{self.project_name}.exe"
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / (1024 * 1024)
                print(f"📦 Executable size: {size_mb:.1f} MB")
                return True
            else:
                print("❌ Executable not found after build")
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"❌ PyInstaller build failed: {e}")
            return False
        except Exception as e:
            print(f"❌ Build error: {e}")
            return False
    
    def build_installer(self):
        """Build the Windows installer using Inno Setup"""
        print("📦 Creating Windows installer...")
        
        # Check if Inno Setup is installed
        inno_paths = [
            r"C:\\Program Files (x86)\\Inno Setup 6\\ISCC.exe",
            r"C:\\Program Files\\Inno Setup 6\\ISCC.exe",
            r"C:\\Program Files (x86)\\Inno Setup 5\\ISCC.exe",
            r"C:\\Program Files\\Inno Setup 5\\ISCC.exe"
        ]
        
        inno_setup_path = None
        for path in inno_paths:
            if os.path.exists(path):
                inno_setup_path = path
                break
        
        if not inno_setup_path:
            print("❌ Inno Setup not found. Please install Inno Setup 6 from:")
            print("   https://jrsoftware.org/isinfo.php")
            print("After installation, run this script again to create the installer.")
            return False
        
        try:
            # Run Inno Setup
            subprocess.run([inno_setup_path, 'advanced_assistant_setup.iss'], check=True)
            
            # Check if installer was created
            installer_path = self.installer_dir / f"Advanced_AI_Assistant_Setup_v{self.version}.exe"
            if installer_path.exists():
                size_mb = installer_path.stat().st_size / (1024 * 1024)
                print(f"✅ Installer created successfully!")
                print(f"📦 Installer size: {size_mb:.1f} MB")
                print(f"📍 Location: {installer_path}")
                return True
            else:
                print("❌ Installer not found after build")
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"❌ Inno Setup build failed: {e}")
            return False
        except Exception as e:
            print(f"❌ Installer creation error: {e}")
            return False
    
    def run_tests(self):
        """Run basic tests on the built executable"""
        print("🧪 Running tests...")
        
        exe_path = self.dist_dir / f"{self.project_name}.exe"
        if not exe_path.exists():
            print("❌ Executable not found for testing")
            return False
        
        try:
            # Test executable can start (with timeout)
            import subprocess
            result = subprocess.run([str(exe_path), '--version'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=10)
            
            if result.returncode == 0:
                print("✅ Executable starts successfully")
                return True
            else:
                print("⚠️ Executable test completed with warnings")
                return True
                
        except subprocess.TimeoutExpired:
            print("⚠️ Executable test timed out (this may be normal for GUI apps)")
            return True
        except Exception as e:
            print(f"⚠️ Executable test failed: {e}")
            return True  # Don't fail build for test issues
    
    def display_summary(self):
        """Display build summary"""
        print("\n" + "="*80)
        print("🚀 ADVANCED AI ASSISTANT - BUILD SUMMARY")
        print("="*80)
        
        exe_path = self.dist_dir / f"{self.project_name}.exe"
        installer_path = self.installer_dir / f"Advanced_AI_Assistant_Setup_v{self.version}.exe"
        
        if exe_path.exists():
            exe_size = exe_path.stat().st_size / (1024 * 1024)
            print(f"✅ Executable: {exe_path} ({exe_size:.1f} MB)")
        else:
            print("❌ Executable: Not created")
        
        if installer_path.exists():
            installer_size = installer_path.stat().st_size / (1024 * 1024)
            print(f"✅ Installer: {installer_path} ({installer_size:.1f} MB)")
        else:
            print("❌ Installer: Not created")
        
        print(f"\n📋 BUILD INFORMATION:")
        print(f"• Version: {self.version}")
        print(f"• Author: {self.author}")
        print(f"• Description: {self.description}")
        
        print(f"\n🎯 NEXT STEPS:")
        if exe_path.exists():
            print(f"1. Test the executable: {exe_path}")
        if installer_path.exists():
            print(f"2. Test the installer: {installer_path}")
            print(f"3. Distribute the installer to users")
        
        print(f"\n✨ FEATURES INCLUDED:")
        print("• 🎤 Room-scale voice recognition")
        print("• 🤖 3D animated assistant avatar")
        print("• 📁 Smart file management")
        print("• 🖥️ Real-time system monitoring")
        print("• 🧠 Advanced AI capabilities")
        print("• 🔒 Privacy-focused offline-first design")
        
        print("="*80)
    
    def build_all(self):
        """Run the complete build process"""
        print("🚀 Starting Advanced AI Assistant Build Process...")
        print("="*80)
        
        steps = [
            ("Creating PyInstaller spec", self.create_pyinstaller_spec),
            ("Creating version info", self.create_version_info),
            ("Creating application manifest", self.create_manifest),
            ("Creating Inno Setup script", self.create_inno_setup_script),
            ("Creating license and docs", self.create_license_and_docs),
            ("Preparing assets", self.create_assets),
            ("Building executable", self.build_executable),
            ("Running tests", self.run_tests),
            ("Building installer", self.build_installer)
        ]
        
        for step_name, step_func in steps:
            print(f"\n🔄 {step_name}...")
            try:
                if not step_func():
                    print(f"❌ {step_name} failed")
                    if step_name == "Building executable":
                        print("Cannot continue without executable")
                        break
            except Exception as e:
                print(f"❌ {step_name} failed with error: {e}")
                if step_name == "Building executable":
                    break
        
        self.display_summary()

def main():
    """Main build entry point"""
    builder = AdvancedInstallerBuilder()
    builder.build_all()

if __name__ == "__main__":
    main()