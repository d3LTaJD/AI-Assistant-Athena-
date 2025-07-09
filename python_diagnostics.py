#!/usr/bin/env python3
"""
Python Diagnostics and Workaround Script
Specifically designed to handle _signal module issues in WebContainer environments
"""

import sys
import os

def check_python_environment():
    """Check the current Python environment and identify issues"""
    print("🔍 Python Environment Diagnostics")
    print("=" * 50)
    
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print(f"Platform: {sys.platform}")
    
    # Check if we're in a WebContainer environment
    if '/home/project' in os.getcwd():
        print("📍 Detected: WebContainer environment")
        return True
    
    return False

def test_core_modules():
    """Test core Python modules availability"""
    print("\n🧪 Testing Core Modules:")
    
    # Test modules that don't depend on _signal
    safe_modules = [
        'os', 'sys', 'json', 'time', 'datetime', 
        'random', 'math', 're', 'collections'
    ]
    
    working_modules = []
    
    for module in safe_modules:
        try:
            __import__(module)
            print(f"✅ {module} - OK")
            working_modules.append(module)
        except ImportError as e:
            print(f"❌ {module} - FAILED: {e}")
    
    # Test problematic modules
    problematic_modules = ['signal', 'subprocess', 'threading']
    
    print("\n🚨 Testing Problematic Modules:")
    for module in problematic_modules:
        try:
            __import__(module)
            print(f"✅ {module} - OK")
        except ImportError as e:
            print(f"❌ {module} - FAILED: {e}")
    
    return working_modules

def create_signal_workaround():
    """Create a minimal signal module workaround"""
    print("\n🔧 Creating signal module workaround...")
    
    workaround_code = '''"""
Minimal signal module workaround for WebContainer environments
This provides basic signal functionality without requiring _signal
"""

# Signal constants (most common ones)
SIGINT = 2
SIGTERM = 15
SIGKILL = 9
SIGHUP = 1
SIGQUIT = 3

class SignalHandler:
    def __init__(self):
        self.handlers = {}
    
    def signal(self, signum, handler):
        """Mock signal handler registration"""
        self.handlers[signum] = handler
        return None
    
    def alarm(self, time):
        """Mock alarm function"""
        return 0

# Create global instance
_handler = SignalHandler()
signal = _handler.signal
alarm = _handler.alarm

# Default handler
SIG_DFL = 0
SIG_IGN = 1

def default_int_handler(signum, frame):
    """Default interrupt handler"""
    raise KeyboardInterrupt()
'''
    
    try:
        with open('signal_workaround.py', 'w') as f:
            f.write(workaround_code)
        print("✅ Created signal_workaround.py")
        return True
    except Exception as e:
        print(f"❌ Failed to create workaround: {e}")
        return False

def create_subprocess_alternative():
    """Create an alternative to subprocess that doesn't use signal"""
    print("\n🔧 Creating subprocess alternative...")
    
    subprocess_alt_code = '''"""
Alternative subprocess implementation for environments without _signal
Uses os.system and basic process management
"""

import os
import sys

class CompletedProcess:
    def __init__(self, args, returncode, stdout=None, stderr=None):
        self.args = args
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr

class CalledProcessError(Exception):
    def __init__(self, returncode, cmd, output=None, stderr=None):
        self.returncode = returncode
        self.cmd = cmd
        self.output = output
        self.stderr = stderr
        super().__init__(f"Command '{cmd}' returned non-zero exit status {returncode}")

def run(args, shell=False, check=False, capture_output=False, text=True):
    """Simple subprocess.run alternative"""
    if isinstance(args, list):
        cmd = ' '.join(args) if shell else args[0] + ' ' + ' '.join(args[1:])
    else:
        cmd = args
    
    print(f"🔄 Running: {cmd}")
    
    if capture_output:
        # For WebContainer, we'll use a simple approach
        returncode = os.system(cmd + " > /tmp/cmd_output.txt 2> /tmp/cmd_error.txt")
        
        try:
            with open('/tmp/cmd_output.txt', 'r') as f:
                stdout = f.read()
        except:
            stdout = ""
        
        try:
            with open('/tmp/cmd_error.txt', 'r') as f:
                stderr = f.read()
        except:
            stderr = ""
    else:
        returncode = os.system(cmd)
        stdout = None
        stderr = None
    
    # Convert os.system return code
    returncode = returncode >> 8 if returncode > 255 else returncode
    
    if check and returncode != 0:
        raise CalledProcessError(returncode, cmd, stdout, stderr)
    
    return CompletedProcess(args, returncode, stdout, stderr)

def check_call(args, shell=False):
    """Simple subprocess.check_call alternative"""
    result = run(args, shell=shell, check=True)
    return result.returncode

def call(args, shell=False):
    """Simple subprocess.call alternative"""
    result = run(args, shell=shell, check=False)
    return result.returncode

# Constants
PIPE = -1
STDOUT = -2
DEVNULL = -3
'''
    
    try:
        with open('subprocess_alt.py', 'w') as f:
            f.write(subprocess_alt_code)
        print("✅ Created subprocess_alt.py")
        return True
    except Exception as e:
        print(f"❌ Failed to create subprocess alternative: {e}")
        return False

