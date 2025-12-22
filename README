# How To Handle
### Import 
```
from unihandle import UniHandle, In_Opt, Out_Opt
```
- Unihandle - The tool itself
- In_Opt/Out_Opt - Startup options (Can be skipped)

### Create new UniHandle object where you wish the menu loop to sit
```
handle = UniHandle(in_opt=In_Opt.BOTH, out_opt=Out_Opt.MENU)
```
A launch flag enum is provided for Input and Output (In_Opt/Out_Opt):
#### ***in_opt***:
* ARGV => Only take in startup arguments.
* INPUT => Only take in menu loop options.
* BOTH => Take in both argv and menu loop.

#### ***out_opt***:
* NONE => Do not include menu entry.
* MENU => Include menu entry.
* ALL => Print all items in dictionary through menu.

### Add your functions to the object 
```
handle["key"] = function
```
Adds the function to the dictionary in a UniWrap Wrapper Class.

### Remove a function from the object
```
handle["key"] = None
```
Quickly removes the function from the dictionary 

### Run the handle object
```
handle()
```
Starts the configuration of ARGV and Menus specified in creation.

### Using the menu (as it is)
TBD
