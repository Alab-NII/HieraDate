import date_support as date_sup

def convert_tups2dict(tups):
	dict_ = dict()
	for tup in tups:
		if tup[0] in dict_.keys():
			dict_[tup[0]].append(tup[1])
		else:
			dict_[tup[0]] = [tup[1]]
	return dict_


def check_group(question, group_small, group_large, templates_old):
    for ques in group_small:
        if ques in question.lower():
            return 1
    for ques in group_large:
        if ques in question.lower():
            return 2
    for ques in  templates_old:
        if ques in question.lower():
            return 3 
    return -1


def process_sps(sps):
    dic = {}
    for sp in sps:
        key_ = sp[0] # .lower()
        if key_ not in dic.keys():
            dic[key_] = [sp[1]]
        else:
            dic[key_].append(sp[1])
    return dic


def process_para_sp(paragraphs, sps):
    sents = {}
    for key in paragraphs:
        para = paragraphs[key]
        sp = sps[key]
        if 0 not in sp:
            sp.append(0)
        if 1 not in sp and len(para) > 2:
            sp.append(1)
        text = ''
        for idx in sp:
            if idx < len(para):
                text += para[idx]   
        sents[key] = text
    return sents      


def process_evidence(evidences):
    names = dict()
    for evi in evidences:
        if evi[0] not in names.keys():
        #
            if evi[1] == 'date of birth':
                dic = {}
                dic['date_of_birth']= evi[2]
            
                names[evi[0]] = dic
            if evi[1] == 'date of death':
                dic = {}
                dic['date_of_death']= evi[2]
            
                names[evi[0]] = dic
        else:
            if evi[1] == 'date of birth':
                names[evi[0]]['date_of_birth'] = evi[2]
            if evi[1] == 'date of death':
                names[evi[0]]['date_of_death'] = evi[2]
    #
    return names


def choose_dict(wikidata_items, id_, evidences, relation_id, dict_names):
    relations = convert_tups2dict(wikidata_items[id_]['relations'])
    values = relations[relation_id]
    if len(values) == 1:
        return values[0]
    else:
        label = wikidata_items[id_]['label']
        date_ = ''
        if label in dict_names.keys():
            if relation_id == 'P569':
                date_ = dict_names[label]['date_of_birth']
            elif relation_id == 'P570':
                date_ = dict_names[label]['date_of_death']
        for value in values:
            list_str = date_sup.convert_date2str(value)
            if date_ in list_str:
                return value
    return values[0]


def choose_date_of_death(wikidata_items, id_, infor, relation_id='P570'):
    relations = convert_tups2dict(wikidata_items[id_]['relations'])
    if relation_id not in relations.keys():
        return {}
    values = relations[relation_id]
    #
    label = wikidata_items[id_]['label']
    # print(label.lower())
    # print(infor['name'].lower())
    # assert infor['name'].lower() in label.lower()
    #
    if len(values) == 1:
        list_str = date_sup.convert_date2str(values[0])
        for ele in list_str:
            if ele in infor['text']:
                infor['date_of_death_str'] = ele
                infor['date_of_death'] = values[0]
                return infor        
    else:
        for value in values:
            list_str = date_sup.convert_date2str(value)
            for ele in list_str:
                if ele in infor['text']:
                    infor['date_of_death_str'] = ele
                    infor['date_of_death'] = value
                    return infor
    if id_ == "Q7377809":
        print(infor)    
    return {}



