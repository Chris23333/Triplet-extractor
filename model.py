import json
import openai

import itertools

prompt_en = "Suppose you are an entity-relationship triple extraction model. I'll give you list of head entity types: subject_types, list of tail entity types: object_types, list of relations: relations. Give you a sentence, please extract the subject and object in the sentence based on these three lists, and form a triplet in the form of (subject, relation, object).\n\
            The given sentence is {}.\n relation list:[{}].\n subject_types:[{}].\n object_types:[{}].\n In the given sentence, what triples might be contained? Please answer in the form (subject, relation, object): Please note that the relation can only be chosen from the relation list I have given."

prompt_ch = "假设你是一个实体关系三元组抽取模型。我会给你头实体类型列表subject_types，尾实体类型列表object_types，关系列表relations，再给你一个句子，请你根据这三个列表抽出句子中的subject和object，并组成三元组，且形式为(subject, relation, object)。\
            给定的句子为：{} relations list：{}。 subject_types：{}。object_types：{}。在给定的句子中，可能包含了哪些三元组？请按照形式(subject, relation, object)回答：请注意relation只能从我给定的relations list中选。"






# 封装openai Create,实现换key功能
with open("keys.txt", "r") as f:
    keys = f.readlines()
    keys = [key.strip() for key in keys]
all_keys = itertools.cycle(keys)

openai.api_key = all_keys
def create(**args):
    global all_keys
    openai.api_key = next(all_keys)
    openai.api_key = all_keys
    try:
        result = openai.ChatCompletion.create(**args)
    except openai.error.RateLimitError:
        result = create(**args)
    
    return result


def chat(mess):
    
    responde = create(
        model="gpt-3.5-turbo",
        messages=mess
    )

    res = responde['choices'][0]['message']['content']
    return res


def Triples_extract(input_data,out_path):
    text = input_data["sentence"]
    lang = input_data["language"]
    s_type = input_data["subject_type"]
    o_type = input_data["object_type"]
    relation = input_data["relations"]
    mess = []
    '''
    try:
        if lang == "Chinese":
            prompt = prompt_ch.format(text,relation,s_type,o_type)
        elif lang == "English":
             prompt = prompt_en.format(text,relation,s_type,o_type)
        else:
            raise ValueError("language error")
        
        mess.append({"role": "user", "content": prompt})
        result = chat(mess)
        with open(out_path,"wt") as f:
            f.write(result)
        return result
    
    except Exception as e:
        print("some error")'''
    if lang == "Chinese":
            prompt = prompt_ch.format(text,relation,s_type,o_type)
    elif lang == "English":
             prompt = prompt_en.format(text,relation,s_type,o_type)
    else:
            raise ValueError("language error")

    mess.append({"role": "user", "content": prompt})
    result = chat(mess)
    with open(out_path,"wt") as f:
            f.write(result)
    return result

