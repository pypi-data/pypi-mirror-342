from setuptools import setup, find_packages
from pathlib import Path

## Get the parent directory of this file
dir_parent = Path(__file__).parent

with open(str(dir_parent / "romatch" / "__init__.py"), "r") as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.split("=")[1].strip().replace("\"", "").replace("\'", "")
            break
## Get README.md
with open(str(dir_parent / "README.md"), "r", encoding="utf-8") as f:
    readme = f.read()

setup(
    name="romatch_roicat",
    packages=find_packages(include=("romatch*",)),
    version=version,
    author="Johan Edstedt",
    long_description=readme,
    long_description_content_type="text/markdown",
    install_requires=open("requirements.txt", "r").read().split("\n"),
)
