# contains definitions of the possible inputs to keep track of

# what items to let user add to database
options = {
    'alarm': ['date', 'time'],
    'micro-habit': ['habit'],
    'reminder': ['date', 'time', 'text'],
    'todo': ['date', 'time', 'text', 'priority'],
}

# type of input each field of each item is
input_types = {
    'alarm': ['date', 'time'],
    'micro-habit' : ['text'],
    'reminder': ['date', 'time', 'text'],
    'todo': ['date', 'time', 'text', 'number'],
}
