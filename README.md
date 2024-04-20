# C64py
A simple C64 Simulator in Python (Does not run actual software)

Requires a font file named 'font.tff' to be placed in the main directory.
I recommend ["C64 Pro Mono" by Style64](style64.org/c64-truetype)


## Commands
| Command | Syntax | Description | Status |
| --- | --- | --- | --- |
| HELP | | Displays a short list of all commands and their descriptions. | :white_check_mark: |
| PRINT | PRINT [\<expression>] | Prints the following varible, whether a string, variable or numerical expression (Same Inputs as Python). | :white_check_mark: |
| LOAD | LOAD ["\<filename>" [,\<device number>]] | Loads selected data or program file into memory variable, from where it can be ran. | Incomplete |
| LIST | | Displays the data currently in the memory variable | :white_check_mark: |
| RUN | | Runs basic program currently in the memory variable | :white_check_mark: |