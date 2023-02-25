# this will download the changesets from a source control and extract the downloaded zip

import os

import requests
from werkzeug.utils import secure_filename

from file_manager_utils import decompress, get_file_path


# returns the output file path
def download_file(url: str, session: str) -> str:
    file_path = "./changesets/" + secure_filename(url) + ".zip"
    file_path = get_file_path("", file_path, absolute=True)
    dirname = os.path.dirname(file_path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    with requests.get(url, stream=True, ) as r:
        r.raise_for_status()
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    # decompress(file_path,Fakse)
    return get_file_path("", file_path)
