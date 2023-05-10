# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 02:22:14 2023

@author: Benghy Lipa
"""

import pandas as pd
import cx_Oracle
from pathlib import Path
import streamlit as st
from datetime import datetime
import plotly.express as px 
from plotly.subplots import make_subplots
import plotly.graph_objs as go

dir_now = Path.cwd()
lib_dir = dir_now / 'Lib_Oracle'
try:
    cx_Oracle.init_oracle_client(lib_dir=str(lib_dir))
except Exception as ex:
    print(ex)
    print(" ")

dic_banda = {'AWS':100,
             'B700':75,
             '1900':50}



def ReturnQueryOnlyDelta(vendor,banda_filter,fecha_query_ini,fecha_query_fin,filter_ebc):
    if vendor=='NOKIA':
        queryonlyDelta = '''
                    SELECT 
                   to_char(N4.PERIOD_START_TIME, 'yyyy-mm-dd hh24 ') FECHA,
                   MC.NOMBRE_EBC_2 NOMBRE_EBC,MC.SECTOR SECTOR,MC.BANDA,
                   to_char(N4.LNCEL_ID) CODIGO_SECTOR_BANDA,
                   (N4.AVG_RTWP_RX_ANT_1)/10 AVG_RTWP_RX_ANT_1,
                   (N4.AVG_RTWP_RX_ANT_2)/10 AVG_RTWP_RX_ANT_2,
                   (N4.AVG_RTWP_RX_ANT_3)/10 AVG_RTWP_RX_ANT_3,
                   (N4.AVG_RTWP_RX_ANT_4)/10 AVG_RTWP_RX_ANT_4
            FROM NOKLTE_P_LPQUL1_LNCEL_DAY@NETACT19 N4
            INNER JOIN 
            		osiptel.mc_4g MC ON MC.COD_CRUCE=TO_CHAR(N4.LNCEL_ID)
            WHERE N4.PERIOD_START_TIME BETWEEN to_date('{} 00', 'ddmmyy hh24') AND to_date('{} 23', 'ddmmyy hh24')
            AND MC.NOMBRE_EBC_2='{}' AND MC.BANDA='{}'
            ORDER BY NOMBRE_EBC,SECTOR
        '''.format(fecha_query_ini,fecha_query_fin,filter_ebc,banda_filter)
    elif vendor=='HUAWEI':
        queryonlyDelta='''
                SELECT to_char(MIN(H4.FECHA),'yyyy-mm-dd') FECHA,
        MAX(MC.NOMBRE_SECTOR) NOMBRE_EBC,
        MAX(MC.SECTOR) SECTOR,
        MAX(MC.BANDA) BANDA,
        MAX(MC.CODIGO_SECTOR_BANDA) CODIGO_SECTOR_BANDA,
        AVG(C1526737656) AVG_RTWP_RX_ANT_1, 
        AVG(C1526737657) AVG_RTWP_RX_ANT_2, 
        AVG(C1526737658) AVG_RTWP_RX_ANT_3, 
        AVG(C1526737659) AVG_RTWP_RX_ANT_4
        FROM almacen.H4_1526726806 H4,osiptel.mc_4g MC
        WHERE H4.FECHA BETWEEN to_date('{} 00', 'ddmmyy hh24') AND to_date('{} 23', 'ddmmyy hh24')
        AND to_char(MC.ENODEB)=SUBSTR(SUBSTR(H4.OBJ_NAME,INSTR(OBJ_NAME,'=',1,3)+1),0,INSTR(SUBSTR(H4.OBJ_NAME,INSTR(OBJ_NAME,'=',1,3)+1),',',1,1)-1)
        AND to_char(MC.SECTOR)=SUBSTR(H4.OBJ_NAME,INSTR(OBJ_NAME,'=',1,2) + 1,1)
        AND MC.NOMBRE_SECTOR='{}' AND MC.BANDA='{}'
        GROUP BY OBJ_NAME
        ORDER BY NOMBRE_EBC,SECTOR ASC
        '''.format(fecha_query_ini,fecha_query_ini,filter_ebc,banda_filter)
    elif vendor=='ERICSSON':
        queryonlyDelta='''
                SELECT to_char(MIN(H4.FECHA),'yyyy-mm-dd') FECHA,
        MAX(MC.NOMBRE_SECTOR) NOMBRE_EBC,
        MAX(MC.SECTOR) SECTOR,
        MAX(MC.BANDA) BANDA,
        MAX(MC.CODIGO_SECTOR_BANDA) CODIGO_SECTOR_BANDA,
        AVG(C1526737656) AVG_RTWP_RX_ANT_1, 
        AVG(C1526737657) AVG_RTWP_RX_ANT_2, 
        AVG(C1526737658) AVG_RTWP_RX_ANT_3, 
        AVG(C1526737659) AVG_RTWP_RX_ANT_4
        FROM almacen.H4_1526726806 H4,osiptel.mc_4g MC
        WHERE H4.FECHA BETWEEN to_date('{} 00', 'ddmmyy hh24') AND to_date('{} 23', 'ddmmyy hh24')
        AND to_char(MC.ENODEB)=SUBSTR(SUBSTR(H4.OBJ_NAME,INSTR(OBJ_NAME,'=',1,3)+1),0,INSTR(SUBSTR(H4.OBJ_NAME,INSTR(OBJ_NAME,'=',1,3)+1),',',1,1)-1)
        AND to_char(MC.SECTOR)=SUBSTR(H4.OBJ_NAME,INSTR(OBJ_NAME,'=',1,2) + 1,1)
        AND MC.NOMBRE_SECTOR='{}' AND MC.BANDA='{}'
        GROUP BY OBJ_NAME
        ORDER BY NOMBRE_EBC,SECTOR ASC
        '''.format(fecha_query_ini,fecha_query_ini,filter_ebc,banda_filter)
    return queryonlyDelta

def ReturnDataFrameOnlyDelta(vendor,banda_filter,fecha_query_ini,fecha_query_fin,filter_ebc):
    try:
        connection = cx_Oracle.connect(user='DW_MOVIL',
                                         password='YTUMMAFasd656',
                                         dsn='10.10.61.162:1521/DIRNEN',
                                         encoding='UTF-8',)
        #st.write(connection.version)
        cursor = connection.cursor()
        #st.write("Ejecutado")
        query=ReturnQueryOnlyDelta(vendor,banda_filter,fecha_query_ini,fecha_query_fin,filter_ebc)#Query para onlyDelta
        cursor.execute(query)
        names= [x[0] for x in cursor.description]
        #st.write(names)
        rows = cursor.fetchall()
        #st.write(rows)
        df_sectores_only_delta = pd.DataFrame(rows,columns=names)
        df_sectores_only_delta['AVG_RTWP_RX_ANT_1'] = df_sectores_only_delta['AVG_RTWP_RX_ANT_1']
        df_sectores_only_delta['AVG_RTWP_RX_ANT_2'] = df_sectores_only_delta['AVG_RTWP_RX_ANT_2']
        df_sectores_only_delta['AVG_RTWP_RX_ANT_3'] = df_sectores_only_delta['AVG_RTWP_RX_ANT_3']
        df_sectores_only_delta['AVG_RTWP_RX_ANT_4'] = df_sectores_only_delta['AVG_RTWP_RX_ANT_4']
        df_sectores_only_delta['FECHA'] = pd.to_datetime(df_sectores_only_delta['FECHA'])
        return df_sectores_only_delta
    except Exception as ex:
        st.write(ex)
        st.write(ex.__cause__())
        st.write(ex)

def DownloadGrahpCSV(df_sectores_banda,fig_line,vendor,banda_filter,fecha_query_ini,fecha_query_fin,filter_ebc):
    #-------------------------------Creacion de Archivos para el Zip-----------------------#
    #Grahp de Líneas
    return True

def ReturnGraphHistDelta(vendor,banda_filter,fecha_query_ini,fecha_query_fin,filter_ebc):
    df_sectores_only_delta=pd.DataFrame()
    if vendor=='HUAWEI':
        dia_ini = pd.to_datetime(fecha_query_ini,format='%d%m%y')
        dia_fin = pd.to_datetime(fecha_query_fin,format='%d%m%y')
        dias_range = pd.date_range(dia_ini,dia_fin)
        for dia in dias_range:
            dia_query = pd.to_datetime(dia).strftime('%d%m%y')
            #st.write(dia_query)
            df = ReturnDataFrameOnlyDelta(vendor,banda_filter,dia_query,dia_query,filter_ebc)
            df_sectores_only_delta = pd.concat([df_sectores_only_delta,df],ignore_index=True)
        #st.dataframe(df_sectores_only_delta)
    elif vendor=='NOKIA':
        df_sectores_only_delta = ReturnDataFrameOnlyDelta(vendor,banda_filter,fecha_query_ini,fecha_query_fin,filter_ebc)
    df_sectores_banda = df_sectores_only_delta.query('BANDA==@banda_filter & NOMBRE_EBC==@filter_ebc')
    df_sectores_banda.sort_values(by=['FECHA','NOMBRE_EBC','SECTOR'],inplace=True)
    
    num_sectores = df_sectores_banda.SECTOR.unique()
    fig = make_subplots(rows=1, cols=3)
    dic = {'title':{'text':'Plots para el vendor {} y banda {}'.format(vendor,banda_filter)}}
    fig.update_layout(dic)
    for sector in num_sectores:
        df_sector_banda = df_sectores_banda.query('SECTOR==@sector')
        df_grahp = df_sector_banda.melt(id_vars=['FECHA'],value_vars=['AVG_RTWP_RX_ANT_1','AVG_RTWP_RX_ANT_2','AVG_RTWP_RX_ANT_3','AVG_RTWP_RX_ANT_4'])
        fig_line = px.line(df_grahp,
                           x='FECHA',
                           y='value',
                           color='variable',
                           title='{}_Sector_{} - {} '.format(filter_ebc,sector,banda_filter),
                           template='plotly_white',
                           )
        #fig_line.update_traces(mode="markers+lines", hovertemplate=None)
        fig_line.update_traces( hovertemplate=None)
        fig_line.update_layout(xaxis=dict(showgrid=False),
                              yaxis=dict(showgrid=False),hovermode='x unified')
        #st.dataframe(df_grahp)
        st.plotly_chart(fig_line, use_container_width=True)
    st.header("Historial del EBC {} y BANDA {}".format(filter_ebc,banda_filter))    
    st.dataframe(df_sectores_banda)
    
    #DownloadGrahpCSV(df_sectores_banda,list_figline,vendor,banda_filter,fecha_query_ini,fecha_query_fin,filter_ebc)


st.sidebar.success("Seleccione el proveedor para su análisis")

with st.sidebar:
    filter_vendor = st.radio(
        "Eliga un proveedor Disponible 👉",
        options=["Análisis Delta para NOKIA", "Análisis Delta para HUAWEI","Análisis Delta para ERICSSON"]
    )


filters = st.container()

with filters:
    now = datetime.now()
    if 'NOKIA' in filter_vendor:
        vendor='NOKIA'
        st.subheader('Histórico de Delta para NOKIA')
        filter_1,filter_2,filter_3,filter_4 = st.columns(4)
        with filter_1:
            banda_filter = st.selectbox("Seleccione Banda",dic_banda.keys())
        with filter_2:
            try:
                FECHA_PRB = st.date_input(label='Eliga el rango de Fechas que desea analizar',
                    value=(datetime(year=now.year, month=now.month, day=now.day), 
                            datetime(year=now.year, month=now.month, day=now.day)),
                    key='#date_range',
                    help="Eliga el inicio y el fin de la fecha")
                fecha_query_ini = pd.to_datetime(FECHA_PRB[0]).strftime('%d%m%y')
                fecha_query_fin = pd.to_datetime(FECHA_PRB[1]).strftime('%d%m%y')
            except:
                pass
        with filter_3:
            filter_ebc = st.text_input(label='Ingrese NOMBER EBC')
        with filter_4:
            st.write('Click Para consultar')
            btn_Consultar = st.button('Consultar',type='primary')
        if btn_Consultar:
            ReturnGraphHistDelta(vendor,banda_filter,fecha_query_ini,fecha_query_fin,filter_ebc.upper())
    if 'HUAWEI' in filter_vendor:
        vendor='HUAWEI'
        st.subheader('Histórico de Delta para HUAWEI')
        filter_1,filter_2,filter_3,filter_4 = st.columns(4)
        with filter_1:
            banda_filter = st.selectbox("Seleccione Banda",dic_banda.keys())
        with filter_2:
            try:
                FECHA_PRB = st.date_input(label='Eliga el rango de Fechas que desea analizar',
                    value=(datetime(year=now.year, month=now.month, day=now.day), 
                            datetime(year=now.year, month=now.month, day=now.day)),
                    key='#date_range',
                    help="Eliga el inicio y el fin de la fecha")
                fecha_query_ini = pd.to_datetime(FECHA_PRB[0]).strftime('%d%m%y')
                fecha_query_fin = pd.to_datetime(FECHA_PRB[1]).strftime('%d%m%y')
            except:
                pass
        with filter_3:
            filter_ebc = st.text_input(label='Ingrese NOMBER EBC')
        with filter_4:
            st.write('Click Para consultar')
            btn_Consultar = st.button('Consultar',type='primary')
        if btn_Consultar:
            ReturnGraphHistDelta(vendor,banda_filter,fecha_query_ini,fecha_query_fin,filter_ebc.upper())



