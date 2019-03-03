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
            \na +(project name or names if any) message @(context if any) \
                due due_date (today/tomorrow or any valid DD MON)\
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
                print('\nnot valid input, please refer help by running todo help add\n')

        def call_list(self, *args):
                #calling_func_dict=defaultdict(lambda:1)
            list_choices={   'all':todo.list_todo\
                            ,'by project':todo.list_by_project\
                            ,'by context':todo.list_by_context\
                            ,'overdue':todo.list_by_overdue\
                            ,'archived':display_archived    
                            }
            result_list_function=list_choices.get(self.input_command,UI.call_check_project_context)
            result_list_function()


        def call_complete(self):
            if(todo.check_valid_input(self.input_command)):
                todo.complete_todo(self.input_command)
            else:
                print('\nElement not present in the list, please insert valid serial number\
                    \nrun todo help add for more\n')

        def call_delete(self):
            if(todo.check_valid_input(self.input_command)):
                todo.delete_todo(self.input_command)
            else:
                print('\nElement not present in the list, please insert valid serial number\
                    \nrun todo help del for more\n')
        
        def call_archive(self):
            if(todo.check_valid_input(self.input_command)):
                todo.archive_todo(int(self.input_command))
            else:
                print('\nElement not present in the list, please insert valid serial number\
                    \nrun todo help arc for more\n')
        def call_extend(self):
            valid_flag,serial_number,new_date=todo.check_valid_extend(self.input_command)
            if(valid_flag):
                todo.extend_todo(serial_number,new_date)
            else:
                print('\nIncorrect details, make sure you give right serial_number\
 and date, run todo help ext for more\n')

        def call_check_project_context(self):
                if(self.input_command.split(' ')[0]=='due'): #check if it's for a day/date
                    search_str='(today|tomorrow|[\d]{1,2}\s[jan,feb,mar\,apr,may,jun,jul,aug,sep,oct,nov,dec]{3})'
                    if(len(re.findall(search_str,self.input_command))>0):
                        date_search=re.findall(search_str,self.input_command)[0]
                        todo.list_by_duedate(date_search)
                    else:
                        print('not a valid choice, try with a different due [value]')
                else: #check for project or context
                    value_type,check_result=check_project_context(self.input_command)
                    if(check_result=='False'):
                        print('couldn\'t find any thing like this')
                    else:
                        if(value_type=='project' and todo.check_valid_project_name(check_result)):
                            todo.list_by_project_name(check_result)
                        elif(value_type=='context' and todo.check_valid_context_name(check_result)):
                            todo.list_by_context_name(check_result)
                        else:
                            print('No such project/context/option exist, run todo help list for more')

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
        #choice['[]']=UI.call_help
        choice['a']=UI.call_add
        choice['d']=UI.call_delete
        choice['c']=UI.call_complete
        choice['l']=UI.call_list
        choice['e']=UI.call_extend
        choice['ar']=UI.call_archive
        choice['help']=UI.call_command_help
        choice[inputs[0]]()
    else:
        print(help_guide)