import click

from charts.sinmatplot import chart
from utilities.text import fnSay

@click.command()
# @click.option('--count', default=1, help='Number of greetings.')
@click.option('--function', prompt="function name: sinmatplot|hello", help='A function to call.')
@click.option('--arg', default="", help='argument')

def commands(function, arg):
    """Simple program that greets NAME for a total of COUNT times."""
    if function:
       if function == "sinmatplot":
          chart()
       if function == "hello":
          fnSay(arg)
       else:
          print("Function " + function + " does not exit")
    else:
      print("Please supply a function")

if __name__ == '__main__':
    commands()
