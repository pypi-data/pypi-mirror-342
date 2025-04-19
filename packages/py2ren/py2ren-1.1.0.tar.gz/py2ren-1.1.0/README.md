# py2ren
A tool to automate the transformation of native python module to ren'py store module.

## Requirements

* python >= 2.7

## Installation

You can install with pip, `pip install py2ren`

Or you can download a py2ren [release](https://www.github.com/yoimerdr/py2ren/releases).

## Usage
### CLI usage
Located in the py2ren's parent folder, you can now use the command.

```shell
    python -m py2ren path [options]
```


Positional argument:

  - **path**: target transformation path.


Options:

  - **-o, --out**:                     the output folder for the transformation result.
  - **-n, --name**:                    the base module name, must not contain spaces.
  - **-il, --init-level**:             the init level for the init expression.
  - **-c, --config**:                  path to the configuration file.
  - **-ad, --analyze-dependencies**:   flag to analyze internal modules on create config.
  - **-nks, --no-keep-structure**:     flag to disable keeping the module structure.
  - **-fc, --force-config**:           flag to force the creation of the configuration file.
  - **-h, --help**:                    show the help message and exit



For example, if you have the following file:

```python
def say_hello(name: str):
    return "Hello, " + name + "."
```

And run the command

```shell
    python -m py2ren sample.py -n sample_module
```

After the conversion, you will get:

````python
init -1 python in sample_module:
    def say_hello(name: str):
        return "Hello, " + name + "."
````

> py2ren does not remove type annotations, so if you want better compatibility with renpy projects, you should remove them.

### Module usage


You can also use py2ren as a python module; and continuing with the previous example, you can obtain the same result by doing the following.


````python
# this script is located in py2ren's parent folder
import py2ren

py2ren.convert("filename.py", ".", "sample_module")
````

### Docs

You can read the docs [here](https://yoimerdr.github.io/py2ren/docs/).
