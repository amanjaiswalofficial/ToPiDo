import argparse
import pandas as pd
from ToDoClass import *
parser = argparse.ArgumentParser()
parser.add_argument('echo', nargs='*', default=None)
help_guide='\nPlease refer to the following commands\
                    \na: add an item to the todolist (for help run python3 ToDoApp.py addh)\
                    \nl: list items from the todolist (for help run python3 ToDoApp.py listh)\
                    \nc: mark an item as complete (for help run python3 ToDoApp.py completeh)\
                    \nd: delete an item from the todolist (for help run python3 ToDoApp.py deleteh)\n'
add_help='\nPlease try input in the following format for a successful entry\
                    \na +(project name or names if any) message @(context if any) due due_date (today/tomorrow or any valid DD MON)\
                    \nEx-a +project_name meet with @meghan due 21 jun\n'
delete_help='\nPlease try the input in the following format for a success entry\
                    \nd valid_todo_serial_number\
                    \nEx- d 10\n'
list_help='\nPlease use any of the following commands to list todo\
                    \n1. l all: to display all the todo complete and incomplete\
                    \n2. l by context: to display all the todo grouping by context\
                    \n3. l by project: to display all the todo grouping by project\
                    \n4. l +valid_project_name: to display all the todo with that project\
                    \n5. l @valid_context_name: to display all the todo with that context\
                    \n6. l overdue: to display all the todo that are remaining\n'
complete_help='\nPlease try the input in the following format for completing a task\
                    \nc valid_todo_serial_number\
                    \nEx- c 10\n'
#parser.add_argument('a',)

class UserInteraction:
    inputs = ''

    def __init__(self, inputs):
        self.inputs = inputs

    def call_add(self):
        if(len(self.inputs[1:]) != 0):
            input_stmt = ' '.join(i for i in inputs[1:])
            todo.add_todo(input_stmt)
        else:
            print(" ")

    def call_list(self, *args):
        def call_check_by_due_date():
            check_by_due_date(inputs)

        def call_check_project_context():
            check_project_context(inputs)

        def no_function():
            raise AnyPossibleError

        def list_one_argument():
            calling_func = {'all': todo.list_todo,
                            'overdue': todo.list_by_overdue}
            call_method = calling_func.get(
                inputs[1], call_check_project_context)
            call_method()

        def list_two_argument():
            calling_func = {'by project': todo.list_by_project,
                            'by context': todo.list_by_context}
            call_method = calling_func.get(
                inputs[1]+' '+inputs[2], call_check_by_due_date)
            call_method()

        input_len = {0: no_function, 1: list_one_argument,
                        2: list_two_argument, 3: list_two_argument}
        result_method = input_len.get(len(inputs[1:]), default)
        result_method()

    


try:
    readdata = read_todo_file()
    todo = Todo(readdata)

    args = parser.parse_args()
    if(args.echo != []):
        inputs = args.echo
        UI = UserInteraction(inputs[1:])
        choice = {'a': UI.call_add, 'l': UI.call_list,
                    'c': UI.call_complete, 'd': UI.call_delete,'addh':UI.call_help,'completeh':UI.call_help,'deleteh':UI.call_help,'listh':UI.call_help}

        def default():
            print('not applicable choice, refer help by running with no argument')
        result = choice.get(inputs[0], default)
        result()
    else:
        print(help_guide)

except AnyPossibleError:
    print('Invalid Command please refer help by running with no argument')
