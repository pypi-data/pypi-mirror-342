Dev Notes

## on every upload to pypi increment version in pyproject.toml

python3 -m pip install --upgrade build
# where is twine?
make sure in llmutils directory with pyproject.ml, README, LICENSE in llmutils and llmutilsdougc333 as dir
build will create a dist/ if there is no dist/ then this is first build

python3 -m pip install --upgrade twine

# ** COMMON ERROR repo name is NOT the package install name but either pypi or testpypi
## This builds the whl and tar.gz files in dist. There shuold be only 2 files
## the pypi names come from the tar.gz and whl file names
python -m build 
# verify there are only 2 files in /dist
python3 -m twine upload --repository pypi dist/*
##

### Install locally before uploading
python3 -m pip install "SomeProject"

When uploading it uses the file names under dist/ to create the project names in pypi. Make sure this is clean before uploading

## Usage: in colab cell or in colab terminal window (avail on pro)
from colab_dc333 import nvidia
nvidia.update_12_4()

* takes > 5m