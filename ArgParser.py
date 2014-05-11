"""
Author: Kevin Owens
Date: 11 May 2014
Class: ArgParser

Problem description summary (from TopCoder):  Implement a class ArgParser with a method parse(string) that splits
a single string of arguments into a list of string arguments; e.g., '{a, b, c}' -> ['a', 'b', 'c'].  The input string
must conform to the following rules:

    begins with '{', ends with '}'
    can't have internal curly braces without a preceding escape char \
    commas delineate arguments
    escaped commas do not delineate
    delineating commas must be followed by a space
"""

class ArgParser:

    def parse(self, arg):

        # must begin with { and end with }
        if len(arg) < 2 or arg[0] != '{' or arg[-1] != '}':
            return 'INVALID'

        # discard outer {}
        arg = arg[1:-1]

        # can't have internal {} without escape char
        if len(arg.split('\{')) != len(arg.split('{')) or len(arg.split('\}')) != len(arg.split('}')):
            return 'INVALID'
        arg = arg.replace('\{', '{')
        arg = arg.replace('\}', '}')

        # all non-escaped commas have trailing space
        arg = arg.replace('\,', ';') # replace escaped commas with a token
        if arg.replace(', ', '#').find(',') != -1:
            return 'INVALID'

        # break out individual args
        args = arg.split(', ')

        # restore tokenized commas
        return [arg.replace(';',',') for arg in args]


if __name__ == '__main__':

    examples = '{a, b, c}', '{a\,b, c}', '{, , a, }', r'{\\, \,\, }', '{\ , \,, }', '{}', \
               '{a, b, c', '{a, {b, c}', '{a,b,c}'

    parser = ArgParser()
    for example in examples:
        print(example, ':', parser.parse(example))