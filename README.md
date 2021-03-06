# Prototype

## generate.py

The generator can create an output csv and json file and uses the json file *param.json* to determine the form of the generated file(s).
The following attributes are used to create the files:
- **createcsv**: Boolean value that determines if a result.csv file is created.
- **createjson**: Boolean value that determines if a result.json file is created.
- **lines**: Amount of lines that are generated (integer/numeric value).
- **delimiter**: This value determines what symbol is used to seperate values in the csv file. If it's a char or 1 symbol long string, it's value is used, if it's an integer, the number is converted to a char through Python's chr() function. I recommend using "|" as the delimiter.
- **param**: Array of JSON dictionaries that are used to generate attributes / values. Further information about this can be found in the param section.

### param

dictionaries within the param-array need to have the following attributes:
- **name**: Name of the attribute that should be generated. Self-explanatory.
- **generator**: Determines how the value is generated. Further information about this can be found in the generator section.

### generator

Right now the following methods of generating values are available:
- **"name"**: Generates a random name with a variable length between 6 and 12. These names are just random letters, with the first one being upper case and the rest being lower case to ensure that they follow naming regex.
- **"randchar"**: Generates a string from random symbols including upper case letters, lower case letters, numbers, ` and _. The "randchar" is followed by a number to represent the length of the generated string. Example: "randchar8" could produce the following string: "2oI'UgHe".
- **"randint"**: Generates a random number up to 10^x where x is the number following the randint. Example: randint6 could produce anything from 0 to 999999.

### example param.json

```
{
	"createjson":true,
	"createcsv":true,
	"lines":25000,
	"delimiter":23,
	"param":[
		{
			"propname":"firstname",
			"generator":"name"
		},
		{
			"propname":"lastname",
			"generator":"name"
		},
		{
			"propname":"uid",
			"generator":"randchar8"
		},
		{
			"propname":"income",
			"generator":"randint4"
		}
	]
}
```

### args
args always overwrite param.json

- -json / --writejson: creates the JSON output, independent of the preset in param.json
- -csv / --writecsv: creates the CSV output, independent of the preset in param.json
- -l / --lines: set the amount of lines generated
- -csvn / --csvname: sets the name and location of the generated csv file
- -jsonn / --jsonname: sets the name and location of the generated json file
- -h / --help: spells the stuff in the lines above out for you

## import.py

### purpose

Gathers data from a CSV file and puts it into a JSON-structure that is compatible with mwintersperger-tgm's validation/rules program

### usage

Reads the inconfig.json found in the resources folder, which includes the following attributes:
- "file": location of the source CSV
- "delimiter": delimiter used to seperate values in the CSV file
- "out": location of the output JSON

#### args

Using these arguments overwrites the values found in inconfig.json
- -file / --fileinput: location of the source CSV
- -d / --delimiter: delimiter used to seperate values in the CSV file
- -out / --fileoutput: location of the output JSON

## export.py

### purpose

export the JSON structure used internally as Excel or CSV file.

### TODO

literally everything but the writing as an Excel File.
