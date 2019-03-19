import click

from charts.sinmatplot import chart
from utilities.text import fnSay
from nano_degree.template.report import outputHTML

@click.command()
# @click.option('--count', default=1, help='Number of greetings.')
@click.option('--function', '-f', required=False, help='call a function')
@click.option('--show', '-s', is_flag=True, required=False, help='list functions.')
@click.option('--arg', '-a', required=False, default="", help='argument')

def commands(function, arg, show):
    """Simple program that greets NAME for a total of COUNT times."""
    if show:
       print("functions: sinmatplot | hello")
    if function:
       if function == "chart":
          chart()
       if function == "sinmatplot":
          chart()
       if function == "hello":
          fnSay(arg)
       if function == "report":
          outputHTML(arg)
       else:
          raise AssertionError("Function " + function + " does not exit")
    # else:
       # raise AssertionError("usage: cli.py --function [sinmatplot | hello] --list --arg")

if __name__ == '__main__':
   try:
    commands()
   except AssertionError as error:
    print(error)
   else: 
    print("No exceptions!")
   finally:
    print("Complete!")