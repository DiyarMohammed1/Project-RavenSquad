# ZLIB Chunk Extractor for .SLOT Files (v1.0.0)

## Overview
This tool scans `.slot` files from the game **Raven Squad** and extracts **zlib-compressed chunks**. Each chunk is saved in a separate file, and the tool generates CSV and JSON logs with metadata for each extracted chunk.

**Supported file types inside zlib streams:**
- DDS (DirectDraw Surface textures)
- TXT / XML (text-based configuration)
- BIN (binary data)
- OGG (audio)
- WAV (audio)
- ZIP (archives)

> **Note:** Only data inside **zlib-compressed streams** is extracted. Raw DDS or other uncompressed data will not be detected.

---

## Features
- Processes **all `.slot` files** in a given input folder automatically.
- Creates **separate output folders** for each `.slot` file.
- Generates **CSV and JSON logs** for all extracted chunks.
- Creates `failed_chunks.log` for any decompression failures.
- Automatically detects common file types from decompressed data.
- Prints a summary of total chunks, total size, and breakdown by file type.
- CLI support for easy use: `--input` and `--output` arguments.

---

## Installation
1. Make sure you have [**Python 3.x**](https://www.python.org/downloads/).
2. download [this](https://github.com/DiyarMohammed1/Project-RavenSquad/blob/main/tools/extract_slot.py).
3. Place your `.slot` files in a folder (e.g., slot files/).

---

## Usage
Run the script from the command line:

``` bash
python extract_slot.py --input "slot files" --output "output"
```
--input : Path to the folder containing .slot files.
--output: Path to the folder where extracted chunks and logs will be saved.
After running, you will see a folder structure like:

```lua
output/
└─ m01/
   ├─ chunk_0000.dds
   ├─ chunk_0001.txt
   ├─ m01IndexLog.csv
   ├─ m01IndexLog.json
   └─ failed_chunks.log
```

---

> **Notes**
- This tool does not distribute any game assets. You must own the game to use it.
- Only chunks inside zlib streams are extracted; raw DDS files outside zlib streams are ignored.
- Failed decompression attempts are logged in failed_chunks.log
