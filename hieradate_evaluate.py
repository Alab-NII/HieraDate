"""
    HieraDate evaluation script
    Adapted from 2WikiMultiHopQA evaluation at https://github.com/Alab-NII/2wikimultihop/blob/main/2wikimultihop_evaluate.py
    and Drop evaluation at https://github.com/allenai/allennlp-reading-comprehension/blob/master/allennlp_rc/eval/drop_eval.py
"""
import sys
import ujson as json
import re
import string
from collections import Counter


def normalize_answer(s):

    def remove_articles(text):
        return re.sub(r'\b(a|an|the)\b', ' ', text)

    def white_space_fix(text):
        return ' '.join(text.split())

    def remove_punc(text):
        exclude = set(string.punctuation)
        return ''.join(ch for ch in text if ch not in exclude)

    def lower(text):
        return text.lower()

    return white_space_fix(remove_articles(remove_punc(lower(s))))


def is_number(number):
    try:
        float(number)
        return True
    except ValueError:
        return False


def normalize_number(number):
    if is_number(number):
        return str(float(number))
    else:
        return number


def normalize_date(date_):
    date_['year'] = normalize_number(date_['year'])
    date_['month'] = normalize_number(date_['month'])
    date_['day'] = normalize_number(date_['day'])
    return date_


def compute_f1(prediction_tokens, ground_truth_tokens):
    common = Counter(prediction_tokens) & Counter(ground_truth_tokens)
    num_same = sum(common.values())
    if num_same == 0:
        return (0, 0, 0)
    precision = 1.0 * num_same / len(prediction_tokens)
    recall = 1.0 * num_same / len(ground_truth_tokens)
    f1 = (2 * precision * recall) / (precision + recall)
    return f1, precision, recall


def f1_score(prediction, ground_truth):
    normalized_prediction = normalize_answer(prediction)
    normalized_ground_truth = normalize_answer(ground_truth)

    ZERO_METRIC = (0, 0, 0)

    if normalized_prediction in ['yes', 'no', 'noanswer'] and normalized_prediction != normalized_ground_truth:
        return ZERO_METRIC
    if normalized_ground_truth in ['yes', 'no', 'noanswer'] and normalized_prediction != normalized_ground_truth:
        return ZERO_METRIC

    prediction_tokens = normalized_prediction.split()
    ground_truth_tokens = normalized_ground_truth.split()
    f1, precision, recall = compute_f1(prediction_tokens, ground_truth_tokens)
    return f1, precision, recall


def exact_match_score(prediction, ground_truth):
    return (normalize_answer(prediction) == normalize_answer(ground_truth))


def update_em_f1(metrics, prediction, gold, key_em, key_f1, key_prec, key_recall):
    em = exact_match_score(prediction, gold)
    # 
    f1, prec, recall = f1_score(prediction, gold)
    metrics[key_em] += float(em)
    metrics[key_f1] += f1
    metrics[key_prec] += prec
    metrics[key_recall] += recall


def update_em(metrics, prediction, gold, key_em):
    em = exact_match_score(prediction, gold)
    #
    metrics[key_em] += float(em)


def update_em_f1_date(metrics, prediction, gold, key_em, key_f1, key_prec, key_recall):
    if type(prediction) is dict:
        normalized_prediction = normalize_date(prediction)
        prediction_tokens = [normalized_prediction['year'], normalized_prediction['month'], normalized_prediction['day']]
    else:
        normalized_prediction = normalize_number(prediction)
        prediction_tokens = normalize_number(prediction)
    
    normalized_ground_truth = normalize_date(gold)

    em = (normalized_prediction == normalized_ground_truth) 
    
    ground_truth_tokens = [normalized_ground_truth['year'], normalized_ground_truth['month'], normalized_ground_truth['day']]
    f1, prec, recall = compute_f1(prediction_tokens, ground_truth_tokens) 
    #
    metrics[key_em] += float(em)
    metrics[key_f1] += f1
    metrics[key_prec] += prec
    metrics[key_recall] += recall


