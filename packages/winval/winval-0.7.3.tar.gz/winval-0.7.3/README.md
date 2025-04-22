# winval
### Workflow inputs validation python library

* Currently, supports WDL workflows.
* Constraints on inputs can be written as specially tagged (#@wv) comments in the WDL inputs section.
* The syntax of constraints is a python-similar DSL, with ANTLR defined grammar.
* The WDL + inputs.json can be validated using a script/function before submitting a workflow.


## Installation:
~~~
pip install winval
~~~

## Usage:

### validate_wdl_constraints
From python
~~~
from winval.validate_wdl_constraints import run_winval
is_validated = run_winval(wdl_file, json_file)
~~~

From unix command-line:
~~~
python winval/validate_wdl_constraints.py --wdl <wdl_file> --json <json_file>
~~~

### cloud_files_validater
#### Make sure google-storage permissions are equivalent to the batch workers permissions 

From python
~~~
from winval.cloud_files_validator import CloudFilesValidator
is_validated = CloudFilesValidator(args.wdl, args.json).validate()
~~~

From unix command-line:
~~~
python winval/cloud_files_validator.py --wdl <wdl_file> --json <json_file>
~~~

## WDL constraints example
~~~
workflow MyWorkflow {

  input {
    File file
    Int c
    File* opt_file_1
    File* opt_file_2
    Array[File] files
    Array[File] index_files
    MyStruct struct_instance

    #@wv defined(opt_file_1) <-> defined(opt_file_2)
    #@wv defined(opt_file_1) -> c > 1
    #@wv len(files) == len(index_files)
    #@wv len(files) >= 0
    #@wv len(index_files) >= 0
    #@wv c <= 1 and c >= 0
    #@wv suffix(file) == ".fasta"
    #@wv suffix(files) <= {".bam", ".cram"} 
    #@wv prefix(index_files) == files
    #@wv len(struct_instance['field_a']) > 0
  }
  ...
}
  
  struct MyStruct{
     String field_a,
     String field_b
  }
~~~

## Generate parsers from grammar:
~~~
cd <project_root>/winval
antlr4 -Dlanguage=Python3 winval.g4 -visitor -o antlr
~~~

## Available atomic expressions:
* int: 5
* float: 5.6
* bool: True, False
* str: "some string", 'some_string'
* workflow_variable: my_var
* evaluates to value given by json conf, or None if not defined in json
* empty_set: {} 

## Available python operators
* `+`,`-`,`*`,`**`,`/`,`&`,`|`,`%`
* `and`, `or`, `in`
* `<`, `<=`, `==`, `>=`, `>`, `!=`
* Notice the following useful operators work for sets:
  * `-`: set subtraction
  * `&`: set intersection
  * `|` : is set union 
  * `<=`:  subset 

## Available python functions
* `len()`, `not()`
* `basename()`, `splitext()` (from os.path)

## Available convenience functions and operators:
* `x <-> y`: if-and-only-if logical operator (if x is true if and only if y is true)
* `x -> y`: implies logical operator (if x is true then y should be true)
* `defined(x)`: if x a defined variable
* `prefix(x)`: return path prefix of String/File or list of prefixes for 
* `suffix(x)`: return path suffix of String/File or set of suffixes for Array[String]/Array[File]
