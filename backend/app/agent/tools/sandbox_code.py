"""
Sovereign AI - Restricted Python Code Execution Sandbox

Purpose:
    Safely execute small engineering/calculation Python programs.

Security model:
    - Runs code in a separate subprocess.
    - No network access through Python sockets.
    - Blocks dangerous imports.
    - Blocks subprocess / OS command execution.
    - Blocks file access.
    - Blocks eval/exec/compile and similar dynamic execution.
    - AST validates code before execution.
    - Strict execution timeout.
    - Limits source-code and output size.
    - Uses an isolated temporary working directory.
    - Uses a minimal environment.

IMPORTANT:
    This is a restricted execution layer, NOT a full OS-level security
    boundary. For production deployment, use a VM/container/AppContainer/
    Windows Job Object based isolation in addition to these controls.
"""

from __future__ import annotations

import ast
import os
import subprocess
import sys
import tempfile
from typing import Any, Dict, List


# ---------------------------------------------------------------------------
# Limits
# ---------------------------------------------------------------------------

DEFAULT_TIMEOUT_SECONDS = 5.0

MAX_TIMEOUT_SECONDS = 5.0

MAX_CODE_SIZE = 20_000          # characters
MAX_OUTPUT_SIZE = 50_000        # characters


# ---------------------------------------------------------------------------
# Allowed Python functionality
# ---------------------------------------------------------------------------

ALLOWED_IMPORTS = {
    "math",
    "statistics",
    "decimal",
}

ALLOWED_FROM_IMPORTS = {
    "math",
    "statistics",
    "decimal",
}


# ---------------------------------------------------------------------------
# Dangerous Python functions / names
# ---------------------------------------------------------------------------

BLOCKED_CALLS = {
    "eval",
    "exec",
    "compile",
    "__import__",
    "open",
    "input",
    "breakpoint",

    # Dynamic / reflection
    "getattr",
    "setattr",
    "delattr",
    "globals",
    "locals",
    "vars",

    # Object construction / inspection that can aid sandbox escapes
    "help",
    "dir",

    # Process execution
    "system",
    "popen",
    "spawn",
    "fork",
}


BLOCKED_NAMES = {
    "__builtins__",
    "__import__",
    "__loader__",
    "__spec__",
    "__package__",
    "__file__",
    "__cached__",

    # Dunder/reflection
    "__class__",
    "__bases__",
    "__base__",
    "__subclasses__",
    "__mro__",
    "__globals__",
    "__getattribute__",
    "__dict__",

    # Environment / process
    "os",
    "sys",
    "subprocess",
    "socket",
    "shutil",
    "pathlib",
    "ctypes",
    "multiprocessing",
    "threading",

    # Network
    "requests",
    "urllib",
    "http",
    "httpx",
    "ftplib",
    "telnetlib",

    # Serialization / potentially dangerous loaders
    "pickle",
    "marshal",

    # Database / external access
    "sqlite3",
}


# ---------------------------------------------------------------------------
# AST validator
# ---------------------------------------------------------------------------

class SandboxViolation(Exception):
    """Raised when submitted code violates sandbox policy."""