def convert_2_dict(data):
    dic = {}
    for item in data:
        dic[item['_id']] = item
    return dic


def eval(prediction_file, gold_file):
    with open(prediction_file) as f:
        prediction = json.load(f)

    pred_dict = convert_2_dict(prediction)

    with open(gold_file) as f:
        gold = json.load(f)

    metrics = {'em': 0, 'f1': 0, 'prec': 0, 'recall': 0,
        'ex_em': 0, 'ex_f1': 0, 'ex_prec': 0, 'ex_recall': 0,
        'em_math': 0, 'f1_math': 0, 'prec_math': 0, 'recall_math': 0, 'em_compare': 0,  
        'ro_em': 0, 'ro_f1': 0, 'ro_prec': 0, 'ro_recall': 0}

    count_extract = 0
    count_reason_math = 0
    count_reason_compare = 0
    count_sample = 0

    for dp in gold:
        cur_id = dp['_id']
        # print(cur_id)
        if cur_id not in pred_dict.keys():
            print('missing sample {}'.format(cur_id))
        #
        else:
            count_sample += 1
            pred_item = pred_dict[cur_id]
            update_em_f1(metrics, pred_item['answer'], dp['answer'], 'em', 'f1', 'prec', 'recall')
            # robustess level
            update_em_f1(metrics, pred_item['ans_robust'], dp['ans_robust'], 'ro_em', 'ro_f1', 'ro_prec', 'ro_recall')
            # extraction level
            update_em_f1(metrics, pred_item['ans_extract_1'], dp['ans_extract_1'], 'ex_em', 'ex_f1', 'ex_prec', 'ex_recall')
            update_em_f1(metrics, pred_item['ans_extract_2'], dp['ans_extract_2'], 'ex_em', 'ex_f1', 'ex_prec', 'ex_recall')
            count_extract += 2
            if 'ques_extract_3' in pred_item.keys():
                # case ask about age
                update_em_f1(metrics, pred_item['ans_extract_3'], dp['ans_extract_3'], 'ex_em', 'ex_f1', 'ex_prec', 'ex_recall')
                update_em_f1(metrics, pred_item['ans_extract_4'], dp['ans_extract_4'], 'ex_em', 'ex_f1', 'ex_prec', 'ex_recall')
                count_extract += 2
                # reasoning level - mathematical reasoning
                update_em_f1_date(metrics, pred_item['ans_reason_1'], dp['ans_reason_1'], 'em_math', 'f1_math', 'prec_math', 'recall_math')
                update_em_f1_date(metrics, pred_item['ans_reason_2'], dp['ans_reason_2'], 'em_math', 'f1_math', 'prec_math', 'recall_math')
                count_reason_math += 2
                # reasoning level - comparison reasoning
                update_em(metrics, pred_item['ans_reason_3'], dp['ans_reason_3'], 'em_compare')
                count_reason_compare += 1
            else:
                update_em(metrics, pred_item['ans_reason_1'], dp['ans_reason_1'], 'em_compare')
                update_em(metrics, pred_item['ans_reason_2'], dp['ans_reason_2'], 'em_compare')
                count_reason_compare += 2

    # N = len(gold)
    for k in metrics.keys():
        if 'ex_' in k:
            metrics[k] = round(metrics[k]/count_extract*100, 2)
        elif '_math' in k:
            metrics[k] = round(metrics[k]/count_reason_math*100, 2)
        elif '_compare' in k:
            metrics[k] = round(metrics[k]/count_reason_compare*100, 2)
        else:
            metrics[k] = round(metrics[k]/count_sample*100, 2)
    print(json.dumps(metrics, indent=4))


if __name__ == '__main__':
    # prediction_file, gold_file
    eval(sys.argv[1], sys.argv[2])
