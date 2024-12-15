from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize
from utils.deepseek import get_deepseek
import re
from utils.para import  get_discription,process_response
import json

def process_html_text(html_text):
    text=html_text.replace("&nbsp;","")
    text = text.replace("<i class=\"nite-writer-pen_2\">", "")
    text = text.replace("<i class=\"nite-writer-pen\">", "")
    text = text.replace("</i>", "")
    sentences = sent_tokenize(text)

    return sentences
def get_css_content(html_text):
    soup = BeautifulSoup(html_text, 'lxml')
    target_tags = soup.find_all("i", class_=["nite-writer-pen_2","nite-writer-pen"])
    extracted_texts = [tag.get_text(strip=True) for tag in target_tags]
    temp=[]
    for item in extracted_texts:
        sentence=sent_tokenize(item)
        if len(sentence)==1:
            temp.append(item)
        else:
            for item2 in sentence:
                temp.append(item2)
    return temp

def matching_alg(sen1,sen2):
    data=[]
    for item in sen1:
        temp=[]
        temp.append(item)
        temp2=[]
        for choice in sen2:
            if choice in item:
                temp2.append(choice)
                sen2.remove(choice)
        temp.append(temp2)
        data.append(temp)
    return data


def simplify_complex_content(con_list,tag):
    temp=[]
    client=get_deepseek()
    target_sentence=con_list[0]
    operate=con_list[2]
    dis = get_discription(tag)
    example1 = """Target_Sentence:Finally, the scientists applied the same method to data from two large psychology studies of American teens.version 1:Joel and her team then applied the same method to two large studies of American teens done by major universities.version 2:Joel and her team then applied the same method to two large studies of American teens.version 3:The scientists then looked at two large studies of American teens done by universities.version 4:The scientists then studied two big groups of American teens."""
    example2 = "Target_Sentence:Councilman Joe Buscaino led an unsuccessful attempt to exempt bars and nightclubs from the ban, a measure sought by lobbyists for the e-cigarette industry.version 1:Councilman Joe Buscaino led an unsuccessful attempt to exclude bars and nightclubs from the ban, a measure sought by supporters of the e-cigarette industry.version 2:Councilman Joe Buscaino led an unsuccessful attempt to exempt bars and nightclubs from the ban, a measure sought by advocates for the e-cigarette industry.version 3:Councilman Joe Buscaino led an unsuccessful attempt to let bars and nightclubs still allow e-cigarettes.version 4:Councilman Joe Buscaino tried to let bars and nightclubs still allow e-cigarettes."
    example3 = "Target_Sentence:He would remotely log on to people's sluggish computers and optimize the machine's performance for $25.version 1:For $25, he would remotely log on to people's slow-running computers and help the computers run faster.version 2:For $25, he would remotely log on to people's computers, which were running too slow, and help them perform better.version 3:For $25, he would help people's computers run faster.version 4:For $25, he fixed computers so they ran faster."
    if operate==1:
        temp.append(0)
        temp.append(target_sentence)
        return temp
    elif operate==3:
        try:
            messages = [
                {"role": "user",
                 "content": f"Target_Sentence:{target_sentence} \n You are a text simplification expert. You need to simplify the sentence while maintaining the original meaning. You need to generate four versions of the simplified sentence, each version becoming more and more readable. VERSION 1 has the least readable simplified sentences and is targeted at ninth grade students with a vocabulary of approximately 5,500. The target audience of simplified sentences of VERSION 2 is 7th grade students with a vocabulary of about 3300. The target audience of simplified sentences of VERSION 3 is 5th grade students with a vocabulary of about 2500. The simplified sentences of VERSION 4 are the most readable and the target audience is students with a vocabulary of about 2500. for 1,000 3rd graders."},
                {"role": "assistant", "content": " Please give some simplified examples."},
                {"role": "user", "content": f"example1:{example1} example2:{example2} example3:{example3} "},
                {"role": "assistant", "content": "Are there any other requirements?"},
                {"role": "user",
                 "content": """Just return simplified sentences . Return json format ```{"version1": "xxx","version2": "xxx", "version3": "xxx","version4": "xxx"}``` with NO other texts."""},
            ]
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=messages,
                temperature=1.3
            )
            re = response.choices[0].message.content
            # re = process_response(re)
            re = re.replace("```", "")
            re = re.replace("json", "")
            # print(re)
            sentence4 = json.loads(re)
            if tag == 1:
                sc= sentence4["version1"]
            elif tag == 2:
                sc= sentence4["version2"]
            elif tag == 3:
                sc= sentence4["version3"]
            elif tag == 4:
                sc= sentence4["version4"]
            temp.append(2)
            temp.append(sc)
            temp.append("")
            return temp
        except:
            temp.append(0)
            temp.append(sc)
            temp.append("")
            return temp
    else:

        complex_words_list=con_list[1]
        sy_temp=[]
        sen_temp=target_sentence
        for item in complex_words_list:
            messages = [
                {"role": "user",
                "content": f"Contextual_Information:{target_sentence} \n TargetWords:{item} \n Reader_Readingability_information:{dis} You are an English language expert，when users input  complex word, phrases, or short sentences, you need to combine context information and the reader's ability information to generate corresponding simplified results.The simplified content replaces the original content in the context information and needs to be appropriate and fluent.If there is punctuation in the content that needs to be simplified, don't miss the punctuation that comes with the content that needs to be simplified."},
                {"role": "assistant",
                "content": "I will generate a unique alternative simplified content for target_words that needs to be simplified by the user. Are there any other requirements?"},
                {"role": "user",
                "content": "Return strictly as requested. Return ```OUTPUT your_generated_synonym ``` with NO other texts."},
            ]
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=messages,
                temperature=1.3
            )
            re=response.choices[0].message.content
            re=re.replace("```", "")
            re = re.replace("OUTPUT", "")
            sy_temp.append(re)
            sen_temp=sen_temp.replace(item,re)
        temp.append(1)
        temp.append(sen_temp)
        temp.append(sy_temp)
        return temp


def checking_tag(sen_list):
    temp=sen_list
    if  sen_list[1]!=[]:
        if (len(sen_list[0])-len(sen_list[1][0])<=4) & (len(sen_list[1])==1):
            temp.append(3)
        else:
            temp.append(2)
    else:
        temp.append(1)
    return temp

def get_simplify(text,tag):
    sentences = process_html_text(text[0])
    css_content = get_css_content(text[0])
    data = matching_alg(sentences, css_content)
    def process_item(item):
        item = checking_tag(item)
        re = simplify_complex_content(item, tag)
        return re
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(process_item, item): idx for idx, item in enumerate(data)}
        results = [None] * len(data)
        for future in futures:
            idx = futures[future]
            result = future.result()
            results[idx] = result
    return results


