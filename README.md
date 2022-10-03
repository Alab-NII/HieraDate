This is the repository for the paper: How Well Do Multi-hop Reading Comprehension Models Understand Date Information? (AACL-IJCNLP 2022).

## Dataset Information
Our HieraDate dataset has two versions:
- [Normal settting](https://www.dropbox.com/s/0p7a5ce4ks92yj3/normal_setting.zip?dl=0): the context contains 2 gold paragraphs 
- [Distractor setting](https://www.dropbox.com/s/5weoi77lf6wlh3n/distractor_setting.zip?dl=0): the context contains 2 gold paragraphs and 8 distractor paragraphs


Each sample include the following information:
  * ```id```
  * ```question```
  * ```answer```
  * ```context```: list of N paragraphs (N=2 for normal setting and N=10 for distractor setting)
  * ```data_label```: 2wikimultihopqa or hotpotqa
  * For the extraction task: 2 or 4 questions (each question has 3 keys: ```ques_extract_1```, ```ans_extract_1```, and ```ans_extract_1_date```)
  * For the reasoning task: 2 or 3 questions (each question has 2 keys: ```ques_reason_1``` and ```ans_reason_1```)
  * For the robustness task: 1 question with 2 keys: ```ques_robust``` and ```ans_robust```


## Evaluate on HieraDate

```
python3 hieradate_evaluate.py prediction_file.json gold_file.json
```

## Data Creation Process

### For 2Wiki
1. Run file 1_obtain_date_ques.py (edit the path and the file name if necessary)

2. There are some cases that the date value in the tripe (of the evidence) does not exactly match with the text. We have munually update these cases:
id: e618b2c608c911ebbd92ac1f6bf848b6 ("1568" => "February 1568")
id: 460ca32008a111ebbd78ac1f6bf848b6 ("2010" => "25 December 2010")
...
The updated files are: dev_line_update and train_line_update

3. Run file 2_wiki_generate_sub.py 


### For HotpotQA
1. Run 1_obtain_date_ques.py (edit the path and the file name if necessary)

2. Use Spacy to extract names and then annotate the date with two formats: unstructured and structured

3. Run file 2_hotpot_generate_sub.py


### Combine HotpotQA and 2Wiki
After obtaining the probing questions for each data, we do the following steps to obtain the final dataset:
- Update the samples that have month-0 and day-0 to month-1 and day-1
- Obtain more combined reasoning questions for 2Wiki
- Split to train, dev, and test
- Obtain two versions: normal setting (without distractor paragraphs) and distractor setting (with distractor paragraphs)

Note: to run the code in the data creation process, you need to use the data [here](https://www.dropbox.com/s/fw06kzlonjmvh1w/data.zip?dl=0).