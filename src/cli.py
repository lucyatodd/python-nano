import click

from charts.sinmatplot import chart
from utilities.text import fnSay

@click.command()
# @click.option('--count', default=1, help='Number of greetings.')
@click.option('--function', required=False, help='call a function')
@click.option('--list', required=False, help='list functions.')
@click.option('--arg', required=False, default="", help='argument')

def commands(function, arg, list):
    """Simple program that greets NAME for a total of COUNT times."""
    if list:
       print("functions: sinmatplot | hello")
    elif function:
       if function == "sinmatplot":
          chart()
       if function == "hello":
          fnSay(arg)
       else:
          raise AssertionError("Function " + function + " does not exit")
    else:
       raise AssertionError("usage: cli.py --function --list --arg")
 
if __name__ == '__main__':
   try:
    commands()
   except AssertionError as error:
    print(error)
   else: 
    print("No exceptions!")
   finally:
    print("Complete!")