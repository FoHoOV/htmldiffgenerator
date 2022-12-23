import os, difflib
from datetime import datetime, timezone

from diff_generator.file_utils.utils import read_file


def file_mtime(path: str) -> str:
    t = datetime.fromtimestamp(os.stat(path).st_mtime,
                               timezone.utc)
    return t.astimezone().isoformat()


def generate_html_diff_folders(folder1_path: str, folder2_path: str, just_context: bool = True, context_lines: int = 5):
    pass


def generate_html_diff_files(file1_path: str, file2_path: str, just_context: bool = True, context_lines: int = 5) -> str:
    diff = difflib.HtmlDiff(wrapcolumn=95).make_file(file_mtime(file1_path),
                                                     file_mtime(file2_path),
                                                     read_file(file1_path),
                                                     read_file(file2_path),
                                                     context=just_context,
                                                     numlines=context_lines)
    return diff
