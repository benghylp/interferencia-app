# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 13:52:49 2023

@author: Benghy Lipa
"""

import pandas as pd
import numpy as np
import streamlit as st  # data web app development
from pathlib import Path
import plotly.graph_objs as go
import cx_Oracle
from datetime import datetime
import plotly.express as px 


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

dir_now = Path.cwd()
lib_dir = dir_now / 'Lib_Oracle'
try:
    cx_Oracle.init_oracle_client(lib_dir=str(lib_dir))
except Exception as ex:
    print(ex)
    print(" ")


#LIMIT_PRB = -105




    
def ReturnPRBValue(col):
    if col < 1 :
        return -120
    return np.round(10 * np.log10(col * (0.00000000000005684341886080801486968994140625/90000)),0)

def SearchProvin(departamento):
    try:
        connection = cx_Oracle.connect(user='DW_MOVIL',
                                         password='YTUMMAFasd656',
                                         dsn='10.10.61.162:1521/DIRNEN',
                                         encoding='UTF-8',)
        print(connection.version)
        cursor = connection.cursor()
        print("Ejecutado")
        query = '''
            SELECT UNIQUE(MC.PROVINCIA) PROVINCIA FROM osiptel.mc_4g MC WHERE MC.DEPARTAMENTO='{}' ORDER BY PROVINCIA ASC
        '''.format(departamento)
        print("Extrayendo los datos")
        cursor.execute(query)
        names= [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        df = pd.DataFrame(rows,columns=names)
        df.dropna(inplace=True)
        df.reset_index(inplace=True)
        return df['PROVINCIA']
    except:
        pass
    
def SearchDist(departamento,provincia):
    try:
        connection = cx_Oracle.connect(user='DW_MOVIL',
                                         password='YTUMMAFasd656',
                                         dsn='10.10.61.162:1521/DIRNEN',
                                         encoding='UTF-8',)
        print(connection.version)
        cursor = connection.cursor()
        print("Ejecutado")
        query = '''
            SELECT UNIQUE(MC.DISTRITO) DISTRITO FROM osiptel.mc_4g MC WHERE MC.DEPARTAMENTO='{}' AND MC.PROVINCIA='{}' ORDER BY DISTRITO ASC
        '''.format(departamento,provincia)
        print("Extrayendo los datos")
        cursor.execute(query)
        names= [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        df = pd.DataFrame(rows,columns=names)
        df.dropna(inplace=True)
        df.reset_index(inplace=True)
        return df['DISTRITO']
    except:
        pass

def ReturnQueryVendor(vendor,dep_filter,prov_filter,banda_filter,fecha_query):
    if vendor=='NOKIA':
        query = '''
        SELECT 
      		to_char(N4.PERIOD_START_TIME, 'yyyy-mm-dd hh24') AS FECHA,
      		MC.COD_CRUCE,MC.BANDA,MC.DISTRITO,
      		N4.MEAN_UL_RIP_PER_PRB0 PRB0,
      		N4.MEAN_UL_RIP_PER_PRB1 PRB1,
      		N4.MEAN_UL_RIP_PER_PRB2 PRB2,
      		N4.MEAN_UL_RIP_PER_PRB3 PRB3,
      		N4.MEAN_UL_RIP_PER_PRB4 PRB4,
      		N4.MEAN_UL_RIP_PER_PRB5 PRB5,
      		N4.MEAN_UL_RIP_PER_PRB6 PRB6,
      		N4.MEAN_UL_RIP_PER_PRB7 PRB7,
      		N4.MEAN_UL_RIP_PER_PRB8 PRB8,
      		N4.MEAN_UL_RIP_PER_PRB9 PRB9,
      		N4.MEAN_UL_RIP_PER_PRB10 PRB10,
      		N4.MEAN_UL_RIP_PER_PRB11 PRB11,
      		N4.MEAN_UL_RIP_PER_PRB12 PRB12,
      		N4.MEAN_UL_RIP_PER_PRB13 PRB13,
      		N4.MEAN_UL_RIP_PER_PRB14 PRB14,
      		N4.MEAN_UL_RIP_PER_PRB15 PRB15,
      		N4.MEAN_UL_RIP_PER_PRB16 PRB16,
      		N4.MEAN_UL_RIP_PER_PRB17 PRB17,
      		N4.MEAN_UL_RIP_PER_PRB18 PRB18,
      		N4.MEAN_UL_RIP_PER_PRB19 PRB19,
      		N4.MEAN_UL_RIP_PER_PRB20 PRB20,
      		N4.MEAN_UL_RIP_PER_PRB21 PRB21,
      		N4.MEAN_UL_RIP_PER_PRB22 PRB22,
      		N4.MEAN_UL_RIP_PER_PRB23 PRB23,
      		N4.MEAN_UL_RIP_PER_PRB24 PRB24,
      		N4.MEAN_UL_RIP_PER_PRB25 PRB25,
      		N4.MEAN_UL_RIP_PER_PRB26 PRB26,
      		N4.MEAN_UL_RIP_PER_PRB27 PRB27,
      		N4.MEAN_UL_RIP_PER_PRB28 PRB28,
      		N4.MEAN_UL_RIP_PER_PRB29 PRB29,
      		N4.MEAN_UL_RIP_PER_PRB30 PRB30,
      		N4.MEAN_UL_RIP_PER_PRB31 PRB31,
      		N4.MEAN_UL_RIP_PER_PRB32 PRB32,
      		N4.MEAN_UL_RIP_PER_PRB33 PRB33,
      		N4.MEAN_UL_RIP_PER_PRB34 PRB34,
      		N4.MEAN_UL_RIP_PER_PRB35 PRB35,
      		N4.MEAN_UL_RIP_PER_PRB36 PRB36,
      		N4.MEAN_UL_RIP_PER_PRB37 PRB37,
      		N4.MEAN_UL_RIP_PER_PRB38 PRB38,
      		N4.MEAN_UL_RIP_PER_PRB39 PRB39,
      		N4.MEAN_UL_RIP_PER_PRB40 PRB40,
      		N4.MEAN_UL_RIP_PER_PRB41 PRB41,
      		N4.MEAN_UL_RIP_PER_PRB42 PRB42,
      		N4.MEAN_UL_RIP_PER_PRB43 PRB43,
      		N4.MEAN_UL_RIP_PER_PRB44 PRB44,
      		N4.MEAN_UL_RIP_PER_PRB45 PRB45,
      		N4.MEAN_UL_RIP_PER_PRB46 PRB46,
      		N4.MEAN_UL_RIP_PER_PRB47 PRB47,
      		N4.MEAN_UL_RIP_PER_PRB48 PRB48,
      		N4.MEAN_UL_RIP_PER_PRB49 PRB49,
      		N4.MEAN_UL_RIP_PER_PRB50 PRB50,
      		N4.MEAN_UL_RIP_PER_PRB51 PRB51,
      		N4.MEAN_UL_RIP_PER_PRB52 PRB52,
      		N4.MEAN_UL_RIP_PER_PRB53 PRB53,
      		N4.MEAN_UL_RIP_PER_PRB54 PRB54,
      		N4.MEAN_UL_RIP_PER_PRB55 PRB55,
      		N4.MEAN_UL_RIP_PER_PRB56 PRB56,
      		N4.MEAN_UL_RIP_PER_PRB57 PRB57,
      		N4.MEAN_UL_RIP_PER_PRB58 PRB58,
      		N4.MEAN_UL_RIP_PER_PRB59 PRB59,
      		N4.MEAN_UL_RIP_PER_PRB60 PRB60,
      		N4.MEAN_UL_RIP_PER_PRB61 PRB61,
      		N4.MEAN_UL_RIP_PER_PRB62 PRB62,
      		N4.MEAN_UL_RIP_PER_PRB63 PRB63,
      		N4.MEAN_UL_RIP_PER_PRB64 PRB64,
      		N4.MEAN_UL_RIP_PER_PRB65 PRB65,
      		N4.MEAN_UL_RIP_PER_PRB66 PRB66,
      		N4.MEAN_UL_RIP_PER_PRB67 PRB67,
      		N4.MEAN_UL_RIP_PER_PRB68 PRB68,
      		N4.MEAN_UL_RIP_PER_PRB69 PRB69,
      		N4.MEAN_UL_RIP_PER_PRB70 PRB70,
      		N4.MEAN_UL_RIP_PER_PRB71 PRB71,
      		N4.MEAN_UL_RIP_PER_PRB72 PRB72,
      		N4.MEAN_UL_RIP_PER_PRB73 PRB73,
      		N4.MEAN_UL_RIP_PER_PRB74 PRB74,
      		N4.MEAN_UL_RIP_PER_PRB75 PRB75,
      		N4.MEAN_UL_RIP_PER_PRB76 PRB76,
      		N4.MEAN_UL_RIP_PER_PRB77 PRB77,
      		N4.MEAN_UL_RIP_PER_PRB78 PRB78,
      		N4.MEAN_UL_RIP_PER_PRB79 PRB79,
      		N4.MEAN_UL_RIP_PER_PRB80 PRB80,
      		N4.MEAN_UL_RIP_PER_PRB81 PRB81,
      		N4.MEAN_UL_RIP_PER_PRB82 PRB82,
      		N4.MEAN_UL_RIP_PER_PRB83 PRB83,
      		N4.MEAN_UL_RIP_PER_PRB84 PRB84,
      		N4.MEAN_UL_RIP_PER_PRB85 PRB85,
      		N4.MEAN_UL_RIP_PER_PRB86 PRB86,
      		N4.MEAN_UL_RIP_PER_PRB87 PRB87,
      		N4.MEAN_UL_RIP_PER_PRB88 PRB88,
      		N4.MEAN_UL_RIP_PER_PRB89 PRB89,
      		N4.MEAN_UL_RIP_PER_PRB90 PRB90,
      		N4.MEAN_UL_RIP_PER_PRB91 PRB91,
      		N4.MEAN_UL_RIP_PER_PRB92 PRB92,
      		N4.MEAN_UL_RIP_PER_PRB93 PRB93,
      		N4.MEAN_UL_RIP_PER_PRB94 PRB94,
      		N4.MEAN_UL_RIP_PER_PRB95 PRB95,
      		N4.MEAN_UL_RIP_PER_PRB96 PRB96,
      		N4.MEAN_UL_RIP_PER_PRB97 PRB97,
      		N4.MEAN_UL_RIP_PER_PRB98 PRB98,
      		N4.MEAN_UL_RIP_PER_PRB99 PRB99
      	FROM  
      		almacen.n4_ps_lrip_mnc_raw N4
      	INNER JOIN 
      		osiptel.mc_4g MC ON MC.COD_CRUCE =TO_CHAR(N4.LNCEL_ID) 
      	WHERE 
      		N4.PERIOD_START_TIME BETWEEN to_date('{} 00', 'ddmmyy hh24') AND to_date('{} 23', 'ddmmyy hh24') 
              AND MC.DEPARTAMENTO='{}' AND MC.PROVINCIA='{}' AND MC.BANDA='{}'
        ORDER BY FECHA ASC
      '''.format(fecha_query,fecha_query,dep_filter,prov_filter,banda_filter)
    elif vendor=='HUAWEI':
        query = '''
        SELECT 
		to_char(H4.FECHA, 'yyyy-mm-dd hh24') AS FECHA,
		MC.COD_CRUCE, MC.BANDA,MC.DISTRITO,
		H4.C1526730620 PRB0,
		H4.C1526730621 PRB1,
		H4.C1526730622 PRB2,
		H4.C1526730623 PRB3,
		H4.C1526730624 PRB4,
		H4.C1526730625 PRB5,
		H4.C1526730626 PRB6,
		H4.C1526730627 PRB7,
		H4.C1526730628 PRB8,
		H4.C1526730629 PRB9,
		H4.C1526730630 PRB10,
		H4.C1526730631 PRB11,
		H4.C1526730632 PRB12,
		H4.C1526730633 PRB13,
		H4.C1526730634 PRB14,
		H4.C1526730635 PRB15,
		H4.C1526730636 PRB16,
		H4.C1526730637 PRB17,
		H4.C1526730638 PRB18,
		H4.C1526730639 PRB19,
		H4.C1526730640 PRB20,
		H4.C1526730641 PRB21,
		H4.C1526730642 PRB22,
		H4.C1526730643 PRB23,
		H4.C1526730644 PRB24,
		H4.C1526730645 PRB25,
		H4.C1526730646 PRB26,
		H4.C1526730647 PRB27,
		H4.C1526730648 PRB28,
		H4.C1526730649 PRB29,
		H4.C1526730650 PRB30,
		H4.C1526730651 PRB31,
		H4.C1526730652 PRB32,
		H4.C1526730653 PRB33,
		H4.C1526730654 PRB34,
		H4.C1526730655 PRB35,
		H4.C1526730656 PRB36,
		H4.C1526730657 PRB37,
		H4.C1526730658 PRB38,
		H4.C1526730659 PRB39,
		H4.C1526730660 PRB40,
		H4.C1526730661 PRB41,
		H4.C1526730662 PRB42,
		H4.C1526730663 PRB43,
		H4.C1526730664 PRB44,
		H4.C1526730665 PRB45,
		H4.C1526730666 PRB46,
		H4.C1526730667 PRB47,
		H4.C1526730668 PRB48,
		H4.C1526730669 PRB49,
		H4.C1526730670 PRB50,
		H4.C1526730671 PRB51,
		H4.C1526730672 PRB52,
		H4.C1526730673 PRB53,
		H4.C1526730674 PRB54,
		H4.C1526730675 PRB55,
		H4.C1526730676 PRB56,
		H4.C1526730677 PRB57,
		H4.C1526730678 PRB58,
		H4.C1526730679 PRB59,
		H4.C1526730680 PRB60,
		H4.C1526730681 PRB61,
		H4.C1526730682 PRB62,
		H4.C1526730683 PRB63,
		H4.C1526730684 PRB64,
		H4.C1526730685 PRB65,
		H4.C1526730686 PRB66,
		H4.C1526730687 PRB67,
		H4.C1526730688 PRB68,
		H4.C1526730689 PRB69,
		H4.C1526730690 PRB70,
		H4.C1526730691 PRB71,
		H4.C1526730692 PRB72,
		H4.C1526730693 PRB73,
		H4.C1526730694 PRB74,
		H4.C1526730695 PRB75,
		H4.C1526730696 PRB76,
		H4.C1526730697 PRB77,
		H4.C1526730698 PRB78,
		H4.C1526730699 PRB79,
		H4.C1526730700 PRB80,
		H4.C1526730701 PRB81,
		H4.C1526730702 PRB82,
		H4.C1526730703 PRB83,
		H4.C1526730704 PRB84,
		H4.C1526730705 PRB85,
		H4.C1526730706 PRB86,
		H4.C1526730707 PRB87,
		H4.C1526730708 PRB88,
		H4.C1526730709 PRB89,
		H4.C1526730710 PRB90,
		H4.C1526730711 PRB91,
		H4.C1526730712 PRB92,
		H4.C1526730713 PRB93,
		H4.C1526730714 PRB94,
		H4.C1526730715 PRB95,
		H4.C1526730716 PRB96,
		H4.C1526730717 PRB97,
		H4.C1526730718 PRB98,
		H4.C1526730719 PRB99
	FROM 
		ALMACEN.H4_1526726783 H4
	INNER JOIN 
		osiptel.mc_4g MC ON MC.COD_CRUCE=SUBSTR(SUBSTR(OBJ_NAME,INSTR(OBJ_NAME,'=',1,3) + 1),0,INSTR(SUBSTR(OBJ_NAME,INSTR(OBJ_NAME,'=',1,3) + 1),'-',1,1)-1) || SUBSTR(OBJ_NAME,INSTR(OBJ_NAME,'=',1,2) + 1,1)
	WHERE 
		FECHA BETWEEN to_date('{} 00', 'ddmmyy hh24') AND to_date('{} 23', 'ddmmyy hh24')
        AND MC.DEPARTAMENTO='{}' AND MC.PROVINCIA='{}' AND MC.BANDA='{}'
    ORDER BY FECHA ASC
      '''.format(fecha_query,fecha_query,dep_filter,prov_filter,banda_filter)
    
    elif vendor=='ERICSSON':
        query = '''
        SELECT 
		to_char(E4.DATETIME_ID, 'yyyy-mm-dd hh24:mi') AS FECHA,
		MC.COD_CRUCE, MC.BANDA,MC.DISTRITO,
		E4.PMRADIOINTERFERENCEPWRPRB1 PRB0,
		E4.PMRADIOINTERFERENCEPWRPRB2 PRB1,
		E4.PMRADIOINTERFERENCEPWRPRB3 PRB2,
		E4.PMRADIOINTERFERENCEPWRPRB4 PRB3,
		E4.PMRADIOINTERFERENCEPWRPRB5 PRB4,
		E4.PMRADIOINTERFERENCEPWRPRB6 PRB5,
		E4.PMRADIOINTERFERENCEPWRPRB7 PRB6,
		E4.PMRADIOINTERFERENCEPWRPRB8 PRB7,
		E4.PMRADIOINTERFERENCEPWRPRB9 PRB8,
		E4.PMRADIOINTERFERENCEPWRPRB10 PRB9,
		E4.PMRADIOINTERFERENCEPWRPRB11 PRB10, 
		E4.PMRADIOINTERFERENCEPWRPRB12 PRB11,
		E4.PMRADIOINTERFERENCEPWRPRB13 PRB12,
		E4.PMRADIOINTERFERENCEPWRPRB14 PRB13,
		E4.PMRADIOINTERFERENCEPWRPRB15 PRB14,
		E4.PMRADIOINTERFERENCEPWRPRB16 PRB15,
		E4.PMRADIOINTERFERENCEPWRPRB17 PRB16,
		E4.PMRADIOINTERFERENCEPWRPRB18 PRB17,
		E4.PMRADIOINTERFERENCEPWRPRB19 PRB18,
		E4.PMRADIOINTERFERENCEPWRPRB20 PRB19,
		E4.PMRADIOINTERFERENCEPWRPRB21 PRB20, 
		E4.PMRADIOINTERFERENCEPWRPRB22 PRB21,
		E4.PMRADIOINTERFERENCEPWRPRB23 PRB22,
		E4.PMRADIOINTERFERENCEPWRPRB24 PRB23,
		E4.PMRADIOINTERFERENCEPWRPRB25 PRB24,
		E4.PMRADIOINTERFERENCEPWRPRB26 PRB25,
		E4.PMRADIOINTERFERENCEPWRPRB27 PRB26, 
		E4.PMRADIOINTERFERENCEPWRPRB28 PRB27,
		E4.PMRADIOINTERFERENCEPWRPRB29 PRB28,
		E4.PMRADIOINTERFERENCEPWRPRB30 PRB29,
		E4.PMRADIOINTERFERENCEPWRPRB31 PRB30, 
		E4.PMRADIOINTERFERENCEPWRPRB32 PRB31, 
		E4.PMRADIOINTERFERENCEPWRPRB33 PRB32, 
		E4.PMRADIOINTERFERENCEPWRPRB34 PRB33, 
		E4.PMRADIOINTERFERENCEPWRPRB35 PRB34, 
		E4.PMRADIOINTERFERENCEPWRPRB36 PRB35, 
		E4.PMRADIOINTERFERENCEPWRPRB37 PRB36, 
		E4.PMRADIOINTERFERENCEPWRPRB38 PRB37, 
		E4.PMRADIOINTERFERENCEPWRPRB39 PRB38, 
		E4.PMRADIOINTERFERENCEPWRPRB40 PRB39, 
		E4.PMRADIOINTERFERENCEPWRPRB41 PRB40, 
		E4.PMRADIOINTERFERENCEPWRPRB42 PRB41, 
		E4.PMRADIOINTERFERENCEPWRPRB43 PRB42, 
		E4.PMRADIOINTERFERENCEPWRPRB44 PRB43, 
		E4.PMRADIOINTERFERENCEPWRPRB45 PRB44, 
		E4.PMRADIOINTERFERENCEPWRPRB46 PRB45, 
		E4.PMRADIOINTERFERENCEPWRPRB47 PRB46, 
		E4.PMRADIOINTERFERENCEPWRPRB48 PRB47, 
		E4.PMRADIOINTERFERENCEPWRPRB49 PRB48, 
		E4.PMRADIOINTERFERENCEPWRPRB50 PRB49, 
		E4.PMRADIOINTERFERENCEPWRPRB51 PRB50, 
		E4.PMRADIOINTERFERENCEPWRPRB52 PRB51, 
		E4.PMRADIOINTERFERENCEPWRPRB53 PRB52, 
		E4.PMRADIOINTERFERENCEPWRPRB54 PRB53, 
		E4.PMRADIOINTERFERENCEPWRPRB55 PRB54, 
		E4.PMRADIOINTERFERENCEPWRPRB56 PRB55, 
		E4.PMRADIOINTERFERENCEPWRPRB57 PRB56, 
		E4.PMRADIOINTERFERENCEPWRPRB58 PRB57, 
		E4.PMRADIOINTERFERENCEPWRPRB59 PRB58, 
		E4.PMRADIOINTERFERENCEPWRPRB60 PRB59, 
		E4.PMRADIOINTERFERENCEPWRPRB61 PRB60, 
		E4.PMRADIOINTERFERENCEPWRPRB62 PRB61, 
		E4.PMRADIOINTERFERENCEPWRPRB63 PRB62, 
		E4.PMRADIOINTERFERENCEPWRPRB64 PRB63, 
		E4.PMRADIOINTERFERENCEPWRPRB65 PRB64, 
		E4.PMRADIOINTERFERENCEPWRPRB66 PRB65, 
		E4.PMRADIOINTERFERENCEPWRPRB67 PRB66, 
		E4.PMRADIOINTERFERENCEPWRPRB68 PRB67, 
		E4.PMRADIOINTERFERENCEPWRPRB69 PRB68, 
		E4.PMRADIOINTERFERENCEPWRPRB70 PRB69, 
		E4.PMRADIOINTERFERENCEPWRPRB71 PRB70, 
		E4.PMRADIOINTERFERENCEPWRPRB72 PRB71, 
		E4.PMRADIOINTERFERENCEPWRPRB73 PRB72, 
		E4.PMRADIOINTERFERENCEPWRPRB74 PRB73, 
		E4.PMRADIOINTERFERENCEPWRPRB75 PRB74, 
		E4.PMRADIOINTERFERENCEPWRPRB76 PRB75, 
		E4.PMRADIOINTERFERENCEPWRPRB77 PRB76, 
		E4.PMRADIOINTERFERENCEPWRPRB78 PRB77, 
		E4.PMRADIOINTERFERENCEPWRPRB79 PRB78, 
		E4.PMRADIOINTERFERENCEPWRPRB80 PRB79, 
		E4.PMRADIOINTERFERENCEPWRPRB81 PRB80, 
		E4.PMRADIOINTERFERENCEPWRPRB82 PRB81, 
		E4.PMRADIOINTERFERENCEPWRPRB83 PRB82, 
		E4.PMRADIOINTERFERENCEPWRPRB84 PRB83, 
		E4.PMRADIOINTERFERENCEPWRPRB85 PRB84, 
		E4.PMRADIOINTERFERENCEPWRPRB86 PRB85, 
		E4.PMRADIOINTERFERENCEPWRPRB87 PRB86, 
		E4.PMRADIOINTERFERENCEPWRPRB88 PRB87, 
		E4.PMRADIOINTERFERENCEPWRPRB89 PRB88, 
		E4.PMRADIOINTERFERENCEPWRPRB90 PRB89, 
		E4.PMRADIOINTERFERENCEPWRPRB91 PRB90, 
		E4.PMRADIOINTERFERENCEPWRPRB92 PRB91, 
		E4.PMRADIOINTERFERENCEPWRPRB93 PRB92, 
		E4.PMRADIOINTERFERENCEPWRPRB94 PRB93, 
		E4.PMRADIOINTERFERENCEPWRPRB95 PRB94, 
		E4.PMRADIOINTERFERENCEPWRPRB96 PRB95, 
		E4.PMRADIOINTERFERENCEPWRPRB97 PRB96, 
		E4.PMRADIOINTERFERENCEPWRPRB98 PRB97, 
		E4.PMRADIOINTERFERENCEPWRPRB99 PRB98, 
		E4.PMRADIOINTERFERENCEPWRPRB100 PRB99
	FROM 
		almacen.e4_erbs_eutrancellfdd E4
	INNER JOIN 
		osiptel.mc_4g MC ON MC.COD_CRUCE=E4.EUTRANCELLFDD 
	WHERE 
		E4.DATETIME_ID BETWEEN to_date('{} 00 00', 'ddmmyy hh24:mi') AND to_date('{} 23 59', 'ddmmyy hh24:mi')
        AND MC.DEPARTAMENTO='{}' AND MC.PROVINCIA='{}' AND MC.BANDA='{}'
    ORDER BY FECHA ASC
      '''.format(fecha_query,fecha_query,dep_filter,prov_filter,banda_filter)
    return query

def ReturnDistritoPRB(vendor,dep_filter,prov_filter,banda_filter,fecha_query,dic_banda,LIMIT_PRB):
    try:
      connection = cx_Oracle.connect(user='DW_MOVIL',
                                       password='YTUMMAFasd656',
                                       dsn='10.10.61.162:1521/DIRNEN',
                                       encoding='UTF-8',)
      print(connection.version)
      cursor = connection.cursor()
      print("Ejecutado")
      query = ReturnQueryVendor(vendor,dep_filter,prov_filter,banda_filter,fecha_query)
      #st.write(query)
      print("Extrayendo los datos")
      cursor.execute(query)
      names= [x[0] for x in cursor.description]
      #st.write(names)
      rows = cursor.fetchall()
      #st.write(rows)
      df = pd.DataFrame(rows,columns=names)
      #st.write(df)
      #st.dataframe(df)
      dic_prb = {}
      if df.empty:
          st.subheader('No posee data para el vendor {}, departamento {} , provincia {}, banda {}, y fecha {}'.format(vendor,dep_filter,prov_filter,banda_filter,fecha_query))
          return dic_prb
      else:
          #st.dataframe(df)
          list_prbs=[]
          list_dataframe=[]
          list_dataframe.append('DISTRITO')
          for i in range(0,dic_banda[banda_filter]):
              list_prbs.append('PRB'+str(i))
              list_dataframe.append('PRB'+str(i))
          df_prbs = df[list_dataframe]
          df_count_prbs = pd.DataFrame()
          
          if vendor=='ERICSSON':
              #Para cuando tenga data
              df_new = pd.DataFrame(columns=df.columns)
              #Se obtienen los valores de cada columna PRB
              #st.dataframe(df)
              for prb in list_prbs:
                  df[prb] = df[prb].map(ReturnPRBValue)
              #df_min = df.copy()
              #st.dataframe(df)
              fechas  = (df['FECHA'].apply(lambda row: row[:-5])).unique()
              #Cantidad de HXH minxmin para cada COD_CRUCE -> Transformacion a HXH
              for cod_cruce in pd.unique(df.COD_CRUCE):
                  data_cod_cruce = df.query('COD_CRUCE==@cod_cruce')
                  distrito = pd.unique(data_cod_cruce['DISTRITO'])[0]
                  for f in fechas:
                      for i in range(0,24):
                          fecha = f
                          fecha_sig = fecha
                          j=i+1
                          if i < 10:
                              fecha = fecha + '0{}'.format(i)
                          else:
                              fecha = fecha +'{}'.format(i)
                          if j < 10:
                              fecha_sig = fecha_sig + '0{}'.format(j)
                          else:
                              fecha_sig = fecha_sig +'{}'.format(j)
                          #st.write(fecha)
                          #st.write(fecha_sig)
                          #st.write(" ")
                          d = data_cod_cruce[ (data_cod_cruce['FECHA']>=fecha) & (data_cod_cruce['FECHA']<fecha_sig) ]
                          if not(d.empty):
                              d = d.loc[:,list_prbs].mean()
                              d = d.to_frame()
                              d = d.T
                              d['FECHA'] = fecha
                              d['DISTRITO'] = distrito
                              d['COD_CRUCE'] = cod_cruce
                              d['BANDA'] = banda_filter
                              df_new = pd.concat([df_new,d],ignore_index=True)
                              
              df_prbs = df_new.copy()       
              #st.dataframe(df_prbs)
              #Cantidad de Codigo de Sectores Banda por Distrito HxH
              for idx,distrito in enumerate(pd.unique(df.DISTRITO)):
                  data_distrito = df_prbs.query('DISTRITO==@distrito')
                  for prb in list_prbs:
                      value = (data_distrito[data_distrito[prb]>=LIMIT_PRB][prb]).shape[0]
                      df_count_prbs.loc[idx,'DISTRITO'] = distrito
                      df_count_prbs.loc[idx,prb]= value
          else:
              #Cantidad de Codigo de Sectores Banda por Distrito HxH
              for idx,distrito in enumerate(pd.unique(df.DISTRITO)):
                  data_distrito = df_prbs.query('DISTRITO==@distrito')
                  for prb in list_prbs:
                      value = (data_distrito[data_distrito[prb]>=LIMIT_PRB][prb]).shape[0]
                      df_count_prbs.loc[idx,'DISTRITO'] = distrito
                      df_count_prbs.loc[idx,prb]= value
                  #st.dataframe(df_count_prbs.style.format(subset=list_prbs,formatter="{:.0f}"))}
              #st.dataframe(df_count_prbs.style.format(subset=list_prbs,formatter="{:.0f}"))
          
          #---------------------------------- Distribución de la Cantidad de Código Sector Banda HxH por PRBs----------------#
          st.subheader('Acumulado de la Cantidad de Código de Sector Banda HxH por Departamento: {} - Provincia: {} y Banda {}'.format(dep_filter,prov_filter,banda_filter))
          df_PRBS= pd.DataFrame(df_count_prbs.loc[:,list_prbs].sum(),columns=['num_Sectores'])
          df_PRBS.reset_index(inplace=True)
          #st.dataframe(df_PRBS)
          fig_bars = px.bar(
                    df_PRBS,
                    x='index',
                    y='num_Sectores',
                    orientation='v',
                    barmode='relative',
                    labels={'index': 'PRBs', 'num_Sectores': 'Cantidad de Código Sector Banda HxH'},
                    template='plotly_white',
                    text_auto=True)  # 'ggplot2', 'seaborn', 'simple_white', 'plotly', 'plotly_white'
          st.plotly_chart(fig_bars, theme="streamlit", use_container_width=True)
          
          #---------------------------------- Distribución de la Cantidad de Código Sector Banda HxH por TOP 10 PRBs----------------#
          TOP = 10
          #Se suma la cantidad de Codigo de Sectores Banda HxH
          st.subheader('Ranking (Top {}) de los PRBs más Interferidos de acuerdo al Departamento: {} - Provincia: {} y Banda {}'.format(TOP,dep_filter,prov_filter,banda_filter))
          df_PRBS_dia = pd.DataFrame(df_count_prbs.loc[:,list_prbs].sum(),columns=['num_Sectores'])
          df_PRBS_dia.sort_values(by='num_Sectores',ascending=False,inplace=True)
          df_PRBS_dia.reset_index(inplace=True)
          #Seleccionamos el Top 10
          
          df_PRBS_dia_grahp = df_PRBS_dia.loc[0:TOP-1,:]
          fig_bars = px.bar(
                    df_PRBS_dia_grahp,
                    x='index',
                    y='num_Sectores',
                    orientation='v',
                    barmode='relative',
                    labels={'index': 'PRBs', 'num_Sectores': 'Acumulado de la Cantidad de Código Sector Banda HxH'},
                    template='plotly_white',
                    text_auto=True)  # 'ggplot2', 'seaborn', 'simple_white', 'plotly', 'plotly_white'
          st.plotly_chart(fig_bars, theme="streamlit", use_container_width=True)
          #---------------------------------- Distribución de la Cantidad de Código Sector Banda HxH por Distrito----------------#
          prbs_ignorados = ['PRB0','PRB1','PRB2','PRB3','PRB{}'.format(dic_banda[banda_filter]-1),'PRB{}'.format(dic_banda[banda_filter]-2),'PRB{}'.format(dic_banda[banda_filter]-3),'PRB{}'.format(dic_banda[banda_filter]-4)]
          for prb in pd.unique(df_PRBS_dia_grahp['index']):
              if not(prb in prbs_ignorados):
                  with st.expander("Ranking (Top {}) de los Distritos más Interferidos para el {}".format(TOP,prb)):
                      st.subheader('Ranking (Top {}) de los Distritos más interferidos del PRB: {}'.format(TOP,prb))
                      df_PRB_select = df_count_prbs.sort_values(by=prb,ascending=False)[['DISTRITO',prb]]
                      df_PRB_select.reset_index(inplace=True)
                      df_PRB_grahp = df_PRB_select.loc[0:TOP-1,:]
                      fig_bars = px.bar(
                              df_PRB_grahp,
                              x='DISTRITO',
                              y=prb,
                              orientation='v',
                              barmode='relative',
                              labels={'DISTRITO': 'DISTRITOS', '{}'.format(prb): 'Acumulado de la Cantidad de Código Sector Banda HxH'},
                              template='plotly_white',
                              text_auto=True)  # 'ggplot2', 'seaborn', 'simple_white', 'plotly', 'plotly_white'
                      st.plotly_chart(fig_bars, theme="streamlit", use_container_width=True)
                      dic_prb[prb]=sorted((pd.unique(df_PRB_grahp['DISTRITO'])).tolist())
                  
          #-----------------Return--------------#
          return dic_prb
              
    except Exception as ex:
        print(ex)
        pass


def ReturnQueryDataFrameMap(vendor,dep_filter,prov_filter,banda_filter,fecha_query,dic_prb,LIMIT_PRB):
    distritos = []
    for list_dist in dic_prb.values():
        for dist in list_dist:
            if not(dist in distritos):
                distritos.append(dist)
    distritos = tuple(sorted(distritos))
    #st.write(distritos)
    if vendor=='NOKIA':
        query = '''
        SELECT 
		to_char(N4.PERIOD_START_TIME, 'yyyy-mm-dd hh24') AS FECHA,
		MC.COD_CRUCE CODIGO_SECTOR_BANDA, MC.BANDA BANDA, MC.UNICO UNICO,
        MC.NOMBRE_EBC NOMBRE_EBC,MC.SECTOR SECTOR,MC.DEPARTAMENTO DEPARTAMENTO,MC.PROVINCIA PROVINCIA,MC.DISTRITO DISTRITO,
        MC.LATITUD LATITUD,MC.LONGITUD LONGITUD,INV.AZIMUT,65 BEAN,
		N4.MEAN_UL_RIP_PER_PRB0 PRB0,
		N4.MEAN_UL_RIP_PER_PRB1 PRB1,
		N4.MEAN_UL_RIP_PER_PRB2 PRB2,
		N4.MEAN_UL_RIP_PER_PRB3 PRB3,
		N4.MEAN_UL_RIP_PER_PRB4 PRB4,
		N4.MEAN_UL_RIP_PER_PRB5 PRB5,
		N4.MEAN_UL_RIP_PER_PRB6 PRB6,
		N4.MEAN_UL_RIP_PER_PRB7 PRB7,
		N4.MEAN_UL_RIP_PER_PRB8 PRB8,
		N4.MEAN_UL_RIP_PER_PRB9 PRB9,
		N4.MEAN_UL_RIP_PER_PRB10 PRB10,
		N4.MEAN_UL_RIP_PER_PRB11 PRB11,
		N4.MEAN_UL_RIP_PER_PRB12 PRB12,
		N4.MEAN_UL_RIP_PER_PRB13 PRB13,
		N4.MEAN_UL_RIP_PER_PRB14 PRB14,
		N4.MEAN_UL_RIP_PER_PRB15 PRB15,
		N4.MEAN_UL_RIP_PER_PRB16 PRB16,
		N4.MEAN_UL_RIP_PER_PRB17 PRB17,
		N4.MEAN_UL_RIP_PER_PRB18 PRB18,
		N4.MEAN_UL_RIP_PER_PRB19 PRB19,
		N4.MEAN_UL_RIP_PER_PRB20 PRB20,
		N4.MEAN_UL_RIP_PER_PRB21 PRB21,
		N4.MEAN_UL_RIP_PER_PRB22 PRB22,
		N4.MEAN_UL_RIP_PER_PRB23 PRB23,
		N4.MEAN_UL_RIP_PER_PRB24 PRB24,
		N4.MEAN_UL_RIP_PER_PRB25 PRB25,
		N4.MEAN_UL_RIP_PER_PRB26 PRB26,
		N4.MEAN_UL_RIP_PER_PRB27 PRB27,
		N4.MEAN_UL_RIP_PER_PRB28 PRB28,
		N4.MEAN_UL_RIP_PER_PRB29 PRB29,
		N4.MEAN_UL_RIP_PER_PRB30 PRB30,
		N4.MEAN_UL_RIP_PER_PRB31 PRB31,
		N4.MEAN_UL_RIP_PER_PRB32 PRB32,
		N4.MEAN_UL_RIP_PER_PRB33 PRB33,
		N4.MEAN_UL_RIP_PER_PRB34 PRB34,
		N4.MEAN_UL_RIP_PER_PRB35 PRB35,
		N4.MEAN_UL_RIP_PER_PRB36 PRB36,
		N4.MEAN_UL_RIP_PER_PRB37 PRB37,
		N4.MEAN_UL_RIP_PER_PRB38 PRB38,
		N4.MEAN_UL_RIP_PER_PRB39 PRB39,
		N4.MEAN_UL_RIP_PER_PRB40 PRB40,
		N4.MEAN_UL_RIP_PER_PRB41 PRB41,
		N4.MEAN_UL_RIP_PER_PRB42 PRB42,
		N4.MEAN_UL_RIP_PER_PRB43 PRB43,
		N4.MEAN_UL_RIP_PER_PRB44 PRB44,
		N4.MEAN_UL_RIP_PER_PRB45 PRB45,
		N4.MEAN_UL_RIP_PER_PRB46 PRB46,
		N4.MEAN_UL_RIP_PER_PRB47 PRB47,
		N4.MEAN_UL_RIP_PER_PRB48 PRB48,
		N4.MEAN_UL_RIP_PER_PRB49 PRB49,
		N4.MEAN_UL_RIP_PER_PRB50 PRB50,
		N4.MEAN_UL_RIP_PER_PRB51 PRB51,
		N4.MEAN_UL_RIP_PER_PRB52 PRB52,
		N4.MEAN_UL_RIP_PER_PRB53 PRB53,
		N4.MEAN_UL_RIP_PER_PRB54 PRB54,
		N4.MEAN_UL_RIP_PER_PRB55 PRB55,
		N4.MEAN_UL_RIP_PER_PRB56 PRB56,
		N4.MEAN_UL_RIP_PER_PRB57 PRB57,
		N4.MEAN_UL_RIP_PER_PRB58 PRB58,
		N4.MEAN_UL_RIP_PER_PRB59 PRB59,
		N4.MEAN_UL_RIP_PER_PRB60 PRB60,
		N4.MEAN_UL_RIP_PER_PRB61 PRB61,
		N4.MEAN_UL_RIP_PER_PRB62 PRB62,
		N4.MEAN_UL_RIP_PER_PRB63 PRB63,
		N4.MEAN_UL_RIP_PER_PRB64 PRB64,
		N4.MEAN_UL_RIP_PER_PRB65 PRB65,
		N4.MEAN_UL_RIP_PER_PRB66 PRB66,
		N4.MEAN_UL_RIP_PER_PRB67 PRB67,
		N4.MEAN_UL_RIP_PER_PRB68 PRB68,
		N4.MEAN_UL_RIP_PER_PRB69 PRB69,
		N4.MEAN_UL_RIP_PER_PRB70 PRB70,
		N4.MEAN_UL_RIP_PER_PRB71 PRB71,
		N4.MEAN_UL_RIP_PER_PRB72 PRB72,
		N4.MEAN_UL_RIP_PER_PRB73 PRB73,
		N4.MEAN_UL_RIP_PER_PRB74 PRB74,
		N4.MEAN_UL_RIP_PER_PRB75 PRB75,
		N4.MEAN_UL_RIP_PER_PRB76 PRB76,
		N4.MEAN_UL_RIP_PER_PRB77 PRB77,
		N4.MEAN_UL_RIP_PER_PRB78 PRB78,
		N4.MEAN_UL_RIP_PER_PRB79 PRB79,
		N4.MEAN_UL_RIP_PER_PRB80 PRB80,
		N4.MEAN_UL_RIP_PER_PRB81 PRB81,
		N4.MEAN_UL_RIP_PER_PRB82 PRB82,
		N4.MEAN_UL_RIP_PER_PRB83 PRB83,
		N4.MEAN_UL_RIP_PER_PRB84 PRB84,
		N4.MEAN_UL_RIP_PER_PRB85 PRB85,
		N4.MEAN_UL_RIP_PER_PRB86 PRB86,
		N4.MEAN_UL_RIP_PER_PRB87 PRB87,
		N4.MEAN_UL_RIP_PER_PRB88 PRB88,
		N4.MEAN_UL_RIP_PER_PRB89 PRB89,
		N4.MEAN_UL_RIP_PER_PRB90 PRB90,
		N4.MEAN_UL_RIP_PER_PRB91 PRB91,
		N4.MEAN_UL_RIP_PER_PRB92 PRB92,
		N4.MEAN_UL_RIP_PER_PRB93 PRB93,
		N4.MEAN_UL_RIP_PER_PRB94 PRB94,
		N4.MEAN_UL_RIP_PER_PRB95 PRB95,
		N4.MEAN_UL_RIP_PER_PRB96 PRB96,
		N4.MEAN_UL_RIP_PER_PRB97 PRB97,
		N4.MEAN_UL_RIP_PER_PRB98 PRB98,
		N4.MEAN_UL_RIP_PER_PRB99 PRB99
	FROM  
		almacen.n4_ps_lrip_mnc_raw N4
	INNER JOIN 
		osiptel.mc_4g MC ON MC.COD_CRUCE =TO_CHAR(N4.LNCEL_ID)
    INNER JOIN 
        inv_mc@db_gerweb_siggsm INV ON MC.COD_CRUCE=INV.CODIGO_CRUCE AND INV.CODIGO_CRUCE=TO_CHAR(N4.LNCEL_ID)
	WHERE 
		N4.PERIOD_START_TIME BETWEEN to_date('{} 00', 'ddmmyy hh24') AND to_date('{} 23', 'ddmmyy hh24')
        AND MC.BANDA='{}' AND MC.DEPARTAMENTO='{}' AND MC.PROVINCIA='{}' AND MC.DISTRITO IN {}
        ORDER BY MC.NOMBRE_EBC,MC.SECTOR,FECHA ASC
        '''.format(fecha_query,fecha_query,banda_filter,dep_filter,prov_filter,distritos)
    return query


def ReturnDataFrameMapHTML(vendor,dep_filter,prov_filter,banda_filter,fecha_query,dic_banda,dic_prb,fecha_mapa,LIMIT_PRB):
    if (pd.DataFrame(dic_prb)).empty:
        st.subheader('No posee data para el vendor {}, departamento {} , provincia {}, banda {}, y fecha {}'.format(vendor,dep_filter,prov_filter,banda_filter,fecha_query))
    else:
        try:
          connection = cx_Oracle.connect(user='DW_MOVIL',
                                           password='YTUMMAFasd656',
                                           dsn='10.10.61.162:1521/DIRNEN',
                                           encoding='UTF-8',)
          print(connection.version)
          cursor = connection.cursor()
          print("Ejecutado")
          #st.write(dic_prb)
          query = ReturnQueryDataFrameMap(vendor,dep_filter,prov_filter,banda_filter,fecha_query,dic_prb,LIMIT_PRB)
          #st.write(query)
          print("Extrayendo los datos")
          cursor.execute(query)
          names= [x[0] for x in cursor.description]
          #st.write(names)
          rows = cursor.fetchall()
          #st.write(rows)
          df = pd.DataFrame(rows,columns=names)
          #st.dataframe(df)
          

          #Agregamos columna 'RADIO_MAP'
          radio_map = {'AWS': 75, '1900': 70, 'B700': 65, 'AWS_E': 60, 'B900': 50, 'B700_E': 55}
          df['RADIO_MAP'] = df['BANDA'].map(radio_map)

          columns_prbs=[]
          columns_data = ['FECHA', 'CODIGO_SECTOR_BANDA', 'BANDA', 'UNICO', 'NOMBRE_EBC', 'SECTOR','DEPARTAMENTO','PROVINCIA' ,'DISTRITO', 'LATITUD', 'LONGITUD', 'AZIMUT', 'BEAN','RADIO_MAP']
          for i in range(0,dic_banda[banda_filter]):
              columns_prbs.append('PRB'+str(i))
              columns_data.append('PRB'+str(i))

          df = df[columns_data]

          df['LATITUD'] = pd.to_numeric(df['LATITUD'],errors='coerce')
          df['LONGITUD'] = pd.to_numeric(df['LONGITUD'],errors='coerce')
          df['AZIMUT'] = pd.to_numeric(df['AZIMUT'], errors='coerce')
          df['BEAN'] = pd.to_numeric(df['BEAN'],errors='coerce')


          #Eliminamos aquellos que no tienen latitud y longitud
          df.dropna(subset=['LATITUD','LONGITUD','AZIMUT','BEAN'],inplace=True)


          df_new = pd.DataFrame(columns=columns_data)
          idx=0
          for cod_sector in pd.unique(df['CODIGO_SECTOR_BANDA']):
              d = df.query('CODIGO_SECTOR_BANDA==@cod_sector')
              d1 = d.loc[:,columns_prbs].mean().to_frame().T
              d1['FECHA'] = fecha_mapa
              d1['CODIGO_SECTOR_BANDA'] = cod_sector
              d1['BANDA'] = banda_filter
              d1['UNICO'] = pd.unique(d['UNICO'])
              d1['DEPARTAMENTO'] = pd.unique(d['DEPARTAMENTO'])
              d1['PROVINCIA'] = pd.unique(d['PROVINCIA'])
              d1['NOMBRE_EBC'] = pd.unique(d['NOMBRE_EBC'])
              d1['SECTOR']=pd.unique(d['SECTOR'])
              d1['DISTRITO'] = pd.unique(d['DISTRITO'])
              d1['LATITUD'] = pd.unique(d['LATITUD'])
              d1['LONGITUD'] = pd.unique(d['LONGITUD'])
              d1['AZIMUT'] = pd.unique(d['AZIMUT'])
              d1['BEAN'] = pd.unique(d['BEAN'])
              d1['RADIO_MAP'] = pd.unique(d['RADIO_MAP'])
              df_new.loc[idx,:] = d1[columns_data].loc[0,:]
              idx+=1
          prbs_inter = []
          
          def EvalListPRBsINTER(row):
              global LIMIT_PRB
              if row>=LIMIT_PRB:
                  return 1
              else:
                  return 0
          for prb in list(dic_prb.keys()):
              df_new[prb+'_INTER']=df_new[prb].apply(EvalListPRBsINTER)
              prbs_inter.append(prb+'_INTER')
          #Por si las dudas    
          d = df_new.groupby(by=prbs_inter)['CODIGO_SECTOR_BANDA'].count().reset_index().sort_values(by='CODIGO_SECTOR_BANDA',ascending=False)
          st.dataframe(d)
          st.dataframe(df_new[['FECHA','CODIGO_SECTOR_BANDA','BANDA','UNICO','NOMBRE_EBC','SECTOR','DISTRITO']+prbs_inter])
          
          
          if not(df.empty & df_new.empty):
              path_csv = dir_now / 'RANKING_PRB' / vendor / banda_filter / fecha_query
              if Path.exists(path_csv) == False:
                  Path.mkdir(path_csv)
                  
              name_df = 'Sectores_PRBHxH_{}_limit_{}.csv'.format(fecha_query,LIMIT_PRB)
              name_df_new = 'Sectores_PRBDay_{}_limit_{}.csv'.format(fecha_query,LIMIT_PRB)
              df.to_csv(path_csv / name_df,index=False)
              df_new.to_csv(path_csv / name_df_new,index=False)
              name_prbs = path_csv / "PRBs_Inter_{}_limit_{}.txt".format(fecha_query,LIMIT_PRB)
              with open(name_prbs,'w') as file:
                  for row in prbs_inter:
                      file.write(row+'\n')
              
             
              
              return dic_prb
              
          
          
        except Exception as ex:
            st.write(ex)
            pass
def AnalizarDataSeleccionada(vendor,dep_filter,prov_filter,banda_filter,fecha_query,dic_banda,fecha_mapa,LIMIT_PRB):
    if vendor=='NOKIA':
        path_csv = dir_now / 'RANKING_PRB' / vendor / banda_filter / fecha_query
        if Path.exists(path_csv) == False:
            Path.mkdir(path_csv)
        name_df = 'Sectores_PRBHxH_{}_limit_{}.csv'.format(fecha_query,LIMIT_PRB)
        name_df_new = 'Sectores_PRBDay_{}_limit_{}.csv'.format(fecha_query,LIMIT_PRB)
        df = pd.read_csv(path_csv / name_df)
        df_new = pd.read_csv(path_csv / name_df_new)
        name_prbs = path_csv / "PRBs_Inter_{}_limit_{}.txt".format(fecha_query,LIMIT_PRB)
        global prbs_inter
        prbs_inter= []
        with open(name_prbs,'r') as file:
            for line in file.readlines():
                prbs_inter.append(line.replace('\n',''))
            
        st.subheader('Cantidad de Sectores afectados de Acuerdo a los PRBs más interferidos para la Region de {} y banda {}'.format(dep_filter,banda_filter))    
        d = df_new.groupby(by=prbs_inter)['CODIGO_SECTOR_BANDA'].count().reset_index().sort_values(by='CODIGO_SECTOR_BANDA',ascending=False)
        #st.dataframe(d)
        
        #---------------------------------- Distribución de la Cantidad de Código Sector Segun Ranking PRBs Afectados----------------#
        def ReturnCombinacionPRBAfectados(row):
            global prbs_inter
            if row=='00':
                return "Ninguno"
            elif row=='01':
                return prbs_inter[1]
            elif row=='10':
                return prbs_inter[0]
            else:
                return prbs_inter[0]+'&'+prbs_inter[1]
        d['COMBINE'] = d[prbs_inter[0]].apply(str) + d[prbs_inter[1]].apply(str)
        #st.dataframe(d)
        d['COMBINE'] = d['COMBINE'].apply(ReturnCombinacionPRBAfectados)
        #st.dataframe(d)
        fig_bars = px.bar(
                d,
                x='COMBINE',
                y='CODIGO_SECTOR_BANDA',
                color='COMBINE',
                orientation='v',
                barmode='relative',
                labels={'CODIGO_SECTOR_BANDA': 'Num_Sector', 'COMBINE': 'PRBs Afectados'},
                color_discrete_map={'Ninguno': 'Blue', prbs_inter[0]: 'Cyan', prbs_inter[1]: 'Orange',prbs_inter[0]+'&'+prbs_inter[1]:'Red'},
                template='plotly_white',
                text_auto=True)  # 'ggplot2', 'seaborn', 'simple_white', 'plotly', 'plotly_white'
        fig_bars.update_layout(title='Cantidad de Sectores según PRBs más interferidos para la region {} y banda {}'.format(prov_filter,banda_filter),xaxis=dict(showgrid=False),
                              yaxis=dict(showgrid=False))
        st.plotly_chart(fig_bars, theme="streamlit", use_container_width=True)
    
    
    
        with st.expander("Sectores afectados, Grafico 2D y Grafico 3D"):
            #Inicio para la descarga del CSV
            st.dataframe(df_new[['FECHA','CODIGO_SECTOR_BANDA','BANDA','UNICO','NOMBRE_EBC','SECTOR','DISTRITO']+prbs_inter])
            @st.cache
            def convert_df(df):
                # IMPORTANT: Cache the conversion to prevent computation on every rerun
                return df.to_csv(index=False).encode('utf-8')
            
            csv = convert_df(df_new)
            label_document = 'Download data as CSV de la fecha {}'.format(fecha_query)
            name_file = '{}_{}_Sectores_PRBDay_{}_limit_{}.csv'.format(vendor,prov_filter,fecha_query,LIMIT_PRB)
            st.subheader("Descargar Archivo csv")
            st.download_button(
                label=label_document,
                data=csv,
                file_name=name_file,
                mime='text/csv',
                )
            
            #-------------------------------------------------------INICIO DE LOS GRAFICOS 3D y 2D--------------------------------#
            st.subheader('Tabla de Sectores afectados de Acuerdo a los PRBs más interferidos para la Region de {} y banda {}'.format(dep_filter,banda_filter))
            #st.dataframe(df_new)
            col1,col2,col3 = st.columns(3)
            with col1:
                filter_ebc = st.selectbox('Seleccione Nombre EBC', pd.unique(df_new['NOMBRE_EBC']))
            with col2:
                filter_sector = st.selectbox('Seleccione Sector', pd.unique(df_new['SECTOR']))
            df_filtrado = df.query('NOMBRE_EBC==@filter_ebc & SECTOR==@filter_sector')
            with col3:
                st.text_input('Codigo Sector Banda Seleccionado',value=pd.unique(df_filtrado.CODIGO_SECTOR_BANDA)[0],disabled=True)
            columns_prbs=[]
            columns_data = ['FECHA', 'CODIGO_SECTOR_BANDA', 'BANDA', 'UNICO', 'NOMBRE_EBC', 'SECTOR', 'DISTRITO', 'LATITUD', 'LONGITUD', 'AZIMUT', 'BEAN','RADIO_MAP']
            for i in range(0,dic_banda[banda_filter]):
                columns_prbs.append('PRB'+str(i))
                columns_data.append('PRB'+str(i))
            fig1,fig2 = st.columns(2)
            df_prbs_grahp = df_filtrado[columns_prbs]
            fig_surf = go.Figure(data=[go.Surface(z=df_prbs_grahp,
                                                  cmin=-120,
                                                  cmax=-90 ,
                                                  x=columns_prbs, 
                                                  y=pd.to_datetime(df_filtrado['FECHA']),
                                                  colorscale =px.colors.diverging.RdYlGn_r,
                                                  surfacecolor=df_prbs_grahp)])
            fig_surf.update_layout(title='Surface 3D para {}_{} y banda {}'.format(filter_ebc,filter_sector,banda_filter),
                     autosize=True,margin=dict(l=65, r=50, b=65, t=90),height=800)
            with fig1:
                st.plotly_chart(fig_surf, theme="streamlit", use_container_width=True)
                
            #list_prbs.reverse()
            fig = go.Figure().set_subplots(rows=1, cols=1)
            fig.add_trace(go.Heatmap(x=columns_prbs, y=pd.to_datetime(df_filtrado['FECHA']), z=df_prbs_grahp, coloraxis="coloraxis"), row=1, col=1)
            fig.update_layout(title='Spectrograma para {}_{} y banda {}'.format(filter_ebc,filter_sector,banda_filter),height=800,coloraxis=dict(colorscale=px.colors.diverging.RdYlGn_r, cmin=-120, cmid=-105, cmax= -90))
            with fig2:
                st.plotly_chart(fig, theme="streamlit", use_container_width=True)
        
        
        
        # CREAR ESTILOS PARA APLICAR A LOS POLIGONOS DE LOS KML

        #Interferencia Un PRB -> SEGUNDA COLUMNA DE LOS PRBS AFECTADOS
        sharedstyle_1 = Style()
        sharedstyle_1.linestyle.color = simplekml.Color.orange
        sharedstyle_1.polystyle.color = simplekml.Color.changealphaint(200, simplekml.Color.orange)

        #Interferencia Otro PRB -> PRIMERA COLUMNA DE LOS PRBS AFECTADOS
        sharedstyle_2 = Style()
        sharedstyle_2.linestyle.color = simplekml.Color.cyan
        sharedstyle_2.polystyle.color = simplekml.Color.changealphaint(200, simplekml.Color.cyan)

        #Interferencia dos PRBs
        sharedstyle_3 = Style()
        sharedstyle_3.linestyle.color = simplekml.Color.red
        sharedstyle_3.polystyle.color = simplekml.Color.changealphaint(200, simplekml.Color.red)

        #Ningun PRB
        sharedstyle_4 = Style()
        sharedstyle_4.linestyle.color = simplekml.Color.blue
        sharedstyle_4.polystyle.color = simplekml.Color.changealphaint(200, simplekml.Color.blue)

        # FUNCION PARA CALCULAR LOS PUNTOS DE LOS POLIGONOS SECTOR
        def puntos_poligonos(lat, lon, azimth, beamwidth, radius):
            puntos = [(lon, lat)]
            coordenadas = coordinates.Coordinate(lat, lon)
            coords_arc = paths.ArcPath(origin=coordenadas, start_bearing=azimth + (beamwidth / 2),
                                     end_bearing=azimth - (beamwidth / 2), radius=radius * 0.0006, direction='Clockwise',
                                     points=10)
            for k in range(10):
                puntos.append((coords_arc.coordinates[k].longitude, coords_arc.coordinates[k].latitude))
            puntos.append((lon, lat))#Editado
            return puntos
        # FUNCION PARA CLASIFICAR LAS INTERFERENCIAS Y APLICAR ESTILO A LOS POLIGONOS
        def estilo_poligono(sector,prbs_inter):
            if sector[prbs_inter[0]]==0:
                if sector[prbs_inter[1]]==1:
                    estilo = sharedstyle_1
                    color_sector = "orange"
                else:
                    estilo = sharedstyle_4
                    color_sector = "blue"
            else:
                if sector[prbs_inter[1]]==1:
                    estilo = sharedstyle_3
                    color_sector = "red"
                else:
                    estilo = sharedstyle_2
                    color_sector = "cyan"
            return estilo, color_sector

        # LISTA DE TECNOLOGIAS
        tecnologia = ['LTE']
        
        # INICIALIZAR VARIABLES AUXILIARES
        coords_inter = []
        sector_ant = []
        # CREAR ARCHIVOS KML Y MAPAS HTML POR REGIONAL
        provincias = df_new.PROVINCIA.unique()
        for provincial in provincias:
            #kml_create = f"kml_{provincial} = simplekml.Kml()"
            kml_provincia = simplekml.Kml()
            latitud_provincial=df_new.query('PROVINCIA==@provincial')['LATITUD'].min()
            longitud_provincial=df_new.query('PROVINCIA==@provincial')['LONGITUD'].min()
            zoom_scale_provincial = 7
            #map_create = f"hmap_{provincial} = folium.Map(location=[{latitud_provincial}, {longitud_provincial}], control_scale=True, zoom_start={str(zoom_scale_provincial)})"
            map_provincia = folium.Map(location=[latitud_provincial, longitud_provincial], control_scale=True, zoom_start=str(zoom_scale_provincial))
            #popup = f"hmap_{provincial}.add_child(folium.LatLngPopup())"
            map_provincia.add_child(folium.LatLngPopup())
            #full_screen = f"plugins.Fullscreen(position='bottomright', title='Expand me', title_cancel='Exit', force_separate_button=True).add_to(hmap_{provincial})"
            plugins.Fullscreen(position='bottomright', title='Expand me', title_cancel='Exit', force_separate_button=True).add_to(map_provincia)
            #exec(kml_create)
            #exec(map_create)
            #exec(popup)
            #exec(full_screen)
        
        # CICLO PARA RECORRER POR TECNOLOGIAS Y  DISTRITOS
        for provincial in provincias:
            kml_provincia = simplekml.Kml()
            latitud_provincial=df_new.query('PROVINCIA==@provincial')['LATITUD'].min()
            longitud_provincial=df_new.query('PROVINCIA==@provincial')['LONGITUD'].min()
            zoom_scale_provincial = 7
            map_provincia = folium.Map(location=[latitud_provincial, longitud_provincial], control_scale=True, zoom_start=str(zoom_scale_provincial))
            map_provincia.add_child(folium.LatLngPopup())
            plugins.Fullscreen(position='bottomright', title='Expand me', title_cancel='Exit', force_separate_button=True).add_to(map_provincia)
            for y in range(len(tecnologia)):
                #tech_folder = f"fol{tecnologia[y]}=kml_{provincial}.newfolder(name='{tecnologia[y]}')"
                tech_folder_provincial = kml_provincia.newfolder(name=tecnologia[y])
                #exec(tech_folder)
                sectores_provinciales = df_new.query('PROVINCIA==@provincial')#En caso exista por tecnologia
                for dist in sectores_provinciales.DISTRITO.unique():
                    sectores_distritales = sectores_provinciales.query('DISTRITO==@dist')
                    sectores_distritales = sectores_distritales.sort_values(by=['UNICO', 'SECTOR'])
                    dist1 = dist.replace(' ', '_')
                    #dist_folder = f"fol{dist1} = fol{tecnologia[y]}.newfolder(name='Distrito {dist1}')"
                    distrital_folder = tech_folder_provincial.newfolder(name='Distrito ' + dist1)
                    #dist_layer = f"ldist_{dist1} = folium.FeatureGroup(name='{tecnologia[y]} {dist1}').add_to(hmap_{provincial})"
                    distrital_layer = folium.FeatureGroup(name=tecnologia[y] + ' ' + dist1).add_to(map_provincia)
                    #exec(dist_folder)
                    #exec(dist_layer)
                    # Ciclo para dibujar los sectores
                    for index, sector in sectores_distritales.iterrows():
                        sector_act = sector['NOMBRE_EBC']
                        sector['UL_INTER'] = sector[columns_prbs].mean(axis=0,skipna=True)
                        # Dibubar sectores en KML
                        if sector_act != sector_ant:
                            #folder = f"fol = fol{dist1}.newfolder(name='{str(sector['NOMBRE_EBC'])}')"
                            distrital_ebc = distrital_folder.newfolder(name=sector['NOMBRE_EBC'])
                            #exec(folder)
                        pol = distrital_ebc.newpolygon(name=str(index))#Cambio
                        pol.outerboundaryis = puntos_poligonos(sector['LATITUD'], sector['LONGITUD'], sector['AZIMUT'], sector['BEAN'], sector['RADIO_MAP'])
                        pol.description = f"""Sitio: {str(sector['UNICO'])}<br/>
                                                Sector: {str(sector['SECTOR'])}<br/>
                                                Proveedor: {str(vendor)}<br/>
                                                Nombre: {str(sector['NOMBRE_EBC'])}<br/>
                                                UL Int Avg = {str(round(sector['UL_INTER'], 2))}<br/>
                                                Azimuth = {str(sector['AZIMUT'])}"""
                        
                       
                        
                        # Definir estilo del poligono kml
                        # Definir color de sector para mapa html
                        # Agregar columna de tipo de interferencia al dataframe sectores
                        pol.style, color = estilo_poligono(sector,prbs_inter)

                        
                        #Dibujar sectores en mapa html (folium)
                        #l_map = f'ldist_{dist1}'
                        plugins.SemiCircle((sector['LATITUD'], sector['LONGITUD']),
                                     radius=sector['RADIO_MAP'],
                                     start_angle=sector['AZIMUT'] + (sector['BEAN'] / 2),
                                     stop_angle=sector['AZIMUT'] - (sector['BEAN'] / 2),
                                     color=color,
                                     fill_color=color,
                                     opacity=0.8,
                                     popup=f"""Sitio: {str(sector['UNICO'])}<br/>
                                               Sector: {str(sector['SECTOR'])}<br/>
                                               Proveedor: {str(vendor)}<br/>
                                               Nombre: {str(sector['NOMBRE_EBC'])}<br/>
                                               UL Int Avg = {str(round(sector['UL_INTER'], 2))}<br/>
                                               Azimuth = {str(sector['AZIMUT'])}"""
                                     ).add_to(distrital_layer)
                        sector_ant = sector_act
                        coords_inter.clear()
              
            # GUARDAR LOS ARCHIVOS KML Y HTML
            file_kml = dir_now / 'RANKING_PRB' / vendor / banda_filter / fecha_query
            if Path.exists(file_kml) == False:
                Path.mkdir(file_kml)
          
        
            folium.LayerControl(collapsed=False).add_to(map_provincia)
            print('inicio de creado')
            file_kml = file_kml / '{}_{}_limit_{}.kml'.format(provincial,fecha_query,LIMIT_PRB)
            file_kml = str(file_kml).replace('\\', '/')
            file_map = dir_now / 'RANKING_PRB' / vendor / banda_filter / fecha_query
            file_map = file_map / '{}_{}_limit_{}.html'.format(provincial,fecha_query,LIMIT_PRB)
            file_map = str(file_map).replace('\\', '/')
            #file_to_save = f"{str(file_kml)}"
            kml_provincia.save(file_kml)
            map_provincia.save(file_map)
            
            HtmlFile = open(file_map, 'r', encoding='utf-8')
            source_code = HtmlFile.read() 
            components.html(source_code, height = 1000)
            name_kml = file_kml
            name_html = file_map
            #with file_kml:
            #st.write("Descargar Archivo kml")
            with open(str(name_kml), "rb") as file:
                st.download_button(
                        label="Descargar Archivo kmz de la fecha: {} y {}".format(fecha_query,banda_filter),
                        data=file,
                        file_name="{}_{}_{}_limit_{}.kml".format(vendor,banda_filter,fecha_query,LIMIT_PRB),
                        mime="image/kml"
                      )
            with open(str(name_html), "rb") as file:
                st.download_button(
                        label="Descargar Archivo html de la fecha: {} y {}".format(fecha_query,banda_filter),
                        data=file,
                        file_name="{}_{}_{}_limit_{}.html".format(vendor,banda_filter,fecha_query,LIMIT_PRB),
                        mime="image/html"
                      )
         





with st.sidebar:
    filter_vendor = st.radio(
        "Eliga un proveedor Disponible 👉",
        options=["Análisis PRBs para NOKIA", "Análisis PRBs para HUAWEI","Análisis PRBs para ERICSSON"]
    )
    
    
filters = st.container()

#Tomando la cantidad de PRBs para cada tipo de Banda
dic_banda = {'AWS':100,
             'B700':75,
             '1900':50}
departamentos = ['AREQUIPA','LORETO','UCAYALI','CUSCO','APURIMAC','CAJAMARCA',
                 'PIURA','MADRE DE DIOS','LAMBAYEQUE','TACNA','TUMBES',
                 'HUANCAVELICA','ANCASH','AYACUCHO','ICA','PASCO','MOQUEGUA',
                 'SAN MARTIN','JUNIN','HUANUCO','PUNO','LIMA','AMAZONAS','LA LIBERTAD']


with filters:
    now = datetime.now()
    if 'NOKIA' in filter_vendor:
        st.subheader('Análisis de PRBs para NOKIA')
        filter_1,filter_2,filter_3,filter_4,filter_5,filter_6 = st.columns(6)
        with filter_1:
            dep_filter = st.selectbox("Seleccione Departamento", departamentos)
            provincias = SearchProvin(dep_filter)
        with filter_2:
            prov_filter = st.selectbox("Seleccione Provincia", provincias)
            #st.dataframe(distritos)
        with filter_3:
            banda_filter = st.selectbox("Seleccione Banda",dic_banda.keys() )
        with filter_4:
            FECHA_PRB = st.date_input(label='Eliga la fecha a analizar')
            fecha_mapa = pd.to_datetime(FECHA_PRB).strftime('%Y-%m-%d')
            #st.write(fecha_mapa)
            fecha_query = pd.to_datetime(FECHA_PRB).strftime('%d%m%y')
            LIMIT_PRB = st.number_input('Ingrese Umbral Mínimo de PRB')
            st.sidebar.success("Seleccione el proveedor para su análisis(Umbral PRB > {})".format(LIMIT_PRB))
        with filter_5:
            st.write('Click Para consultar')
            btn_Consultar = st.button('Consultar',type='primary')
        with filter_6:
            st.write('Seleccione para analizar')
            filter_box = st.checkbox('Analizar')
            
        if btn_Consultar:
            dic_prb = ReturnDistritoPRB('NOKIA',dep_filter,prov_filter,banda_filter,fecha_query,dic_banda,LIMIT_PRB)
            ReturnDataFrameMapHTML('NOKIA',dep_filter,prov_filter,banda_filter,fecha_query,dic_banda,dic_prb,fecha_mapa,LIMIT_PRB)
            #st.write(dic_prb)
        if filter_box:
            AnalizarDataSeleccionada('NOKIA',dep_filter,prov_filter,banda_filter,fecha_query,dic_banda,fecha_mapa,LIMIT_PRB)
        
    elif 'HUAWEI' in filter_vendor:
        st.subheader('Análisis de PRBs para HUAWEI')
        filter_1,filter_2,filter_3,filter_4,filter_5,filter_6 = st.columns(6)
        with filter_1:
            dep_filter = st.selectbox("Seleccione Departamento", departamentos)
            provincias = SearchProvin(dep_filter)
        with filter_2:
            prov_filter = st.selectbox("Seleccione Provincia", sorted(provincias))
            #st.dataframe(distritos)
        with filter_3:
            banda_filter = st.selectbox("Seleccione Banda",dic_banda.keys() )
        with filter_4:
            FECHA_PRB = st.date_input(label='Eliga la fecha a analizar')
            fecha_mapa = pd.to_datetime(FECHA_PRB).strftime('%Y-%m-%d')
            #st.write(fecha_mapa)
            fecha_query = pd.to_datetime(FECHA_PRB).strftime('%d%m%y')
            
        with filter_5:
            st.write('Click Para consultar')
            btn_Consultar = st.button('Consultar',type='primary')
        with filter_6:
            st.write('Seleccione para analizar')
            filter_box = st.checkbox('Analizar')
        if btn_Consultar:
            dic_prb = ReturnDistritoPRB('HUAWEI',dep_filter,prov_filter,banda_filter,fecha_query,dic_banda,LIMIT_PRB)
            st.write(dic_prb)
        
            
    elif 'ERICSSON' in filter_vendor:
        st.subheader('Análisis de PRBs para ERICSSON')
        filter_1,filter_2,filter_3,filter_4,filter_5 = st.columns(5)
        with filter_1:
            dep_filter = st.selectbox("Seleccione Departamento", departamentos)
            provincias = SearchProvin(dep_filter)
        with filter_2:
            prov_filter = st.selectbox("Seleccione Provincia", provincias)
            #st.dataframe(distritos)
        with filter_3:
            banda_filter = st.selectbox("Seleccione Banda",dic_banda.keys() )
        with filter_4:
            FECHA_PRB = st.date_input(label='Eliga la fecha a analizar')
            fecha_mapa = pd.to_datetime(FECHA_PRB).strftime('%Y-%m-%d')
            #st.write(fecha_mapa)
            fecha_query = pd.to_datetime(FECHA_PRB).strftime('%d%m%y')
        with filter_5:
            st.write('Click Para consultar')
            btn_Consultar = st.button('Consultar',type='primary')
        if btn_Consultar:
            dic_prb = ReturnDistritoPRB('ERICSSON',dep_filter,prov_filter,banda_filter,fecha_query,dic_banda,LIMIT_PRB)
            st.write(dic_prb)
        