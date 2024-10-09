import json
import sys
import time
import os

# assert len(sys.argv) == 3

input_file = 'out-more.json' # sys.argv[1]
resume = 'false' # sys.argv[2]
assert resume in ["true", "false"]
if resume == 'false':
    mode = 'w+'
else:
    mode = 'a+'

done = set()
if resume == 'true':
    with open(input_file + '.intermediate.json', 'r') as f:
        for line in f:
            title = json.loads(line.strip())['title']
            done.add(title)
    print("already accomplished {} lines".format(len(done)))

fw = open(input_file + '.intermediate.json', mode)

start_time = time.time()
idx = 0
with open(input_file, 'r') as f:
    for line_id, line in enumerate(f):
        data = json.loads(line.strip())
        if data['title'] in done:
            continue
        
        if data['title'].startswith('List of') or data['title'].startswith('Category'):
            continue
        
        sfiles_string = data.get('sfiles_string', '')
        if not sfiles_string:
            continue
        
        text = data.get('text', '')
        if not text:
            continue
        
        entry = {
            'id': idx,
            'url': data['url'],
            'title': data['title'],
            'title_kb_id': sfiles_string,  # SFILES 문자열을 title_kb_id로 사용
            'sfiles_string': sfiles_string,
            'text': sfiles_string,      # 임의로 SFILES 문자열을 text로 사용
            'kblinks': [sfiles_string],  # SFILES 문자열을 kblinks로 사용
            'hyperlinks': [sfiles_string]  # SFILES 문자열을 hyperlinks로 사용
        }
        
        fw.write(json.dumps(entry) + '\n')
        idx += 1
        
        if line_id % 1000 == 0:
            sys.stdout.write("finished {}, used time = {} \r".format(line_id, time.time() - start_time))
            sys.stdout.flush()

fw.close()
print("\nFinished processing. Total entries: {}".format(idx))