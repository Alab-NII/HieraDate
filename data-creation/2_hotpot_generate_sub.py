"""
Generate subquestions for HotpotQA 
"""

import json
import copy
import random
from tqdm import tqdm
#
import file_utils as utils
import date_support as date_sup
from functions import *


# hotpot
type_ = 'dev'
filename = "data-preparation/date_hotpotqa/{}_annotate.json".format(type_)


with open(filename) as f:
    data = json.load(f)


templates_birth = ['What is the birth date of #name?', "What's the birth date of #name?", \
    'What is the date of birth of #name?', "What's the date of birth of #name?", \
    'When was #name born?']

templates_death = ['What is the death date of #name?', "What's the death date of #name?", \
    'What is the date of death of #name?', "What's the date of death of #name?", \
    'When did #name die?']

# For robustness level
templates_ques = ['who was born first', 'who was born earlier', 'who was born later', 'who was born first out of', 'born first?', \
    'who died first', 'who died earlier', 'who died later', 'who lived longer']


count_extract = 0
count_robust = 0
count_reason = 0


# for reasoning level
reason_ques_old = 'How old is {}?'
reason_ques_first = 'Does {} come before {}?'
reason_ques_later = 'Does {} come after {}?'

# label 1
group_small = ['who was born first', 'who was born earlier', 'who was born first out of', 'born first?', \
    'who died first', 'who died earlier', 'was born first', 'was born earlier']
# label 2
group_large = ['who was born later', 'who died later', 'was born later', 'died later', 'died more recently', 'died last', 'died second']
# label 3
templates_old = ['who lived longer']


# group to get relation
# label 1
group_birth = ['who was born first', 'who was born earlier', 'who was born first out of', 'born first?', \
    'who was born later', 'was born first', 'was born later', 'was born earlier']
# label 2
group_death = ['who died first', 'who died earlier', 'who died later', 'died later', 'died more recently', 'died last', 'died second']
# label 3
templates_old = ['who lived longer']


total = 0
count_live_long = 0
count_reason_label12 = 0
count_reason_label12_birth = 0
count_reason_label12_death = 0
count_special_reason = 0

