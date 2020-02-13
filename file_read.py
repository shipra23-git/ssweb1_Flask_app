import pandas
from io import StringIO
from geopy.geocoders import ArcGIS
import folium
def geoconvert(df5):

    nom = ArcGIS()
    print(type(df5))
    df5=df5.set_index("ID")
    print(df5.Address)
    df5['full_Address']=df5['Address']+','+ df5['State']+','+df5['Country']
    print("fULLADDRSSSS",df5)
    df5['geoLocation']=df5['full_Address'].apply(nom.geocode)
    print("geo",df5)
    # calculate Latitude
    df5['latitude']=df5['geoLocation'].apply(lambda x: x.latitude if x != None else None)
    print("lat",df5)
    df5['longitude']=df5['geoLocation'].apply(lambda x: x.longitude if x != None else None)
    print("lon",df5)
    df6=df5.drop(df5.columns[6:8],1)
    print(df6)
    df5.to_csv('a2.csv')
    return df6
