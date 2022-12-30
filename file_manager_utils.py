import dataclasses
import os
import shutil
import zipfile
from datetime import datetime

from werkzeug.utils import secure_filename


def get_file_path(path: str, file_name: str, absolute: bool = False) -> str:
    file_path = file_name
    if path != "":
        file_path = path + "/" + file_name
    file_path = file_path.replace("\\", "/")
    if absolute:
        return os.path.abspath(file_path)
    return file_path


def write_to_file(content: str, file_name: str, path: str = ""):
    file_path = get_file_path(path, file_name)
    dirname = os.path.dirname(file_path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    print(f"writing to: {file_path}")
    with open(file_path, mode="w", encoding="utf-8") as file:
        file.write(content)


def get_changeset_names(folder1_path: str, folder2_path: str) -> str:
    folder1_path = folder1_path.replace("./", "").replace("extracted-", "")
    folder2_path = folder2_path.replace("./", "").replace("extracted-", "")
    return folder1_path[folder1_path.rfind("/") + 1:] + "--" + folder2_path[folder2_path.find("/") + 1:]


def generate_output_path(folder1_path: str, folder2_path: str) -> str:
    return secure_filename(get_changeset_names(folder1_path, folder2_path) + "--" + generate_timestamp())


def generate_timestamp() -> str:
    return datetime.utcnow().strftime('%Y-%m-%d--%H_%M_%S.%F')[:-3]


def move_folder_contents(source_path: str, dest_path: str):
    file_names = os.listdir(source_path)
    for file_name in file_names:
        shutil.move(os.path.join(source_path, file_name), dest_path)
    try:
        os.rmdir(source_path)
    except(FileNotFoundError, OSError) as e:
        raise f"We tried to move all contents from {source_path} one directory up (might be due to using the --git flag)" \
              f"but this folder still had some contents after the move. If this error exists just extract the files yourself" \
              f"and use the --ddc1 and --ddc2 flags"


# returns the extracted file output path
# if is_git flag is set then we move all files within the extracted folder, one folder up since
# git includes the commit hash as well, which makes this program think all files are different
def decompress(file_name: str, is_git: bool, path: str = "") -> str:
    print(f"extracting: {file_name}")
    file_path = get_file_path(path, file_name)
    extraction_path = file_path.replace(".zip", "")
    extraction_path = "changesets/extracted-" + extraction_path[extraction_path.rfind("/") + 1:] + "--" + generate_timestamp()
    dirname = os.path.dirname(extraction_path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    with zipfile.ZipFile(get_file_path(path, file_name), 'r') as zip_ref:
        zip_ref.extractall(extraction_path)
        if is_git:
            move_folder_contents(os.path.join(extraction_path, zip_ref.filelist[0].filename), extraction_path)
    print(f"extracted to: {extraction_path}")
    return extraction_path


# if path == "" then we expect that file_name is the relative/abs path
# otherwise it should be the file_name only and path is appended to it
def read_file(file_name: str, path: str = "", default: str = None, as_str: bool = True) -> str | list[str]:
    file_path = get_file_path(path, file_name)
    try:
        return read_file_with_unicode(file_path, "utf-8", default, as_str)
    except UnicodeDecodeError as e1:
        try:
            return read_file_with_unicode(file_path, "utf-16-be", default, as_str)
        except UnicodeDecodeError as e2:
            return read_file_with_unicode(file_path, "utf-16-le", default, as_str)


def read_file_with_unicode(file_path: str, encoding: str, default: str = None, as_str: bool = True) -> str | list[str]:
    try:
        with open(file_path, mode="r", encoding=encoding) as file:
            return str.join("\n", file.readlines()) if as_str else file.readlines()
    except FileNotFoundError as e:
        if default is not None:
            return default
        raise e


@dataclasses.dataclass
class Result:
    path: str
    content: str


def _file_has_extension(file_name: str, included_extensions: list[str], excluded_extensions: list[str]) -> bool:
    if len(included_extensions) == 0:
        return True
    for extension in included_extensions:
        if extension == "*" or file_name.endswith(extension):
            for excluded_extension in excluded_extensions:
                if file_name.endswith(excluded_extension):
                    return False
            return True
    return False


def read_all_files_recursive(root_path: str, included_extension: list[str], excluded_extensions: list[str]) -> list[
    Result]:
    results = []
    for current_dir_path, current_subdirs, current_files in os.walk(root_path):
        for file_name in current_files:
            if _file_has_extension(file_name, included_extension, excluded_extensions):
                file_path = str(os.path.join(current_dir_path, file_name))
                results.append(Result(file_path, read_file(file_path)))

    return results


def get_all_file_paths_recursive(root_path: str, included_extension: list[str], excluded_extensions: list[str]) -> str:
    for current_dir_path, current_subdirs, current_files in os.walk(root_path):
        for file_name in current_files:
            if _file_has_extension(file_name, included_extension, excluded_extensions):
                file_path = str(os.path.join(current_dir_path, file_name))
                yield file_path
