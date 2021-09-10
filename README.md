# Convert SRT to TextGrid

The script uses the pysrt package to parse srt files: https://github.com/byroot/pysrt

### Setup
```bash
pip install -r requirements.txt
```

### Usage
```bash
python srt2textgrid.py -i <PATH_TO_SRT> [-o <PATH_TO_TEXTGRID>]
```
_Note_: The default path and file name of the TextGrid is the same as SRT, but with `.TextGrid` extension.
