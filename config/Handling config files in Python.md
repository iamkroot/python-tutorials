# Handling config files in Python

An essential component of any application is its configurability. The user should be able to tweak the program's behaviour to their liking, and more importantly, these settings have to be read by our app safely and properly.

## The Why

We *could* just directly write the values in our program where they are used, instead of reading them from a separate file, but this is not favoured due to several reasons:

1. The user should not have to read through all the source code, only to change some settings.
2. As the size of the code-base grows, it becomes increasingly difficult to pinpoint the location of variable(s) that would create the desired effects.
3. If the code is under version control, it would mean that some secrets (like API keys) that are used by the program will be exposed to the world if our repo is made public. This can easily lead to misuse of the keys by malicious entities.

For these reasons, it is generally recommended to separate out the code from the config, and the earlier we start doing so, the easier our lives as developers will be.

## The How

There exist many, *many* ways to manage configuration files. From storing the settings as Python classes, to using environment variables, each method has its strengths and weaknesses. But everything essentially boils down to processing 'key-value' pairs of strings, where the key specifies the name of the setting.

### 1. As Python data structures

This is pretty straightforward. We simply store the settings as a `dict` inside a python file, usually named `config.py`.

You can use dictionaries for simple configurations:

```python
# config.py
# This just contains one big dictionary with all the settings
import sys
CONFIG = {
    'output': 'png',
    'timeout': 20,
    'creds': {  # you can even have dictionaries inside dictionaries
        'username': 'hunter2',
        'password': 'hunter2'
    },
    'err_stream': sys.stdout  # you can have any python object as a value
}

# main.py
... # other imports
from config import CONFIG

print(CONFIG['timeout'])  # 20
```

Besides simplicity, this method has the added benefit of directly using Python objects as values, so you aren't just limited to strings or ints.
However, this flexibility comes at a cost. These files can only be read by Python scripts. So this method should be considered only when you are limited to a single language.

You can find a good example of this in the Django ecosystem, where `settings.py` serves as the central config file.

### 2. Using external files

Using a language agnostic config file is generally considered good practice, and there are multiple options available here.

#### a. `configparser`

In this case, the config is stored in `.ini` files, which have sections and subsections. Here's a sample file:

```ini
; config.ini
; (yes, comments start with a ';' here :P)
[DEFAULT]  ; this is the name of the default section
ServerAliveInterval = 45
Compression = yes  ; strings don't need double quotes around them unless they contain spaces
CompressionLevel = 9  ; everything is stored as strings
ForwardX11 = yes

[bitbucket.org]  ; another section
User = hg
Pass = gh

[topsecret.server.com]
Port = 50022
ForwardX11 = no
```

To access this in python, we use the `configparser` module.

```python
# main.py
import configparser

config = configparser.ConfigParser()
with open('config.ini') as f:
    config.read_file(f)

print(config['bitbucket.org']['User'])  # hg"
```

As you can see, the configparser can be treated very much like a dictionary. For more details, have a look at the official [docs](https://docs.python.org/3/library/configparser.html).

Using an `ini` file is pretty simple and straightforward, but there are some drawbacks to the `configparser` module, the biggest one being that all values are stored and read as strings, so the program has to manually convert them to desired data types. Additionally, it is mandatory to have at least one section in the file.

#### b. JSON - JavaScript Object Notation

This file format has become the ubiquitous mode of data exchange on the web, a title previously held by `XML`. A JSON file looks very much like a Python dict:

```json
{
  "fruit": [
    {
      "name": "apple",
      "physical": {
        "color": "red",
        "shape": "round"
      },
      "variety": [
        { "name": "red delicious" },
        { "name": "granny smith" }
      ]
    },
    {
      "name": "banana",
      "variety": [
        { "name": "plantain" }
      ]
    }
  ]
}
```

We can use the built-in `json` module for parsing json files.

```python
import json

with open('config.json') as f:
    config = json.load(f)  # config is a dict

print(config['fruit'][0]['name'])  # "apple"
```

Python users find `json` very familiar due to its similarity with a `dict`. However, a major downside to this file format is that comments aren't allowed by the `JSON Spec`, which drastically reduces its viability as a `config` store, where some settings may have to be explained to the user via comments. JSON is therefore more suited to direct machine to machine interactions, where human intervention is minimal.

#### c. YAML - YAML Ain't a Markup Language

As a direct antagonist to `XML`(which stands for `eXtended Markup Language`), `YAML` is meant to be a human readable data serialization standard.

```yml
# config.yml  (Yay! Comments are back!)
product:
    - sku         : BL394D
      quantity    : 4
      description : Basketball
      price       : 450.00
    - sku         : BL4438H
      quantity    : 1
      description : Super Hoop
      price       : 2392.00
```

For parsing YAML in Python, use the `pyyaml` library, which can be installed using `pip install pyyaml`.

```python
import yaml

with open('config.yml') as f:
    config = yaml.load(f)  # config is a dict

print(config['product'][0]['description'])  # Basketball
```
You can read about the YML spec from [here](https://yaml.org/spec/1.2/spec.html).

#### d. TOML - Tom's Obvious, Minimal Language

Combining all the strengths of the major config file formats, TOML is designed to be minimal and easily readable.

```toml
# config.toml

title = "TOML Example"

[owner]
name = "Tom Preston-Werner"
dob = 1979-05-27T07:32:00-08:00

[database]
server = "192.168.1.1"
ports = [ 8001, 8001, 8002 ]
connection_max = 5000
enabled = true
```

The Python standard library doesn't ship with a parser for `toml`. You can install one using `pip install pytoml`.

```python
import pytoml

with open('config.toml') as f:
    config = pytoml.load(f)  # config is a dict
print(config['owner']['name'])  # "Tom Preston-Werner"
```

For detailed information on TOML, you can refer to the official SPEC [here](https://github.com/toml-lang/toml).

### 3. Using environment variables

Both the methods described above suffer from one common drawback; the config files cannot be added to a version control system if they contain some secrets (well, no one is stopping you from doing so, but it is BAD practice to do this!). The workaround for this is to create a `sample-config` file, which has all the same fields, but doesn't contain the secrets. This file can be added to the VCS, and you can keep using the `config` file in your program.

Another way to handle this is to use [environment variables](https://en.wikipedia.org/wiki/Environment_variable) from your os. Put simply, these are key-value pairs of strings that can be read using the `os.environ` dict in Python. To set them, in your terminal type:

```bash
export API_KEY="mySECRETkey"  # for linux/mac
set API_KEY="mySECRETkey"  # for windows
```

And then run the Python script from this terminal.

```python
import os
print(os.environ['API_KEY'])  # "mySECRETkey"
```

As you may notice, this is a very primitive way of storing configurations. Environment variables are generally used to store only mission critical secrets, while the other settings are stored in a separate file. Additionally, the variables have to be set every time the program is run, which becomes quite tedious. Devs tend to write shell scripts that load these before the program is run, but this again introduces the VCS problem mentioned earlier.

## The End

Outlined above are the various ways to handle configuration files in Python. There is no *best* way. Choose the method that suits your project requirements the best. Most of the information mentioned here is enough to get you started with the relevant module, and you should refer to the official documentation for further details.
