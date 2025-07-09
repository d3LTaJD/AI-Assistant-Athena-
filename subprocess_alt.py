"""
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
