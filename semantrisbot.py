import pyautogui
import pytesseract
import time
from PIL import Image
import json
import spacy
from nltk.corpus import wordnet
import enchant

language_model = spacy.load("en_core_web_md")
d = enchant.Dict("en_US")

with open("dictionary_data.json", 'r') as fin:
    data = json.load(fin)
with open("right.json", 'r') as fil:
    ez_dict = json.load(fil)
datak = list(data.keys())
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
finopen = open("wrongs.txt")
fin = [i for i in finopen.readlines() if i != "\n"]
finopen.close()
finn = open("wrongs.txt", "w").close()
backup = {}
for cur in fin:
    backup[cur] = input(cur)
    ez_dict[cur] = backup[cur]
with open("right.json", 'w') as fill:
    json.dump(ez_dict, fill)
fill.close()

out = 0
synonyms_visited = []
count = 0
cnt = 0
initkind = False
blanks = []
keyword = False
for i in range(1000):
    blanks.append(Image.new(mode="1", size=(500, 900)))

while True:
    flag = False
    flags = False
    pastkeyword = keyword
    raw = list(pyautogui.screenshot(region=(1550, 700, 500, 900)).getdata())
    secondary_raw = list(pyautogui.screenshot(region=(1550, 700, 500, 900)).getdata())
    for i in range(450000):
        if raw[i][2] > 200:
            raw[i] = 0
            secondary_raw[i] = 0
        elif raw[i][2] > 100:
            raw[i] = 255
            secondary_raw[i] = 0
        else:
            raw[i] = 255
            secondary_raw[i] = 255
    keyword_im = blanks[count]
    count += 1
    keyword_im.putdata(raw)
    keywords = pytesseract.image_to_string(keyword_im).split('\n')[0: -1]
    keywords = [i for i in keywords if i != '']
    try:
        keyword = keywords[0].lower()
    except IndexError:
        continue
    keyword = keyword.split(' ')[0]
    if "strea" in keyword or keyword in "strea" or not keyword.isalpha() or not d.check(keyword):
        continue
    names_im = blanks[count]
    count += 1
    names_im.putdata(secondary_raw)
    names = pytesseract.image_to_string(names_im).split('\n')[0: -1]
    names = [i for i in names if (i != '' and i not in keywords)]
    if keyword in ez_dict:
        cnt += 1
        out = ez_dict[keyword]
        if out[:4].lower() not in keyword:
            pyautogui.write(' '.join(out.split('_')))
            pyautogui.press('enter')
            time.sleep(1.5)
            continue
        else:
            finopen = open("wrongs.txt")
            fin = [i.rstrip() for i in finopen.readlines() if i != "\n"]
            finopen.close()
            if keyword not in fin:
                fin.append(keyword)
            fout = open("wrongs.txt", 'w')
            for i in fin:
                fout.write(i + "\n")
            fout.close()
    elif (keyword + '\n') in ez_dict:
        cnt += 1
        out = ez_dict[keyword + '\n']
        if out[:4].lower() not in keyword:
            pyautogui.write(' '.join(out.split('_')))
            pyautogui.press('enter')
            time.sleep(1.5)
            continue
        else:
            finopen = open("wrongs.txt")
            fin = [i.rstrip() for i in finopen.readlines() if i != "\n"]
            finopen.close()
            if keyword not in fin:
                fin.append(keyword)
            fout = open("wrongs.txt", 'w')
            for i in fin:
                fout.write(i + "\n")
            fout.close()
    if keyword not in synonyms_visited:
        synonyms_visited.append(keyword)
        synonyms = list(wordnet.synsets(keyword))
        if len(synonyms) > 0:
            synonyms.extend(list(synonyms[0].hyponyms()))
            synonyms.extend(list(synonyms[0].hypernyms()))
            synonyms.extend(list((synonyms[0].lemmas())[0].antonyms()))
        flag = False
        for cur in synonyms:
            if (cur.name()[:4]).lower() in keyword:
                continue
            out = cur.name().split('.')[0]
            pyautogui.write(' '.join(out.split('_')))
            pyautogui.press('enter')
            time.sleep(1.5)
            flag = True
            break
        if flag:
            continue
    elif synonyms_visited.count(keyword) < 3:
        ind = synonyms_visited.count(keyword)
        synonyms_visited.append(keyword)
        k = 0
        flags = False
        while k < ind:
            try:
                if (synonyms[k].name()[:4]).lower() in keyword:
                    ind += 1
            except IndexError:
                flags = True
                break
            k += 1
        if not flags:
            try:
                out = synonyms[k].name().split('.')[0]
                pyautogui.write(' '.join(out.split('_')))
                pyautogui.press('enter')
                time.sleep(1.5)
                continue
            except IndexError:
                pass
    if flag or not flags:
        cnt = 0
        finopen = open("wrongs.txt")
        fin = [i.rstrip() for i in finopen.readlines() if i != "\n"]
        finopen.close()
        if keyword not in fin:
            fin.append(keyword)
        fout = open("wrongs.txt", 'w')
        for i in fin:
            fout.write(i + "\n")
        fout.close()
    try:
        if initkind != datak.index(keyword):
            initkind = datak.index(keyword)
            kind = initkind
            if pastkeyword != False and pastkeyword not in ez_dict:
                ez_dict[pastkeyword] = out.lower()
            with open("right.json", 'w') as fin:
                json.dump(ez_dict, fin)
            fin.close()
            cnt += 1
        else:
            cnt = 0
            finopen = open("wrongs.txt")
            fin = [i.rstrip() for i in finopen.readlines() if i != "\n"]
            finopen.close()
            if keyword not in fin:
                fin.append(keyword)
            fout = open("wrongs.txt", 'w')
            for i in fin:
                fout.write(i + "\n")
            fout.close()
    except KeyError:
        pass
    except ValueError:
        continue
    kind += 1
    flagged = False
    while True:
        if d.check(datak[kind]) and datak[kind].isalpha() and datak[kind].islower() and (
                datak[kind][:4]).lower() not in keyword:
            for cur in names:
                if language_model(keyword).similarity(language_model(cur)[0]) > language_model(keyword).similarity(
                        language_model(datak[kind])[0]):
                    kind += 1
                    flagged = True
                    break
            if flagged:
                flagged = False
                continue
            out = datak[kind]
            break
        else:
            kind += 1
    pyautogui.write(' '.join(out.split('_')))
    pyautogui.press('enter')
    time.sleep(1.5)