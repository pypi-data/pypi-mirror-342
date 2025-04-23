# qdown

A Python client for downloading files from QualitegDrive operated by Qualiteg Inc.

# install

```
pip install qdown
```

or 

```
pip install git+https://github.com/qualiteg/qdown.git
```

# usage

```

qdown ID [options]

Options:
-O FILENAME     Specify output filename
-o DIR          Specify output directory
-s SERVER       Specify server URL (default: https://drive.qualiteg.com)
-q, --quiet     Hide progress display
-h, --help      Display help
```

## download example1

```
qdown xxxxxxxxxxxxx -O my_file.txt
```

## download example2

From Your Original HTTP Server

```
qdown xxxxxxxxxxxxx -O my_file.txt -s http://host.docker.internal:3000 
```


# uninstall

```
pip uninstall qdown -y
```