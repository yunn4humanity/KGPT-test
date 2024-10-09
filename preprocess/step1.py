import json
import regex
import nltk.data
from nltk.tokenize import word_tokenize
import sys
sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')


def tokenize(string):
    return word_tokenize(string)

def split_paragraphs(text):
    """
    remove urls, lowercase all words and separate paragraphs
    """
    splits = regex.split(r'\n+', text)
    paras = []
    for split in splits[1:]: # skip the titles
        split = split.strip()
        if len(split) == 0:
            continue
        if 'Section::' in split:
            continue
        paras.append(split)
    
    paras = " ".join(paras)
    return sent_detector.tokenize(paras)

def split_sent(sent):
    strings = regex.split('<a |</a>', sent)
    new_strings = []
    count = 0
    for s in strings:
        s = s.strip()
        if s:
            if 'href=' in s:
                s = s.lstrip('href="')
                href, text = s.split('">')
                new_strings.append((text, href))
                count += 1            
            else:
                ss = tokenize(s)
                new_strings.extend([(_, None) for _ in ss])
    
    return new_strings, count / len(new_strings), count

fw = open('out-more.json', 'w')
with open('en.json', 'r') as f:
    for i, line in enumerate(f):
        data = json.loads(line)
        entry = {"id": data['id'], "url": data['url'], 'title': data['title']}
        # SFILES 2.0 문자열을 그대로 사용
        entry['text'] = data['text']
        entry['sfiles_string'] = data['title']
        
        fw.write(json.dumps(entry) + '\n')
        
        sys.stdout.write('finished {}/{} \r'.format(i, 5989879))
fw.close()
