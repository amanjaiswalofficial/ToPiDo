import argparse
import sys
from collections import defaultdict
from ToDo import *
parser = argparse.ArgumentParser()
parser.add_argument('echo', nargs='*', default=None)
help_guide='\nPlease refer to the following commands\
            \na: add an item to the todolist (for help run todo help add)\
            \nl: list items from the todolist (for help run todo help list)\
            \nc: mark an item as complete (for help run todo help comp)\
            \nd: delete an item from the todolist (for help run todo help del)\
            \ne: extend an item to a new due date(for help run todo help ext)\
            \nf: archive an item for later(for help run todo help arch)\n'
add_help='\nPlease try input in the following format for a successful entry\
            \na +(project name or names if any) message @(context if any) \
due due_date (today/tomorrow or any valid DD MMM)\
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
            \n6. l overdue: to display all the todo that are remaining\
            \n7. l archived: to display the items from the archived list\n'
complete_help='\nPlease try the input in the following format for completing a task\
            \nc valid_todo_serial_number\
            \nEx- c 10\n'
extend_help='\nPlease try the input in the following format for extending due date of a task\
            \ne valid_todo_serial_number set due new_due_date (Tomorrow/Any other date)\
            \nEx- e 10 set due 21 aug\n'
archive_help='\nPlease try the input in the following format for archiving a task\
            \nar valid_todo_serial_number\
            \nEx- ar 10\n'

class UserInteractionHelper:
    """A helper class containing methods to call operations on ToDo"""
    def __init__(self,inputs,command):
        self.input_command=' '.join(command)
        self.input_args =inputs
    
    def call_help(self):
            print(help_guide)
    

    def call_add(self):
        if(len(self.input_command) != 0):
            todo.add_todo(self.input_command)
        else:
            print('\nnot valid input, please refer help by running todo help add\n')

    def call_list(self, *args):
        """Check for the input and call the specific list choice from ToDoClass"""
        list_choices={   'all':todo.list_todo\
                        ,'by project':todo.list_by_project\
                        ,'by context':todo.list_by_context\
                        ,'overdue':todo.list_by_overdue\
                        ,'archived':display_archived\
                        ,'pending':todo.list_pending    
                        }
        result_list_function=list_choices.get(self.input_command,UI.call_check_project_context)
        result_list_function()


    def call_complete(self):
        """Calls the method to mark a todo complete"""
        if(todo.check_valid_input(self.input_command)):
            todo.complete_todo(self.input_command)
        else:
            print('\nElement not present in the list, please insert valid serial number\
                \nrun todo help add for more\n')

    def call_delete(self):
        """Calls method to delete a todo"""
        if(todo.check_valid_input(self.input_command)):
            todo.delete_todo(self.input_command)
        else:
            print('\nElement not present in the list, please insert valid serial number\
                \nrun todo help del for more\n')
    
    def call_archive(self):
        """Calls archive method to send a todo to archived"""
        if(todo.check_valid_input(self.input_command)):
            todo.archive_todo(int(self.input_command))
        else:
            print('\nElement not present in the list, please insert valid serial number\
                \nrun todo help arc for more\n')

    def call_extend(self):
        """Calls extend method to change due date of a todo"""
        valid_flag,serial_number,new_date=todo.check_valid_extend(self.input_command)
        if(valid_flag):
            todo.extend_todo(serial_number,new_date)
        else:
            print('\nIncorrect details, make sure you give right serial_number\
and date, run todo help ext for more\n')

    def call_check_project_context(self):
        """Check if a project or context exist in provided"""
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
        """Displays help for the user input"""
        help_dict=defaultdict(lambda: help_guide)
        help_dict['add']=add_help
        help_dict['del']=delete_help
        help_dict['list']=list_help
        help_dict['comp']=complete_help
        help_dict['ext']=extend_help
        help_dict['arch']=archive_help
        print(help_dict[self.input_command])

if __name__=='__main__':
    try:
        args = parser.parse_args()
        if(args.echo != []):
            inputs = args.echo
            UI = UserInteractionHelper(inputs[0],inputs[1:])
            readdata = read_todo_file()
            todo = Todo(readdata)
            choice=defaultdict(lambda:UI.call_help)
            choice['a']=UI.call_add
            choice['d']=UI.call_delete
            choice['c']=UI.call_complete
            choice['l']=UI.call_list
            choice['e']=UI.call_extend
            choice['ar']=UI.call_archive
            choice['help']=UI.call_command_help
            choice[inputs[0]]()
        else:
            raise Exception
    except FileNotFoundError as error:
        print('Error: '+str(error))
    except:
        print(help_guide)