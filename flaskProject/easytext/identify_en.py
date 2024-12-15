from utils.deepseek import get_deepseek
from nltk.tokenize import sent_tokenize
from utils.para import get_discription,process_response
from concurrent.futures import ThreadPoolExecutor

def get_sentence_complex_deepseek(sentence,discription):
    client=get_deepseek()
    temp=[]
    messages = [
        {"role": "user",
         "content": f"Target_Sentence:{sentence}  \n   Reader_discription: {discription} \n  You are a linguist, and you need to analyze sentences by gathering information about the readers' abilities. Lexical analysis: Analyze whether the target sentence contains long words, low-frequency words, technical terms, compound words, etc., which are complex for readers. Sentence structure analysis: Analyze whether the text contains long sentences. Long sentences often contain too much clause information and are less readable. Analyze whether the text is long, repetitive, or overly embellished, which makes it difficult to read. Finally, based on the above analysis, if the sentence is not difficult for readers in terms of vocabulary and sentence structure, return to 1.The sentence is a compound sentence or the sentence is not short or contains some clauses, return 3. If the  sentence structure is simple, the sentence length is appropriate, and there are no syntactic or embellishing relationships that make it difficult for the reader to understand, but there are some complex words, return to 2; "},
        {"role": "assistant",
         "content": "I will consider the user's ability information, especially their grade and vocabulary information.I will judge the sentences according to your requirements.Are there any other format requirements?"},
        {"role": "user",
         "content": "Only return  number 1 or number 2 or number 3 to represent your judgment without any analysis .Return ```OUTPUT your_judgment_result ```with NO other texts."},

    ]
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        temperature=1.3
    )
    re = response.choices[0].message.content
    re=process_response(re)
    # print(re)
    if "3" in re:
        temp.append(3)
        temp.append(sentence)
        temp.append("")
    elif "1" in re:
        temp.append(1)
        temp.append(sentence)
        temp.append("")
    else:
        messages = [
            {"role": "user",
             "content": f"Target_Sentence:{sentence}  \n Reader_Readingability_information:{discription}  \n You are an experienced linguist. Readers find that the target sentence contains some complex vocabulary. Identify complex words in the target sentence based on the reader's reading ability. Person names, organizational names, and place names are not complex words. Discontinuous words, conjunctions, pronouns, and prepositions are not complex words. Complex words include long words, compound words, rare phrases, etc. Complex words usually appear in verbs, adjectives, adverbs, and nouns."},
            {"role": "assistant",
             "content": "I will identify the complex words of the sentence in conjunction with the reader's reading ability. Are there any other requirements?"},
            {"role": "user",
             "content": "Only return complex words in sentences separated by “,”.Return ```OUTPUT your_recognized_complex_words ```with NO other texts."},

        ]
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            temperature=1.3
        )
        re = response.choices[0].message.content
        re = process_response(re)
        word_list=re.split(",")
        temp.append(2)
        temp.append(sentence)
        temp.append(word_list)

    return temp

def identify_complex_conponent_en_bf(complex_text, tag):
    reader_info = get_discription(tag)
    sentences = sent_tokenize(complex_text)
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(get_sentence_complex_deepseek, sentence, reader_info): idx for idx, sentence in
                   enumerate(sentences)}
        data = [None] * len(sentences)
        for future in futures:
            idx = futures[future]
            data[idx] = future.result()
    return data

# t1=time.time()
# data=identify_complex_conponent_en_bf("However, the Corolla herd is now facing new and significant problems. While hurricanes were once their biggest threat, human activity has become a major issue. Many tourists visit Corolla to see the famous wild horses, but some visitors disturb the animals or leave trash in their habitat. Additionally, vacation homes built near the beach to allow people to observe the mustangs are encroaching on their limited space. The mustangs cannot leave the island to find safer or more peaceful areas to live, nor can they find mates outside their herd, leading to inbreeding. This has resulted in serious health issues for their foals, such as broken legs or deformities."
#                              ,2)
# t2=time.time()
# print(t2-t1)
# for item in data:
#     print(item)