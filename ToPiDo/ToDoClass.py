import csv
import re
import datetime
from termcolor import colored



class Todoitems():
    serial_num = 0
    status = ''
    date = ''
    message = ''

    def __init__(self, serial_num, status, date, message, project='Default project', context='sample context'):
        self.serial_num = int(serial_num)
        self.status = status
        self.date = date
        self.message = message
        self.project = project
        self.context = context


class Todo():
    def __init__(self, items_list):
        self.items_list = items_list

    def list_todo(self):
        """Displays all the todo items without any filtering"""
        display_todo(self.items_list)

    def add_todo(self, inpt_stmt):
        """adds the input to the to do list"""
        duedate_current, message, projects, context = add_todo_parser(inpt_stmt)
        todo = Todoitems(get_todo_count(), 'incomplete',duedate_current, message, str(projects), str(context))
        self.items_list.append(todo)
        write_todo_file(self.items_list)
        print('\nTask added successfully\n')

    def complete_todo(self, serial_number):
        
        """Completes a todo after taking it's serial number as input"""
        serial_num = int(serial_number)
        items = []
        for item in self.items_list:
            if(item.serial_num == int(serial_num)):
                item.status = 'complete'
            items.append(item)
        print('Task marked complete')
        write_todo_file(items)

    def delete_todo(self, serial_number):
        """Deletes a todo item from the list using the given serial number"""
        serial_num = int(serial_number)
        items = []
        for item in self.items_list:
            if(item.serial_num != int(serial_num)):
                items.append(item)
        print('Task deleted')
        write_todo_file(items)
    
    def extend_todo(self,serial_num,new_due_date):
        items=[]
        for item in self.items_list:
            if(item.serial_num==int(serial_num)):
                item.date=new_due_date
            items.append(item)
        write_todo_file(items)
    
    def list_by_project(self):
        """Lists all the todo Items on the basis of project names"""
        avail_project = get_project_names(self.items_list)
        projects = sorted(avail_project)
        for project in projects:
            print(project)
            for item in self.items_list:
                temp_list = []
                if(project in item.project.split('|')):
                    temp_list.append(item)
                display_todo(temp_list)

    def list_by_status(self):
        """displays all the todo items ordering the completed and then the incomplete"""
        avail_status_complete = []
        avail_status_incomplete = []
        for item in self.items_list:
            if(item.status == 'complete'):
                avail_status_complete.append(item)
            else:
                avail_status_incomplete.append(item)
        print('Complete')
        display_todo(avail_status_complete)
        print('Incomplete')
        display_todo(avail_status_incomplete)

    def list_by_project_name(self, project_name):
        """Displays records for a particular project"""
        avail_projects = get_project_names(self.items_list)
        projects = []
        if project_name.lower() not in avail_projects:
            print('project not present, try again')
        else:
            for item in self.items_list:
                if(project_name.lower() in item.project.split('|')):
                    projects.append(item)
            print(project_name)
            display_todo(projects)

    def list_by_duedate(self, due_dates):
        due_dates=[items for items in due_dates.split(' ')]
        """Display the records based on a due date"""
        if(check_date(due_dates) != 'no error'):
            print(check_date(due_dates))
        else:
            due_date = due_dates
            validdays = ['today', 'tom', 'tomorrow']
            items = []
            if(due_date[0] in validdays and due_date[0] == 'tom'):
                due_date[0] = 'tomorrow'
                # print(due_date[0])
                for item in self.items_list:
                    if(item.date == due_date[0]):
                        items.append(item)
                display_todo(items)
            else:
                due_date = ' '.join(item for item in due_date)
                items = []
                for item in self.items_list:
                    if(item.date == due_date):
                        items.append(item)
                if(len(items) > 0):
                    display_todo(items)
                else:
                    print('No todo for given date found')

    def list_by_overdue(self):
        items_dict={'pending':[],'today':[],'tomorrow':[],'other':[]}
        for items in self.items_list:
            if(items.status=='incomplete'):
                if items.date not in ['today','tomorrow']:
                    now=datetime.datetime.now().date()
                    item_due_date=datetime.datetime.strptime(items.date+' 2019','%d %b %Y').date()
                    if(item_due_date<now):
                        items_dict['pending'].append(items)
                    else:
                        items_dict['other'].append(items)
                else:
                    if items.date=='today':
                        items_dict['today'].append(items)
                    elif items.date=='tomorrow':
                        items_dict['tomorrow'].append(items)
        for key,val in items_dict.items():
            display_todo(val)

    def list_by_context(self):
        """Display all the todo Items on basis of context"""
        contexts = []
        for item in self.items_list:
            if(len(re.findall('|', item.context)) != 0):
                values = item.context.split('|')
                contexts.extend(values)
        contexts = sorted(set(contexts))
        for context in contexts:
            display_item = []
            print(context)
            for item in self.items_list:
                if(context in item.context.split('|')):
                    display_item.append(item)
            display_todo(display_item)

    def list_by_context_name(self, context_name):
        """Display the ToDo items based on a context"""
        display_items=[]
        print(context_name)
        for item in self.items_list:
            if(context_name.lower() in item.context.split('|')):
                display_items.append(item)
        display_todo(display_items)

    def archive_todo(self,serial_num):
        items=[]
        print(type(serial_num))
        for item in self.items_list:
            if(item.serial_num==serial_num):
                #items.append(item)
                write_archive_file(item)
            else:
                items.append(item)
        write_todo_file(items)
            
    def check_valid_input(self,input_val):
        input_val=[input_val]
        """To see if provided input for delete or complete is valid or not"""
        if(len(input_val) > 1):
            return False
        else:
            if(input_val[0].isdigit()):
                input_val = int(input_val[0])
                avail_serial_num = []
                for item in self.items_list:
                    avail_serial_num.append(int(item.serial_num))
                if input_val in avail_serial_num:
                    return True
                else:
                    return False
            else:
                return False
    
    def check_valid_project_name(self,input_val):
        """Get whether the given project name is valid or not"""
        projects = get_project_names(self.items_list)
        if input_val.lower() not in projects:
            print('\nChoose one of the avaliable projects: '+str(projects)+'\n')
            return False
            
        else:
            return True

    def check_valid_context_name(self,input_val):
        """Check if the context given to search is valid or not"""
        avail_contexts = []
        final_context_avail = []
        for item in self.items_list:
            avail_contexts.append(item.context) #collect all contexts
        for item in avail_contexts:
            contexts = item.split('|') #split ones with multiple contexts
            for context in contexts:
                final_context_avail.append(context)
        final_context_avail = set(final_context_avail) #keep single entries
        if(input_val.lower() not in final_context_avail):
            return False
        else:
            return True

    def check_valid_extend(self,input_statement):  
        try:    
            input_command=input_statement.split('set due')
            if(len(input_command)>1):
                serial_number_string=input_command[0]
                new_due_date_string=str(input_command[1:])
                serial_number=0
                search_str='(tomorrow|(\d{2})\s[jan,feb,mar,apr,may,jun,jul,aug,sep,oct,nov,dec]{3})'
                new_due_date=(re.findall(search_str,new_due_date_string)[0][0])
                if(len(re.findall('[\d]{2}',serial_number_string))>0 and \
                    re.search(search_str,new_due_date_string)!=None and check_date(new_due_date.split(' '))):

                        serial_number=int(re.findall('[\d]{2}',serial_number_string)[0])
                        return True,serial_number,new_due_date
                else:
                    raise Exception
            else:
                raise Exception
        except:
                return False,None,None

