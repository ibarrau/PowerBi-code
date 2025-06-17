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
    table = tree.xpath('//table[@class="table"]/tbody')
    rango = 0
    if len(table) >= 4:
        rango = len(table)-1
    tipo = ""
    #Loop tables except for last like rango says
    for i in range(rango):
        #Loop rows tr from table
        tipo_feriado = tree.xpath('//section[@class="mod-headersection  --line"]')[i].text_content()
        for ul in table[i]:
            if len(ul) == 0:
                #Set tipo = title of the table to use as a column later
                tipo = ul[0].text_content()                
                pass
            else:
                if len(ul)==2:
                    uls = []
                    #Append columns for single row
                    uls.append(ul[0].text_content())
                    uls.append(ul[1].text_content())
                    uls.append(tipo_feriado)
                    uls.append(tipo_feriado)
                    print(uls)
                    if len(uls) == 4:
                        new_row = pd.DataFrame([uls], columns=['Fecha', 'Dia', 'Desc', 'Tipo'])
                        df = pd.concat([df, new_row], ignore_index=True)
                    else:
                        print("Fila inválida:", uls)

                else:
                    uls = []
                    #Append columns for single row
                    uls.append(ul[0].text_content())
                    uls.append(ul[1].text_content())
                    uls.append(ul[2].text_content())
                    uls.append(tipo_feriado)
                    print(uls)
                    if len(uls) == 4:
                        new_row = pd.DataFrame([uls], columns=['Fecha', 'Dia', 'Desc', 'Tipo'])
                        df = pd.concat([df, new_row], ignore_index=True)
                    else:
                        print("Fila inválida:", uls)
    # Create a clean date
    df["Año"]= str(year)
    df[['nroDia','Mes']] = df['Fecha'].str.split(' de ',expand=True)
    df ["nroDia"] = ("0" + df["nroDia"]).apply(lambda x: x[-2:]) 
    df = df[["nroDia", "Mes", "Año", "Fecha", "Dia", "Desc","Tipo"]]                
    m = { 'Enero': "01", 'Febrero': "02", 'Marzo': "03", 'Abril': "04", 'Mayo': "05", 'Junio': "06", 'Julio': "07", 'Agosto': "08", 'Septiembre': "09", 'Octubre': "10", 'Noviembre': "11", 'Diciembre': "12"   }
    df["Mes"] = df["Mes"].apply(lambda x: m[x.capitalize()])
    df["Fecha"] = df.nroDia+"-"+ df.Mes +"-"+ df.Año
    df = df[["Fecha", "Dia", "Desc", "Tipo"]]
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
        print("Error en extracción o guardado en frame.\nExcepcion: " , ex)
        quit()        
    
    print('Guardando...')    
    df.to_csv(r'C:\PATHX\Feriados'+str(year)+'.csv', sep=",", encoding="iso8859", index=False, index_label=False)
    
else:
    print("Error, fallo el main.")