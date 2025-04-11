import time
import commandline


FILE = None
FILECONTENTS = None
EXECUTING = None

if __name__ == "__main__":
    from commandline import *

def run(file, execute=True):
    global statements, FILE, FILECONTENTS, EXECUTING
    FILE = file
    EXECUTING = execute
    with open(file, "r") as _file:
        FILECONTENTS = _file.read().split("\n")
    num = 0
    if not execute:
        statements = {}
    for line in FILECONTENTS:
        num += 1
        parseLine(line, num)

def parseLine(line, num = -1):
    line = line.replace("\n", "")
    if "\t" in line: # skip indented lines they will always be parsed alongside functions
        return
    if "##" in line[:2] or line == "#" or line.replace(" ", "") == "":
        return #prevent comments and blank lines from parsing
    # replace all <varname> with the var
    for variable in vars.items():
        line = line.replace("<"+str(variable[0])+">", str(vars[variable[0]]))
    try: 
        if "define(function)" in line[:17]: #check for definitions
            define(line.replace("define(function) ", ""))
        elif "var" in line[:3]: #check for vars
            var(line.replace("\t", "").replace(" ", "").split("=")[0], line.replace("\t", "").replace(" ", "").split("=")[1])
        else:
            try: #try normal statement
                if EXECUTING:
                    statements[line.split("(")[0]](line.split("(")[1].replace(")", "").split(", "))
            except: #parse functions if not normal statement
                try: # make sure its actually a function call
                    for part in statements[line.split("(")[0]]:
                        parseLine(part.replace("\t", ""))
                except:
                   raise Exception(f"Failed to parse statement/method call!\n   Line: {num}\n   Content: {line}") 
    except:
        raise Exception(f"Failed to parse line!\n   Line: {num}\n   Content: {line}")

statements = {
    "writeline": lambda args : commandline.outputLine(args[0]),
    "freeze": lambda args : input(),
    "wait": lambda args : time.sleep(int(args[0]))
}

vars = {
    "null": None
}

# By default it is just a list of strings as argumetns, you can evaluate them and index them for like arg1 = args[0]

def var(name, value):
    vars[name.replace("var", "")] = eval(value)

def define(name):
    _e = []
    ln = 1
    z = FILECONTENTS.index("define(function) " + name)
    while True:
        next = z+ln
        if FILECONTENTS[next].replace("\t", "").replace("\n", "") == "end":
            statements[name] = _e
            return
        _e.append(FILECONTENTS[next])
        ln+=1