def get_infor(wikidata_items, evidences, entity_ids):
    id1, id2 = entity_ids.split("_")
    infor_1, infor_2 = {}, {}
    infor_1['name'] = ''
    infor_2['name'] = ''
    #
    dict_names = process_evidence(evidences)
    if len(evidences) == 4:
        #
        #
        infor_1['date_of_birth'] = choose_dict(wikidata_items, id1, evidences, 'P569', dict_names) 
        infor_1['date_of_death'] = choose_dict(wikidata_items, id1, evidences, 'P570', dict_names) 
        #
        infor_2['date_of_birth'] = choose_dict(wikidata_items, id2, evidences, 'P569', dict_names) 
        infor_2['date_of_death'] = choose_dict(wikidata_items, id2, evidences, 'P570', dict_names) 
        #
        # hard code
        if id1 == 'Q11941050':
            infor_1['date_of_birth']['day'] = 0
            infor_1['date_of_birth']['month'] = 0
            #
            infor_1['date_of_death']['day'] = 0
            infor_1['date_of_death']['month'] = 0  
        #
        if id1 == 'Q1369206':
            infor_1['date_of_birth']['month'] = 0
            
        if id1 == 'Q15300579':
            infor_1['date_of_death']['day'] = 18
            infor_1['date_of_death']['month'] = 3
            infor_1['date_of_death']['year'] = 1969
        #
        if id2 == 'Q3470342':
            infor_2['date_of_death']['year'] = 1947
        if id2 == 'Q4867098':
            infor_2['date_of_death']['day'] = 27
        #
        if id2 == 'Q18527076':
            infor_2['date_of_birth']['day'] = 16
            infor_2['date_of_birth']['month'] = 7
            infor_2['date_of_death']['day'] = 20
            infor_2['date_of_death']['month'] = 11        
        if id2 == 'Q3271704':
            infor_2['date_of_birth']['month'] = 0
        if id2 == 'Q1961244':
            infor_2['date_of_birth']['day'] = 29
            infor_2['date_of_birth']['month'] = 1
            infor_2['date_of_birth']['year'] = 1580
            #
            infor_2['date_of_death']['day'] = 31
            infor_2['date_of_death']['month'] = 5     
        if id2 == 'Q119968':
            infor_2['date_of_death']['day'] = 5 
        if id2 == 'Q18576661':
            infor_2['date_of_death']['year'] = 1954
        #
        date_str_1_birth = date_sup.convert_date2str(infor_1['date_of_birth'])
        date_str_1_death = date_sup.convert_date2str(infor_1['date_of_death'])
        date_str_2_birth = date_sup.convert_date2str(infor_2['date_of_birth'])
        date_str_2_death = date_sup.convert_date2str(infor_2['date_of_death'])
        #
        for name in dict_names:
            birth = dict_names[name]['date_of_birth']
            death = dict_names[name]['date_of_death']
            if birth in date_str_1_birth and death in date_str_1_death:
                infor_1['name'] = name.title()
            if birth in date_str_2_birth and death in date_str_2_death:
                infor_2['name'] = name.title()
    #
    elif len(evidences) == 2:
        relation = evidences[0][1]
        if relation == 'date of death':
            # infor_1['date_of_death'] = wikidata_id1['P570'][0]
            # infor_2['date_of_death'] = wikidata_id2['P570'][0]
            infor_1['date_of_death'] = choose_dict(wikidata_items, id1, evidences, 'P570', dict_names) 
            #
            infor_2['date_of_death'] = choose_dict(wikidata_items, id2, evidences, 'P570', dict_names) 
            # hard-code ---- these cases are need to update in 2WikiMultihopQA
            if id1 == 'Q1584707':
                infor_1['date_of_death']['day'] = 27
                infor_1['date_of_death']['month'] = 3
                infor_1['date_of_death']['year'] = 1564
            #            
            if id2 == 'Q652253': 
                infor_2['date_of_death']['day'] = 25
                infor_2['date_of_death']['month'] = 2
                infor_2['date_of_death']['year'] = 2004
            
            if id1 == 'Q3712924':
                infor_1['date_of_death']['day'] = 9
                infor_1['date_of_death']['month'] = 7
                infor_1['date_of_death']['year'] = 2019
            if id2 == 'Q6793514':
                infor_2['date_of_death']['day'] = 1
                infor_2['date_of_death']['month'] = 3
                infor_2['date_of_death']['year'] = 1965
            #
            #
            date_str_1_death = date_sup.convert_date2str(infor_1['date_of_death'])
            date_str_2_death = date_sup.convert_date2str(infor_2['date_of_death'])
            for name in dict_names:
                death = dict_names[name]['date_of_death']
                if death in date_str_1_death:
                    infor_1['name'] = name.title()
                if death in date_str_2_death:
                    infor_2['name'] = name.title()
        elif relation == 'date of birth':
            # infor_1['date_of_birth'] = wikidata_id1['P569'][0]
            # infor_2['date_of_birth'] = wikidata_id2['P569'][0]
            #
            infor_1['date_of_birth'] = choose_dict(wikidata_items, id1, evidences, 'P569', dict_names) 
            infor_2['date_of_birth'] = choose_dict(wikidata_items, id2, evidences, 'P569', dict_names) 
            # hard-code
            if id1 == 'Q8046469':
                infor_1['date_of_birth']['day'] = 22
                infor_1['date_of_birth']['month'] = 11
                infor_1['date_of_birth']['year'] = 1990  
            if id1 == 'Q176743':
                infor_1['date_of_birth']['month'] = 9              
            if id1 == 'Q3173178':
                infor_1['date_of_birth']['day'] = 26
                infor_1['date_of_birth']['month'] = 2              
            #
            if id2 == 'Q2914570':
                infor_2['date_of_birth']['day'] = 17
            if id2 == 'Q14501054':
                infor_2['date_of_birth']['year'] = 1992
            if id2 == 'Q6509729':
                infor_2['date_of_birth']['month'] = 4
            if id2 == 'Q6142804':
                infor_2['date_of_birth']['year'] = 1954
            #
            date_str_1_birth = date_sup.convert_date2str(infor_1['date_of_birth'])
            date_str_2_birth = date_sup.convert_date2str(infor_2['date_of_birth'])
            for name in dict_names:
                birth = dict_names[name]['date_of_birth']
                if birth in date_str_1_birth:
                    infor_1['name'] = name.title()
                if birth in date_str_2_birth:
                    infor_2['name'] = name.title()
    return infor_1, infor_2


def copy_dict_few_keys(dic):
    wanted_keys = ['year', 'month', 'day']
    new_dict = {k: dic[k] for k in set(wanted_keys) & set(dic.keys())}
    return new_dict