def display_todo(args):
    """To display all the todo items given in the input in form of a list""" 
    for display_item in args:
        if(display_item.status == 'complete'):
            display_item.symbol = '[x]'
            display_item.symbol = colored(display_item.symbol,'green')
        elif(display_item.status == 'incomplete'):
            display_item.symbol = '[ ]'
            display_item.symbol = colored(display_item.symbol,'white')
        print('{0:<10}{1:20}{2:30}{3:20}'.format(display_item.serial_num, display_item.symbol,
                                                        display_item.date, colored(display_item.message,'blue')))

def display_archived():
    with open('archive.csv') as file:
        today,tomorrow=get_today_tomorrow()
        csvreader = csv.DictReader(file, delimiter=',')
        items = []
        for row in csvreader:
            if(row['date']==today):
                row['date']='today'
            elif(row['date']==tomorrow):
                row['date']='tomorrow'
            #colored_date=colored(display_item.serial_num,'yellow')
            item = Todoitems(row['serial_num'], row['status'], row['date'],
                            row['message'], row['project'], row['context'])
            items.append(item)
    display_todo(items)

def write_archive_file(args):
    item=args
    today,tomorrow=get_today_tomorrow()
    with open('archive.csv', 'a') as file:
        field_names = ['serial_num', 'status',
                    'date', 'project', 'context', 'message']
        csvwriter = csv.DictWriter(file, fieldnames=field_names)
        if(item.date=='today'):
            item.date=today
        elif(item.date=='tomorrow' or item.date=='tom'):
            item.date=tomorrow
        csvwriter.writerow({'serial_num': item.serial_num, 'status': item.status, 'date': item.date.lower(),
                            'project': item.project.lower(), 'context': item.context.lower(), 'message': item.message})

def write_todo_file(args):
    """Write all the items to the file, based on the input that is a list of items"""
    today,tomorrow=get_today_tomorrow()
    with open('items.csv', 'w') as file:
        field_names = ['serial_num', 'status',
                    'date', 'project', 'context', 'message']
        csvwriter = csv.DictWriter(file, fieldnames=field_names)
        csvwriter.writeheader()
        for item in args:
            if(item.date=='today'):
                item.date=today
            elif(item.date=='tomorrow' or item.date=='tom'):
                item.date=tomorrow
            #print(str(item.serial_num)+' '+item.status+' '+item.date+' '+item.project+' '+item.message)
            csvwriter.writerow({'serial_num': item.serial_num, 'status': item.status, 'date': item.date.lower(),
                                'project': item.project.lower(), 'context': item.context.lower(), 'message': item.message})

