# !!!
from html import escape

def build_form(elements):
  form_html = '<form>\n'
  for element in elements:
    if element.startswith('text:'):
      _, label, name = element.split(':')
      form_html += f'  <label for="{name}">{label}:</label><br>\n'
      form_html += f'  <input type="text" id="{name}" name="{name}"><br><br>\n'
    elif element.startswith('radio:'):
      _, label, name, *options = element.split(':')
      form_html += f'  <label>{label}:</label><br>\n'
      for option in options:
        form_html += f'  <input type="radio" name="{name}" value="{option}">{option}<br>\n'
      form_html += '  <br>\n'
  form_html += '  <input type="submit" value="Submit">\n'
  form_html += '</form>'
  return form_html

def create_form( form_data, db_hook ):
    #print( form_data[ 'Form_Name' ] )  
    #print( type(form_data  ))  
    #print( db_hook )
    #print( type(db_hook ) )
    fn = form_data[ 'Form_Name' ].lower()
    form = f"<form method='post' id='new_{ fn }' action='/{ db_hook }/{ fn }' enctype='application/json' onsubmit='assign_hidden_inputs()'>"
    
    for i in range(1, 16):
        input_name = form_data.get(f"input{i}")
        if input_name:
            form += f"<label for='{input_name}'>{input_name}:</label><br>"
            form += f"<input type='text' id='{input_name}' name='{input_name}'><br>"
    form += "<input type='submit' value='Submit'>"
    form += "</form>"
    return form

Path = "./templates/form/"
def Save_Form_HTML( HTML, name ):
    #try:
    name = str( name ) + ".html"

    # Open the file in write mode
    with open( Path + name, 'w' ) as file:
        # Write the 1content of the file
        file.write( HTML )
    return True
    #except:
    return False
# !!!