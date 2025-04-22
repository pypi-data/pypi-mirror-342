import platform
import os

from subprocess import run
from typing import Type

from langchain.tools import BaseTool
from pydantic import BaseModel, Field

import tempfile


KILL_TIMEOUT = 30  # seconds


class PythonInput(BaseModel):
    """Commands for the Python Interpreter tool."""

    script: str = Field(
        description=f"Python script to run with ipython on this {platform.system()} system. Stdout and stderr are returned but truncated to 1024 characters. If you need any values from the script, make sure you print them at the end. The command will be killed after {KILL_TIMEOUT} seconds."
    )
    reason: str = Field(
        description="One-sentence reason (up to 140 chars) for running the command."
    )


class PythonInterpreter(BaseTool):
    name: str = "PythonInterpter"
    description: str = "Runs a python script"
    args_schema: Type[BaseModel] = PythonInput

    def _run(self, script: str, reason: str) -> str:
        print(f"## {reason}")
        print(f"{script}")
        # put script in a temporary directory and run it
        try:
            with tempfile.TemporaryDirectory() as tmp:
                script_path = os.path.join(tmp, "script.py")
                with open(script_path, "w") as script_fd:
                    script_fd.write(script)
                with open(script_path, "r") as script_fd:
                    process = run(
                        ["/usr/bin/timeout", "-s", "9", f"{KILL_TIMEOUT}", "ipython", "--no-banner"],
                        capture_output=True,
                        stdin=script_fd,
                    )
        except Exception as exn:
            print(f"Error running script: {exn}")
            raise

        stdout = process.stdout.decode("utf-8")
        stderr = process.stderr.decode("utf-8")
        trunc_limit = 1024
        stdout_truncated = len(stdout) > trunc_limit
        stderr_truncated = len(stderr) > trunc_limit
        # timedout when it got killed by 9
        timeout = process.returncode == 137
        result = {
            "stdout": stdout[:trunc_limit],
            "stdout_truncated": stdout_truncated,
            "stderr": stderr[:trunc_limit],
            "stderr_truncated": stderr_truncated,
            "returncode": process.returncode,
            "timeout": timeout,
        }
        print(result)
        if self.verbose:
            print(result)
        else:
            print(result["stdout"])
            print(result["stderr"])
        return str(result)