class CodeSecurityValidator(ast.NodeVisitor):
    """
    Static AST validator.

    The goal is not to prove arbitrary Python code mathematically safe.
    Instead, it rejects the common dangerous capabilities before execution.
    """

    def __init__(self) -> None:
        self.violations: List[str] = []

    def violation(self, message: str) -> None:
        self.violations.append(message)

    # ------------------------------------------------------------------
    # Imports
    # ------------------------------------------------------------------

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            module = alias.name.split(".")[0]

            if module not in ALLOWED_IMPORTS:
                self.violation(
                    f"Import blocked: '{alias.name}'"
                )

        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        module = (node.module or "").split(".")[0]

        if module not in ALLOWED_FROM_IMPORTS:
            self.violation(
                f"Import blocked: '{node.module}'"
            )

        self.generic_visit(node)

    # ------------------------------------------------------------------
    # Names
    # ------------------------------------------------------------------

    def visit_Name(self, node: ast.Name) -> None:
        if node.id in BLOCKED_NAMES:
            self.violation(
                f"Restricted name blocked: '{node.id}'"
            )

        if node.id.startswith("__"):
            self.violation(
                f"Dunder name blocked: '{node.id}'"
            )

        self.generic_visit(node)

    # ------------------------------------------------------------------
    # Attribute access
    # ------------------------------------------------------------------

    def visit_Attribute(self, node: ast.Attribute) -> None:
        if node.attr.startswith("__"):
            self.violation(
                f"Dunder attribute blocked: '{node.attr}'"
            )

        if node.attr in {
            "system",
            "popen",
            "spawn",
            "fork",
            "exec",
            "eval",
            "compile",
            "open",
            "getattr",
            "setattr",
            "remove",
            "unlink",
            "rmdir",
            "listdir",
            "walk",
        }:
            self.violation(
                f"Restricted attribute blocked: '{node.attr}'"
            )

        self.generic_visit(node)

    # ------------------------------------------------------------------
    # Function calls
    # ------------------------------------------------------------------

    def visit_Call(self, node: ast.Call) -> None:
        if isinstance(node.func, ast.Name):
            if node.func.id in BLOCKED_CALLS:
                self.violation(
                    f"Restricted function blocked: '{node.func.id}'"
                )

        if isinstance(node.func, ast.Attribute):
            if node.func.attr in BLOCKED_CALLS:
                self.violation(
                    f"Restricted method blocked: '{node.func.attr}'"
                )

        self.generic_visit(node)

    # ------------------------------------------------------------------
    # Lambda / dynamic features
    # ------------------------------------------------------------------

    def visit_Lambda(self, node: ast.Lambda) -> None:
        # Lambdas are not inherently dangerous, but keeping the execution
        # language simple makes auditing easier.
        self.violation("Lambda expressions are not allowed.")

    # ------------------------------------------------------------------
    # Class definitions
    # ------------------------------------------------------------------

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.violation("Class definitions are not allowed.")

    # ------------------------------------------------------------------
    # Function definitions
    # ------------------------------------------------------------------

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        # Small helper functions are useful for calculations.
        # Allow normal functions but reject dunder functions.
        if node.name.startswith("__"):
            self.violation(
                f"Dunder function definition blocked: '{node.name}'"
            )

        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self.violation("Async functions are not allowed.")

    # ------------------------------------------------------------------
    # Dangerous exception machinery / context managers
    # ------------------------------------------------------------------

    def visit_With(self, node: ast.With) -> None:
        self.violation("Context managers are not allowed.")

    def visit_AsyncWith(self, node: ast.AsyncWith) -> None:
        self.violation("Async context managers are not allowed.")

    # ------------------------------------------------------------------
    # Yield / generators
    # ------------------------------------------------------------------

    def visit_Yield(self, node: ast.Yield) -> None:
        self.violation("Yield is not allowed.")

    def visit_YieldFrom(self, node: ast.YieldFrom) -> None:
        self.violation("Yield is not allowed.")

    # ------------------------------------------------------------------
    # Await
    # ------------------------------------------------------------------

    def visit_Await(self, node: ast.Await) -> None:
        self.violation("Await is not allowed.")


# ---------------------------------------------------------------------------
# Code validation
# ---------------------------------------------------------------------------

def validate_code(code: str) -> Dict[str, Any]:
    """
    Parse and statically validate submitted Python code.
    """

    if not isinstance(code, str):
        return {
            "allowed": False,
            "reasons": ["Code must be a string."]
        }

    if not code.strip():
        return {
            "allowed": False,
            "reasons": ["No code was provided."]
        }

    if len(code) > MAX_CODE_SIZE:
        return {
            "allowed": False,
            "reasons": [
                f"Code exceeds maximum size of {MAX_CODE_SIZE} characters."
            ]
        }

    try:
        tree = ast.parse(code, mode="exec")
    except SyntaxError as exc:
        return {
            "allowed": False,
            "reasons": [
                f"Syntax error: {exc}"
            ]
        }

    validator = CodeSecurityValidator()
    validator.visit(tree)

    if validator.violations:
        return {
            "allowed": False,
            "reasons": validator.violations
        }

    return {
        "allowed": True,
        "reasons": []
    }


# ---------------------------------------------------------------------------
# Runtime wrapper
# ---------------------------------------------------------------------------

SANDBOX_WRAPPER = r'''
import socket
import subprocess
import os

# ============================================================
# NETWORK BLOCK
# ============================================================

def blocked_socket(*args, **kwargs):
    raise PermissionError(
        "Air-Gap Violation: network access is disabled."
    )

socket.socket = blocked_socket
socket.create_connection = blocked_socket


# ============================================================
# PROCESS EXECUTION BLOCK
# ============================================================

def blocked_process(*args, **kwargs):
    raise PermissionError(
        "Sandbox Violation: process creation is disabled."
    )

subprocess.Popen = blocked_process
subprocess.run = blocked_process
subprocess.call = blocked_process
subprocess.check_call = blocked_process
subprocess.check_output = blocked_process


# ============================================================
# USER CODE
# ============================================================

{user_code}
'''


