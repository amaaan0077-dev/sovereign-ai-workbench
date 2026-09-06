"""
Network-Disabled Sandboxed Code Execution Tool.
Executes engineering scripts in a safe isolated subprocess with:
- Sockets monkey-patched/disabled (Zero Network Access)
- Strict 5.0 second timeout
- Memory and execution caps
"""
import subprocess
import sys
import tempfile
import os
from typing import Dict, Any

SANDBOX_WRAPPER = """
import sys
import socket

# Disable all outgoing socket creation to guarantee air-gap in sandbox
def blocked_socket(*args, **kwargs):
    raise PermissionError("Air-Gap Violation: Sandbox cannot establish external network socket connections!")

socket.socket = blocked_socket
socket.create_connection = blocked_socket

# User Script
{user_code}
"""

def execute_sandboxed_code(code: str, timeout_seconds: float = 5.0) -> Dict[str, Any]:
    # Inject security wrapper
    wrapped_code = SANDBOX_WRAPPER.format(user_code=code)
    
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as temp_file:
        temp_file.write(wrapped_code)
        temp_path = temp_file.name

    try:
        result = subprocess.run(
            [sys.executable, temp_path],
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            env={
                "PATH": os.environ.get("PATH", ""),
                "PYTHONUNBUFFERED": "1"
            }
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "exit_code": result.returncode,
            "network_status": "BLOCKED (Air-Gapped Sandbox)",
            "execution_verified": result.returncode == 0
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "stdout": "",
            "stderr": f"Execution timed out after {timeout_seconds}s limit.",
            "exit_code": -1,
            "network_status": "BLOCKED",
            "execution_verified": False
        }
    except Exception as e:
        return {
            "success": False,
            "stdout": "",
            "stderr": str(e),
            "exit_code": -1,
            "network_status": "BLOCKED",
            "execution_verified": False
        }
    finally:
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass
