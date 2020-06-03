
import requests 
from bs4 import BeautifulSoup
import pandas as pd


pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 150)


URL = 'https://www.atptour.com/en/scores/results-archive?year=2018'

	
page = requests.get(URL).text 
soup = BeautifulSoup(page, "lxml")


tabla = soup.find('table', attrs={'class': 'results-archive-table mega-table'})

span =  tabla.find_all('span', attrs = {'class':'tourney-title'})
span_location = tabla.find_all('span', attrs = {'class':'tourney-location'})
span_dates = tabla.find_all('span', attrs = {'class':'tourney-dates'})


div_indout = tabla.find_all('div', attrs = {'class':'item-details'})
span_surface = tabla.find_all('span', attrs = {'class':'item-value'})


torneos = []
for a in span:
    torneo = str(a.getText()).strip()
    torneos.append(torneo)
    
paises = []
ciudades = []    
for a in span_location:
    pais = str(a.getText()).strip().split(',')[1]
    ciudad = str(a.getText()).strip().split(',')[0]
    paises.append(pais)
    ciudades.append(ciudad)

fechas = []
for a in span_dates:
    fecha = str(a.getText()).strip()
    fechas.append(fecha)

superficies = []
for a in span_surface:
    supr = str(a.getText()).strip()
    if supr in ['Clay', 'Hard', 'Grass']:
        superficies.append(supr)

indout =[]
for i in range(0, len(div_indout)):
    val = div_indout[i].getText().strip().split('\r')[0].strip()
    if val in ['Outdoor', 'Indoor']:
        indout.append(val)


dicc = {'Torneo' : torneos, 'Pais' : paises, 'Ciudad' : ciudades , 'Fecha' : fechas, 'Superficie' : superficies, 'Indoor/Outdoor' : indout} 
torneos = pd.DataFrame(dicc)


ruta_csv = r'C:\Users\alexr\OneDrive\Escritorio\Projects\Tablas_salida/torneos.csv'
torneos.to_csv(ruta_csv, sep = ';', index = False)
