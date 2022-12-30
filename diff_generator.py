import argparse

from file_manager_utils import decompress
from html_patch_generator import generate_html_diff_folders


def generate_diffs():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jc", type=bool, default=True, help="Produce a context format diff (default = True)")
    parser.add_argument("--cl", default=5, help="How many context lines you want to be included (default = 5)")
    parser.add_argument("--ex",
                        type=list[str],
                        help='extensions that we search for(use "*" for all extensions the default) default = [".aspx", ".ascx", ".html", "htm", ".py", ".vb", ".cs", ".sln", ".vbproj", ".csproj"]',
                        default=[".aspx", ".ascx", ".html", "htm", ".py", ".vb", ".cs", ".sln", ".vbproj", ".csproj"])
    parser.add_argument("--eex",
                        type=list[str],
                        help='extensions that we dont search for (default = [".designer.vb", ".designer.cs", ".dll", ".pdb"])',
                        default=[".designer.vb", ".designer.cs", ".dll", ".pdb"])
    parser.add_argument("--c1",
                        type=str,
                        required=True,
                        help="first downloaded changeset/commit zip archive path")
    parser.add_argument("--c2",
                        type=str,
                        required=True,
                        help="second downloaded changeset/commit zip archive path")

    parser.add_argument("--ddc1",
                        action=argparse.BooleanOptionalAction,
                        default=False,
                        help="dont decompress changeset1/commit1 (use this if it's not a zip file)")

    parser.add_argument("--ddc2",
                        action=argparse.BooleanOptionalAction,
                        default=False,
                        help="dont decompress changeset2/commit2 (use this if it's not a zip file)")

    parser.add_argument("--ww",
                        action=argparse.BooleanOptionalAction,
                        default=True,
                        help="use word wrap (wraps the generated diff to 90 characters per line)")

    parser.add_argument("--output",
                        default="./output",
                        help="output path (default= ./output)")

    parser.add_argument("--git",
                        action=argparse.BooleanOptionalAction,
                        default=False,
                        help="help if the zip is download from git use this flag(we default to azure file structure)")

    options = parser.parse_args()

    path_c1 = decompress(options.c1, options.git) if not options.ddc1 else options.c1
    path_c2 = decompress(options.c2, options.git) if not options.ddc2 else options.c2

    if path_c1.endswith(".zip"):
        raise Exception("c1 ended with '.zip' when dont compress for c1 flag was turned on")

    if path_c2.endswith(".zip"):
        raise Exception("c2 ended with '.zip' when dont compress for c2 flag was turned on")

    generate_html_diff_folders(path_c1, path_c2, options.ex, options.eex, options.output, options.jc, options.cl,
                               options.ww)


if __name__ == "__main__":
    generate_diffs()
