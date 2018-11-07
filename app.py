import os
import sys

import click


@click.command()
@click.option('-p', '--path', help='Number of greetings.')
def import_file(path):
    if path is None:
        path = input("Please enter path to Graphml file: ")
    if not os.path.isfile(path) or os.path.splitext(path)[1] != '.graphml':
        sys.exit('Incorrect path')



if __name__ == '__main__':
    import_file()
