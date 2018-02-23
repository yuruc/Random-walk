import sys
import os
import numpy as np
import string 


input_directory = sys.argv[1]
P = int(sys.argv[2]) #n-gram 
N = int(sys.argv[3])

n_gram = dict() #probablity distribution of n-gram 
n_gram_stat = dict() #condtional probablity distribution of p(w(i) | w(i-1), w(i-2)..)
n_gram_count = 0.0 #number of n-grams for normalization 
p_length = dict() 
#probablity distribution of paragraph length, i.e. p(w(i)=='<e>'), 
#can be used to model paragraph length but I didn't have time to include it 

p_length_count = 0.0 #number of paragraphs for normalization 
n_start = dict() #probablity distribution of start of paragraph n-grams 
n_start_count = 0.0 #number of start of paragraph n-grams for normalization 
start = '<s>' #mark start of paragragh
end = '<e>' #mark end of paragragh

############################helper functions############################ 

#Get the whole list of file under folder 
def get_filelist(folder):
    return [folder+'/'+name for name in os.listdir(folder)
            if not os.path.isdir(os.path.join(folder, name))]

#Build n_gram, p_length, n_start
def build_n_gram(P, paragraph, n_gram, p_length, n_start):
    global n_gram_count
    global p_length_count
    global n_start_count 
    n = len(paragraph)
    for i in range(n - P + 1):
        s = paragraph[i]
        for j in range(1, P):
            s += ' ' + paragraph[j + i]
        if s not in n_gram:
            n_gram[s] = 0.0
        if '<s>' in s:
            if s not in n_start:
                n_start[s] = 0.0
            n_start[s] += 1
            n_start_count += 1
        n_gram[s] +=1
        n_gram_count += 1
    if n not in p_length:
        p_length[n] = 0.0
    p_length[n] += 1
    p_length_count += 1

#Build n_gram_stat
def build_n_gram_count(P, paragraph, n_gram_next):
    for i in range(len(paragraph) - P):
        s = paragraph[i]
        for j in range(1, P):
            s += ' ' + paragraph[j + i]
        suffix = paragraph[i + P]
        if s in n_gram:
            if s not in n_gram_next:
                n_gram_next[s] = dict()
            if suffix not in n_gram_next[s]:
                n_gram_next[s][suffix] = 0.0
            n_gram_next[s][suffix] += 1

#Normalize as probability distribution 
def cal_table(n_gram, n_gram_next, n_start, p_length):
    for word in n_gram:
        n_gram[word] = n_gram[word] / n_gram_count
    for prex in n_gram_next:
        each_prex_count = 0.0
        for each_suffix in n_gram_next[prex]:
            each_prex_count+= n_gram_next[prex][each_suffix]
        for each_suffix in  n_gram_next[prex]:
             n_gram_next[prex][each_suffix] /= each_prex_count
    for p in p_length:
        p_length[p] /= p_length_count
    for s in n_start:
        n_start[s] /= n_start_count

#Generate random paragraphs
def random(n_start, n_gram, n_gram_next, N):
    p = '' #output paragraph

    #Randomly choose the start n-gram based on probility distribution 
    keys = list(n_start.keys()) 
    values = [n_start[x] for x in keys ]
    token = np.random.choice(keys, p = values) 
    p += token[4::] #not include <s>

    #start random walk 
    next_token = ''
    for i in range(N - P): #restrict number of token to N 
        
        #randomly choose the next token based on condtional probility distribution 
        next_k = list(n_gram_next[token].keys())
        next_v = [n_gram_next[token][x] for x in next_k]
        next_token = np.random.choice(next_k, p = next_v)

        if next_token == '<e>': 
        #if the next token is the end of the paragrah, stop random walk 
            break

        p += " " + next_token #append the next token to the output 
        new = token.split()
        token = " ".join(new[1::]) + ' '+next_token
        token = token.strip()

    print(p)    
    

############################main()############################
file_list = get_filelist(input_directory)

for each_file in file_list:
    with open(each_file, 'r') as file:
        for row in file.readlines():
            paragraph = row.split()
            paragraph = [token.strip(string.punctuation) for token in paragraph]
            paragraph = list(filter(len, paragraph))
            if len(paragraph) < P : # paragrath lenth less then prefix length
                    continue
            paragraph = [start] + paragraph + [end]
            build_n_gram(P, paragraph, n_gram, p_length, n_start)
            build_n_gram_count(P, paragraph, n_gram_stat)
cal_table(n_gram, n_gram_stat, n_start , p_length)        


for j in range(N):
    random(n_start, n_gram, n_gram_stat, 100) #restrict the max length of paragrah to 100 

print('number of unique prefix phrases =' + str(len(n_gram_stat))) 
#prefix includes start of paragraph token 

