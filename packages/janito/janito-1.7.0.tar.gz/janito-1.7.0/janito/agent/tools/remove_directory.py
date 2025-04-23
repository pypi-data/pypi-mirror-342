from janito.agent.tool_base import ToolBase
from janito.agent.tool_registry import register_tool
from janito.agent.tools.tools_utils import pluralize

import shutil
import os
import zipfile


@register_tool(name="remove_directory")
class RemoveDirectoryTool(ToolBase):
    """
    Remove a directory. If recursive=False and directory not empty, raises error.

    Args:
        directory (str): Path to the directory to remove.
        recursive (bool, optional): Remove recursively if True. Defaults to False.
        backup (bool, optional): If True, create a backup (.bak.zip) before removing. Recommend using backup=True only in the first call to avoid redundant backups. Defaults to False.
    Returns:
        str: Status message indicating result. Example:
            - "Directory removed: /path/to/dir"
            - "Error removing directory: <error message>"
    """

    def call(
        self, directory: str, recursive: bool = False, backup: bool = False
    ) -> str:
        self.report_info(
            f"\U0001f5c3\ufe0f  Removing directory: {directory} (recursive={recursive})"
        )
        try:
            if backup and os.path.exists(directory) and os.path.isdir(directory):
                backup_zip = directory.rstrip("/\\") + ".bak.zip"
                with zipfile.ZipFile(backup_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
                    for root, dirs, files in os.walk(directory):
                        for file in files:
                            abs_path = os.path.join(root, file)
                            rel_path = os.path.relpath(
                                abs_path, os.path.dirname(directory)
                            )
                            zipf.write(abs_path, rel_path)
            if recursive:
                shutil.rmtree(directory)
            else:
                os.rmdir(directory)
            self.report_success(f"\u2705 1 {pluralize('directory', 1)}")
            return f"Directory removed: {directory}"
        except Exception as e:
            self.report_error(f" \u274c Error removing directory: {e}")
            return f"Error removing directory: {e}"
