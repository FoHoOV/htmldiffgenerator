import argparse
import json

import file_manager_utils
from file_manager_utils import decompress
from html_patch_generator import generate_html_diff_folders


def generate_diffs():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jc", type=bool, default=True, help="Produce a context format diff (default = True)")
    parser.add_argument("--cl", default=5, help="How many context lines you want to be included (default = 5)")
    parser.add_argument("--ex",
                        nargs='*',
                        help='extensions that we search for(use "*" for all extensions) default = [".aspx", ".ascx", ".html", "htm", ".py", ".vb", ".cs", ".sln", ".vbproj", ".csproj",".config"]',
                        default=[".aspx", ".ascx", ".html", "htm", ".py", ".vb", ".cs", ".sln", ".vbproj", ".csproj",
                                 ".config", ".css", ".ts", ".js", ".xml"])
    parser.add_argument("--eex",
                        nargs='*',
                        help='extensions that we dont search for (default = [".designer.vb", ".designer.cs", ".dll", ".pdb"])',
                        default=[".designer.vb", ".designer.cs", ".dll", ".pdb", ".pdf", ".xlsx", ".xls", "doc",
                                 "docx"])
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
                        help="use word wrap (wraps the generated diff to 90 characters per line for each side)")

    parser.add_argument("--output",
                        default="./output",
                        help="output path (default= ./output)")

    parser.add_argument("--git",
                        action=argparse.BooleanOptionalAction,
                        default=False,
                        help="enable this flag if the downloaded zips come from github(we default to azure file structure)")

    parser.add_argument("--ignored-paths",
                        default=[],
                        nargs='*',
                        help="path to a file that contains a list of paths we try to match with regex inorder to ignore that path")

    options = parser.parse_args()

    if options.c1.endswith(".zip") and options.ddc1:
        raise Exception("c1 ended with '.zip' when --ddc1 flag was turned on")
    elif not options.c1.endswith(".zip") and not options.ddc1:
        raise Exception("c1 is not a zip file when --ddc1 flag was not used")

    if options.c2.endswith(".zip") and options.ddc2:
        raise Exception("c2 ended with '.zip' when --ddc2 flag was turned on")
    elif not options.c2.endswith(".zip") and not options.ddc2:
        raise Exception("c2 is not a zip file when --ddc2 flag was not used")

    path_c1 = decompress(options.c1, options.git) if not options.ddc1 else options.c1
    path_c2 = decompress(options.c2, options.git) if not options.ddc2 else options.c2

    generate_html_diff_folders(path_c1,
                               path_c2,
                               options.ignored_paths,
                               options.ex,
                               options.eex,
                               options.output,
                               options.jc,
                               options.cl,
                               options.ww)


if __name__ == "__main__":
    generate_diffs()
