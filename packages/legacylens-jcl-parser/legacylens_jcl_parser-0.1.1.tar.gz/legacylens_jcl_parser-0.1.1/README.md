# LegacyLens JCL Parser

A simple, extensible Python parser for JCL (Job Control Language) files with JSON output.

## Features

- Parse JCL files and extract structured information
- Output results in JSON format
- Command-line interface for easy use
- Library for integration into other Python applications
- No external dependencies - uses only Python standard libraries

## Installation

### From Source

```bash
git clone https://github.com/yourusername/legacylens-jcl-parser.git
cd legacylens-jcl-parser
pip install -e .
```

## Usage

### Command Line

```bash
# Parse a JCL file and print JSON to stdout
legacylens-jcl-parser path/to/your/jcl_file.jcl

# Parse a JCL file and save pretty-printed JSON to a file
legacylens-jcl-parser path/to/your/jcl_file.jcl --output result.json --pretty
```

### As a Library

The JCL parser is designed to be easily integrated into your Python applications as a library.

```python
from legacylens_jcl_parser import JCLParser

# Initialize the parser
parser = JCLParser()

# Parse a JCL file
jcl_data = parser.parse_file("path/to/your/jcl_file.jcl")

# Convert to JSON
json_output = parser.to_json(jcl_data, pretty=True)
print(json_output)

# Parse JCL from a string
jcl_string = """//JOBNAME JOB (ACCT),'TEST JOB',CLASS=A
//STEP1    EXEC PGM=IEFBR14
//DD1      DD   DSN=TEST.DATA,DISP=SHR"""
jcl_data = parser.parse_string(jcl_string)

# Save parsed data to a file
with open('output.json', 'w') as f:
    f.write(parser.to_json(jcl_data, pretty=True))
```

You can access specific elements from the parsed data structure:

```python
# Access job information
job_name = jcl_data["job"]["name"]
job_parameters = jcl_data["job"]["parameters"]

# Access steps
for step in jcl_data["steps"]:
    step_name = step["name"]
    step_program = step["parameters"].get("PGM")
    
    # Access DD statements in this step
    for dd in step["dd_statements"]:
        dd_name = dd["name"]
        dataset = dd["parameters"].get("DSN")
```

## Output Format

The parser generates a JSON structure with the following main components:

```json
{
  "job": {
    "name": "JOBNAME",
    "parameters": { /* parsed job parameters */ },
    "line": 1
  },
  "steps": [
    {
      "name": "STEP1",
      "parameters": { /* parsed step parameters */ },
      "dd_statements": [
        {
          "name": "DD1",
          "parameters": { /* parsed DD parameters */ },
          "line": 3
        }
      ],
      "line": 2
    }
  ],
  "procedures": [
    {
      "name": "PROC1",
      "parameters": { /* parsed procedure parameters */ },
      "steps": [ /* procedure steps */ ],
      "line": 10
    }
  ],
  "comments": [
    {
      "text": "This is a comment",
      "line": 5
    }
  ]
}
```

## Extending the Parser

The parser is designed to be easily extended. To add support for new JCL statements or features:

1. Add new regex patterns in the `JCLParser.__init__` method
2. Add handling logic in the `parse_file` method
3. Update the output structure as needed

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.