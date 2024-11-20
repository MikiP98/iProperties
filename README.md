# iProperties

## Description

### Iris Properties

An alternative preprocessing app to [PoTater](https://github.com/Null-MC/PoTater)

## Features

Auto .glst generation  
Auto numering  
Variable groups

## How to use

### First install the package:

- Make sure you have [Python](https://www.python.org/downloads/) installed  
  The app was tested using Python 3.12
- Open console and run `pip install "git+https://github.com/MikiP98/iProperties.git"`

### Create template files for processing

IProperties will try to find a file named `block.iProperties.properties` to process  
If such a file won't be found it will try to find file named `block.template.properties`

These files will then be processed into 3 files:
- `block.properties` - ready to use by Iris or Optifine properties file
- `block.glsl` - ready to use by Iris or Optifine glsl mapping file
- `block.PoTater.properties` - template in PoTater format if you would need it

### How to run the app

- Open the console in the target directory or use the `cd` command to go there
- Run command `iProperties` or `Iris`

`block.iProperties.properties` or `block.template.properties` will be processed to `block.properties`, `block.glsl` and `block.PoTater.properties`