def create_fixed_environment_script():
    """Create a fixed version of the environment script"""
    print("\n🔧 Creating fixed environment script...")
    
    fixed_script = '''#!/usr/bin/env python3
"""
Fixed Environment Setup Script for WebContainer
Works without _signal module dependency
"""

import sys
import os
import platform

# Use our workarounds
try:
    import subprocess_alt as subprocess
except ImportError:
    print("❌ subprocess_alt not found. Please run python_diagnostics.py first.")
    sys.exit(1)

def check_python_installation():
    """Check if Python installation is working properly"""
    print("🔍 Diagnosing Python installation...")
    
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print(f"Current directory: {os.getcwd()}")
    
    # Test core modules that should work
    core_modules = ['os', 'sys', 'platform', 'json', 'time']
    missing_modules = []
    
    for module in core_modules:
        try:
            __import__(module)
            print(f"✅ {module} - OK")
        except ImportError as e:
            print(f"❌ {module} - MISSING: {e}")
            missing_modules.append(module)
    
    return missing_modules

def install_requirements():
    """Install requirements using our subprocess alternative"""
    print("\\n📦 Installing requirements...")
    
    requirements_files = [
        'requirements.txt',
        'requirements_enhanced.txt'
    ]
    
    for req_file in requirements_files:
        if os.path.exists(req_file):
            print(f"Installing from {req_file}...")
            try:
                result = subprocess.run([
                    sys.executable, '-m', 'pip', 'install', '-r', req_file
                ], check=False)
                
                if result.returncode == 0:
                    print(f"✅ Successfully installed from {req_file}")
                else:
                    print(f"⚠️ Some packages from {req_file} may have failed to install")
            except Exception as e:
                print(f"❌ Error installing from {req_file}: {e}")
        else:
            print(f"📄 {req_file} not found, skipping...")

def run_setup():
    """Run the main setup process"""
    print("\\n🚀 Running setup process...")
    
    setup_files = [
        'enhanced_setup.py',
        'setup.py'
    ]
    
    for setup_file in setup_files:
        if os.path.exists(setup_file):
            print(f"\\nRunning {setup_file}...")
            try:
                result = subprocess.run([sys.executable, setup_file], check=False)
                if result.returncode == 0:
                    print(f"✅ {setup_file} completed successfully")
                    return True
                else:
                    print(f"⚠️ {setup_file} completed with warnings")
            except Exception as e:
                print(f"❌ Error running {setup_file}: {e}")
    
    return False

def main():
    """Main function"""
    print("🚀 Athena AI Assistant - Fixed Environment Setup")
    print("=" * 60)
    
    # Check Python installation
    missing_modules = check_python_installation()
    
    if missing_modules:
        print(f"\\n⚠️ Some modules are missing: {missing_modules}")
        print("This is expected in WebContainer environments.")
    
    # Install requirements
    install_requirements()
    
    # Run setup
    if run_setup():
        print("\\n✅ Setup completed successfully!")
        print("\\n📋 You can now try running:")
        print("   python enhanced_athena.py")
        print("   or")
        print("   python Athena.py")
    else:
        print("\\n⚠️ Setup completed with some issues.")
        print("You may still be able to run the application.")

if __name__ == "__main__":
    main()
'''
    
    try:
        with open('fixed_environment_setup.py', 'w') as f:
            f.write(fixed_script)
        print("✅ Created fixed_environment_setup.py")
        return True
    except Exception as e:
        print(f"❌ Failed to create fixed setup script: {e}")
        return False

def main():
    """Main diagnostic and fix function"""
    print("🚀 Python _signal Module Fix Tool")
    print("=" * 50)
    
    # Check environment
    is_webcontainer = check_python_environment()
    
    # Test modules
    working_modules = test_core_modules()
    
    if len(working_modules) < 5:
        print("\n❌ Critical: Too many core modules are missing")
        print("This indicates a severely corrupted Python installation")
        return False
    
    # Create workarounds
    print("\n🔧 Creating workarounds for WebContainer environment...")
    
    success = True
    success &= create_signal_workaround()
    success &= create_subprocess_alternative()
    success &= create_fixed_environment_script()
    
    if success:
        print("\n✅ Workarounds created successfully!")
        print("\n📋 Next steps:")
        print("1. Run: python fixed_environment_setup.py")
        print("2. This will install dependencies and run setup")
        print("3. Then try running your main application")
        
        print("\n💡 Note: These workarounds are specifically designed for")
        print("   WebContainer environments where _signal may not be available.")
    else:
        print("\n❌ Failed to create some workarounds")
        print("You may need to manually address the Python installation issues")
    
    return success

if __name__ == "__main__":
    main()