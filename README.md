# Safecopy
## Usage
- `virtualenv -p python3 venv`
- `cp bin/magick venv/bin/`
- `source venv/bin/activate`
- `python scan-extensions.py > spec.txt` and edit this file according to the copy specs format
- `python safecopy.py --spec <spec_file> --in <input_root> --out <output_root>` 

## Copy Specs Format
The copy specs / extensions file contains a list of expected file extensions, one extension per line. Files with an extension which is not in the extensions file are skipped by default (i.e. will not be copied). For every line in the extensions file, follow this format:

```
<ext>:<handler>#<args>
```

where `ext` is any file extension (no leading dot, case-sensitive), handler is any of `c` (copy without transform), `s` (skip, do not copy) and `mag` (transform: convert with ImageMagick). Handlers `c` and `c` do not need arguments (`# not needed`). For the `mag` handler, the argument specifies the destination file extension (no leading dot).

### Examples
- `txt:c`: Copy `.txt` files without transform
- `docx:s`: Skip `.docx` files
- `png:mag#jpg`: Convert `.png` files to `.jpg` using ImageMagick (case sensitive, does not apply to `.PNG`)

## Dependencies
- ImageMagick 7.0.10-25

## License
See [LICENSE](LICENSE), [LICENSE_IMAGEMAGICK](LICENSE_IMAGEMAGICK) (`bin/magick`). This project is not associated with or endorsed by ImageMagick.
