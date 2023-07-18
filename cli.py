import argparse
import os
import zipfile
import random
import dotenv

from processor import processor, stub

# Load environment variables
dotenv.load_dotenv()
EXECUTOR_URL = os.environ.get("EXECUTOR_URL")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


def process_file(input_file_path: str, instruction: str):
    with open(input_file_path, "rb") as f:
        input_file_contents = f.read()

        with stub.run():
            # Process file with instruction
            output_file_info = processor.call(
                [input_file_path, input_file_contents],
                instruction,
                OPENAI_API_KEY,
                EXECUTOR_URL,
            )

            # Extract output
            [output_filename, output_file_contents] = output_file_info

            # Write zip to tmp
            tmp_zip_path = os.path.join("/tmp", output_filename)
            with open(tmp_zip_path, "wb") as out_file:
                out_file.write(output_file_contents)

            # Unzip the file in current dir
            with zipfile.ZipFile(tmp_zip_path, "r") as zip_ref:
                # Add random value to avoid overwriting
                OUTPUT_DIR = "./output" + str(random.randint(0, 1000))
                zip_ref.extractall(OUTPUT_DIR)

                # Print the `stdout.txt` file
                with open(os.path.join(OUTPUT_DIR, "stdout.txt"), "r") as f:
                    print(f.read())


def main():
    parser = argparse.ArgumentParser(description="Aero")
    parser.add_argument("input_file", type=str, help="The input file to be processed.")
    parser.add_argument(
        "instruction", type=str, help="The instruction for processing the input file."
    )

    args = parser.parse_args()

    process_file(args.input_file, args.instruction)


if __name__ == "__main__":
    main()

# Examples
# --------
# MKV file - convert to GIF
# PNG - convert to video
# png file - parse all the text
# CSV - count the number of rows in it
# txt file - (list of URLs) - grab the URLs and extract the SEO tags for me
# txt file - (list of URLs) - grab the URLs and tell me what technologies the app is built with
# [x] txt file - (list of URLs) - grab the URLs and get me screenshots of the page
