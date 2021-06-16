def templating(model_keywords):
    model_keywords = model_keywords.split(",")
    n = -1
    for i in model_keywords:
        n+=1
        model_keywords[n] = model_keywords[n].lower()
        if "|" in i:
            model_keywords[n] = i.split("|")
    return list(filter(lambda i:i!="",model_keywords))

def empty_model_keywords_response(model_awnser):    #Model Answer Reference Procedure
    model_keywords = []
    excepted_syms = ["=","+","-","/",">","<","%","^","$"]
    common_words = ["the","of","and","a","to","in","is","that","it","for","on","are","as","with","at","be","this","have","or","by","been","but",'has','only']
    placeholder = list(model_awnser.replace(", "," ").replace(","," ").replace(".",""))
    n = -1
    for i in placeholder:
        n+=1
        if i in excepted_syms:
            continue
        elif not i.isalpha() and not i.isdigit() and not i.isspace():
            placeholder[n] = ""
    placeholder = filter(lambda x:x not in common_words,"".join(placeholder).split(" "))
    return ",".join(list(map(lambda text:text.lower(),placeholder)))

def give_score(response,model_awnser,model_keywords,banned_words = []):
    if model_keywords == "None":
        model_keywords = empty_model_keywords_response(model_awnser)
        return give_score(response,model_awnser,model_keywords,banned_words)
    else:
        raw_keywords = str(response)
        model_keywords = templating(model_keywords)
        response = response.split(" ")
        #Debug Statement - print(f"{model_keywords}\n||\n{response}")
        score = 0
        #if len(list(filter(lambda x:x not in banned_words,response)))>0:
          #return 0
        print("=>")
        for i in model_keywords:
          if type(i) != list:
            print(f"{i} in {response}")
            if len(i.split(" "))>1:
              if raw_keywords.find(i)!=-1:
                score+=1
            elif i in response:
                score+=1
          else:
            for n in i:
              print(f"{n} in {i} in {response}")
              if len(n.split(" "))>1:
                if raw_keywords.find(n)!=-1:
                  score+=1
                  break
              elif n in response:
                  score+=1
                  break

        return (round(score/len(model_keywords),2)*100)

def Acell(sheet,cell_ref):
    _alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    alpha_ref,c = "",0
    for i in cell_ref:
        if i.isalpha():
            alpha_ref+=i.upper()
            c+=1
    print("Before",alpha_ref,"Row",cell_ref[c:])
    print("Index Reference>>>",_alpha.index(alpha_ref),int(cell_ref[c:])-1)
    #Only Works for Single Column Alphabet Reference
    try:
        val = sheet[int(cell_ref[c:])-1][_alpha.index(alpha_ref)]
    except IndexError:
        val = ""
    return val

def get_sg_time():
    import pytz,datetime
    print("Time Now>>>",pytz.timezone('Asia/Singapore').localize(datetime.datetime.now()).strftime('%c'))
    return (pytz.timezone('Asia/Singapore').localize(datetime.datetime.now()).strftime('%c'))

def iqr(dist):
    import numpy as np
    return np.percentile(dist, 75) - np.percentile(dist, 25)
