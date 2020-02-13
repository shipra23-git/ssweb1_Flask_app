from pandas_datareader import data
from datetime import datetime
from bokeh.plotting import figure,show,output_file
from bokeh.models import ColumnDataSource
from bokeh.embed import components
from bokeh.resources import CDN
def stock_file():
    start=datetime(2019,3,1)
    end=datetime(2019,3,20)
    df=data.DataReader(name="AAPL",data_source="yahoo",start=start,end=end)

    li=[]
    for x,y in zip(df.Close,df.Open):
        if (x>y):
            li.append("Increase")
        elif x<y:
            li.append("Decrease")
        else:
            li.append("Equal")
    df["Status"]=li
    df["Middle"]=(df.Open+df.Close)/2
    df["height"]=abs(df.Close-df.Open)

    p=figure(plot_width=500,plot_height=200,x_axis_type="datetime",sizing_mode="scale_width")
    p.title.text="Candlestick Chart"
    p.grid.grid_line_alpha=0.3 #to add transarency
    hours_12=12*60*60*1000
    date_diff=end-start
    date_diff.days
    p.segment(df.index,df.High,df.index,df.Low)
    #below syntax didint word as it was not filtering y axis values and only filter was applied on x axisresulting in incorrect plot
    #p.rect(df.index[df.Close >df.Open],(df.Open+df.Close)/2,hours_12,abs(df.Close-df.Open) ) #x axis values , center of rect,width of rec, height og rect

    p.rect(df.index[df.Status=="Increase"],df.Middle[df.Status=="Increase"],hours_12,
           df.height[df.Status=="Increase"],fill_color="green",line_color="black")

    p.rect(df.index[df.Status=="Decrease"],df.Middle[df.Status=="Decrease"],hours_12,
           df.height[df.Status=="Decrease"],fill_color="Pink",line_color="black")
    #p.segment(df.index,df.High,df.index,df.Low) adding it afterwards produces line above rect
    p.xaxis.minor_tick_line_color=None
    #p.xgrid[0].ticker.desired_num_ticks=date_diff.days
    #p.xaxis[0].DaysTicker.days=1

    #output_file("CS.html")
    #show(p)
    script1,div1=components(p)
    cdn_js=CDN.js_files[0]
    return([script1,div1,cdn_js])

#a=stock_file()
#print(a)
