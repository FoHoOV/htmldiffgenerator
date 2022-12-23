import argparse

from diff_generator.difflib_utils.difflib_html_generator import generate_html_diff_folders
from diff_generator.file_utils.utils import decompress


def generate_diffs():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jc", type=bool, default=True, help="Produce a context format diff (default)")
    parser.add_argument("--cl", default=5, help="How many context lines are included")
    parser.add_argument("--ex",
                        type=list[str],
                        default=[".aspx", ".ascx", ".html", "htm", ".py", ".vb", ".cs", ".sln", ".vbproj", ".csproj"])
    parser.add_argument("--c1",
                        type=str,
                        required=True,
                        help="first downloaded changeset zip archive path")
    parser.add_argument("--c2",
                        type=str,
                        required=True,
                        help="second downloaded changeset zip archive path")
    # parser.add_argument("-s", action="store_true", help="you azure devops session id after login")
    # parser.add_argument("-c1", action="store_true", help="change set 1 zip download url")
    # parser.add_argument("-c2", action="store_true", help="change set 2 zip download url")
    options = parser.parse_args()

    # path_c1 = download_file(options.c1)
    # path_c2 = download_file(options.c2)
    path_c1 = decompress(options.c1)
    path_c2 = decompress(options.c2)

    generate_html_diff_folders(path_c1, path_c2, options.ex, options.jc, options.cl)
