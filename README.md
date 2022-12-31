# htmldiffgenerator

generates an html diff like winmerge->generate patch/diff for two .zip/foldera that are commit x and commit y

<h1>
    how to use:
</h1>
<code>python diff_generator.py --c1 "path_to_file1.zip" --c2 "path_to_file2.zip"</code>

c1 is considered the old commit and c2 is considered the new commit

<h1>
    how to install
</h1>

<ol>
        <li>
            download the source code
        </li>
        <li>
            install the requirements.txt
        </li>
        <li>
            run diff_generator -h for available commands
        </li>
</ol>
which will generate the output to '[this-project-root]/output'.

* <h3>use the --git flag if you are downloading zip files from github not azure (I default to azure). This flag is used to tell this program to
  move every thing from the root of the extracted folder one directory up, since github also inclues the commit hash in the extracted folder which
  marks everything as different.
  </h3>
* --output arg might result into FileNotFound exceptions and that's because of the antivirus program. If that's the case just don't use this arg
  or allow this program in the ransomware protection exceptions.
* I know that this code is NOT well structured. It is written in a very short time just to get my job done faster.

<h3>
  please consider to leave a star if you found this util helpful >_<
</h3>
