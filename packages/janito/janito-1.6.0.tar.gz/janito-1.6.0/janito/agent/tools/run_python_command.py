import subprocess
import tempfile
import sys
from janito.agent.tool_base import ToolBase
from janito.agent.tool_registry import register_tool


@register_tool(name="run_python_command")
class RunPythonCommandTool(ToolBase):
    """
    Tool to execute Python code in a subprocess and capture output.

    Args:
        code (str): The Python code to execute.
        timeout (int, optional): Timeout in seconds for the command. Defaults to 60.
        require_confirmation (bool, optional): If True, require user confirmation before running. Defaults to False.
        interactive (bool, optional): If True, warns that the command may require user interaction. Defaults to False.
    Returns:
        str: File paths and line counts for stdout and stderr, or direct output if small enough.
    """

    def call(
        self,
        code: str,
        timeout: int = 60,
        require_confirmation: bool = False,
        interactive: bool = False,
    ) -> str:
        if not code.strip():
            self.report_warning("⚠️ Warning: Empty code provided. Operation skipped.")
            return "Warning: Empty code provided. Operation skipped."
        self.report_info(f"🐍 Running Python code:\n{code}\n")
        if interactive:
            self.report_info(
                "⚠️  Warning: This code might be interactive, require user input, and might hang."
            )
        sys.stdout.flush()
        if require_confirmation:
            confirmed = self.confirm_action("Do you want to execute this Python code?")
            if not confirmed:
                self.report_warning("Execution cancelled by user.")
                return "Execution cancelled by user."
        try:
            with (
                tempfile.NamedTemporaryFile(
                    mode="w+",
                    suffix=".py",
                    prefix="run_python_",
                    delete=False,
                    encoding="utf-8",
                ) as code_file,
                tempfile.NamedTemporaryFile(
                    mode="w+",
                    prefix="run_python_stdout_",
                    delete=False,
                    encoding="utf-8",
                ) as stdout_file,
                tempfile.NamedTemporaryFile(
                    mode="w+",
                    prefix="run_python_stderr_",
                    delete=False,
                    encoding="utf-8",
                ) as stderr_file,
            ):
                code_file.write(code)
                code_file.flush()
                process = subprocess.Popen(
                    [sys.executable, code_file.name],
                    stdout=stdout_file,
                    stderr=stderr_file,
                    text=True,
                )
                try:
                    return_code = process.wait(timeout=timeout)
                except subprocess.TimeoutExpired:
                    process.kill()
                    self.report_error(f" ❌ Timed out after {timeout} seconds.")
                    return f"Code timed out after {timeout} seconds."
                # Print live output to user
                stdout_file.flush()
                stderr_file.flush()
                with open(
                    stdout_file.name, "r", encoding="utf-8", errors="replace"
                ) as out_f:
                    out_f.seek(0)
                    for line in out_f:
                        self.report_stdout(line)
                with open(
                    stderr_file.name, "r", encoding="utf-8", errors="replace"
                ) as err_f:
                    err_f.seek(0)
                    for line in err_f:
                        self.report_stderr(line)
                # Count lines
                with open(
                    stdout_file.name, "r", encoding="utf-8", errors="replace"
                ) as out_f:
                    stdout_lines = sum(1 for _ in out_f)
                with open(
                    stderr_file.name, "r", encoding="utf-8", errors="replace"
                ) as err_f:
                    stderr_lines = sum(1 for _ in err_f)
                self.report_success(f" ✅ return code {return_code}")
                warning_msg = ""
                if interactive:
                    warning_msg = "⚠️  Warning: This code might be interactive, require user input, and might hang.\n"
                # Read output contents
                with open(
                    stdout_file.name, "r", encoding="utf-8", errors="replace"
                ) as out_f:
                    stdout_content = out_f.read()
                with open(
                    stderr_file.name, "r", encoding="utf-8", errors="replace"
                ) as err_f:
                    stderr_content = err_f.read()
                # Thresholds
                max_lines = 100
                if stdout_lines <= max_lines and stderr_lines <= max_lines:
                    result = (
                        warning_msg
                        + f"Return code: {return_code}\n--- STDOUT ---\n{stdout_content}"
                    )
                    if stderr_content.strip():
                        result += f"\n--- STDERR ---\n{stderr_content}"
                    return result
                else:
                    result = (
                        warning_msg
                        + f"stdout_file: {stdout_file.name} (lines: {stdout_lines})\n"
                    )
                    if stderr_lines > 0 and stderr_content.strip():
                        result += (
                            f"stderr_file: {stderr_file.name} (lines: {stderr_lines})\n"
                        )
                    result += f"returncode: {return_code}\nUse the get_lines tool to inspect the contents of these files when needed."
                    return result
        except Exception as e:
            self.report_error(f" ❌ Error: {e}")
            return f"Error running code: {e}"
