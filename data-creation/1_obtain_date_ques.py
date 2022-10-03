"""
Extract date question in 2WikiMultiHop and HotpotQA dataset
"""

import json
import file_utils as utils

# ====== Edit here ======
hotpot_or_2wiki = '2wiki' # 2wiki/hotpotqa
type_ = 'train' # dev/train
# ====== End editing ======


filename = "{}/{}.json".format(hotpot_or_2wiki, type_)

out_file = "data-preparation/date_{}/{}.json".format(hotpot_or_2wiki, type_)


with open(filename) as f:
    data = json.load(f)

print("Length data: {}".format(len(data)))

date_data = []
count_compare = 0

keywords = ['born first', 'who died', 'who lived longer', 'born later', 'who is older', 'is younger', 'born earlier', \
    'died first', 'died later', 'died earlier']

for item in data:
    # print(item.keys())
    q_type = item['type']
    if q_type == 'comparison': 
        count_compare += 1
        for word in keywords:
            if word in item['question'].lower():
                date_data.append(item)
                break

print("Length comparison data: {}".format(count_compare))

print("Length date data: {}".format(len(date_data)))



utils.write_json(date_data, out_file)


# 2wikimultihop:
# dev: 984/3040
# train: 8745/51963

# hotpotqa: 
# dev: 119/1487
# train: 878/17456