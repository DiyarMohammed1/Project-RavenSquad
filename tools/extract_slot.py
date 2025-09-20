#!/usr/bin/env python3
"""
==========================================
ZLIB CHUNK EXTRACTOR FOR .SLOT FILES
==========================================

Description:
This script scans all .slot files in a specified input folder, detects zlib-compressed 
chunks, decompresses them, saves each chunk in its own subfolder, and generates a CSV 
log with metadata about each chunk.

Each .slot file is processed independently:
- Each gets its own subfolder in OUTPUT_FOLDER
- Each gets its own CSV log inside that subfolder
- Chunk numbering resets for each file

Usage:
1. Place your .slot files into the folder defined by INPUT_FOLDER.
2. Configure INPUT_FOLDER and OUTPUT_FOLDER below.
3. Run the script with Python 3.x.
4. Check the output folders and CSV logs for extracted data.

Note on Public Use:
This script was originally generated using OpenAI's ChatGPT. You can use, share, or 
adapt it for public repositories, educational purposes, or personal reverse engineering. 
Please do not distribute copyrighted game data.

------------------------------------------
Author / Attribution:
- Generated with ChatGPT
- Adapted by [D1yy_0]
------------------------------------------
"""

import os
import zlib
import json
import argparse
from collections import Counter

# -----------------------------
# Function: detect_file_type
# -----------------------------
def detect_file_type(data):
    """Guess the type of the decompressed data based on its header signature.
    Some detections (ogg, wav, zip) are unconfirmed and may not appear in actual data.
    """
    global seen_file_types

    def log_first_detect(ftype, msg):
        if ftype not in seen_file_types:
            print(f"[!] {msg}")
            seen_file_types.add(ftype)

    if data.startswith(b'DDS '):
        return "dds"   # Confirmed: DirectDraw Surface texture
    elif data.startswith(b'OggS'):
        log_first_detect("ogg", "Possible OGG audio detected (UNTESTED)")
        return "ogg"
    elif data.startswith(b'RIFF') and data[8:12] == b'WAVE':
        log_first_detect("wav", "Possible WAV audio detected (UNTESTED)")
        return "wav"
    elif data.startswith(b'PK\x03\x04'):
        log_first_detect("zip", "Possible ZIP archive detected (UNTESTED)")
        return "zip"
    elif data.startswith(b'<?xml') or (b"<" in data[:20] and b">" in data[:20]):
        return "xml"   # Confirmed: XML text file
    elif data.isascii():
        return "txt"   # Confirmed: ASCII text file
    return "bin"       # Default binary file if unknown

# -----------------------------
# Function: extract_zlib_streams
# -----------------------------
def extract_zlib_streams(input_file, output_root):
    """Extract all zlib-compressed chunks from a single .slot file."""
    with open(input_file, "rb") as f:
        data = f.read()

    slot_name = os.path.splitext(os.path.basename(input_file))[0]
    slot_output_folder = os.path.join(output_root, slot_name)
    os.makedirs(slot_output_folder, exist_ok=True)

    log_csv = os.path.join(slot_output_folder, f"{slot_name}IndexLog.csv")
    log_json = os.path.join(slot_output_folder, f"{slot_name}IndexLog.json")
    failed_log = os.path.join(slot_output_folder, "failed_chunks.log")

    signatures = [b"\x78\x9C", b"\x78\xDA"]
    index = 0
    chunk_count = 0
    results = []
    failures = []
    data_len = len(data)

    while index < data_len:
        if data[index:index+2] in signatures:
            start = index
            decomp_obj = zlib.decompressobj()
            decompressed = b""
            i = start
            try:
                # Feed data until decompressor stops using input
                while i < data_len:
                    chunk = data[i:i+1024]
                    if not chunk:
                        break
                    decompressed += decomp_obj.decompress(chunk)
                    i += len(chunk)
                    if decomp_obj.unused_data:
                        break
                compressed_size = i - start - len(decomp_obj.unused_data)
            except Exception as e:
                failures.append(f"Offset {start}: {str(e)}")
                index += 1
                continue

            file_type = detect_file_type(decompressed)
            file_name = f"chunk_{chunk_count:04d}.{file_type}"
            file_path = os.path.join(slot_output_folder, file_name)

            with open(file_path, "wb") as out:
                out.write(decompressed)

            results.append({
                "index": chunk_count,
                "offset": start,
                "compressed_size": compressed_size,
                "decompressed_size": len(decompressed),
                "file_type": file_type,
                "file_name": file_name
            })

            print(f"[+] {slot_name}: Chunk {chunk_count:04d} | Offset: {start} "
                  f"| {compressed_size} → {len(decompressed)} bytes")
            chunk_count += 1
            index = start + 2
        else:
            index += 1

    # Write CSV log
    with open(log_csv, "w") as csvfile:
        csvfile.write("chunk_index,offset,compressed_size,decompressed_size,file_type,file_name\n")
        for r in results:
            csvfile.write(f"{r['index']},{r['offset']},{r['compressed_size']},"
                          f"{r['decompressed_size']},{r['file_type']},{r['file_name']}\n")

    # Write JSON log
    with open(log_json, "w") as jsonfile:
        json.dump(results, jsonfile, indent=4)

    # Write failure log if needed
    if failures:
        with open(failed_log, "w") as flog:
            flog.write("\n".join(failures))
        print(f"[!] {len(failures)} chunks failed to decompress. See {failed_log}")

    # Print summary
    type_counts = Counter(r['file_type'] for r in results)
    total_size = sum(r['decompressed_size'] for r in results)
    print(f"[Summary] {slot_name}: {chunk_count} chunks extracted ({total_size/1024:.1f} KB)")
    for t, count in type_counts.items():
        print(f"  - {t}: {count}")

# -----------------------------
# Main CLI Entry Point
# -----------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract zlib-compressed chunks from .slot files.")
    parser.add_argument("--input", required=True, help="Folder containing .slot files")
    parser.add_argument("--output", required=True, help="Folder where extracted data will be saved")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    for file in sorted(os.listdir(args.input)):
        if file.endswith(".slot"):
            input_file_path = os.path.join(args.input, file)
            print(f"\nProcessing {input_file_path} ...")
            extract_zlib_streams(input_file_path, args.output)

