# python automation and personal assistant server (PAAPAS)
## ui
### /add/<add_type>
add_type is one of: 'alarm', 'reminder', 'todo'  
displays a form with inputs for specified add_type, see _input_types_  
will add to form data to mongodb  
## api
### /api/add
accepts a json request with the following structure:  
{  
'type': one of 'alarm', 'reminder', 'todo',  
various other parameters based on type, see _input_types_  
}  
will add data to mongodb if json is valid  
will return json status with 'success' and 'reason' if failure
