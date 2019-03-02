import argparse
import pandas as pd
from collections import defaultdict
from ToDoClass import *
parser = argparse.ArgumentParser()
parser.add_argument('echo', nargs='*', default=None)
help_guide='\nPlease refer to the following commands\
            \na: add an item to the todolist (for help run todo addhelp)\
            \nl: list items from the todolist (for help run todo listhelp)\
            \nc: mark an item as complete (for help run todo completeh)\
            \nd: delete an item from the todolist (for help run tododeleteh)\n'
add_help='\nPlease try input in the following format for a successful entry\
            \na +(project name or names if any) message @(context if\
                any) due due_date (today/tomorrow or any valid DD MON)\
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

if __name__=='__main__':
    class UserInteraction:

        def __init__(self,inputs,command):
            self.input_command=' '.join(command)
            self.input_args =inputs
        
        def call_help(self):
                print(help_guide)

        def call_add(self):
            if(len(self.input_command) != 0):
                #print(self.input_command)
                #input_statement = ' '.join(i for i in self.input_command)
                todo.add_todo(self.input_command)
            else:
                print('not valid input, please refer help by running todo help add')

        def call_list(self, *args):
            def call_check_by_due_date():
                check_by_due_date(inputs)

            def call_check_project_context():
                check_project_context(inputs)

            def no_function():
                raise AnyPossibleError

            def list_one_argument():
               """ calling_func = {'all': todo.list_todo,
                                'overdue': todo.list_by_overdue}
                call_method = calling_func.get(
                    inputs[1], call_check_project_context)
                call_method()"""
                #calling_func_dict=defaultdict(lambda:1)




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

        def call_complete(self):
            if(todo.check_valid_input(self.input_command)):
                todo.complete_todo(self.input_command)
            else:
                print('\nElement not present in the list, please insert valid entry\
                    \nrun todo help add for more\n')

        def call_delete(self):
            if(todo.check_valid_input(self.input_command)):
                todo.delete_todo(self.input_command)
            else:
                print('\nElement not present in the list, please insert valid entry\
                    \nrun todo help del for more\n')
             
        def call_command_help(self):
            help_dict=defaultdict(lambda: help_guide)
            help_dict['add']=add_help
            help_dict['del']=delete_help
            help_dict['list']=list_help
            help_dict['comp']=complete_help
            print(help_dict[self.input_command])


    args = parser.parse_args()
    if(args.echo != []):
        inputs = args.echo
        UI = UserInteraction(inputs[0],inputs[1:])
        readdata = read_todo_file()
        todo = Todo(readdata)
        choice=defaultdict(lambda:UI.call_help)
        choice['[]']=UI.call_help
        choice['a']=UI.call_add
        choice['d']=UI.call_delete
        choice['c']=UI.call_complete
        choice['l']=UI.call_list
        choice['help']=UI.call_command_help
        choice[inputs[0]]()
    else:
        pass
        print(help_guide)