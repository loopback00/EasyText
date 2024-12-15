import re
from bs4 import BeautifulSoup

def get_discription(tag: int):
    dis_4 = "Reader  has a 3rd grade reading ability and a vocabulary of approximately 1000. "
    dis_3 = "Reader  has a 5rd grade reading ability and a vocabulary of approximately 2500."
    dis_2 = "Reader  has a 7rd grade reading ability and a vocabulary of approximately 3300."
    dis_1 = "Reader  has a 9rd grade reading ability and a vocabulary of approximately 5500."
    # dis_4="The reader is an  elementary school student with a vocabulary of 2500"
    # dis_3="The reader is an  middle school students student with a vocabulary of 4500"
    # dis_2="The reader is an  high school student with a vocabulary of 6500"
    # dis_1="The reader is an  college school student with a vocabulary of 8500"
    if (tag == 1):
        return dis_1
    elif (tag == 2):
        return dis_2
    elif (tag == 3):
        return dis_3
    elif (tag == 4):
        return dis_4
def process_response(re):
    re = re.replace("OUTPUT", "")
    re = re.replace("\n", "")
    re = re.replace("```", "")
    re = re.replace(":", "")
    re = re.replace("*", "")
    # re=re.replace(","," ")
    re = re.replace(".", "")
    re = re.strip()
    return re
def get_para_structure(text):
    text = text.replace("&nbsp;", "")
    paralist = re.split(r'<br>|</br>', text)
    filtered_list = [item for item in paralist if item and item.strip()]
    data = []
    for i in range(len(filtered_list)):
        temp = []
        temp.append(paralist[i])
        data.append(temp)
    return data

#
# data=get_para_structure("In Corolla, North Carolina, a small island known for its wild mustangs, these horses face numerous challenges. The mustangs, also known as mustangs, are free-roaming and not owned by anyone. Their origins are a mystery, but researchers believe they may have belonged to Spanish explorers whose ships got stranded near the island, forcing the horses to swim ashore. Despite the harsh weather, including hurricanes, the mustangs have survived for hundreds of years without barns or shelter.</br>However, the Corolla herd is now facing new and significant problems. While hurricanes were once their biggest threat, human activity has become a major issue. Many tourists visit Corolla to see the famous wild horses, but some visitors disturb the animals or leave trash in their habitat. Additionally, vacation homes built near the beach to allow people to observe the mustangs are encroaching on their limited space. The mustangs cannot leave the island to find safer or more peaceful areas to live, nor can they find mates outside their herd, leading to inbreeding. This has resulted in serious health issues for their foals, such as broken legs or deformities.</br>To address these challenges, volunteers have come together to help save the Corolla herd. Their goal is to provide the mustangs with more space to roam and to increase the herd's population from 101 to 130 horses. To achieve this, they plan to bring wild horses from another island off North Carolina to introduce new genetic diversity, which will improve the health of future foals.</br>Despite the efforts of volunteers and horse lovers, the Corolla herd still faces another problem: some horses cross into the island's wildlife refuge, which is home to endangered birds and nesting sea turtles. The government is concerned that the horses could harm these other animals. David Viker, a refuge manager, is working with a scientist to find ways to reduce the horses' disabilities and determine how many horses can coexist with the refuge's wildlife. Viker emphasizes the importance of the Corolla herd as an iconic symbol of the region, highlighting the need for a balanced solution that protects both the horses and the island's other inhabitants.</br>")
# for item in data:
#     print(item)
