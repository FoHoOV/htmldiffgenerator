import argparse

from diff_generator.difflib.difflib_html_generator import generate_html_diff_folders
from diff_generator.web_utlils.downloader import download_file


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-jc", action="store_true", default=True, help="Produce a context format diff (default)")
    parser.add_argument("-cl", action="store_true", default=5, help="How many context lines are included")
    parser.add_argument("-s", action="store_true", help="you azure devops session id after login")
    parser.add_argument("-c1", action="store_true", help="change set 1 zip download url")
    parser.add_argument("-c2", action="store_true", help="change set 2 zip download url")
    parser.add_argument("root_dir")
    options = parser.parse_args()

    path_c1 = download_file(options.c1)
    path_c2 = download_file(options.c2)

    generate_html_diff_folders(path_c1, path_c2, options.jc, options.cl)


if __name__ == "__main__":
    main()
