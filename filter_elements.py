#!/usr/bin/env python

"""filter_elements.py: searches elements for specific terms and activates them """

__author__      = "Michael Brunner"
__copyright__   = "Copyright 2022, Cadwork Holz AG"
__maintainer__  = "Michael Brunner"
__email__       = "brunner@cadwork.swiss"
__license__     = "MIT License Agreement"
__version__     = "1.0"
__status__      = "Release"

#---------------------------------------------------------------

import      utility_controller         as uc
import      element_controller         as ec
import      cadwork                    as cw
import      attribute_controller       as ac
import      re
import      visualization_controller   as vc
import      tkinter
import      tkinter.messagebox
from        collections import defaultdict


def main(message):
    
    active_element_ids  = ec.get_active_identifiable_element_ids()
    visible_element_ids = ec.get_visible_identifiable_element_ids()
    
    len_active_element_ids  = len(active_element_ids)
    len_visible_element_ids = len(visible_element_ids)
    
    if len_active_element_ids != 0 and len_active_element_ids != len_visible_element_ids:
        var :bool = uc.get_user_bool(message[1], True)
        if var:
            element_ids = active_element_ids
        else:
            element_ids = visible_element_ids
    else:
        element_ids = visible_element_ids
    
    if len(element_ids) == 0:
        warning_msg(message[0])
        exit()
 
    vc.set_inactive(element_ids)
    
    uc.disable_auto_display_refresh()
   
    names = list(map(get_name, element_ids))

    elements = list()
    
    find_word = uc.get_user_string(message[2])
    if find_word == '':
        exit(1)
        
    search = re.split(', |;|,|\s', find_word) 
    search = list(map(str.lower, search))
       
    for n, e in zip(names, element_ids):
        if any(x in n for x in search): 
            elements.append(e)
        else:
            continue
    
    if not elements:
        warning_msg(message[3])
                 
    uc.enable_auto_display_refresh()
    vc.set_active(elements)
    info_msg(f"{len(elements)} {message[4]} ")
    
    return None
   

#---------------------------------------------------------------
def get_message_lang():
    # language dictionary
    language_dict = defaultdict(list)
    language_dict['en'] = ['No elements are active/visible!', 'Should only active elements be considered?', 'Enter search term', 'Names not found', ' Elements found']
    language_dict['de'] = ['Es sind keine Elemente aktiv/sichtbar!', 'Sollen nur aktive Elemente berücksichtigt werden?', 'Suchbegriff eingeben', 'Namen nicht gefunden!', ' Elemente gefunden']
    language_dict['fr'] = ["Aucun élément n'est actif/visible !", 'Seuls les éléments actifs doivent-ils être pris en compte ?','Saisir un mot-clé', 'Noms non trouvés', ' Éléments trouvés']

    if uc.get_language() == 'de':
        return language_dict['de']
    elif uc.get_language() == 'fr':
        return language_dict['fr']
    else:
        return language_dict['en']
    
def warning_msg(message):
    root = tkinter.Tk()
    root.withdraw()
    tkinter.messagebox.showerror(title= "Achtung",message = message)
    root.destroy()
    
def info_msg(message):
    root = tkinter.Tk()
    root.withdraw()
    tkinter.messagebox.showinfo(title= "Information",message = message)
    root.destroy()
    
def get_name(element:int) -> str:
    name = ac.get_name(element)
    return name.lower()
        

if __name__ == '__main__':
    main(message=get_message_lang())
    
