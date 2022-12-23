# htmldiffgenerator

generates an html diff like winmerge->generate patch/diff for two .zip files that are commit x and commit y

<h1>
    how to use:
</h1>

<code>
    python diff_generator.py --c1 "path_to_file1.zip" --c2 "path_to_file2.zip"\
</code>

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

* --output arg might result into FileNotFound exceptions and that's because of the antivirus program. If that's the case just don't use this arg or 
allow this program in the ransomware protection exceptions.
* I know that this code is NOT well structured. It is written in a very short time just to get my job done faster.