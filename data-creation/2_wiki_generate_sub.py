"""
Generate subquestions for 2Wiki 
"""
import copy
import random
from tqdm import tqdm
#
import file_utils as utils
import date_support as date_sup
from functions import *


# 2wikimultihop
type_ = 'dev'
filename = "data-preparation/date_2wiki/{}_line_update.json".format(type_)

data = utils.read_json_lines_return_list(filename)

wikidata_items = utils.read_json("data_inputs/wikidata_items_small.json")


# For extraction level
templates_birth = ['What is the birth date of #name?', "What's the birth date of #name?", \
    'What is the date of birth of #name?', "What's the date of birth of #name?", \
    'When was #name born?']


templates_death = ['What is the death date of #name?', "What's the death date of #name?", \
    'What is the date of death of #name?', "What's the date of death of #name?", \
    'When did #name die?']


# For robustness level
templates_ques = ['who was born first', 'who was born earlier', 'who was born later', \
    'who was born first out of', 'born first?', \
    'who died first', 'who died earlier', 'who died later', 'who lived longer']


count_extract = 0
count_robust = 0
count_reason = 0


# for reasoning level
reason_ques_old = 'How old was {} when they died?'
reason_ques_first = 'Does {} come before {}?'
reason_ques_later = 'Does {} come after {}?'

# label 1
group_small = ['who was born first', 'who was born earlier', 'who was born first out of', \
    'born first?', 'who died first', 'who died earlier']

# label 2
group_large = ['who was born later', 'who died later']

# label 3
templates_old = ['who lived longer']


