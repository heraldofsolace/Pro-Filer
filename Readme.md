# Pro-Filer
A python script to analyse your file usage.

## Feautres:
Analyzes the current directory, and creates a web page with the following informations - 

* Bar chart with file name and size.
* Bar chart according to extension names with corresponding size
and number of files.
* Bar chart according to file type with corresponding size
and number of files.
* Top 20 files according to size.
* Top 20 extensions according to size and count.
* Top 20 types according to size and count.
* File list.
* Folder list based on size.
* Folder list based on file count.
* Top 20 folders based on size and file count.

## Samples

Visit the [Sample output page](https://github.com/BrokenMutant/Pro-Filer/blob/master/out/output2017-12-11%2018:49:05.787048.html)

## Prerequistics
* Python 3
* [Plotly module](https://plot.ly/python/)
* [PEng](https://github.com/BrokenMutant/PEng)

## Usage
First clone the directory, and cd into it.

Now run - 
```commandline
python profiler.py [options]
```
## Options

Currently three options are allowed - 
* **-s** The size is calculated in bytes. The size is divided by whatever
is passed to this option. Default is 1000000 (MB)
* **-f** Output filename. Default is output{current time} in the out/ folder.
**NOTE:** the generated web page references stuff inside the css and js folder.
If you specify this option, make sure to change the reference paths in the info-page.ptm
file in the templates folder.
* **-p** The path where to analyze. Defaults to current directory.

Based on the number of files, this might take time. At the end of analyzing, the page will
open in a browser.