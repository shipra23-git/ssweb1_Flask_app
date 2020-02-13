import pandas
import requests
from bs4 import BeautifulSoup as bs
def olx():
    r=requests.get("https://www.olx.in/accessories_c1457",headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
    r.status_code

    a=r.content

    soup=bs(a,"html.parser")
    a=soup.find_all('li',{'data-aut-id':'itemBox'})
    li=[]
    for a1 in a:
        items={}
        items["price"] = a1.find_all('span',{'class':'_89yzn','data-aut-id':'itemPrice'})[0].text
        items["title"] = a1.find_all('span',{'class':'_2tW1I','data-aut-id':'itemTitle'})[0].text
        link=a1.find_all('a',{'class':'fhlkh'})
        try:
            a2=link[0].find_all('figure',{'class':'_2grx4'})[0].find_all('img')[0]['srcset']
            a2=a2.splitlines()
            x1=[]
            for x in a2:
                x1.append(x[:-5])
            a2=x1
            items["links"]=a2
        except:
            items["links"]="NO links found"
        li.append(items)
    df=pandas.DataFrame(li)
    return df

def save_csv(df):
      df.to_csv('data_olx.csv')
