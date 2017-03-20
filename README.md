# megadiff
A simple utility to compare the contents of two potentially massive files.

# Installation

```
pip install git+https://github.com/anderfjord/megadiff.git
```

OR to install from source

```
# Make sure you have Python, pip, and virtualenv installed.
git clone https://github.com/anderfjord/megadiff.git
cd megadiff
virtualenv env
source env/bin/activate
pip install .
```

# Usage

## Example #1 - Compare two files line-by-line in verbose mode
```
$ megadiff -p "/tmp/massive_file-1.txt" -q "/tmp/massive_file-2.txt"  --verbose
```

## Example #2 - Compare two files based on their overall sizes
```
$ megadiff -p "/tmp/massive_file-1.txt" -q "/tmp/massive_file-2.txt"  --size
```

# License
megadiff is covered under the MIT License.  See [LICENSE](LICENSE) for more info.
