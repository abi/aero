import modal
from images import executor_image
from fastapi import File, UploadFile, Form, Response

stub = modal.Stub("aero-executor")


@stub.function(image=executor_image)
@modal.web_endpoint(method="POST")
async def code_executor(file: UploadFile = File(...), options: str = Form(...)):
    import os
    import sys
    import io
    import json
    import zipfile

    OUTPUT_DIR = "/tmp/output"

    # Make sure /tmp/output exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    options = json.loads(options)
    code1 = options["code1"]
    code2 = options["code2"]

    # Store input file path in the filePath variable
    # The AI-generated code assumes its existence
    filename = options["filename"]
    filePath = os.path.join("/tmp", os.path.basename(filename))

    # Store the file contents at the filePath
    with open(filePath, "wb") as input_file:
        contents = await file.read()
        input_file.write(contents)

    # Pipe stdout to a buffer, store original stdout to revert back
    buffer = io.StringIO()
    original_stdout = sys.stdout
    sys.stdout = buffer

    # Execute the code
    try:
        exec(code1)
    except Exception as e:
        print("Error executing code #1: ", e)
        print("Continuing with code #2")
        try:
            exec(code2)
        except Exception as e:
            print("Error executing code #2: ", e)
            print("Try again.")

    # Reset stdout back to its original value
    sys.stdout = original_stdout

    # Write stdout to a file
    stdout_value = buffer.getvalue()
    with open(os.path.join(OUTPUT_DIR, "stdout.txt"), "w") as f:
        f.write(stdout_value)

    # Store all output files in a zip file
    ZIP_FILE_NAME = "files.zip"
    with zipfile.ZipFile(ZIP_FILE_NAME, "w") as zipf:
        for filename in os.listdir(OUTPUT_DIR):
            full_path = os.path.join(OUTPUT_DIR, filename)
            zipf.write(full_path, arcname=os.path.basename(filename))

    # Return the ZIP file
    with open(ZIP_FILE_NAME, "rb") as f:
        return Response(f.read(), media_type="application/octet-stream")
