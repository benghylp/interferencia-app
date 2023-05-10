# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 16:01:22 2023

@author: Benghy Lipa
"""


import pandas as pd
import numpy as np
import streamlit as st  # data web app development
from pathlib import Path
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import cx_Oracle
from datetime import datetime
import plotly.express as px 
import tensorflow as tf

def ReturnPRBValue(col):
    if col < 1 :
        return -120
    return np.round(10 * np.log10(col * (0.00000000000005684341886080801486968994140625/90000)),0)

def ReturnQueryVendor(vendor,fecha_query_ini,fecha_query_fin,CODIGO_SECTOR_BANDA):
    if vendor=='NOKIA':
        query = '''
        SELECT 
      		to_char(N4.PERIOD_START_TIME, 'yyyy-mm-dd hh24') AS FECHA,
      		MC.COD_CRUCE,MC.BANDA,
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
              AND MC.COD_CRUCE='{}'
        ORDER BY FECHA ASC
      '''.format(fecha_query_ini,fecha_query_fin,CODIGO_SECTOR_BANDA)
    elif vendor=='HUAWEI':
        query = '''
        SELECT 
            to_char(H4.FECHA, 'yyyy-mm-dd hh24') AS FECHA,
            MC.COD_CRUCE,MC.BANDA BANDA,
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
            osiptel.mc_4g MC ON to_char(MC.CODIGO_SECTOR_BANDA)=CONCAT(SUBSTR(SUBSTR(H4.OBJ_NAME,INSTR(H4.OBJ_NAME,'=',1,3) + 1),0,INSTR(SUBSTR(H4.OBJ_NAME,INSTR(H4.OBJ_NAME,'=',1,3) + 1),'-',1,1)-1), SUBSTR(H4.OBJ_NAME,INSTR(H4.OBJ_NAME,'=',1,2) + 1,1))
            AND MC.NOMBRE_EBC = SUBSTR(SUBSTR(H4.OBJ_NAME,INSTR(H4.OBJ_NAME,'_')+1),0,INSTR(SUBSTR(H4.OBJ_NAME,INSTR(H4.OBJ_NAME,'_')+1),'/')-1)
        WHERE 
            FECHA BETWEEN to_date('{} 00', 'ddmmyy hh24') AND to_date('{} 23', 'ddmmyy hh24')
            AND to_char(MC.SECTOR)=SUBSTR(SUBSTR(OBJ_NAME,INSTR(OBJ_NAME,'=',1,2)+1),0,INSTR(SUBSTR(OBJ_NAME,INSTR(OBJ_NAME,'=',1,2)+1),',')-1)
            AND MC.COD_CRUCE='{}'
        ORDER BY MC.NOMBRE_EBC,MC.SECTOR,FECHA ASC
      '''.format(fecha_query_ini,fecha_query_fin,CODIGO_SECTOR_BANDA)
    elif vendor=='ERICSSON':
        query = '''
        SELECT 
		to_char(E4.DATETIME_ID, 'yyyy-mm-dd hh24:mi') AS FECHA,
		MC.COD_CRUCE, MC.BANDA,
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
        AND MC.COD_CRUCE='{}'
    ORDER BY FECHA ASC
      '''.format(fecha_query_ini,fecha_query_fin,CODIGO_SECTOR_BANDA)
    return query


def ReturnGrahpDataFramePRB(vendor,FECHA_PRB,fecha_query_ini,fecha_query_fin,CODIGO_SECTOR_BANDA):
    try:
      connection = cx_Oracle.connect(user='DW_MOVIL',
                                       password='YTUMMAFasd656',
                                       dsn='10.10.61.162:1521/DIRNEN',
                                       encoding='UTF-8',)
      print(connection.version)
      cursor = connection.cursor()
      print("Ejecutado")
      query = ReturnQueryVendor(vendor,fecha_query_ini,fecha_query_fin,CODIGO_SECTOR_BANDA)
      #st.write(query)
      print("Extrayendo los datos")
      cursor.execute(query)
      names= [x[0] for x in cursor.description]
      rows = cursor.fetchall()
      df = pd.DataFrame(rows,columns=names)
      #st.dataframe(df)
      if df.empty:
          st.subheader('No posee data para la fecha {}  y código de sector {}'.format(FECHA_PRB,CODIGO_SECTOR_BANDA))
      else:
          fecha_file_ini = pd.to_datetime(FECHA_PRB[0]).strftime('%d%m%Y')
          fecha_file_sig = pd.to_datetime(FECHA_PRB[1]).strftime('%d%m%Y')
          sector = CODIGO_SECTOR_BANDA
          banda = df.BANDA.iloc[0]
          list_prbs = [] 
          list_dataframe = []
          list_dataframe.append('FECHA')
          list_dataframe.append('COD_CRUCE')
          list_dataframe.append('BANDA')
          #for i in range(dic_banda[banda]-1,-1,-1):
          #    list_prbs.append('PRB'+str(i))
          #    list_dataframe.append('PRB'+str(i))
          for i in range(0,dic_banda[banda]):
              list_prbs.append('PRB'+str(i))
              list_dataframe.append('PRB'+str(i))
          if vendor=='ERICSSON':
              #Para cuando tenga data
              df_new = pd.DataFrame(columns=df.columns)
              #Se obtienen los valores de cada columna PRB
              for prb in list_prbs:
                  df[prb] = df[prb].map(ReturnPRBValue)
              df_min = df.copy()
              fechas  = (df['FECHA'].apply(lambda row: row[:-5])).unique()
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
                      d = df[ (df['FECHA']>=fecha) & (df['FECHA']<fecha_sig) ]
                      if not(d.empty):
                          d = d.loc[:,list_prbs].mean()
                          d = d.to_frame()
                          d = d.T
                          d['FECHA'] = fecha
                          d['BANDA'] = banda
                          d['COD_CRUCE'] = sector
                          df_new = pd.concat([df_new,d],ignore_index=True)
              df = df_new.copy()
              with st.expander("Tabla de PRBs minXmin para el Sector {} y Banda {} entre las fechas {} - {}".format(CODIGO_SECTOR_BANDA,banda,fecha_file_ini,fecha_file_sig)):
                  #Inicio para la descarga del CSV - Filtrado por departamento
                  @st.cache
                  def convert_df(df):
                      # IMPORTANT: Cache the conversion to prevent computation on every rerun
                      return df.to_csv(index=False).encode('utf-8')
                  
                  csv = convert_df(df_min[list_dataframe])
                  label_document = 'Download data as CSV de la fecha {}-{} y Código de Sector {}'.format(fecha_file_ini,fecha_file_sig,CODIGO_SECTOR_BANDA)
                  name_file = '{}_{}_{}_{}.csv'.format(vendor,CODIGO_SECTOR_BANDA,fecha_file_ini,fecha_file_sig)
                  st.subheader("Descargar Archivo csv")
                  st.download_button(
                      label=label_document,
                      data=csv,
                      file_name=name_file,
                      mime='text/csv',
                      )
                  d_table = df_min[list_dataframe]
                  st.dataframe(d_table.style.format(subset=list_prbs,formatter="{:.0f}"))
          #Se filtra las columnas que se desea analizar(FECHA,COD_CRUCE,BANDA, PRB0,....,PRBX) -> DEPENDE DE LA BANDA
          with st.expander("Tabla de PRBs HxH para el Sector {} y Banda {} entre las fechas {} - {}".format(CODIGO_SECTOR_BANDA,banda,fecha_file_ini,fecha_file_sig)):
              #Inicio para la descarga del CSV - Filtrado por departamento
              @st.cache
              def convert_df(df):
                  # IMPORTANT: Cache the conversion to prevent computation on every rerun
                  return df.to_csv(index=False).encode('utf-8')
              
              csv = convert_df(df[list_dataframe])
              label_document = 'Download data as CSV de la fecha {}-{} y Código de Sector {}'.format(fecha_file_ini,fecha_file_sig,CODIGO_SECTOR_BANDA)
              name_file = '{}_{}_{}_{}.csv'.format(vendor,CODIGO_SECTOR_BANDA,fecha_file_ini,fecha_file_sig)
              st.subheader("Descargar Archivo csv")
              st.download_button(
                  label=label_document,
                  data=csv,
                  file_name=name_file,
                  mime='text/csv',
                  )
              d_table = df[list_dataframe]
              st.dataframe(d_table.style.format(subset=list_prbs,formatter="{:.0f}"))
          
          #Cada Gráfico
          tab1, tab2, tab3 = st.tabs(["Grafico 3D - Surface", "Grafico 2D HeatMap - Spectrograma", "Grafico 2D - Evolutivo AVG_PRGB"])
          
          df_prbs = df[list_prbs]
          
          with tab1:
              #Se revierte la lista de PRBs para fines de gráfico
              #list_prbs.reverse()
              st.subheader('Grafico 3D - Surface')
              fig_surf = go.Figure(data=[go.Surface(z=df_prbs,
                                                    cmin=-120,
                                                    cmax=-90 ,
                                                    x=list_prbs, 
                                                    y=pd.to_datetime(df['FECHA']),
                                                    colorscale =px.colors.diverging.RdYlGn_r,
                                                    surfacecolor=df_prbs)])
              fig_surf.update_layout(title='Plots para el Sector {} y banda {}'.format(sector,banda),
                       autosize=True,margin=dict(l=65, r=50, b=65, t=90),
                       width=900, height=900)
              st.plotly_chart(fig_surf, theme="streamlit", use_container_width=True)
          
          
          
          with tab2:
              st.subheader('Grafica 2D - Spectrograma')    
              k=0
              list_fechas = pd.unique(pd.to_datetime(pd.unique(df['FECHA'])).strftime('%Y-%m-%d'))
              dir_fechas = pd.unique(pd.to_datetime(pd.unique(df['FECHA'])).strftime('%d%m%y'))
              
              #st.write(list_fechas)
              col=5
              row=int(np.ceil(len(list_fechas)//col))
              
              fig = make_subplots(rows=row, cols=col,subplot_titles=dir_fechas.tolist())
              dia_ant = list_fechas[0]
              list_fechas = list_fechas[1:]
              k=0
              for i in range(1,row+1):
                  for j in range(1,col+1):
                      dia = list_fechas[k]
                      #st.write(dia)
                      sector_dia = df[(df['FECHA']>dia_ant)&(df['FECHA']<dia)]
                      if not(sector_dia.empty):
                          #st.dataframe(sector_dia)
                          sector_dia_prbs = sector_dia[list_prbs]
                          fig.add_trace(go.Heatmap(x=list_prbs, y=sector_dia['FECHA'], z=sector_dia_prbs, coloraxis="coloraxis"), row=i, col=j)
                          k+=1
                          dia_ant = dia
              fig.update_layout(title='Sector {} y Banda {}'.format(sector,banda),height=1500,width=2000,coloraxis=dict(colorscale=px.colors.diverging.RdYlGn_r, cmin=-120, cmid=-105, cmax= -90))
              st.plotly_chart(fig, theme="streamlit", use_container_width=True)
          
            
          with tab3:
              df['AVG_PRB'] = df[list_prbs].mean(axis=1,skipna=True)
              
              fig_line = px.line(df,
                                 x='FECHA',
                                 y='AVG_PRB',
                                 labels={'FECHA': 'Date', 'AVG_PRB': 'Promedio PRB'})
              #fig_line.update_traces(line_color='OrangeRed')
              fig_line.update_layout(title_text='Evolutivo AVG PRB')
              fig_line['layout']['yaxis']['autorange'] = "reversed"
              fig_line.update_layout(xaxis=dict(showgrid=True),
                                    yaxis=dict(showgrid=True))
              
              
              st.plotly_chart(fig_line, theme="streamlit", use_container_width=True)
          
    except Exception as ex:
      st.write(ex)
      #st.write(" ")
      #print(ex.__cause__())    
    

with open('css/style.css')as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)


dir_now = Path.cwd()
lib_dir = dir_now / 'Lib_Oracle'
try:
    cx_Oracle.init_oracle_client(lib_dir=str(lib_dir))
except Exception as ex:
    print(ex)
    print(" ")


st.markdown("# Gráficas de PRBs ")


st.sidebar.success("Seleccione el proveedor para su análisis")




with st.sidebar:
    filter_vendor = st.radio(
        "Eliga un proveedor Disponible 👉",
        options=["Análisis PRBs para NOKIA", "Análisis PRBs para HUAWEI","Análisis PRBs para ERICSSON"]
    )
    
graphPRB = st.container()

#Tomando la cantidad de PRBs para cada tipo de Banda
dic_banda = {'AWS':100,
             'B700':75,
             '1900':50,
             'AWS-E':100,
             'B900':25,
             'B700-E':75}  

with graphPRB:
    now = datetime.now()
    if 'NOKIA' in filter_vendor:
        st.subheader('Análisis de PRBs para NOKIA')
        col1,col2,col3 = st.columns(3)
        with col1:
            CODIGO_SECTOR_BANDA = st.text_input("Ingrese Código de Sector Banda")
        with col2:
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
        with col3:
            st.write('Click Para consultar')
            btn_Consultar = st.button('Consultar',type='primary')
        if btn_Consultar:
            ReturnGrahpDataFramePRB('NOKIA',FECHA_PRB,fecha_query_ini,fecha_query_fin,CODIGO_SECTOR_BANDA)
    elif 'HUAWEI' in filter_vendor:
        st.subheader('Análisis de PRBs para HUAWEI')
        col1,col2,col3 = st.columns(3)
        with col1:
            CODIGO_SECTOR_BANDA = st.text_input("Ingrese Código de Sector Banda")
        with col2:
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
        with col3:
            st.write('Click Para consultar')
            btn_Consultar = st.button('Consultar',type='primary')
        if btn_Consultar:
            ReturnGrahpDataFramePRB('HUAWEI',FECHA_PRB,fecha_query_ini,fecha_query_fin,CODIGO_SECTOR_BANDA)
    elif 'ERICSSON' in filter_vendor:
        st.subheader('Análisis de PRBs para ERICSSON')
        col1,col2,col3 = st.columns(3)
        with col1:
            CODIGO_SECTOR_BANDA = st.text_input("Ingrese Código de Sector Banda")
        with col2:
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
        with col3:
            st.write('Click Para consultar')
            btn_Consultar = st.button('Consultar',type='primary')
        if btn_Consultar:
            ReturnGrahpDataFramePRB('ERICSSON',FECHA_PRB,fecha_query_ini,fecha_query_fin,CODIGO_SECTOR_BANDA)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    