new_data = []
for idx, item in tqdm(enumerate(data)):
    if item['label_use'] == 1:
        #
        total += 1
        label_relation = check_group(item['question'], group_birth, group_death, templates_old)
        label_group = check_group(item['question'], group_small, group_large, templates_old)
        #
        infor_1 = {}
        infor_1['name'] = item['name_1']
        #
        infor_2 = {}
        infor_2['name'] = item['name_2']

        if label_relation == 1:
            infor_1['date_of_birth'] = item['date_of_birth_1_date']
            infor_1['date_of_birth_str'] = item['date_of_birth_1']
            #
            infor_2['date_of_birth'] = item['date_of_birth_2_date']
            infor_2['date_of_birth_str'] = item['date_of_birth_2']
            # check annotation data
            list_dates1 = date_sup.convert_date2str(infor_1['date_of_birth'])
            if infor_1['date_of_birth_str'] not in list_dates1:
                assert "error annodation"
            list_dates2 = date_sup.convert_date2str(infor_2['date_of_birth'])
            if infor_2['date_of_birth_str'] not in list_dates2:
                assert "error annodation"
                        
            #
            # For extraction level
            template = random.choice(templates_birth)
            item['ques_extract_1'] = template.replace("#name", infor_1['name'].title(), 1)
            item['ans_extract_1'] = infor_1['date_of_birth_str']
            item['ans_extract_1_date'] = infor_1['date_of_birth']
            #
            template = random.choice(templates_birth)
            item['ques_extract_2'] = template.replace("#name", infor_2['name'].title(), 1)
            item['ans_extract_2'] = infor_2['date_of_birth_str']
            item['ans_extract_2_date'] = infor_2['date_of_birth']
            count_extract += 2

        elif label_relation == 2:
            infor_1['date_of_death'] = item['date_of_death_1_date']
            infor_1['date_of_death_str'] = item['date_of_death_1']
            #
            infor_2['date_of_death'] = item['date_of_death_2_date']
            infor_2['date_of_death_str'] = item['date_of_death_2']

            # check annotation data
            list_dates1 = date_sup.convert_date2str(infor_1['date_of_death'])
            if infor_1['date_of_death_str'] not in list_dates1:
                assert "error annodation"
            list_dates2 = date_sup.convert_date2str(infor_2['date_of_death'])
            if infor_2['date_of_death_str'] not in list_dates2:
                assert "error annodation"

            # For extraction level
            template = random.choice(templates_death)
            item['ques_extract_1'] = template.replace("#name", infor_1['name'].title(), 1)
            item['ans_extract_1'] = infor_1['date_of_death_str']
            item['ans_extract_1_date'] = infor_1['date_of_death']
            #
            template = random.choice(templates_death)
            item['ques_extract_2'] = template.replace("#name", infor_2['name'].title(), 1)
            item['ans_extract_2'] = infor_2['date_of_death_str']
            item['ans_extract_2_date'] = infor_2['date_of_death']
            count_extract += 2    
        
        elif label_relation == 3:
            infor_1['date_of_birth'] = item['date_of_birth_1_date']
            infor_1['date_of_birth_str'] = item['date_of_birth_1']
            #
            infor_1['date_of_death'] = item['date_of_death_1_date']
            infor_1['date_of_death_str'] = item['date_of_death_1']
            # For infor_2
            infor_2['date_of_birth'] = item['date_of_birth_2_date']
            infor_2['date_of_birth_str'] = item['date_of_birth_2']    
            #
            infor_2['date_of_death'] = item['date_of_death_2_date']
            infor_2['date_of_death_str'] = item['date_of_death_2']

            # check annotation data
            list_dates1 = date_sup.convert_date2str(infor_1['date_of_birth'])
            if infor_1['date_of_birth_str'] not in list_dates1:
                assert "error annodation"
            list_dates2 = date_sup.convert_date2str(infor_2['date_of_birth'])
            if infor_2['date_of_birth_str'] not in list_dates2:
                assert "error annodation"

            # check annotation data
            list_dates1 = date_sup.convert_date2str(infor_1['date_of_death'])
            if infor_1['date_of_death_str'] not in list_dates1:
                assert "error annodation"
            list_dates2 = date_sup.convert_date2str(infor_2['date_of_death'])
            if infor_2['date_of_death_str'] not in list_dates2:
                assert "error annodation"

            # For extraction level
            template = random.choice(templates_birth)
            item['ques_extract_1'] = template.replace("#name", infor_1['name'].title(), 1)
            item['ans_extract_1'] = infor_1['date_of_birth_str']
            item['ans_extract_1_date'] = infor_1['date_of_birth']
            #
            template = random.choice(templates_death)
            item['ques_extract_2'] = template.replace("#name", infor_1['name'].title(), 1)
            item['ans_extract_2'] = infor_1['date_of_death_str']
            item['ans_extract_2_date'] = infor_1['date_of_death']
            #
            template = random.choice(templates_birth)
            item['ques_extract_3'] = template.replace("#name", infor_2['name'].title(), 1)
            item['ans_extract_3'] = infor_2['date_of_birth_str']
            item['ans_extract_3_date'] = infor_2['date_of_birth']
            #
            template = random.choice(templates_death)
            item['ques_extract_4'] = template.replace("#name", infor_2['name'].title(), 1)
            item['ans_extract_4'] = infor_2['date_of_death_str']
            item['ans_extract_4_date'] = infor_2['date_of_death']
            count_extract += 4   
        
        else:
            infor_1['date_of_birth'] = item['date_of_birth_1_date']
            infor_1['date_of_birth_str'] = item['date_of_birth_1']
            #
            infor_2['date_of_birth'] = item['date_of_birth_2_date']
            infor_2['date_of_birth_str'] = item['date_of_birth_2']

            # check annotation data
            list_dates1 = date_sup.convert_date2str(infor_1['date_of_birth'])
            if infor_1['date_of_birth_str'] not in list_dates1:
                assert "error annodation"
            list_dates2 = date_sup.convert_date2str(infor_2['date_of_birth'])
            if infor_2['date_of_birth_str'] not in list_dates2:
                assert "error annodation"

            # For extraction level
            template = random.choice(templates_birth)
            item['ques_extract_1'] = template.replace("#name", infor_1['name'].title(), 1)
            item['ans_extract_1'] = infor_1['date_of_birth_str']
            item['ans_extract_1_date'] = infor_1['date_of_birth']
            #
            template = random.choice(templates_birth)
            item['ques_extract_2'] = template.replace("#name", infor_2['name'].title(), 1)
            item['ans_extract_2'] = infor_2['date_of_birth_str']
            item['ans_extract_2_date'] = infor_2['date_of_birth']
            count_extract += 2


        # For reasoning level
        if label_group == 1 or label_group == 2:
            #
            count_reason_label12 += 1
            if label_relation == 1: 
                count_reason_label12_birth += 1
                infor_1['date'] = infor_1['date_of_birth']
                infor_2['date'] = infor_2['date_of_birth']
            elif label_relation == 2: 
                count_reason_label12_death += 1
                infor_1['date'] = infor_1['date_of_death']
                infor_2['date'] = infor_2['date_of_death']
            #
            ans_value = date_sup.compare_two_dates(infor_1['date'], infor_2['date']) # Return 1 if dict_1 < dict_2
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
                    if item['answer'].title() != infor_1['name'].title():
                        print(item['answer'])
                        print(infor_1)
                        print(infor_1['name'].title())
                    assert item['answer'].title() == infor_1['name'].title()
                if label_group == 2: 
                    if item['answer'].title() != infor_2['name'].title():
                        print(item['answer'])
                        print(infor_2)
                        print(infor_2['name'].title())
                    assert item['answer'].title() == infor_2['name'].title()
            elif ans_value == -1:
                item['ques_reason_1'] = reason_ques_first.format(str_date1, str_date2)
                item['ans_reason_1'] = 'no'  
                count_reason += 1
                #
                item['ques_reason_2'] = reason_ques_later.format(str_date1, str_date2)
                item['ans_reason_2'] = 'yes'   
                count_reason += 1  
                if label_group == 1:   
                    if item['answer'].title() != infor_2['name'].title():
                        print(item['answer'])
                        print(infor_2)
                        print(infor_2['name'].title())          
                    assert item['answer'].title() == infor_2['name'].title()     
                if label_group == 2:   
                    if item['answer'].title() != infor_1['name'].title():
                        print(item['answer'])
                        print(infor_1)
                        print(infor_1['name'].title())          
                    assert item['answer'] == infor_1['name'].title() 
            else:
                print("I am a special case ============================")
                count_special_reason += 1
                print(ans_value)
                print(infor_1['date'])
                print(infor_2['date'])

        if label_group == 3:
            count_live_long += 1
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
            

        names = [infor_1['name'], infor_2['name']]

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
        elif 'was born first' in item['question'].lower():
            item['ques_robust'] = item['question'].replace("was born first", 'was born later', 1)
            # print(item['_id'])
            count_robust += 1        
        elif 'was born later' in item['question'].lower():
            item['ques_robust'] = item['question'].replace("was born later", 'was born first', 1)
            # print(item['_id'])
            count_robust += 1  
        elif 'was born earlier' in item['question'].lower():
            item['ques_robust'] = item['question'].replace("was born earlier", 'was born later', 1)
            # print(item['_id'])
            count_robust += 1         
        
        elif 'died later' in item['question'].lower():
            item['ques_robust'] = item['question'].replace("died later", 'died first', 1)
            # print(item['_id'])
            count_robust += 1 
        # 
        elif 'died last' in item['question'].lower():
            item['ques_robust'] = item['question'].replace("died last", 'died first', 1)
            print(item['_id'])
            count_robust += 1         
        elif 'died second' in item['question'].lower():
            item['ques_robust'] = item['question'].replace("died second", 'died first', 1)
            print(item['_id'])
            count_robust += 1 
        elif 'died more recently' in item['question'].lower():
            item['ques_robust'] = item['question'].replace("died more recently", 'died first', 1)
            print(item['_id'])
            count_robust += 1 
        else:
            print(item['question'])
        #
        # the answer part is similar
        if item['answer'] not in names:
            names.remove(item['answer'].title())
        else:
            names.remove(item['answer'])
        # print(names)
        assert len(list(names)) == 1
        item['ans_robust'] = list(names)[0].title()
        new_data.append(item)



# print(count_reason_label12)
# print(count_reason_label12_birth)
# print(count_reason_label12_death)

# print(count_special_reason)
print("Date length: {}".format(len(data)))
print("Live longer questions: {}".format(count_live_long))
print("Number of use examples: {}".format(total))
print("Number of extraction questions: {}".format(count_extract))
print("Number of reason questions: {}".format(count_reason))
print("Number of robustness questions: {}".format(count_robust))



utils.write_json(new_data, "data-preparation/date_hotpotqa/{}_with_sub.json".format(type_))
utils.write_json_lines(new_data, "data-preparation/date_hotpotqa/{}_with_sub_line.json".format(type_))



