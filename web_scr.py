import requests
from bs4 import BeautifulSoup as bs
import pandas
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource
from bokeh.models import NumeralTickFormatter,HoverTool
from bokeh.embed import components


def web_scr1():
    list1=[]
    r = requests.get("http://www.pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/", headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
    c=r.content
    soup=bs(c,'html.parser')
    pag_number2=soup.find_all('a',{"class":'Page'})[-1].text
     # to find page number 1st method
    int(pag_number2)
    list1=[]
    count=0
    base_url='http://www.pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/t=0&s='
    for x in range(0,int(pag_number2)*10,10):
            URL1=base_url+str(x)+".html"
            print(URL1)
            r = requests.get(URL1, headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
            c=r.content
            soup=bs(c,"html.parser")
            p_r=soup.find_all('div',{"class":"propertyRow"})
            print("p_r",len(p_r))
            for x in p_r:
                count=count+1
                items={}
                price=x.find_all('h4',{"class":"propPrice"})[0].text.replace("\n","").replace(" ","")
                print(price)
                items["Price"]=price
                Ad1=x.find_all('span',{"class":"propAddressCollapse"})[0].text
                print(Ad1)
                items["Ad1"]=Ad1
                Ad2=x.find_all('span',{"class":"propAddressCollapse"})[1].text
                print(Ad2)
                items["Ad2"]=Ad2
                try:
                    bed=(x.find_all('span',{"class":"infoBed"}))[0].find('b').text
                    print(bed)
                    items["bed"]=bed
                except:
                    print('None')
                    items["bed"]='NA'
                try:
                    sq_ft=(x.find_all('span',{"class":"infoSqFt"}))[0].find('b').text
                    print(sq_ft)
                    items["sq_ft"]=sq_ft
                except:
                    print('None')
                    items["sq_ft"]='NA'

                try:
                    full_bath=(x.find_all('span',{"class":"infoValueFullBath"}))[0].find('b').text
                    print(full_bath)
                    items["full_bath"]=full_bath
                except:
                    print('None')
                    items["full_bath"]='NA'

                try:
                    half_bath=(x.find_all('span',{"class":"infoValueHalfBath"}))[0].find('b').text
                    print(half_bath)
                    items["half_bath"]='half_bath'
                except:
                    print('None')
                    items["half_bath"]='NA'
                c_g=x.find_all('div',{"class":"columnGroup"})
                for t in c_g:
                    fg=t.find_all('span',{"class":"featureGroup"})
                    fn=t.find_all('span',{"class":"featureName"})
                    for a,b in zip(fg,fn):
                        if "Lot Size" in a.text:
                            items["Lot"]=b.text
                            print(b.text)
                            print("true")
                print(" ")
                list1.append(items)
            print(count)

    df=pandas.DataFrame(list1)
    df.to_csv("web_data.csv")
    a=graph(df=df)
    a.append(df)
    return a



def f(x):
    if x==0:
        return 'NA'
    else:
        return x

def graph(df):
    df["Price"]=df["Price"].astype(str)
    f=lambda x : x.replace("$","")
    df["Price1"]=df["Price"].apply(f)
    h=lambda x : x.replace(",","")
    df["Price1"]=df["Price1"].apply(h)
    df["Price1"]
    #Replacing NA with 0 and removing ',' from area
    df["sq_ft"]=df["sq_ft"].astype(str)
    g=lambda x : x.replace(",","")
    #df["sq_ft1"]=df["sq_ft"].replace("NA",0)
    df["sq_ft1"]=df["sq_ft"].apply(g)
    df["sq_ft1"]=df["sq_ft1"].replace("NA",0)
    p=figure(plot_width=1000,plot_height=500,tools='pan')
    p.xaxis.minor_tick_line_color=None
    p.xgrid[0].ticker.desired_num_ticks=10
    df["Price1"]=df["Price1"].astype(int)
    df["sq_ft1"]=df["sq_ft1"].astype(int)
    d = {'Price' :df["Price1"],'sq_ft1' : df["sq_ft1"],'Address': zip(df["Ad1"],df["Ad2"])}
    df1 = pandas.DataFrame(d)
    #print (df1)
    df1["sq_ft2"]=df1["sq_ft1"].astype(str)
    df1["sq_ft2"]=df1["sq_ft2"].apply(f)
    cds = ColumnDataSource(df1)

    hover=HoverTool(tooltips=[("Address","@Address"),("Price" ,"@Price"),("Area","@sq_ft2")])
    p.add_tools(hover)
    #p.line(df["Price"],df["sq_ft"],line_width=2,source=cds)
    #p.line(x="Price",y="sq_ft1",line_width=2,source=cds)
    p.circle(x="Price",y="sq_ft1",size=10,source=cds)
    p.xaxis.formatter=NumeralTickFormatter(format="00")
    #output_file("web_rk.html")
    #show(p)
    script1, div1= components(p)
    return ([script1,div1])

#a=web_scr1()
#print(a)
