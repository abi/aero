Open source CLI version of code interpreter on self-hosted sandboxed infra using Modal.

![Add video](./assets/ocr.mp4)

## Benefits

- Has access to the Internet
- Runs all GPT generated code in an isolated, remote environment (won't delete your files by accident)
- Modify Modal to run in a GPU environment and use any GPU-enabled library that GPT4 knows about

## Limitations

- Not using a finetuned GPT4 model as code interpreter is suspected to use
- Doesn’t figure out the structure of input file yet. It relies solely on the file format to decided how to process it. (Fix coming soon)
- Containers only contain a few packages for now. PRs welcome to support more!

## TODOs

- Generate two versions of the code to have a fallback if the first one fails
- Support full list of Code Interpreter dependencies in the modal executor

## Setup

pip install python-dotenv modal-client

If you use Poetry,

```
poetry shell
poetry install
```

Copy .env.example to .env and fill in your Open AI API key.

In one tab, run `modal serve executor.py`

Copy the URL and fill in the EXECUTOR_URL in .env

In another tab, run `python cli.py ./test/test.png 'convert to a video'`

Your output will be printed if it's text or download and stored in a output
directory in your current working directory otherwise.

## Examples