# ---------------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------------

def _sandbox_environment() -> Dict[str, str]:
    """
    Create a minimal environment.

    We intentionally do NOT copy the entire parent environment.
    """

    return {
        "PATH": os.environ.get("PATH", ""),
        "PYTHONUNBUFFERED": "1",
        "PYTHONDONTWRITEBYTECODE": "1",
    }


# ---------------------------------------------------------------------------
# Output limiting
# ---------------------------------------------------------------------------

def _limit_output(value: str) -> str:
    if not value:
        return ""

    if len(value) <= MAX_OUTPUT_SIZE:
        return value.strip()

    return (
        value[:MAX_OUTPUT_SIZE]
        + "\n...[OUTPUT TRUNCATED BY SANDBOX]..."
    )


# ---------------------------------------------------------------------------
# Main execution function
# ---------------------------------------------------------------------------

def execute_sandboxed_code(
    code: str,
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
) -> Dict[str, Any]:
    """
    Execute validated Python code inside a restricted subprocess.

    Returns a structured result suitable for the agent workflow.
    """

    # ------------------------------------------------------------
    # Validate timeout
    # ------------------------------------------------------------

    try:
        timeout_seconds = float(timeout_seconds)
    except (TypeError, ValueError):
        timeout_seconds = DEFAULT_TIMEOUT_SECONDS

    timeout_seconds = min(
        max(timeout_seconds, 0.1),
        MAX_TIMEOUT_SECONDS,
    )

    # ------------------------------------------------------------
    # Static security validation
    # ------------------------------------------------------------

    validation = validate_code(code)

    if not validation["allowed"]:
        return {
            "success": False,
            "stdout": "",
            "stderr": "Code rejected by sandbox security policy.",
            "security_status": "BLOCKED",
            "security_reasons": validation["reasons"],
            "exit_code": -2,
            "network_status": "BLOCKED",
            "execution_verified": False,
        }

    # ------------------------------------------------------------
    # Wrap code
    # ------------------------------------------------------------

    wrapped_code = SANDBOX_WRAPPER.format(
        user_code=code
    )

    temp_path = None

    try:
        # --------------------------------------------------------
        # Create isolated temporary directory
        # --------------------------------------------------------

        with tempfile.TemporaryDirectory(
            prefix="sovereign_sandbox_"
        ) as sandbox_dir:

            temp_path = os.path.join(
                sandbox_dir,
                "sandbox_program.py"
            )

            with open(
                temp_path,
                "w",
                encoding="utf-8"
            ) as temp_file:
                temp_file.write(wrapped_code)

            # ----------------------------------------------------
            # Execute in restricted Python mode
            # ----------------------------------------------------

            result = subprocess.run(
                [
                    sys.executable,
                    "-I",
                    temp_path,
                ],
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
                cwd=sandbox_dir,
                env=_sandbox_environment(),
            )

            stdout = _limit_output(result.stdout)
            stderr = _limit_output(result.stderr)

            return {
                "success": result.returncode == 0,
                "stdout": stdout,
                "stderr": stderr,
                "exit_code": result.returncode,

                "security_status": "ALLOWED",
                "security_reasons": [],

                "network_status": "BLOCKED",
                "execution_verified": result.returncode == 0,

                "timeout_seconds": timeout_seconds,
            }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "stdout": "",
            "stderr": (
                f"Execution timed out after "
                f"{timeout_seconds} seconds."
            ),
            "exit_code": -1,

            "security_status": "TIMEOUT",
            "security_reasons": [
                "Execution exceeded sandbox timeout."
            ],

            "network_status": "BLOCKED",
            "execution_verified": False,

            "timeout_seconds": timeout_seconds,
        }

    except Exception as exc:
        return {
            "success": False,
            "stdout": "",
            "stderr": str(exc),
            "exit_code": -1,

            "security_status": "ERROR",
            "security_reasons": [
                "Sandbox execution failed."
            ],

            "network_status": "BLOCKED",
            "execution_verified": False,

            "timeout_seconds": timeout_seconds,
        }


# ---------------------------------------------------------------------------
# Simple local test
# ---------------------------------------------------------------------------

if __name__ == "__main__":

    test_code = """
result = 25 * 4
print(result)
"""

    output = execute_sandboxed_code(test_code)

    print(output)