for item in tqdm(data):
    # print(item['_id'])
    # only apply for 2Wiki
    if 'Who is younger' in item['question']:
        item['question'] = item['question'].replace("Who is younger", 'Who was born later', 1)
    #
    if 'Who is older' in item['question']:
        item['question'] = item['question'].replace("Who is older", 'Who was born first', 1)
    #
    evidences = item['evidences']
    # get two names
    names = set()
    for evi in evidences:
        names.add(evi[0].lower())    

    titles = set([sp[0] for sp in item['supporting_facts']])
    context = dict(item['context'])
    paragraphs = {title: context[title] for title in titles}
    
    entity_ids = item['entity_ids']
    # print(entity_ids)
    label_group = check_group(item['question'], group_small, group_large, templates_old)
    #
    infor_1, infor_2 = get_infor(wikidata_items, evidences, entity_ids)

    assert infor_1['name'] != ""
    assert infor_2['name'] != ""

    # For extraction level
    for idx, evi in enumerate(evidences):
        #
        if evi[1] == 'date of birth':
            template = random.choice(templates_birth)
            ques = template.replace("#name", evi[0].title(), 1)
            #
            extract_ques = 'ques_extract_{}'.format(idx+1)
            extract_ans = 'ans_extract_{}'.format(idx+1)
            extract_ans_date = 'ans_extract_{}_date'.format(idx+1)
            item[extract_ques] = ques
            item[extract_ans] = evi[2]
            count_extract += 1
            item[extract_ans_date] = ""
            if evi[0].lower() == infor_1['name'].lower():
                item[extract_ans_date] = copy_dict_few_keys(infor_1['date_of_birth'])
            if evi[0].lower() == infor_2['name'].lower():
                item[extract_ans_date] = copy_dict_few_keys(infor_2['date_of_birth'])
            assert item[extract_ans_date] != ""
        # 
        if evi[1] == 'date of death':
            template = random.choice(templates_death)
            ques = template.replace("#name", evi[0].title(), 1)
            #
            extract_ques = 'ques_extract_{}'.format(idx+1)
            extract_ans = 'ans_extract_{}'.format(idx+1)
            extract_ans_date = 'ans_extract_{}_date'.format(idx+1)
            item[extract_ques] = ques
            item[extract_ans] = evi[2]
            count_extract += 1
            item[extract_ans_date] = ""
            if evi[0].lower() == infor_1['name'].lower():
                item[extract_ans_date] = copy_dict_few_keys(infor_1['date_of_death'])
            if evi[0].lower() == infor_2['name'].lower():
                item[extract_ans_date] = copy_dict_few_keys(infor_2['date_of_death'])
            assert item[extract_ans_date] != ""

    # For reasoning level
    if label_group == 1 or label_group == 2:
        #
        if evidences[0][1] == 'date of birth': 
            infor_1['date'] = infor_1['date_of_birth']
            infor_2['date'] = infor_2['date_of_birth']
        elif evidences[0][1] == 'date of death': 
            infor_1['date'] = infor_1['date_of_death']
            infor_2['date'] = infor_2['date_of_death']
        #
        ans_value = date_sup.compare_two_dates(infor_1['date'], infor_2['date']) # Return 1 if dict_1 < dict_2
        # print(ans_value)
        assert ans_value != 2
        #
        str_date1 = date_sup.convert_date2str(infor_1['date'])[0]
        str_date2 = date_sup.convert_date2str(infor_2['date'])[0]
        if ans_value == 1:
            #
            item['ques_reason_1'] = reason_ques_first.format(str_date1, str_date2)
            item['ans_reason_1'] = 'yes'  
            count_reason += 1
            #
            item['ques_reason_2'] = reason_ques_later.format(str_date1, str_date2)
            item['ans_reason_2'] = 'no' 
            count_reason += 1
            #
            if label_group == 1: 
                # if item['answer'] != infor_1['name'].title():
                #     print(item['answer'])
                #     print(infor_1)
                #     print(infor_1['name'].title())
                assert item['answer'] == infor_1['name'].title()
            if label_group == 2: 
                # if item['answer'] != infor_2['name'].title():
                #     print(item['answer'])
                #     print(infor_2)
                #     print(infor_2['name'].title())
                assert item['answer'] == infor_2['name'].title()
        elif ans_value == -1:
            item['ques_reason_1'] = reason_ques_first.format(str_date1, str_date2)
            item['ans_reason_1'] = 'no'  
            count_reason += 1
            #
            item['ques_reason_2'] = reason_ques_later.format(str_date1, str_date2)
            item['ans_reason_2'] = 'yes'   
            count_reason += 1  
            if label_group == 1:   
                # if item['answer'] != infor_2['name'].title():
                #     print(item['answer'])
                #     print(infor_2)
                #     print(infor_2['name'].title())          
                assert item['answer'] == infor_2['name'].title()     
            if label_group == 2:   
                # if item['answer'] != infor_1['name'].title():
                #     print(item['answer'])
                #     print(infor_1)
                #     print(infor_1['name'].title())          
                assert item['answer'] == infor_1['name'].title() 

    if label_group == 3:
        # calculate age
        infor_1['age'] = date_sup.subtract_two_dates(copy.deepcopy(infor_1['date_of_birth']), copy.deepcopy(infor_1['date_of_death']))
        infor_2['age'] = date_sup.subtract_two_dates(copy.deepcopy(infor_2['date_of_birth']), copy.deepcopy(infor_2['date_of_death']))
        #
        item['ques_reason_1'] = reason_ques_old.format(infor_1['name'])
        item['ans_reason_1'] = infor_1['age']   
        #
        item['ques_reason_2'] = reason_ques_old.format(infor_2['name'])
        item['ans_reason_2'] = infor_2['age']
        count_reason += 3
        # 
        reason_ques_compare_old = 'Is a {}-year-{}-month-{}-day-old person younger than a {}-year-{}-month-{}-day-old person?'

        reason_ques_compare_old_2 = 'Is a {}-year-{}-month-{}-day-old person older than a {}-year-{}-month-{}-day-old person?'

        y1, m1, d1 = infor_1['age']['year'], infor_1['age']['month'], infor_1['age']['day']
        y2, m2, d2 = infor_2['age']['year'], infor_2['age']['month'], infor_2['age']['day']

        rand_num = random.randint(0,9)
        compare_age = date_sup.compare_two_dates(infor_1['age'], infor_2['age']) # Return 1 if dict_1 < dict_2
        # print(compare_age)
        assert ans_value != 2
        if rand_num % 2 == 0:
            item['ques_reason_3'] = reason_ques_compare_old.format(y1, m1, d1, y2, m2, d2)
            #
            if compare_age == 1:
                item['ans_reason_3'] = "yes"
            elif compare_age == -1:
                item['ans_reason_3'] = "no"
            else:
                assert "equal case"
        else:
            item['ques_reason_3'] = reason_ques_compare_old_2.format(y1, m1, d1, y2, m2, d2)
            #
            if compare_age == 1:
                item['ans_reason_3'] = "no"
            elif compare_age == -1:
                item['ans_reason_3'] = "yes"
            else:
                assert "equal case"            
        

    # For Robustness level
    if 'who was born first out of' in item['question'].lower():
        item['ques_robust'] = "Who was born later, " + list(names)[0].title() + ' or ' + list(names)[1].title() + '?'
        count_robust += 1
    #
    elif 'who was born first' in item['question'].lower():
        item['ques_robust'] = item['question'].replace("Who was born first", 'Who was born later', 1)
        count_robust += 1
    #
    elif 'who was born earlier' in item['question'].lower():
        item['ques_robust'] = item['question'].replace("Who was born earlier", 'Who was born later', 1)
        count_robust += 1    
    #
    elif 'who was born later' in item['question'].lower():
        item['ques_robust'] = item['question'].replace("Who was born later", 'Who was born first', 1)
        count_robust += 1    
    #
    elif 'born first?' in item['question'].lower():
        item['ques_robust'] = "Who was born later, " + list(names)[0].title() + ' or ' + list(names)[1].title() + '?'
        count_robust += 1  
    #
    elif 'who died first' in item['question'].lower():
        item['ques_robust'] = item['question'].replace("Who died first", 'Who died later', 1)
        count_robust += 1  
    #
    elif 'who died earlier' in item['question'].lower():
        item['ques_robust'] = item['question'].replace("Who died earlier", 'Who died later', 1)
        count_robust += 1  
    #
    elif 'who died later' in item['question'].lower():
        item['ques_robust'] = item['question'].replace("Who died later", 'Who died first', 1)
        count_robust += 1 
    # 
    elif 'who lived longer' in item['question'].lower():
        item['ques_robust'] = item['question'].replace("Who lived longer", 'Who lived shorter', 1)
        count_robust += 1 
    #
    # the answer part is similar
    # print(item['_id'])
    names.remove(item['answer'].lower())
    # print(names)
    assert len(list(names)) == 1
    item['ans_robust'] = list(names)[0].title()
    print("Finish id: {}".format(item['_id']))


print("Data length: {}".format(len(data)))
print("Number of extraction questions: {}".format(count_extract))
print("Number of reason questions: {}".format(count_reason))
print("Number of robustness questions: {}".format(count_robust))


utils.write_json(data, "data-preparation/date_2wiki/{}_with_sub.json".format(type_))
utils.write_json_lines(data, "data-preparation/date_2wiki/{}_with_sub_line.json".format(type_))

