# Safecopy
Safecopy is a command line utility for selectively recursively copying files based on their file extension. It can for example be used for recovering images and documents off an old hard drive, while ignoring potentially unwanted files such as executables.

## Setup
Setup instructions for UNIX-like systems. VirtualEnv works slightly differently on Windows.
- `virtualenv -p python3 venv`
- `cp bin/magick venv/bin/`
- `source venv/bin/activate`

## Usage
Safecopy requires a so-called _copy spec file_ for each run. This spec file defines how each file type should be handled, based on its extension. To get a list of all file extensions in your input directry, run:
```
python scan-extensions.py <input_root> > spec.txt
``` 

where `<input_root>` is the root of the directory from which you want to selectively copy files. Then, edit the resulting file according to the copy specs format (see below).

Once the spec file is set up, run
```
python safecopy.py --spec <spec_file> --in <input_root> --out <output_root>
```

### Notes
- The copy process preserves the original directory structure of the source directory in its output.
- Safecopy will refuse to overwrite an existing directory when setting up the output root.
- Safecopy refuses to start the copy process if any of the spec entries are invalid.
- When encountering a file type for which there is no copy spec defined, Safecopy uses the `s` (skip) handler by default.
- A log file is created in the present working directory for every run of the `safecopy.py` script.

## Copy Spec Format and Copy Handlers
The copy specs / extensions file contains a list of expected file extensions, one extension per line. Files with an extension which is not in the extensions file are skipped by default (i.e. will not be copied). For every line in the extensions file, follow this format:

```
<ext>:<handler>[#<args>]
```

where `ext` is any file extension (no leading dot, case-sensitive), handler is any of:
- `c` (copy without transform)
- `s` (skip, do not copy)
- `mag` (transform: convert with ImageMagick)

The `mag` handler is used for converting images into different image formats before copying. For instance, you can define that all `.jpg` files should be converted to `.png`. In this case, only the `.png` version of all JPGs will arrive in the destination directory (the source file is not modified). This feature can be useful if images are suspected to contain malicious payloads. Such malware often exploits a vulnerability in a specific file format or in how that format is processed by some popular image viewer. Hence, converting suspicious images to a different file format may help reduce the risk of damage due to such malicious payloads.

The handlers `c` and `s` do not take any arguments. For the `mag` handler, the argument specifies the target file extension (no leading dot, e.g. `png`). 

### Examples
- `txt:c`: Copy `.txt` files without transform
- `docx:s`: Skip `.docx` files
- `png:mag#jpg`: Convert `.png` files to `.jpg` using ImageMagick (case sensitive, does not apply to `.PNG`)

## Dependencies
- `ImageMagick 7.0.10-25` (provided)

## License
See [LICENSE](LICENSE), [LICENSE_IMAGEMAGICK](LICENSE_IMAGEMAGICK) (binary provided in `bin/magick`). This project is not associated with or endorsed by ImageMagick.
