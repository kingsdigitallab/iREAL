import subprocess
from .md2json import process_directory


def main():
    run_doc2md()
    run_md2json()


def run_doc2md():
    result = subprocess.run(["app/utils/doc2md.sh"], capture_output=True, text=True)
    print(result.stdout)


def run_md2json():
    print("Converting .md to .json...")
    process_directory("data/1_interim/records/md", "data/1_interim/records/json")
    print("Done converting .md to .json")
