import ast
from difflib import SequenceMatcher
database =  []
sequences = []
wordcounts = dict()
row_ID = 0
last_answer = [" ? "]

def think(prompt):
    prompt_li = prompt.split(" ")
    last_word_of_prompt = prompt_li[-1]
    likely_following_words = findNextWord(last_word_of_prompt)
    likely_proceeding_words = findLastWord(prompt_li[0])
    likely_following_words = likely_following_words + likely_proceeding_words
    answer = " ? "
    answer_highscore = -3
    answer_score = 0
    global row_ID
    global last_answer
    global wordcounts
    row_ID = 0
    NEW_VALUE = 0
    best_answer = ""
    highscore_of_following_words = 0
    for x in database:
        for i in x.keys():
            score_of_following_words = 0
            
            for word_i in likely_following_words:
                if word_i in i:
                    score_of_following_words +=1
                    if word_i in wordcounts:
                        score_of_following_words += wordcounts.index(word_i)
                    
                    if score_of_following_words > highscore_of_following_words and i not in last_answer:
                        best_answer = i
                        #print(word_i + " ----> "+ i)
                
            if prompt in i or i in prompt or similar(i,prompt) > 0.7 or score_of_following_words > 0:
                answer_score = x[i] + score_of_following_words
                NEW_VALUE = 1
                if answer_score > answer_highscore:
                    answer = max(x, key=x.get)
                    

                        
                    answer_highscore = answer_score
                    if i != prompt:
                        row_ID = database.index(x)
                
    createAssociation(prompt)
    
    if best_answer == "":
        
        return answer
    else:
        
        return best_answer
    
def createAssociation(prompt):
    global database
    repeated_entry = 0
    for x in database:
        for i in x.keys():
            if prompt in i or i in prompt:
                repeated_entry = 1
                if prompt == i:
                    continue

                if database.index(x) != 0 and len(x)<3:
                    x[prompt]=0
                    print("****NEW VALUE ADDED TO EXISTING DICT****")
                    commit_to_memory()
                    break
            
                else:
                    database.append({prompt:0})
                    print("****NEW DICT ADDED TO DATABASE****")
                    commit_to_memory()
                    break
    
    if repeated_entry == 0:
        database.append({prompt:0})
        print("****NEW DICT ADDED TO DATABASE****")
        commit_to_memory()
    
def findNextWord(word):
    global sequences
    nextword = "<empty>"
    word_li = []
    for srow in sequences:
        if word in srow and srow.index(word) < len(srow)-1:
            nextword = srow[srow.index(word)+1]
            
            if nextword not in word_li and nextword != "" and nextword != " ? ":
                word_li.append(nextword)
    
    print(word_li)
    return word_li

def findLastWord(word):
    global sequences
    lastword = "<empty>"
    word_li2 = []
    for srow in sequences:
        if word in srow and srow.index(word) > 0:
            lastword = srow[srow.index(word)-1]
            
            if lastword not in word_li2 and lastword != "" and lastword != " ? ":
                word_li2.append(lastword)
    
    print(word_li2)
    return word_li2
    
def study():
    global database
    database = []
    global sequences
    sequences = []
    try:      
        with open('data.txt', 'r') as file:
            lines = []
            lines = file.readlines()
            lines = [line.rstrip() for line in lines]
            database2 = lines
            for i in database2:
                d = ast.literal_eval(i)
                database.append(d)
                for e in d.keys():
                    sequences.append(e.split(" "))
            
            #print(sequences)
            #print(database)
            file.close()
        

    except:
        print("NO DATA")
        return "NO DATA"

def commit_to_memory():
    global database
    x_li = []
    for x_i in database:
        if x_i not in x_li:
            x_li.append(x_i)
            
    lines = x_li
    with open('data.txt', 'w') as f:
        for line in lines:
            f.write(str(line))
            f.write('\n')
        
        f.close()
    study()

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def createCommonDict():
    global database
    
    global wordcounts
    wordcounts = {}
    for i in database:
        for x in i.keys():
            x2 = x.split(" ")
            for xx in x2:
                if xx in wordcounts and xx != "":
                    wordcounts[xx] += 1
                else:
                    wordcounts[xx] = 1
    
    wordcounts = sorted(wordcounts.items(), key=lambda x: x[1], reverse=True)  
    print(wordcounts)
    
    
    

study()
createCommonDict()
start = 1
while start == 1:
    prompt = input("Prompt: ")
    if " " not in prompt:
        prompt = " "+prompt+" "
        
    if prompt == "?":
        print("...")
        continue
        
    if prompt == "+" and len(last_answer)>0:
        database[row_ID][last_answer]+=1
        continue
        
    if prompt == "-" and len(last_answer)>0:
        database[row_ID][last_answer]-=1
        continue
        
    answer = think(prompt)
    last_answer.append(answer)
    print("Answer: "+answer)