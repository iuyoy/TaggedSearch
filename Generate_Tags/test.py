



keys = ['type','id'\
        ,{'labels':{'zh-hans':'value','zh-cn':'value','zh':'value','en':'value'}\
        ,'descriptions':{'zh-hans':'value','zh-cn':'value','zh':'value'}\
        #aliases???????ид??
        ,'aliases':{'zh-hans':'value','zh-cn':'value','zh':'value'}\
        ,'claims':\
            #?б┬??property???????ид??
            {'p910':{'mainsnak':{'datavalue':{'value':['entity-type','numeric-id']}}}\
            ,'p279':{'mainsnak':{'datavalue':{'value':['entity-type','numeric-id']}}}\
            ,'p31':{'mainsnak':{'datavalue':{'value':['entity-type','numeric-id']}}}\
            ,'p361':{'mainsnak':{'datavalue':{'value':['entity-type','numeric-id']}}}\
            }\
        }]

labels = ['zh-hans','zh-cn','zh','en']
descriptions = ['zh-hans','zh-cn','zh']
aliases = ['zh-hans','zh-cn','zh']
claims = {'p910':'?б┬бд??ид','p279':'???ид','p31':'????','p361':'????'}
properties = ['mainsnak','datavalue','value',['entity-type','numeric-id']]
keys = {'type':'','id':'','labels':labels,'descriptions':descriptions,'aliases':aliases,'claims':claims}
def traverse_list(wiki_dict):
    for key in keys:
        if (wiki_dict.has_key(key)):
            if(key == 'type' or key == 'id'):
                self.analyse_format[key] = wiki_dict[key]
            if(key == 'labels' or key == 'descriptions'):
                for sub_key in keys[key]:
                    if wiki_dict[key].has_key(sub_key):
                        self.analyse_format[key] = wiki_dict[key][sub_key]['value']
            if(key == 'aliase'):
                for sub_key in keys[key]:
                    if wiki_dict[key].has_key(sub_key):
                        for sub_dict in wiki_dict[key][sub_key]:
                            self.analyse_format[key].append(sub_dict['value'])
            if(key == 'claims'):
                for sub_key in keys[key]:
                    if wiki_dict[key].has_key(sub_key):
                        for sub_dict in wiki_dict[key][sub_key]:
                            self.analyse_format[claims[sub_key]].append(sub_dict['mainsnak']['datavalue']['value']['entity-type'])
                            self.analyse_format[claims[sub_key]].append(sub_dict['mainsnak']['datavalue']['value']['numeric-id'])