import re
import chardet

def detect_language(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()
        encode_info = chardet.detect(data)
        text = data.decode(encode_info['encoding'])
        
    zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')
    en_pattern = re.compile(u'[A-Za-z]+')
    
    zh_match = zh_pattern.search(text)
    en_match = en_pattern.search(text)
    
    if zh_match and en_match:
        # 如果中文和英文都存在，根据出现频率判断
        zh_count = len(zh_pattern.findall(text))
        en_count = len(en_pattern.findall(text))
        return 0 if zh_count > en_count else 1
    elif zh_match:
        return 0
    elif en_match:
        return 1
    else:
        raise ValueError('The file does not contain Chinese or English text')
