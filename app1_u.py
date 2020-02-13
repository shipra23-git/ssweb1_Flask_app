import json
from difflib import get_close_matches
from difflib import SequenceMatcher
from flask import Flask,url_for,render_template
with open ('data.json','r') as f:
    d=json.load(f)

def translate_close_match(d,g):
        #for x in g:
            ans="Did you mean %s ? Press Y for Yes , N for NO:" % g
            d={'flag':1,'l':g}
            #return ans#render_template("dict.html",flag=1,name=ans)
            return d
            #if (ans=='Y'):
                #return d[x]
                #break
            #elif(ans=='N' and (x!=g[-1])):
                #continue
            #elif(x==g[-1]):
                #return ('Word Not Found!')
            # return ('Word Not Found!')
            #else :
                #return ('Incorrect Entry!')#

def get_closest_match(wl,wU,wT):
    gl=get_close_matches(wl,d.keys(),2,0.7)
    gU=get_close_matches(wU,d.keys(),2,0.7)
    gT=get_close_matches(wT,d.keys(),2,0.7)
    '''print("gl: ",gl)
    print("gU:",gU)
    print("gT: ",gT)'''
    if (len(gl)>0):
        l=SequenceMatcher(None,wl,gl[0]).ratio()
    else:
       l=0.0
    if (len(gU)>0):
           U=SequenceMatcher(None,wU,gU[0]).ratio()
    else:
       U=0.0
    if(len(gT)>0):
          T=SequenceMatcher(None,wT,gT[0]).ratio()
    else:
       T=0.0
    '''print("gl: ",l)
    print("gU:",U)
    print("gT: ",T)'''
    a=max(l,U,T)
    if (a!=0.0 and a==l):
        print(gl)
        ans=translate_close_match(d,gl)
    elif (a!=0.0 and a==U):
        print(gU)
        ans=translate_close_match(d,gU)
    elif (a!=0.0 and a==T):
        print(gT)
        ans=translate_close_match(d,gT)
    elif a==0:
         ans={'flag':4,'l':'Word not Found!!'}
         #ans= 'Word not Found!!'
    return ans

def translate(w):
    wl=w.lower()
    wU=w.upper()
    wT=w.title()

    if (wl in d.keys()):
            a={'flag':0,'l':d[wl]}
            return a
            #return d[wl]
    elif (wU in d.keys()):
            b={'flag':0,'l':d[wU]}
            return b
            #return d[wU]
    elif (wT in d.keys()):
            c={'flag':0,'l':d[wT]}
            return c
            #return d[wT]
    else:
        ans=get_closest_match(wl,wU,wT)
        return ans

        #x=input('Enter word: ')
def t_w(word):
    output=translate(word)
    return output
        #if type(output)==list :
            #for x in output:
            #    print(x)
            #else :
                #print(output)
