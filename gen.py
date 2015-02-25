import datetime
import os
import string

# Rafi Khan Copyright (c) 2015


keyfile = open("test.txt", 'r')

filename = "Esplora"
#print('"' + filename + '{{{')


def main():
    keyword_files_list = []
    finddir = input("Is '/usr/share/arduino/' the path for your ide? \n"
            "   Enter Yes or No ... \n")
    if "Yes" in finddir:
        arduino_dir = '/usr/share/arduino/'
    else:
        arduino_dir = input("Please enter the path for the arduino IDE: \n")

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

        i += (gen_keywords(keyword_files_list[idx]))
       
    return i


def gen_keywords(fileobjpath):
    fileobj = open(fileobjpath, 'r')
    heading = ''
    buffer = ''
    firstheading = True
    for rawline in fileobj:
        typedef = ''
        prefix = 'syn keyword'
        word = ''
        keyword = ''
        line = rawline.rstrip('\r\n')
        if line.rstrip():

            if line[0] == '#':
                if not firstheading:
                    buffer += '"}}}' + '\n'
                    buffer += '"' + line + ' ' + '{{{' + '\n'
                    heading = line
                if firstheading:
                    buffer += '"' +  line + ' ' + '{{{' + '\n'
                    firstheading = False

            else:
                try:
                    keyword, word = line.split('\t')[:2]
                except:
                    print(line)
                if keyword.isupper():
                    typedef = 'arduinoConstant'
                elif "datatypes" in heading:
                    typedef = 'arduinoType'
                elif "constant" in heading:
                    typedef = 'arduinoConstant'
                elif "method" in heading:
                    typedef = 'arduinoFunc'
                elif "function" in heading:
                    typedef = 'arduinoFunc'
                elif "USB" in heading:
                    typedef ='arduinoFunc'
                elif "operator" in heading:
                    typedef = 'arduinoOperator'
                buffer += prefix + ' ' + typedef + ' ' + keyword + '\n'

    buffer += '"}}}' + '\n'
    
    return buffer
   

if __name__ == '__main__':
    main()

