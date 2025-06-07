import json
from tqdm import tqdm
import os

path = "mat_train.json"
with open(path, "r") as f:
    raw_data = json.load(f)
   
data = [] 
for d in tqdm(raw_data):
    ok = True
    del d['answer']
    if isinstance(d['image'], str):
        d['image'] = [d['image']]
    else:
        keys = sorted(d['image'].keys())
        for idx, c in enumerate(d['conversations']):
            for k in keys: 
                d['conversations'][idx]['content'] = d['conversations'][idx]['content'].replace(k, "<image>")
        d['image'] = [d['image'][k] for k in keys]
        
    
    for idx, p in enumerate(d['image']):
        if "data/open_llava_next/" in p:
            d['image'][idx] = p.replace("data/open_llava_next/", "")
        if "data/tongagent/" in p:
            d['image'][idx] = p.replace("data/tongagent/", "")
            
        if not os.path.exists(d['image'][idx]):
            print(f"Image path {p} does not exist, removing from data.")
            ok = False
    assert len(d['image']) == sum([c['content'].count("<image>") for c in d['conversations']]), "Image count does not match conversation count"
    if len(d['conversations']) == 0:
        print(f"Conversation is empty for data: {d}")
        ok = False
    if ok:
        d['images'] = d['image']
        del d['image']
        data.append(d)
        

        
print(f"Transformed data size: {len(data)} out of {len(raw_data)} {len(data) / len(raw_data) * 100:.2f}%")
with open("mat_train_transformed.json", "w") as f:  
    json.dump(data[:100], f, indent=4, ensure_ascii=False)
        