def read_todo_file():
    """Reads all the records from the file and return them as a list"""
    with open('items.csv') as file:
        today,tomorrow=get_today_tomorrow()
        csvreader = csv.DictReader(file, delimiter=',')
        items = []
        for row in csvreader:
            if(row['date']==today):
                row['date']='today'
            elif(row['date']==tomorrow):
                row['date']='tomorrow'
            #colored_date=colored(display_item.serial_num,'yellow')
            item = Todoitems(row['serial_num'], row['status'], row['date'],
                            row['message'], row['project'], row['context'])
            items.append(item)
        return items

def get_today_tomorrow():
    """Extract the value of today and tomorrow to display records accordingly"""
    now=datetime.datetime.now()
    today_day=str(now.day)
    today_month=str(now.strftime("%b").lower())
    today=today_day+' '+today_month
    now+=datetime.timedelta(days=1)
    tomorrow_day=str(now.day)
    tomorrow_month=str(now.strftime("%b").lower())
    tomorrow=tomorrow_day+' '+tomorrow_month
    return today, tomorrow

def get_todo_count():
    """Get the count for total number of items in the todo"""
    current_id = 0
    with open('items.csv', 'r') as file:
        content = csv.DictReader(file, delimiter=',')
        for rows in content:
            current_id = int(rows['serial_num'])
    current_id += 1
    return current_id

def get_date(args):
    """Returns a string of the date from the input"""
    date = ' '.join(item for item in args)
    return str(date)

def get_project_names(args):
    """Get list of all the available project names"""
    avail_project = []
    for item in args:
        avail_project.append(item.project)
    for item in avail_project:
        if('|' in item):
            values = item.split('|')
            for value in values:
                avail_project.append(value)
    projects = set()
    for item in avail_project:
        if('|' not in item):
            projects.add(item)
    return projects

def check_date(args):
    """Checks the date to see if it's valid or not"""
    due_date = args
    valid_day = ['today', 'tom', 'tomorrow']
    if((len(due_date) == 1) and (due_date[0] in valid_day)):
        return 'no error'
    elif(len(due_date) == 2):
        valid_days = range(1, 32)
        valid_months = ['jan', 'feb', 'mar', 'apr', 'may',
                    'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
        day = 0
        if(due_date[0].isdigit()):
            day = int(due_date[0])
        else:
            return 'Not correct format, please enter due-date in form of dd mon'
        month = str(due_date[1].lower())
        if(day in valid_days and month in valid_months):
            if(month == 'feb'):
                if (day in range(1, 29)):
                    return 'no error'
                else:
                    return 'The day doesn\'t exist in feb'
            else:
                return 'no error'
        else:
            return 'Not a valid entry, please insert in the form of dd mon'

    else:
        return 'Not a valid entry, please insert in the form of dd mon'

def check_project_context(inputstmt):
    """Check if the given input can be a project name or a context"""
    FirstChar = re.findall('[@]', inputstmt)
    if(len(FirstChar) == 1 and inputstmt.index('@') == 0):
        context_name = inputstmt[1:]
        return 'context',context_name
    else:
        FirstChar=re.findall('[+]', inputstmt)
        if(len(FirstChar) == 1 and inputstmt.index('+') == 0):
            project_name = inputstmt[1:]
            return 'project',project_name
        else:
            return 'none',False

def get_context(inpt_statement):
    """Extracts the context out of the provided message"""
    context_strings = re.findall('[@][^\s]+', inpt_statement)
    contexts = []
    if(len(context_strings) >= 1):
        for item in context_strings:
            context = str(item[1:])
            contexts.append(context)
        if(len(contexts) >= 1):
            context = '|'.join(context for context in contexts)
    else:
        context = 'none'
    return context

def get_project(inpt_stmt):
    """Extracts the projects from the user input message"""
    project_strings = re.findall('[+][^\s]+', inpt_stmt)
    projects=[]
    if(len(project_strings) >= 1):
        for items in project_strings:
            project = str(items[1:])
            projects.append(project)
        if(len(projects) >= 1):
            projects = '|'.join(project for project in projects)
    else:
        print('no project found, setting to to personal')
        projects = 'personal'
    return projects

def get_duedate(inpt_stmt):
    """gets the word 'due' to find the due date and message"""
    input_message = inpt_stmt.split(' ')
    duedate_current = ''
    message=inpt_stmt

    if(inpt_stmt.find('due') > 0):
        due_indexes = []
        for words in range(len(input_message)):
            if input_message[words] == 'due':
                due_indexes.append(words)
        due_index = due_indexes[len(due_indexes)-1]
        message = ' '.join(msg for msg in input_message[0:due_index])
        duedate = [date for date in input_message[due_index+1:]]
        if(check_date(duedate) == 'no error'):
            duedate_current = get_date(duedate)
        else:
            print(check_date(duedate))
    else:
        print('no due found setting it for tomorrow')
        duedate_current = 'tomorrow'
    return duedate_current, message

def add_todo_parser(args):
    """runs all the needed methods to get the message, due date, project and context"""
    project = get_project(args)
    context = get_context(args)
    duedate, message = get_duedate(args)
    return duedate, message, project, context
