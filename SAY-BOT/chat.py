import nltk
from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords
import string
######## Preparing Corpus ###################
QA={}
def process():
    s=open('WikiQACorpus/WikiQA.tsv','rb')
    temp=s.read()
    data=temp.split('\n')
    s=""
    j=0
    prev=""
    noofqu=0
    for i in data:
        t=i.split('\t')
        j=j+1
        if j<29260:
            new=str(t[1])
            s1=str(t[5])
            if(prev!=new):
                QA[prev]=s
                s=s1;
                noofqu=noofqu+1
            else:
                s+=s1
            prev=new
    return noofqu
print("No Of Question: "+str(process()))
# print(QA)
# for i in QA:
#     print(i+" : \n"+QA[i]+"\n")
# for i in QA:
#     print i
CFD={}

######### Creating CFD (Conditional Frequency Distribution)
j=0
stop_words=set(stopwords.words("english"))
print stop_words
for i in QA:
    answer=QA[i]
    # j=j+1
    # if j<25:
    i= i.translate(None, string.punctuation)
    words=word_tokenize(i)
    filtered_sentence=[]
    filtered_sentence=[w for w in words if not w in stop_words]
    l=len(filtered_sentence)

    for i in filtered_sentence:
        if i not in CFD:
            CFD[i]=[];
        CFD[i].append((answer[:100],(1000/l)))

# print(v);
# for i in CFD:
#     print(i,len(CFD[i]))
# print(CFD)
newCFD={}
########### Processing Input########
print("Hi! I am SAY-BOT. Ask me Something!")
while True:
    newCFD={}
    print("You : ")
    i=raw_input()

    words=word_tokenize(i)
    filtered_sentence=[]
    filtered_sentence=[w for w in words if not w in stop_words]

############# CASE 1 : all prompt words are given equal weight
    # for i in filtered_sentence: # for every input word
    #     if i in CFD:            # check word is present in CFD
    #         for j in CFD[i]:    # for every responce of that word
    #             if j[0] in newCFD:
    #                 newCFD[j[0]]+=j[1]
    #             else:
    #                 newCFD[j[0]]=j[1]

############# CASE 2 : Divide by total
    for i in filtered_sentence: # for every input word
        if i in CFD:            # check word is present in CFD
            total=0
            for j in CFD[i]:    # calculate total of all possible responce of word
                total+=j[1]
            # print(total)
            for j in CFD[i]:    # for every responce of that word
                if j[0] in newCFD:
                    newCFD[j[0]]+=(j[1]*1000/total)
                else:
                    newCFD[j[0]]=(j[1]*1000/total)
    # print newCFD
    ip=max(newCFD, key=newCFD.get)
    response=ip
    print("SAY-BOT : "+response)
