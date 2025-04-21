import argparse
from pathlib import Path


def process_vtt(file_path):
    import webvtt

    # Read the VTT file
    vtt = webvtt.read(file_path)
    transcript = ""
    previous = None

    # Extract lines, avoid duplicates
    for caption in vtt:
        for line in caption.text.strip().splitlines():
            if line != previous:
                transcript += " " + line
                previous = line

    return transcript


def main():
    # Setup argparse
    parser = argparse.ArgumentParser(
        description="Process VTT files and save transcripts. File renaming example: *.vtt -> *.txt ."
    )
    parser.add_argument(
        "files", type=str, nargs="+", help="List of VTT file paths to process"
    )
    args = parser.parse_args()

    # Process each VTT file
    for vtt_path in args.files:
        path = Path(vtt_path)
        print(f"Processing {path}")  # Print the path being processed
        transcript = process_vtt(path)

        # Write the output transcript
        output_path = path.with_suffix(".txt")
        with output_path.open("w") as output_file:
            output_file.write(transcript)
            print(f"Transcript written to {output_path}")


if __name__ == "__main__":
    main()
