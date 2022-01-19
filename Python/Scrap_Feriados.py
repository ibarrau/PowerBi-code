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
    #Take section tag values that in this case are tables.
    section = tree.xpath('//section[@class="lista-feriados"]')
    rango = 0
    if len(section) >= 4:
        rango = len(section)-1
    tipo = ""
    #Loop tables  except for last like rango says
    for i in range(rango):
        #Loop rows UL list 
        for ul in section[i]:
            if len(ul.attrib) == 0:
                #Set tipo = title of the table to use as a column later
                tipo = ul[0].text_content()                
                pass
            else:
                if ul.attrib['class'] == 'lista-feriados__header':
                    pass
                else:
                    uls = []
                    #Loop columns to prepare a list [] of the row to insert in the frame 
                    for li in ul.text_content().split('\r\n'):
                        if li.strip() == "":
                            pass
                        else:                            
                            uls.append(li.strip())                            
                    #Add table title as a component in the list to insert in the frame
                    uls.append(tipo)
                    df = df.append(pd.Series(uls, index=['Fecha', 'Dia', 'Desc', 'Tipo']), ignore_index=True)
    return df
    
    '''
    You can also crean a little more the code doing the following
    
    df["Año"]= str(year)
    df[['Dia','Mes']] = df['Fecha'].str.split(' de ',expand=True)
    df ["Dia"] = ("0" + df["Dia"]).apply(lambda x: x[-2:]) 
    df = df[["Dia", "Mes", "Año", "Fecha", "Desc","Tipo"]]                
    m = { 'Enero': "01", 'Febrero': "02", 'Marzo': "03", 'Abril': "04", 'Mayo': "05", 'Junio': "06", 'Julio': "07", 'Agosto': "08", 'Septiembre': "09", 'Octubre': "10", 'Noviembre': "11", 'Diciembre': "12"   }
    df["Mes"] = df["Mes"].apply(lambda x: m[x.capitalize()])
    df["Fecha"] = df.Dia +"-"+ df.Mes +"-"+ df.Año
    df = df[["Año","Fecha", "Desc", "Tipo"]]
    return df
    
    '''

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
    df.to_csv(r'C:\PATHX\Feriados'+str(year)+'.csv', sep=",", encoding="iso8859", index=False, index_label=False)
    
else:
    print("Error, fallo el main.")