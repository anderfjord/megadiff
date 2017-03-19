# megadiff
A simple utility to compare the contents of two massive files.

# Installation

```
pip install megadiff
```

OR to install from source

```
# Make sure you have Python and pip installed.
git clone https://github.com/anderfjord/megadiff.git
cd megadiff
virtualenv env
source env/bin/activate
pip install .
```

# Usage

## Example #1 - Compare two files in verbose mode
```
$ megadiff -v -p "/tmp/massive_file-1.txt" -q "/tmp/massive_file-2.txt"
```

# License
megadiff is covered under the MIT License.  See [LICENSE](LICENSE) for more info.
