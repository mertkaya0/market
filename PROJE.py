
from ürün import istek
import pandas as pd
from market import market
from market import your_loc
import folium
import os
from geopy import distance
from geopy import Point
import osmnx as ox
import networkx as nx
import random



def randommarket(your_location):
    m_adı = []
    lat = []
    lng = []
    for i in range(0,15):
        random_market = random.choice(["Migros", "Şok", "A101", "CarreforuSA"])
        random_loc1 = random.uniform(-0.0050, 0.0050)
        random_loc2 = random.uniform(-0.0050, 0.0050)
        new_my_lat = (your_location[0] + random_loc1)
        new_my_lng = (your_location[1] + random_loc2)
        m_adı.append(random_market)
        lat.append(new_my_lat)
        lng.append(new_my_lng)

    return pd.DataFrame({"Lat": lat,"Lng":lng, "Market": m_adı})

# your_loc() FONKSİYONU İLE MEVCUT OLDUĞUNUZ KONUMU ÖĞRENEBİLİRSİNİZ.
my_loc = your_loc()
#my_loc = 41.08562700972092, 29.00311207629971


# GOOGLE PLACES API KEYE SAHİPSENİZ AŞAĞIDAKİ FONKSİYONLA my_loc DEĞİŞKENİNDEKİ KOORDİNATIN ETRAFINDAKİ MARKETLERİ LİSTELER.
#df = market(my_loc)


#GOOGLE PLACES API KEYE SAHİP DEĞİLSENİZ AŞAĞIDAKİ FONKSİYONU KULLANARAK KONUMUNUZUN ETRAFINDA RASTGELE KONUMA SAHİP OLAN 15 ADET MARKET ÜRETEBİLİRSİNİZ.
df = randommarket(my_loc)

print(f"YOUR CURRENT LOC:{my_loc}")

küme = set()
for i in df["Market"]:
    b = str(i).split(" ")
    for j in b:
        if j == "Migros" or j == "migros" or j == "MİGROS" or j=="Mjet" or j=="mjet":
            df["Market"] = df["Market"].replace(i, "Migros")
            küme.add("Migros")
        elif j == "Şok" or j == "şok" or j=="Sok" or j=="sok" or j=="ŞOK" or j=="SOK":
            df["Market"] = df["Market"].replace(i, "Şok")
            küme.add("Şok")
        elif j == "CarrefourSA" or j == "carrefoursa" or j == "Carrefour" or j == "CARREFOURSA" or j == "CARREFOUR" or j == "CarrefourSa" or j=="carrefour" or j=="Carrefoursa-" or j=="CarrefourSA-":
            df["Market"] = df["Market"].replace(i, "CarrefourSA")
            küme.add("CarrefourSA")
        elif j == "A101" or j == "A-101" or j == "A" or j == "a101" or j == "a" or j == "a-101" or j=="A.101" or j=="a.101":
            df["Market"] = df["Market"].replace(i, "A101")
            küme.add("A101")

print(df)

ürün = input("ARAMA:")


A101 = pd.DataFrame({'Market': 'A101', 'Ürün Adı       ': [], 'Ürün Fiyatı': []})
Car = pd.DataFrame({'Market': 'CarrefourSA', 'Ürün Adı       ': [], 'Ürün Fiyatı': []})
Şok = pd.DataFrame({'Market': 'Şok', 'Ürün Adı       ': [], 'Ürün Fiyatı': []})
Migros = pd.DataFrame({'Market': 'Migros', 'Ürün Adı       ': [], 'Ürün Fiyatı': []})

if "Migros" in küme:
    Migros = istek("Migros",ürün)
if "A101" in küme:
    A101 = istek("A101",ürün)
if "CarrefourSA" in küme:
    Car = istek("CarrefourSA",ürün)
if "Şok" in küme:
    Şok = istek("Şok",ürün)


ürün_listesi = Car.merge(Şok,how="outer").merge(Migros,how="outer").merge(A101,how="outer")
print(ürün_listesi.sort_values("Ürün Fiyatı"))

while True:
    try:
        ürün_seç = int(input("Hangi Ürünü Seçiyorsunuz?:"))
    except:
        continue
    if ürün_seç <= -1:
        continue
    else:
        break


seçilen_ürün =  ürün_listesi.loc[ürün_seç]

if seçilen_ürün["Market"] == "A101" :
    info = (df[(df["Market"]== "A101")])
    market_adı = "A101"
if  seçilen_ürün["Market"] == "Migros" :
    info = (df[(df["Market"] == "Migros")])
    market_adı = "Migros"
if seçilen_ürün["Market"] == "Şok" :
    info = (df[(df["Market"]== "Şok")])
    market_adı = "Şok"
if seçilen_ürün["Market"] == "CarrefourSA":
    info = (df[(df["Market"] == "CarrefourSA")])
    market_adı = "CarrefourSA"


m_map = folium.Map(my_loc, zoom_start=16,width="%100",height="%100")
location=info[["Lat","Lng"]]


for i in range(0,30):
    try:
        all_market_loc = df.loc[i, "Lat"], df.loc[i, "Lng"]
        all_market_name = df.loc[i,"Market"]
        folium.Marker(location=all_market_loc, popup=all_market_name,
                      icon=folium.Icon(icon="shopping-cart", color="lightgray")).add_to(m_map)
    except:
        pass


dists = []
if len(info) >= 2:
    for i in range(0,30):
        try:
            market_koordinat = location.loc[i, "Lat"], location.loc[i, "Lng"]
            folium.Marker(location=market_koordinat, popup=f"<b>{market_adı}</b>",icon=folium.Icon(icon="shopping-cart", color="green")).add_to(m_map)
            p1 = Point(my_loc)
            p2 = Point(market_koordinat)
            result1 = distance.distance(p1, p2).meters
            dists.append([result1,i])
        except:
            pass
    shrtr_dist= min(dists)[1]
    shorter_distance_loc = location.loc[shrtr_dist, "Lat"], location.loc[shrtr_dist, "Lng"]
    folium.Marker(location=shorter_distance_loc, popup=f"<b>{market_adı}</b>",
                  icon=folium.Icon(icon="shopping-cart", icon_color="#23540e", color="green")).add_to(m_map)
else:
    for i in range(0, 30):
        try:
            shorter_distance_loc = location.loc[i, "Lat"], location.loc[i, "Lng"]
            folium.Marker(location=shorter_distance_loc, popup=f"<b>{market_adı}</b>",
                          icon=folium.Icon(icon="shopping-cart", icon_color="#adff8a", color="green")).add_to(m_map)
        except:
            pass




folium.Circle(location=my_loc,radius=710,color='gray',weight=3,fill_color='lightgreen',fill_opacity = 0.25).add_to(m_map)

folium.Marker(location=my_loc,popup="<b>Your Location</b>",icon=folium.Icon(icon="home", color="red"),).add_to(m_map)



ox.config(log_console=True, use_cache=True)

G_walk = ox.graph_from_point(my_loc,network_type='walk')

orig_node = ox.get_nearest_node(G_walk,(my_loc))

dest_node = ox.get_nearest_node(G_walk,shorter_distance_loc)

route = nx.shortest_path(G_walk,orig_node,dest_node,weight='length')

route_map = ox.plot_route_folium(G_walk, route, route_map=m_map, weight=4,fit_bounds=False)



m_map.save("Harita.html")
os.system("Harita.html")






