import os
import sys
from collections import defaultdict

mappings = {
    'HIGH': 'arduinoConstant',
    'abs': 'arduinoStdFunc',
    'arduinoFunc': 'analogReference',
    'setup': 'arduinoMethod',
    'begin': 'arduinoFunc',
    'bitSet': 'arduinoFunc',
    'analogRead': 'arduinoFunc',
    'Serial': 'arduinoIdentifier',
    'boolean': 'arduinoType',
    '+=': None,
}

cppkeywords = set([
    'auto', 'const', 'double', 'float', 'int', 'short', 'struct', 'unsigned',
    'break', 'continue', 'else', 'for', 'long', 'signed', 'switch', 'void',
    'case', 'default', 'enum', 'goto', 'register', 'sizeof', 'typedef', 'volatile',
    'char', 'do', 'extern', 'if', 'return', 'static', 'union', 'while',
    'asm', 'dynamic_cast', 'namespace', 'reinterpret_cast', 'try',
    'bool', 'explicit', 'new', 'static_cast', 'typeid',
    'catch', 'false', 'operator', 'template', 'typename',
    'class', 'friend', 'private', 'this', 'using',
    'const_cast', 'inline', 'public', 'throw', 'virtual',
    'delete', 'mutable', 'protected', 'true', 'wchar_t',
])


def get_keywords(fileobj):
    heading = ''
    paragraph = 0

    for rawline in fileobj:
        line = rawline.rstrip('\r\n')
        if line.strip() == '':
            paragraph += 1
            continue
        elif line[0] == '#':
            heading = line[1:].strip()
        else:
            try:
                keyword, classname = line.split('\t')[:2]
                yield keyword, classname, heading, paragraph
            except:
                print(line)


def get_sections(fileobj):
    sections = defaultdict(lambda: [])

    for keyword, classname, heading, paragraph in get_keywords(fileobj):
        section_id = '%d-%s' % (paragraph, classname)
        sections[section_id].append(keyword)
    return sections


def get_mapped_keywords(sections):
    for keywords in sections.values():
        maps_to = [mappings[keyword] for keyword in keywords if (keyword in mappings)]
        reduced = filter(lambda x: x not in cppkeywords, keywords)

        if len(maps_to) == 1:
            if maps_to[0]:
                yield (reduced, maps_to[0])


def get_syntax_groups(sections):
    syntax_groups = defaultdict(lambda: [])

    for keywords, mapping in get_mapped_keywords(sections):
        syntax_groups[mapping].extend(keywords)

    return syntax_groups


def keyfunction(item):
    return item[1:]


def get_syntax_definitions(filename):
    sections = get_sections(open(filename))
    syntax_groups = sorted(get_syntax_groups(sections).items())
    caseinsensitive_cmp = lambda x, y: cmp(x.lower(), y.lower())

    for name, keywords in syntax_groups:
        linestart = 'syn keyword %-16s' % name
        line = linestart
        lines = ''

        for keyword in sorted(set(keywords), key=keyfunction):
            if len(line) + len(keyword) > 80:
                lines += line
                line = '\n' + linestart

            line += ' ' + keyword

        lines += line

        yield lines


def get_arduino_version(arduino_dir):
    try:
        version_file = os.path.join('/usr/share/arduino/', 'lib', 'version.txt')
        version = open(version_file).next().rstrip('\r\n')  # first line
        print("Arduino IDE Version:", version)
    except:
        version = 'unknown'
        print("Version not found", version)
    return version


def gen_list(keyword_files, arduino_dir):
    for root, dirs, files in os.walk(arduino_dir
    ):
        for file in files:
            if file.endswith("keywords.txt"):
                # print(os.path.join(root, file))
                keyword_files.append(os.path.join(root, file))

def gen_definitions(keyword_files):
    for idx, val in enumerate(keyword_files):
        print('\n\n'.join(get_syntax_definitions(keyword_files[idx])))
        print(idx, val)

def main():
    import datetime
    import string

    keyword_files = []
    arduino_dir = input("Please enter the full path for the arduino IDE: ")
    gen_list(keyword_files, arduino_dir)
    sorted(keyword_files, key=str.lower)

    template = string.Template(open('template.vim').read())

    sys.stdout.write(template.substitute({
        'date': datetime.datetime.now().strftime('%d %B %Y'),
        'arduino_version': get_arduino_version(arduino_dir),
        'rules': '\n\n'.join(gen_definitions(keyword_filesii))),
    }))


if __name__ == '__main__':
    main()

