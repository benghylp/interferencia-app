# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 03:39:49 2023

@author: Benghy Lipa
"""

import pandas as pd
import numpy as np
import streamlit as st  # data web app development
from PIL import Image
from pathlib import Path
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import streamlit.components.v1 as components
import os
import plotly.express as px  # interactive charts

import folium
import simplekml
from folium import plugins
from simplekml import Style
from kmlplus import paths, coordinates
import itertools
from geopy import distance
from operator import itemgetter
from shapely.geometry import Point, Polygon
from polycircles import polycircles
import streamlit.components.v1 as components

dic_banda = {'AWS':100,
             'B700':75,
             '1900':50,
             'AWS_E':100,
             'B900':25,
             'B700_E':75}

dir_now = Path.cwd() 


#lectura de archivos para files procesados_sectores
dir_days = dir_now / 'Prueba' 
all_dirs = os.listdir(dir_days) #Es el definitivo
all_dirs = ['NOKIA']


#lectura de archivos para files interferencia
sectores_interf = pd.DataFrame()
for directory in all_dirs:
    all_fechas = os.listdir((dir_days / directory))
    print(directory)
    for file_fecha in all_fechas:
        try:
            file = dir_days / directory / file_fecha / 'UL_Interferencia_{}_{}.csv'.format(directory,file_fecha)
            print(file)
            sector_interf = pd.read_csv(file,dtype={'SECTOR':'str'})
            sector_interf['PROVEEDOR'] = directory
            #sectores_interf = sectores_interf.append(sector_interf,ignore_index=True)
            sectores_interf = pd.concat([sectores_interf,sector_interf],ignore_index=True)
        except Exception as ex:
            print(ex)
#Momentaneo            
sectores_interf = sectores_interf[sectores_interf['BANDA']=='B700']
#Momentaneo
sectores_interf.sort_values(by='FECHA',inplace=True,ascending=False,ignore_index=True)

st.subheader('Mapa de Calor - Interferencias:')

#Tabla_Interf = {
#    'HUAWEI': {'Critica': -95, 'Alta': -100, 'Media': -105},
#    'ERICSSON': {'Critica': -95, 'Alta': -100, 'Media': -105},
#    'NOKIA': {'Critica': -90, 'Alta': -95, 'Media': -100}}

#clasif_inter = {'ERICSSON': {
#                    'LTE': 
#                         [ 
#                             {'B700':
#                                  {'Critica': -91, 
#                                   'Alta': -95, 
#                                   'Media': -100}
#                              },
#                             {'1900':
#                                  {'Critica': -106, 
#                                   'Alta': -108, 
#                                   'Media': -111}
#                             },
#                             {'AWS':
#                                  {'Critica': -110, 
#                                   'Alta': -112, 
#                                   'Media': -113}
#                             },
#                             {'AWS_E':
#                                  {'Critica': -113, 
#                                   'Alta': -114, 
#                                   'Media': -117}
#                             },
#                             {'B900':#Verificar
#                                  {'Critica': -95, 
#                                   'Alta': -100, 
#                                   'Media': -105}
#                             },
#                             {'B700_E':#Verificar
#                                  {'Critica': -95, 
#                                   'Alta': -100, 
#                                   'Media': -105}
#                             }
#                              
#                          ],
#                     'UMTS': {}
#                     },
#          'HUAWEI': {
#                    'LTE': 
#                       [
#                           {'B700':
#                                {'Critica': -93, 
#                                 'Alta': -96, 
#                                 'Media': -102}
#                                   }
#                               ,
#                           {'1900':
#                                {'Critica': -103, 
#                                 'Alta': -110, 
#                                 'Media': -115}
#                                   },
#                           {'AWS':
#                                {'Critica': -111, 
#                                 'Alta': -114, 
#                                 'Media': -116}
#                                 }
#                       ], 
#                   'UMTS': {}
#                       },
#          'NOKIA': {'LTE':
#                    [
#                        {'B700':
#                             {'Critica': -92, 
#                              'Alta': -98, 
#                              'Media': -104}
#                                
#                         },
#                        {'1900':
#                             {'Critica': -102, 
#                              'Alta': -106, 
#                              'Media': -110}
#                         },
#                        {'AWS':
#                             {'Critica': -106, 
#                              'Alta': -108, 
#                              'Media': -110}
#                              }
#                    ],
#                    'UMTS': {}
#                    }
#          }
#




filters = st.container()
mapa = st.container()

with filters:
    filter_1, filter_2, filter_3,filter_4 = st.columns(4)
    filter_fecha = filter_1.selectbox('Fecha', pd.unique(sectores_interf.FECHA))
    filter_vendor = filter_2.selectbox('Proveedor', sorted(pd.unique(sectores_interf.PROVEEDOR)))
    filter_banda = filter_3.selectbox('Banda',sorted(pd.unique(sectores_interf.BANDA)))
    filter_4.write('Click Para consultar')
    filter_button = filter_4.button('Click para generar Mapa HTML y KMZ',type='primary')
    if filter_button:
        #Se filtran para obtener el DataFrame del dia
        mapa_sector = sectores_interf[(sectores_interf['FECHA']==filter_fecha)&(sectores_interf['PROVEEDOR']==filter_vendor)&(sectores_interf['BANDA']==filter_banda)]
        
        
        






#st.sidebar.success("SECTORES POR REGION")

#with st.sidebar:
    #Para LTE
#    for vendor in clasif_inter.keys():
#        st.subheader("{}".format(vendor))
#        df_interf = pd.DataFrame(clasif_inter[vendor]['LTE'][0])
#        df_interf = df_interf.transpose()
#        for i in range(1,len(clasif_inter[vendor]['LTE'])):
#            d1 = pd.DataFrame(clasif_inter[vendor]['LTE'][i])
#            d1 = d1.transpose()
#            df_interf = pd.concat([df_interf,d1],axis=0)
#        st.dataframe(df_interf[['Media','Alta','Critica']],use_container_width=True)
    

with mapa:
    #with st.expander("Distribución de Sectores de acuerdo a {} y fecha del {}".format(reg_filter,date_filter)):
    #    st.dataframe(sectores_interf.query('FECHA==@date_filter & REGIONAL==@reg_filter'))
    #Elegimos la fecha para el nombre del archibo
    fecha_file = pd.to_datetime(filter_fecha).strftime('%d%m%y')
    HtmlFile = open(f'./Prueba/{filter_vendor}/{fecha_file}/{filter_banda}_{fecha_file}.html', 'r', encoding='utf-8')
    source_code = HtmlFile.read() 
    components.html(source_code, height = 1000)
    name_kml = dir_now / "Prueba" / "{}".format(filter_vendor) / fecha_file /"{}_{}.kml".format(filter_banda,fecha_file)
    name_html = dir_now / "Prueba" / "{}".format(filter_vendor) / fecha_file /"{}_{}.html".format(filter_banda,fecha_file)
   
    #st.write("Descargar Archivo kml")
    with open(str(name_kml), "rb") as file:
        btn = st.download_button(
                label="Descargar Archivo kmz de la fecha: {} y {}".format(filter_banda,filter_fecha),
                data=file,
                file_name="{}_{}.kml".format(filter_banda,fecha_file),
                mime="image/kml"
              )
    with open(str(name_html), "rb") as file:
        btn = st.download_button(
                label="Descargar Archivo html de la fecha: {} y {}".format(filter_banda,filter_fecha),
                data=file,
                file_name="{}_{}.html".format(filter_banda,fecha_file),
                mime="image/html"
              )

st.button("Re-run")