# import.py

### purpose

Gathers data from a CSV file and puts it into a JSON-structure that is compatible with mwintersperger-tgm's validation/rules program

### usage

Reads the inconfig.json found in the resources folder, which includes the following attributes:
- "file": location of the source CSV
- "delimiter": delimiter used to seperate values in the CSV file
- "out": location of the output JSON

### args

Using these arguments overwrites the values found in inconfig.json
- -file / --fileinput: location of the source CSV
- -d / --delimiter: delimiter used to seperate values in the CSV file
- -out / --fileoutput: location of the output JSON