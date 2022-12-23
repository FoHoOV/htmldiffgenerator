import requests
from werkzeug.utils import secure_filename

from diff_generator.file_utils.utils import decompress, get_file_path


# returns the output file path
def download_file(url: str) -> str:
    file_path = "./changesets/" + secure_filename(url) + ".zip"
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    decompress(file_path)
    return get_file_path("", file_path)
