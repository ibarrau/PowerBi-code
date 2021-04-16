import sys
import re
import requests
import pandas as pd
from lxml import html
from datetime import datetime

def get_feriados(year):
    #Create frame
    df = pd.DataFrame(data=None, columns=['Fecha', 'Dia', 'Desc', 'Tipo'])
    #Get data from web with parameter year
    page = requests.get("https://www.lanacion.com.ar/feriados/" + str(year) )
    tree = html.fromstring(page.content)
    #array = tree.xpath('//section[@class="lista-feriados"]//ul[@class="lista-feriados__item"]')
    section = tree.xpath('//section[@class="lista-feriados"]')
    rango = 0
    if len(section) >= 4:
        rango = len(section)-1
    tipo = ""
    for i in range(rango):
        for ul in section[i]:
            if len(ul.attrib) == 0:
                tipo = ul[0].text_content()                
                pass
            else:
                if ul.attrib['class'] == 'lista-feriados__header':
                    pass
                else:
                    uls = []
                    for li in ul.text_content().split('\r\n'):
                        if li.strip() == "":
                            pass
                        else:                            
                            uls.append(li.strip())                            
                    uls.append(tipo)
                    df = df.append(pd.Series(uls, index=['Fecha', 'Dia', 'Desc', 'Tipo']), ignore_index=True)
    return df

if __name__ == "__main__":
    year = int(str(sys.argv[1]))
    
    if isinstance(year,int)==False:
        print('Error en el parametro año: ',type(year))
        quit()        
        
    print ('Año ingresado:', str(year))
    print('Probando Servicio...')
    try:
        page = requests.get('https://www.lanacion.com.ar/feriados/' + str(year) )
        tree = html.fromstring(page.content)
        section = tree.xpath('//section[@class="lista-feriados"]') 
    except Exception as ex:
        print("Servicio caido.\nExcepcion: " , ex)
        quit()
    
    print('Iniciando Scrapping...')
    try:
        df = get_feriados(year)
    except Exception as ex:
        print("Error en extracción o guardado en fram.\nExcepcion: " , ex)
        quit()        
    
    print('Guardando...')    
    df.to_csv(r'C:\Users\IBARRAU\OneDrive - Pi Data Strategy & Consulting\Pruebas Propias\Datos Abiertos\Feriados'+str(year)+'.csv', sep=",", encoding="iso8859", index=False, index_label=False)
    
else:
    print("Error, fallo el main.")