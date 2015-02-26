import datetime
import os
import string

# Rafi Khan Copyright (c) 2015




def main():
    keyword_files_list = []
    finddir = input("Is '/usr/share/arduino/' the path for your ide? \n"
            "   Enter Yes or No ... \n")
    if "Yes" in finddir:
        arduino_dir = '/usr/share/arduino/'
    else:
        arduino_dir = input("Please enter the path for the arduino IDE: \n")

    print (arduino_dir)
    gen_list(keyword_files_list, arduino_dir)
    sorted(keyword_files_list, key=str.lower)
    template = string.Template(open('template.vim').read())

    arduino_vim = open("arduino.vim", "w")

    arduino_vim.write(template.substitute({
        'date': datetime.datetime.now().strftime('%d %B %Y'),
        'arduino_version': get_arduino_version(arduino_dir),
        'rules': get_syntax_definitions(keyword_files_list),
        }))
    
# generate the list of keywords.txt files
def gen_list(keyword_files_list, arduino_dir):
    for root, dirs, files in os.walk(arduino_dir # search all directories
    ):
        for file in files:
            if file.endswith("keywords.txt"):
                # print(os.path.join(root, file))
                keyword_files_list.append(os.path.join(root, file)) # add file to list if it ends with keywords.txt, that is if thats the file name


# function that returns the arduino IDE version specified
def get_arduino_version(arduino_dir):
    try:        # try to get the version number
        version_file = os.path.join(arduino_dir, 'lib', 'version.txt') # specify path to arduino/lib/version.txt as it holds the version number in the first line
        with open(version_file, 'r') as f:  # open the version.txt file with read permision
            version = f.readline()  # set the version as the first line
    except:    # if you cannot find the version number set it as 'unknown' and print that we do not know it
        version = 'unknown' # set version as 'unknown' because we cannot find it
        print("Version not found") # print that we do not know the version
    return version # give the version number back so that we can include it in the template



def get_syntax_definitions(keyword_files_list):
    
    i = ''
    
    for idx, val in enumerate(keyword_files_list):

        if idx == 0:
            first = True
        else:
            first = False
        i += ('"' + val + '\n')
        i += (gen_keywords(keyword_files_list[idx], first))

    return i


def gen_keywords(fileobjpath, first):
    fileobj = open(fileobjpath, 'r')
    heading = ''
    buffer = ''
    constants = []
    types = []
    functions = []
    operators = []

    constantname = 'arduinoConstant'
    typename = 'arduinoType'
    functionname = 'arduinoFunc'
    operatorname = 'arduinoOperator'


    for rawline in fileobj:
        if not first:
            constantname = 'arduinoLibraryConstant'
            typename = 'arduinoLibraryType'
            functionname = 'arduinoLibraryFunc'
            operatorname = 'arduinoLibraryOperator'


        prefix = 'syn keyword '
        word = ''
        keyword = ''
        line = rawline.rstrip('\r\n')
        if line.rstrip():

            if line[0] == '#':
                if first:
                    print (line)
                if '#######################################' in line:
                    continue
                else:
                    heading = line 
            else:

                try:
                    keyword, word = line.split('\t')[:2]
                except:
                    print(line)
                if keyword.isupper():
                    constants.append(keyword)
                elif "datatypes" in heading:
                    types.append(keyword)
                elif "operator" in heading:
                    operators.append(keyword)    
                elif "constant" in heading:
                    constants.append(keyword)
                elif "method" or "Method" or "Methods" or "methods" in heading:
                    functions.append(keyword)
                elif "function" in heading:
                    continue
                    functions.append(keyword)
                elif "USB" in heading:
                    functions.append(keyword)
                else:
                    print(keyword)



    if len(constants) > 0: 
        for idx,val in enumerate(constants):
            if idx % 10 == 0:
                buffer += '\n' + '\t' + prefix + constantname
            elif idx == 0:
                buffer += '\t' + prefix + constantname + constants[idx]
            buffer += ' ' + constants[idx]

    if len(types) > 0:
        for idx, val in enumerate(types):
            if idx % 10 == 0:
                buffer += '\n' + '\t' + prefix + typename
            elif idx == 0:
                buffer += '\t' + '\t' + prefix + typename + types[idx]
            buffer += ' ' + types[idx]
    
    if len(functions) > 0:
        for idx, val in enumerate(functions):
            if idx % 10 == 0:
                buffer += '\n' + '\t' + prefix + functionname
            elif idx == 0:
                buffer += '\t' + prefix + functionname + functions[idx]
            buffer += ' ' + functions[idx]

    if len(operators) > 0:
        for idx, val in enumerate(operators):
            if idx % 10 == 0:
                buffer += '\n' + '\t' + prefix + operatorname
            elif idx == 0:
                buffer += '\t' + prefix + operatorname + operators[idx]
            buffer += ' ' + operators[idx]


    buffer += '"}}}' + '\n'

    return buffer


if __name__ == '__main__':
    main()


