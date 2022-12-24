import dataclasses
import os
import zipfile


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


# returns the extracted file output path
def decompress(file_name: str, path: str = "") -> str:
    file_path = get_file_path(path, file_name)
    extraction_path = file_path.replace(".zip", "")
    extraction_path = "changesets/extracted-" + extraction_path[extraction_path.rfind("/") + 1:]
    dirname = os.path.dirname(extraction_path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    with zipfile.ZipFile(get_file_path(path, file_name), 'r') as zip_ref:
        zip_ref.extractall(extraction_path)
    return extraction_path


# if path == "" then we expect that file_name is the relative/abs path
# otherwise it should be the file_name only and path is appended to it
def read_file(file_name: str, path: str = "", default: str = None, as_str: bool = True) -> str:
    try:
        with open(get_file_path(path, file_name), mode="r", encoding="utf-8") as file:
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
