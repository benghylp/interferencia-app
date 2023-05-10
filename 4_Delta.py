# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 10:30:39 2023

@author: Benghy Lipa
"""

import pandas as pd
import cx_Oracle
from pathlib import Path
import streamlit as st
from datetime import datetime
import plotly.express as px 
from io import StringIO
import streamlit.components.v1 as components
import plotly.graph_objs as go
from zipfile import ZipFile
import os
import numpy as np

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

def ReturnPRBValue(col):
    if col < 1 :
        return -120
    return np.round(10 * np.log10(col * (0.00000000000005684341886080801486968994140625/90000)),0)

def ReturnTipo(col1,col2):
    if col1>-105:
        if col2<-2 or col2>2:
            return 'PIM'
        else:
            return 'EXTERNA'
    elif col1>-115:
        if col2<-2 or col2>2:
            return 'PIM LEVE'
        else:
            return 'NORMAL'
    else:
        if col2<-2 or col2>2:
            return 'HW'
        else:
            return 'NORMAL'

def ReturnQueryVendorDeltaVsPRBs(vendor,banda_filter,fecha_query):
    if vendor=='NOKIA':
        queryAVGPRB = '''
        SELECT 
        		to_char(N4.PERIOD_START_TIME, 'yyyy-mm-dd hh24') AS FECHA,
        		MC.COD_CRUCE CODIGO_SECTOR_BANDA, MC.BANDA BANDA, MC.UNICO UNICO,
                MC.NOMBRE_EBC_2 NOMBRE_EBC,MC.SECTOR SECTOR,MC.DISTRITO DISTRITO,
                MC.LATITUD LATITUD,MC.LONGITUD LONGITUD,
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
                AND MC.BANDA='{}'
                ORDER BY MC.CODIGO_SECTOR_BANDA,MC.SECTOR,FECHA ASC
        '''.format(fecha_query,fecha_query,banda_filter)
        queryDelta='''
        SELECT 
           to_char(N4.PERIOD_START_TIME, 'yyyy-mm-dd hh24 ') FECHA,
           to_char(N4.LNCEL_ID) CODIGO_SECTOR_BANDA,
           (N4.AVG_RTWP_RX_ANT_1)/10 AVG_RTWP_RX_ANT_1,
           (N4.AVG_RTWP_RX_ANT_2)/10 AVG_RTWP_RX_ANT_2,
           (N4.AVG_RTWP_RX_ANT_3)/10 AVG_RTWP_RX_ANT_3,
           (N4.AVG_RTWP_RX_ANT_4)/10 AVG_RTWP_RX_ANT_4
    FROM NOKLTE_P_LPQUL1_LNCEL_DAY@NETACT19 N4
    INNER JOIN 
    		osiptel.mc_4g MC ON MC.COD_CRUCE=TO_CHAR(N4.LNCEL_ID)
    WHERE N4.PERIOD_START_TIME BETWEEN to_date('{} 00', 'ddmmyy hh24') AND to_date('{} 23', 'ddmmyy hh24')
          AND MC.BANDA='{}'
        '''.format(fecha_query,fecha_query,banda_filter)
    if vendor=='HUAWEI':
        queryAVGPRB='''
        SELECT 
		to_char(H4.FECHA, 'yyyy-mm-dd hh24') AS FECHA,
		MC.COD_CRUCE CODIGO_SECTOR_BANDA, MC.BANDA BANDA,
        MC.UNICO UNICO, MC.NOMBRE_SECTOR NOMBRE_EBC,MC.SECTOR SECTOR, MC.DISTRITO DISTRITO,
        MC.LATITUD LATITUD, MC.LONGITUD LONGITUD,
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
    INNER JOIN 
        inv_mc@db_gerweb_siggsm INV ON INV.CODIGO_CRUCE=MC.COD_CRUCE 
        --AND INV.CODIGO_CRUCE=SUBSTR(SUBSTR(OBJ_NAME,INSTR(OBJ_NAME,'=',1,3) + 1),0,INSTR(SUBSTR(OBJ_NAME,INSTR(OBJ_NAME,'=',1,3) + 1),'-',1,1)-1) || SUBSTR(OBJ_NAME,INSTR(OBJ_NAME,'=',1,2) + 1,1) 
    WHERE 
        FECHA BETWEEN to_date('{} 00', 'ddmmyy hh24') AND to_date('{} 23', 'ddmmyy hh24')
        AND to_char(MC.SECTOR)=SUBSTR(SUBSTR(OBJ_NAME,INSTR(OBJ_NAME,'=',1,2)+1),0,INSTR(SUBSTR(OBJ_NAME,INSTR(OBJ_NAME,'=',1,2)+1),',')-1)
        AND MC.BANDA='{}'
    ORDER BY MC.CODIGO_SECTOR_BANDA,MC.SECTOR,FECHA ASC
        '''.format(fecha_query,fecha_query,banda_filter)
        queryDelta='''
    SELECT to_char(MIN(H4.FECHA),'yyyy-mm-dd') FECHA,
    MAX(MC.CODIGO_SECTOR_BANDA) CODIGO_SECTOR_BANDA,
    AVG(C1526737656) AVG_RTWP_RX_ANT_1, 
    AVG(C1526737657) AVG_RTWP_RX_ANT_2, 
    AVG(C1526737658) AVG_RTWP_RX_ANT_3, 
    AVG(C1526737659) AVG_RTWP_RX_ANT_4
    FROM almacen.H4_1526726806 H4,osiptel.mc_4g MC
    WHERE H4.FECHA BETWEEN to_date('{} 00', 'ddmmyy hh24') AND to_date('{} 23', 'ddmmyy hh24')
    AND to_char(MC.ENODEB)=SUBSTR(SUBSTR(H4.OBJ_NAME,INSTR(OBJ_NAME,'=',1,3)+1),0,INSTR(SUBSTR(H4.OBJ_NAME,INSTR(OBJ_NAME,'=',1,3)+1),',',1,1)-1)
    AND to_char(MC.SECTOR)=SUBSTR(H4.OBJ_NAME,INSTR(OBJ_NAME,'=',1,2) + 1,1)
    AND MC.BANDA='{}'
    GROUP BY OBJ_NAME
        '''.format(fecha_query,fecha_query,banda_filter)
    if vendor=='ERICSSON':
        queryAVGPRB='''
        SELECT 
    		to_char(E4.DATETIME_ID, 'yyyy-mm-dd hh24:mi') AS FECHA,
    		MC.COD_CRUCE CODIGO_SECTOR_BANDA,MC.BANDA BANDA, MC.UNICO UNICO,
            MC.NOMBRE_EBC NOMBRE_EBC,MC.SECTOR SECTOR,MC.DISTRITO DISTRITO,
            MC.LATITUD LATITUD,MC.LONGITUD LONGITUD,
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
        INNER JOIN
            inv_mc@db_gerweb_siggsm INV ON INV.CODIGO_CRUCE=MC.COD_CRUCE 
    	WHERE 
    		E4.DATETIME_ID BETWEEN to_date('{} 00 00', 'ddmmyy hh24:mi') AND to_date('{} 23 59', 'ddmmyy hh24:mi')
        AND MC.BANDA='{}'
        ORDER BY MC.NOMBRE_EBC,MC.SECTOR,MC.BANDA,FECHA ASC
        '''.format(fecha_query,fecha_query,banda_filter)
        queryDelta='''
        SELECT 
        to_char(MIN(E4.DATETIME_ID), 'yyyy-mm-dd') FECHA,
        MAX(MC.CODIGO_SECTOR_BANDA) CODIGO_SECTOR_BANDA,
        AVG((E4.DIST0_0_CAL2 + E4.DIST0_0_CAL)/E4.PMBRANCHDELTASINRDISTR0) DELTA_1,
        AVG((E4.DIST1_1_CAL2 + E4.DIST1_1_CAL1)/E4.PMBRANCHDELTASINRDISTR1) DELTA_2,
        AVG((E4.DIST2_2_CAL2 + E4.DIST2_2_CAL1)/E4.PMBRANCHDELTASINRDISTR2) DELTA_3
    FROM ALMACEN.E4_ERBS_SECTORCARRIER_V_RAW E4, osiptel.mc_4g MC
    WHERE E4.DATETIME_ID BETWEEN to_date('{} 00', 'ddmmyy hh24') AND to_date('{} 23', 'ddmmyy hh24')
    AND E4.ERBS=MC.NOMBRE_EBC
    AND E4.SECTORCARRIER=MC.SECTOR_LOGICO
    AND MC.BANDA='{}'
    GROUP BY E4.ERBS,E4.SECTORCARRIER
        '''.format(fecha_query,fecha_query,banda_filter)
    return (queryAVGPRB,queryDelta)
def ReturnDataFrameSectoresAVGPRBs(vendor,banda_filter,fecha_query):
    try:
        connection = cx_Oracle.connect(user='DW_MOVIL',
                                         password='YTUMMAFasd656',
                                         dsn='10.10.61.162:1521/DIRNEN',
                                         encoding='UTF-8')
        #st.write(connection.version)
        cursor = connection.cursor()
        #st.write("Ejecutado")
        query = ReturnQueryVendorDeltaVsPRBs(vendor, banda_filter, fecha_query)[0]#AVGPRBs
        #st.write(query)
        #st.write("Extrayendo los datos")
        cursor.execute(query)
        names= [x[0] for x in cursor.description]
        #st.write(names)
        rows = cursor.fetchall()
        #st.write(rows)
        df_sectores_prbs = pd.DataFrame(rows,columns=names)
        #st.dataframe(df)
        cols_name=[]
        cols_name = ['FECHA','CODIGO_SECTOR_BANDA','BANDA','UNICO','NOMBRE_EBC','SECTOR','DISTRITO','LATITUD','LONGITUD']
        for i in range(0,dic_banda[banda_filter]):
            if vendor=='ERICSSON':
                df_sectores_prbs['PRB'+str(i)] = df_sectores_prbs['PRB'+str(i)].apply(ReturnPRBValue)
            cols_name.append('PRB'+str(i))
        
        #Se filtran los PRBs y demás columnas de acuerdo al tipo de Banda
        df_sectores_prbs = df_sectores_prbs.loc[:,cols_name]
        #st.dataframe(df_sectores_prbs)
        #Se agrupan para hallar el promedio
        df_g=df_sectores_prbs.groupby(by=['CODIGO_SECTOR_BANDA','SECTOR','NOMBRE_EBC']).mean().reset_index()
        #st.dataframe(df_g)
        df_g['AVG_PRBs'] = df_g.mean(axis=1,numeric_only=True)
        df_sectores_avgPRB = df_g[['CODIGO_SECTOR_BANDA','NOMBRE_EBC','SECTOR','AVG_PRBs']]
        #df_sectores_avgPRB = df_g.copy()
        df_sectores_avgPRB.sort_values(by=['NOMBRE_EBC','SECTOR'],inplace=True,ignore_index=True)
        return (df_sectores_avgPRB,df_sectores_prbs)
    except Exception as ex:
        st.write(ex)
        st.write(ex.__cause__())
        st.write(ex)
        return pd.DataFrame()
    

def ReturnDataFrameSectoresDeltas(vendor,banda_filter,fecha_query):
    try:
        connection = cx_Oracle.connect(user='DW_MOVIL',
                                         password='YTUMMAFasd656',
                                         dsn='10.10.61.162:1521/DIRNEN',
                                         encoding='UTF-8')
        #st.write(connection.version)
        cursor = connection.cursor()
        #st.write("Ejecutado")
        query=ReturnQueryVendorDeltaVsPRBs(vendor, banda_filter, fecha_query)[1]#Query para Delta
        cursor.execute(query)
        names= [x[0] for x in cursor.description]
        #st.write(names)
        rows = cursor.fetchall()
        #st.write(rows)
        df_sectores_delta = pd.DataFrame(rows,columns=names)
        return df_sectores_delta
    except Exception as ex:
        st.write(ex)
        st.write(ex.__cause__())
        st.write(ex)
def ReturnQueryOnlyDelta(vendor,banda_filter,fecha_query):
    if vendor=='NOKIA':
        queryonlyDelta = '''
                    SELECT 
                   to_char(N4.PERIOD_START_TIME, 'yyyy-mm-dd hh24 ') FECHA,
                   MC.NOMBRE_EBC_2 NOMBRE_EBC,MC.SECTOR SECTOR,
                   to_char(N4.LNCEL_ID) CODIGO_SECTOR_BANDA,
                   (N4.AVG_RTWP_RX_ANT_1)/10 AVG_RTWP_RX_ANT_1,
                   (N4.AVG_RTWP_RX_ANT_2)/10 AVG_RTWP_RX_ANT_2,
                   (N4.AVG_RTWP_RX_ANT_3)/10 AVG_RTWP_RX_ANT_3,
                   (N4.AVG_RTWP_RX_ANT_4)/10 AVG_RTWP_RX_ANT_4
            FROM NOKLTE_P_LPQUL1_LNCEL_DAY@NETACT19 N4
            INNER JOIN 
            		osiptel.mc_4g MC ON MC.COD_CRUCE=TO_CHAR(N4.LNCEL_ID)
            WHERE N4.PERIOD_START_TIME BETWEEN to_date('{} 00', 'ddmmyy hh24') AND to_date('{} 23', 'ddmmyy hh24')
             AND MC.BANDA='{}'
            ORDER BY NOMBRE_EBC,SECTOR ASC
        '''.format(fecha_query,fecha_query,banda_filter)
    if vendor=='HUAWEI':
        queryonlyDelta='''
                SELECT to_char(MIN(H4.FECHA),'yyyy-mm-dd') FECHA,
        MAX(MC.NOMBRE_SECTOR) NOMBRE_EBC,
        MAX(MC.SECTOR) SECTOR,
        MAX(MC.CODIGO_SECTOR_BANDA) CODIGO_SECTOR_BANDA,
        AVG(C1526737656) AVG_RTWP_RX_ANT_1, 
        AVG(C1526737657) AVG_RTWP_RX_ANT_2, 
        AVG(C1526737658) AVG_RTWP_RX_ANT_3, 
        AVG(C1526737659) AVG_RTWP_RX_ANT_4
        FROM almacen.H4_1526726806 H4,osiptel.mc_4g MC
        WHERE H4.FECHA BETWEEN to_date('{} 00', 'ddmmyy hh24') AND to_date('{} 23', 'ddmmyy hh24')
        AND to_char(MC.ENODEB)=SUBSTR(SUBSTR(H4.OBJ_NAME,INSTR(OBJ_NAME,'=',1,3)+1),0,INSTR(SUBSTR(H4.OBJ_NAME,INSTR(OBJ_NAME,'=',1,3)+1),',',1,1)-1)
        AND to_char(MC.SECTOR)=SUBSTR(H4.OBJ_NAME,INSTR(OBJ_NAME,'=',1,2) + 1,1)
        AND MC.BANDA='{}'
        GROUP BY OBJ_NAME
        ORDER BY NOMBRE_SECTOR,SECTOR ASC
        '''.format(fecha_query,fecha_query,banda_filter)
    if vendor=='ERICSSON':
        queryonlyDelta='''
            SELECT 
        to_char(MIN(E4.DATETIME_ID), 'yyyy-mm-dd') FECHA,
        MAX(E4.ERBS) NOMBRE_EBC,
        MAX(MC.CODIGO_SECTOR_BANDA) CODIGO_SECTOR_BANDA,
        MAX(MC.BANDA) BANDA,
        MAX(MC.SECTOR) SECTOR_MC,
        MAX(E4.SECTORCARRIER) SECTOR,
        AVG((E4.DIST0_0_CAL2 + E4.DIST0_0_CAL)/E4.PMBRANCHDELTASINRDISTR0) DELTA_1,
        AVG((E4.DIST1_1_CAL2 + E4.DIST1_1_CAL1)/E4.PMBRANCHDELTASINRDISTR1) DELTA_2,
        AVG((E4.DIST2_2_CAL2 + E4.DIST2_2_CAL1)/E4.PMBRANCHDELTASINRDISTR2) DELTA_3
        FROM ALMACEN.E4_ERBS_SECTORCARRIER_V_RAW E4, osiptel.mc_4g MC
        WHERE E4.DATETIME_ID BETWEEN to_date('{} 00', 'ddmmyy hh24') AND to_date('{} 23', 'ddmmyy hh24')
        AND E4.ERBS=MC.NOMBRE_EBC
        AND E4.SECTORCARRIER=MC.SECTOR_LOGICO
        AND MC.BANDA='{}'
        GROUP BY E4.ERBS,E4.SECTORCARRIER
        '''.format(fecha_query,fecha_query,banda_filter)
    return queryonlyDelta
def ReturnDataFrameOnlyDelta(vendor,banda_filter,fecha_query):
    def ReturnPIM(row):
        if row>=2:
            return 'PIM'
        else:
            return 'OK'
    try:
        connection = cx_Oracle.connect(user='DW_MOVIL',
                                         password='YTUMMAFasd656',
                                         dsn='10.10.61.162:1521/DIRNEN',
                                         encoding='UTF-8',)
        #st.write(connection.version)
        cursor = connection.cursor()
        #st.write("Ejecutado")
        query=ReturnQueryOnlyDelta(vendor, banda_filter, fecha_query)#Query para onlyDelta
        cursor.execute(query)
        names= [x[0] for x in cursor.description]
        #st.write(names)
        rows = cursor.fetchall()
        #st.write(rows)
        df_sectores_only_delta = pd.DataFrame(rows,columns=names)
        df_sectores_only_delta['DELTA_1'] = (df_sectores_only_delta['AVG_RTWP_RX_ANT_1']-df_sectores_only_delta['AVG_RTWP_RX_ANT_2'])
        df_sectores_only_delta['DELTA_2'] = (df_sectores_only_delta['AVG_RTWP_RX_ANT_3']-df_sectores_only_delta['AVG_RTWP_RX_ANT_4'])
        df_sectores_only_delta['RESULT_DELTA1'] = df_sectores_only_delta['DELTA_1'].apply(ReturnPIM)
        df_sectores_only_delta['RESULT_DELTA2'] = df_sectores_only_delta['DELTA_2'].apply(ReturnPIM)
        return df_sectores_only_delta
    except Exception as ex:
        st.write(ex)
        st.write(ex.__cause__())
        st.write(ex)
def ReturnSectoresConcat(vendor,banda_filter,fecha_query):
    if vendor!='ERICSSON':
        df_sectores_delta = ReturnDataFrameSectoresDeltas(vendor,banda_filter,fecha_query)
        (df_sectores_avg_PRB,df_sectores_prbs) = ReturnDataFrameSectoresAVGPRBs(vendor, banda_filter, fecha_query)
        df_sectores = df_sectores_avg_PRB.merge(df_sectores_delta, on=['CODIGO_SECTOR_BANDA'], how='left')
        df_sectores['DELTA_1'] = (df_sectores['AVG_RTWP_RX_ANT_1']-df_sectores['AVG_RTWP_RX_ANT_2'])
        df_sectores['DELTA_2'] = (df_sectores['AVG_RTWP_RX_ANT_3']-df_sectores['AVG_RTWP_RX_ANT_4'])
        #df_sectores_graph = df_sectores[['CODIGO_SECTOR_BANDA', 'NOMBRE_EBC', 'SECTOR', 'AVG_PRBs', 'DELTA_1']]
    else:
        df_sectores_delta = ReturnDataFrameSectoresDeltas(vendor,banda_filter,fecha_query)#BOTA CON LOS DELTA_0,DELTA_1,DELTA_2
        #st.dataframe(df_sectores_delta)
        (df_sectores_avg_PRB,df_sectores_prbs) = ReturnDataFrameSectoresAVGPRBs(vendor, banda_filter, fecha_query)
        df_sectores = df_sectores_avg_PRB.merge(df_sectores_delta, on=['CODIGO_SECTOR_BANDA'], how='left')
    return df_sectores,df_sectores_prbs

def DescargarHTMLCSV(df_sectores_delta,vendor,banda_filter,fecha_query,fig_scat,fig_bars_delta1):
    
    #Inicio para la descarga del HTML - Graph
    #@st.cache
    #def convertGrahpHTML(fig_scat,fecha_query,vendor,banda_filter):
    #    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    #    buffer = StringIO()
    #    fig_scat.write_html(buffer, include_plotlyjs='cdn')
    #    html_bytes = buffer.getvalue().encode()
    #    return html_bytes
    
    #Inicio para la creación de la grafica
    #grahp_html = convertGrahpHTML(fig_scat,fecha_query,vendor,banda_filter)
    #label_html = 'Download Grahp as HTML de la fecha {} y BANDA {}'.format(fecha_query,banda_filter)
    #name_file = 'GraghDelta_{}_{}_{}.html'.format(vendor,banda_filter,fecha_query)
    #st.subheader("Descargar Archivo html")
    
    #st.download_button(
    #    label=label_html,
    #    data=grahp_html,
    #    file_name=name_file,
    #    mime='image/html'
    #    )
    
    
    #Inicio para la descarga del CSV 
    #@st.cache
    #def convert_df(df_sectores_delta):
    #    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    #    return df_sectores_delta.to_csv(index=False).encode('utf-8')
    #
    #csv = convert_df(df_sectores_delta)
    #label_document = 'Download data as CSV de la fecha {} y BANDA {}'.format(fecha_query,banda_filter)
    #name_file = 'TableDelta_{}_{}_{}.csv'.format(vendor,banda_filter,fecha_query)
    #st.subheader("Descargar Archivo csv")
    
    
    #st.download_button(
    #    label=label_document,
    #    data=csv,
    #    file_name=name_file,
    #    mime='text/csv'
    #    )
    
    #-------------------------------Creacion de Archivos para el Zip-----------------------#
    #Grahp de Barras
    name_html_2  = 'BarDelta_{}_{}_{}.html'.format(vendor,banda_filter,fecha_query)
    path_html_2 = dir_now / 'pages' / name_html_2
    fig_bars_delta1.write_html(path_html_2, include_plotlyjs='cdn')
    
    #Graph de Division
    name_html  = 'GraghDelta_{}_{}_{}.html'.format(vendor,banda_filter,fecha_query)
    path_html = dir_now / 'pages' / name_html
    fig_scat.write_html(path_html, include_plotlyjs='cdn')
    
    #Archhivo CSV
    name_csv = 'TableDelta_{}_{}_{}.csv'.format(vendor,banda_filter,fecha_query)
    path_csv = dir_now / 'pages' / name_csv
    df_sectores_delta.to_csv(path_csv,index=False)
    
    #Proceso de ZIP
    name_zip = 'Delta_{}_{}_{}.zip'.format(vendor,banda_filter,fecha_query)
    path_zip = dir_now / 'pages' / name_zip
    with ZipFile(path_zip,'w') as zipObj:
        zipObj.write(path_html,name_html)
        zipObj.write(path_csv,name_csv)
        zipObj.write(path_html_2,name_html_2)
        os.remove(path_html)
        os.remove(path_csv)
        os.remove(path_html_2)
     
    #Proceso de Descarga
    label_document = 'Download data as CSV & HTML de la fecha {} y BANDA {}'.format(fecha_query,banda_filter)
    with open(path_zip,'rb') as zip_file:
        btn_1 = st.download_button(
            label=label_document, 
            data=zip_file,
            file_name=name_zip,
            mime='application/zip')
        
    
    
    
    
def ReturnDownloadCSVDelta(df_sectores_delta,vendor,banda_filter,fecha_query):
    #Inicio para la descarga del CSV 
    @st.cache
    def convert_df(df_sectores_delta):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df_sectores_delta.to_csv(index=False).encode('utf-8')
    
    csv = convert_df(df_sectores_delta)
    label_document = 'Download data as CSV de la fecha {} y BANDA {}'.format(fecha_query,banda_filter)
    name_file = 'TableDelta_{}_{}_{}.csv'.format(vendor,banda_filter,fecha_query)
    st.subheader("Descargar Archivo csv")
    st.download_button(
        label=label_document,
        data=csv,
        file_name=name_file,
        mime='text/csv',
        )

def ReturnGraphTableDelta(vendor,banda_filter,fecha_query):
    (df_sectores_graph,df_sectores_prbs) = ReturnSectoresConcat(vendor,banda_filter,fecha_query)
    if not(df_sectores_graph.empty):
        df_sectores_graph.dropna(subset=['FECHA'],inplace=True,axis=0)
        tab1, tab2 = st.tabs(["Análisis Delta", "Tabla Delta"])
        with tab1:
            st.header("Análisis AVG PRBs vs Delta")
            fig_scat = px.scatter(df_sectores_graph,
                                  x="AVG_PRBs", 
                                  y="DELTA_1", 
                                  color='DELTA_1',
                                  
                                  hover_data=['CODIGO_SECTOR_BANDA','NOMBRE_EBC','SECTOR'],
                                  labels={'CODIGO_SECTOR_BANDA': 'CODIGO SECTOR BANDA', 'DELTA_1':'DELTA 1','AVG_PRBs':'AVG PRB'},
                                  template='plotly_white')
            
            #PIM
            fig_scat.add_shape(type='rect',
                               xref="x",yref="y",
                               x0=-70,y0=2,
                               x1=-105+0.2,y1=df_sectores_graph['DELTA_1'].max() + 0.5,
                               line=dict(color="RoyalBlue",width=2),
                               )
            fig_scat.add_annotation(
                x=df_sectores_graph['AVG_PRBs'].max(),
                y=df_sectores_graph['DELTA_1'].min()-1,
                text='PIM',
                showarrow=False,
                font=dict(color="RoyalBlue",size=18))
            fig_scat.add_shape(type='rect',
                               xref="x",yref="y",
                               x0=-70,y0=-2,
                               x1=-105+0.2,y1=df_sectores_graph['DELTA_1'].min() - 0.5,
                               line=dict(color="RoyalBlue",width=2),
                               )
            fig_scat.add_annotation(
                x=-70,
                y=df_sectores_graph['DELTA_1'].max()+1,
                text='PIM',
                showarrow=False,
                font=dict(color="RoyalBlue",size=18))
            
            #PIM LEVE
            fig_scat.add_shape(type='rect',
                               xref="x",yref="y",
                               x0=-105+0.1,y0=2,
                               x1= -115+0.1,y1=df_sectores_graph['DELTA_1'].max() + 0.5,
                               line=dict(color="LightSeaGreen",width=2),
                               )
            fig_scat.add_annotation(
                x=-105,
                y=df_sectores_graph['DELTA_1'].max() + 1,
                text='PIM LEVE',
                showarrow=False,
                font=dict(color="LightSeaGreen",size=18))
            fig_scat.add_shape(type='rect',
                               xref="x",yref="y",
                               x0=-105+0.1,y0=-2,
                               x1= -115+0.1,y1=df_sectores_graph['DELTA_1'].min() - 0.5,
                               line=dict(color="LightSeaGreen",width=2),
                               )
            fig_scat.add_annotation(
                x=-105,
                y=df_sectores_graph['DELTA_1'].min() - 1,
                text='PIM LEVE',
                showarrow=False,
                font=dict(color="LightSeaGreen",size=18))
            #HW
            fig_scat.add_shape(type='rect',
                               xref="x",yref="y",
                               x0=-115,y0=2,
                               x1=df_sectores_graph['AVG_PRBs'].min() - 0.5,y1=df_sectores_graph['DELTA_1'].max() + 0.5,
                               line=dict(color="Red",width=2),
                               )
            fig_scat.add_annotation(
                x=-115,
                y=df_sectores_graph['DELTA_1'].max() + 1,
                text='HW',
                showarrow=False,
                font=dict(color="Red",size=18))
            fig_scat.add_shape(type='rect',
                               xref="x",yref="y",
                               x0=-115,y0=-2,
                               x1=df_sectores_graph['AVG_PRBs'].min() - 0.5,y1=df_sectores_graph['DELTA_1'].min() - 0.5,
                               line=dict(color="Red",width=2),
                               )
            fig_scat.add_annotation(
                x=-115,
                y=df_sectores_graph['DELTA_1'].min() - 1,
                text='HW',
                showarrow=False,
                font=dict(color="Red",size=18))
            #Externa
            fig_scat.add_shape(type='rect',
                               xref="x",yref="y",
                               x0=-70,y0=2,
                               x1=-105+0.1,y1=-2,
                               line=dict(color="Orange",width=2),
                               )
            fig_scat.add_annotation(
                x=-70,
                y=2,
                text='Externa',
                showarrow=False,
                font=dict(color="Orange",size=18))
            #delta
            fig_scat.add_shape(type='rect',
                               xref="x",yref="y",
                               x0=-70,y0=-2,
                               x1=df_sectores_graph['AVG_PRBs'].min() - 0.5,y1=2,
                               line=dict(color="Black",width=1,dash='dot'),
                               )
            fig_scat.update_layout(title='Análisis AVG_PRBs vs Delta',autosize=True,height=900)
            #Mostrar Grafico
            st.plotly_chart(fig_scat, theme="streamlit", use_container_width=True)
                
        with tab2:
            #---------------------------Catalogar Tipo de Interferencia---------------------#
            df_sectores_tipos = df_sectores_graph.copy()
            df_sectores_tipos['TIPO'] = df_sectores_tipos.apply(lambda row: ReturnTipo(row.AVG_PRBs,row.DELTA_1),axis=1)
            #---------------------------Inicio del gráfico de los Tipos de Interferencia--------------#
            df_sectores_tipos_grahp = df_sectores_tipos.groupby(by=['TIPO'])['CODIGO_SECTOR_BANDA'].count().reset_index().sort_values(by='CODIGO_SECTOR_BANDA',ascending=False)
            fig_bars_delta1 = px.bar(
                    df_sectores_tipos_grahp,
                    x='TIPO',
                    y='CODIGO_SECTOR_BANDA',
                    color='TIPO',
                    orientation='v',
                    barmode='relative',
                    labels={'TIPO': 'Tipo de Interferencia','CODIGO_SECTOR_BANDA':'CANTIDAD DE CODIGO SECTOR BANDA'},
                    template='plotly_white',
                    text_auto=True)  # 'ggplot2', 'seaborn', 'simple_white', 'plotly', 'plotly_white'
            fig_bars_delta1.update_layout(title='Análisis Tipo de Interferencia',autosize=True)
            st.plotly_chart(fig_bars_delta1, theme="streamlit", use_container_width=True)
            #Mostrar Tabla
            if vendor!='ERICSSON':
                st.dataframe(df_sectores_tipos.style.format(subset=['AVG_PRBs','AVG_RTWP_RX_ANT_1','AVG_RTWP_RX_ANT_2', 'AVG_RTWP_RX_ANT_3', 'AVG_RTWP_RX_ANT_4','DELTA_1','DELTA_2'],formatter="{:.2f}"))
            else:
                st.dataframe(df_sectores_tipos.style.format(subset=['AVG_PRBs','DELTA_1','DELTA_2', 'DELTA_3'],formatter="{:.2f}"))
            #Descargar Archivo HTML y CSV 
            DescargarHTMLCSV(df_sectores_tipos,vendor,banda_filter,fecha_query,fig_scat,fig_bars_delta1)
    else:
        st.header("Análisis Delta - delta ≥ 2")
        df_sectores_only_delta = ReturnDataFrameOnlyDelta(vendor,banda_filter,fecha_query)
        df_sectores_only_delta_grahp = df_sectores_only_delta.groupby(['RESULT_DELTA1','RESULT_DELTA2'])['CODIGO_SECTOR_BANDA'].count().reset_index()
        df_sectores_only_delta_grahp['RESULT_DELTA1__RESULT_DELTA2'] = df_sectores_only_delta_grahp['RESULT_DELTA1'] + ' & ' + df_sectores_only_delta_grahp['RESULT_DELTA2']
        st.subheader('Cantidad de Sectores vs Tipo Interf.')
        fig_bars_delta1 = px.bar(
                df_sectores_only_delta_grahp,
                x='RESULT_DELTA1__RESULT_DELTA2',
                y='CODIGO_SECTOR_BANDA',
                color='RESULT_DELTA1__RESULT_DELTA2',
                orientation='v',
                barmode='relative',
                labels={'RESULT_DELTA1__RESULT_DELTA2': 'RESULT_DELTA1 & RESULT_DELTA2','CODIGO_SECTOR_BANDA':'CANTIDAD DE CODIGO SECTOR BANDA'},
                template='plotly_white',
                text_auto=True)  # 'ggplot2', 'seaborn', 'simple_white', 'plotly', 'plotly_white'
        st.plotly_chart(fig_bars_delta1, theme="streamlit", use_container_width=True)
        #Visualiazr la Tabla
        #ReturnDownloadCSVDelta(df_sectores_only_delta,vendor,banda_filter,fecha_query)
        if vendor!='ERICSSON':
            st.dataframe(df_sectores_only_delta.style.format(subset=['AVG_RTWP_RX_ANT_1','AVG_RTWP_RX_ANT_2', 'AVG_RTWP_RX_ANT_3', 'AVG_RTWP_RX_ANT_4','DELTA_1','DELTA_2'],formatter="{:.2f}"))
        else:
            st.dataframe(df_sectores_tipos.style.format(subset=['AVG_PRBs','DELTA_1','DELTA_2', 'DELTA_3'],formatter="{:.2f}"))
      
    
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
        st.subheader('Análisis de Delta para NOKIA')
        filter_1,filter_2,filter_3 = st.columns(3)
        with filter_2:
            FECHA_DELTA = st.date_input(label='Eliga la fecha a analizar')
            fecha_query = pd.to_datetime(FECHA_DELTA).strftime('%d%m%y')
        with filter_1:
            banda_filter = st.selectbox("Seleccione Banda",dic_banda.keys())
        with filter_3:
            st.write('Click Para consultar')
            btn_Consultar = st.button('Consultar',type='primary')
        if btn_Consultar:
            ReturnGraphTableDelta(vendor,banda_filter,fecha_query)
    elif 'HUAWEI' in filter_vendor:
        vendor='HUAWEI'
        st.subheader('Análisis de Delta para HUAWEI')
        filter_1,filter_2,filter_3 = st.columns(3)
        with filter_2:
            FECHA_DELTA = st.date_input(label='Eliga la fecha a analizar')
            fecha_query = pd.to_datetime(FECHA_DELTA).strftime('%d%m%y')
        with filter_1:
            banda_filter = st.selectbox("Seleccione Banda",dic_banda.keys())
        with filter_3:
            st.write('Click Para consultar')
            btn_Consultar = st.button('Consultar',type='primary')
        if btn_Consultar:
            ReturnGraphTableDelta(vendor,banda_filter,fecha_query)
    elif 'ERICSSON' in filter_vendor:
        vendor='ERICSSON'
        st.subheader('Análisis de Delta para ERICSSON')
        filter_1,filter_2,filter_3 = st.columns(3)
        with filter_2:
            FECHA_DELTA = st.date_input(label='Eliga la fecha a analizar')
            fecha_query = pd.to_datetime(FECHA_DELTA).strftime('%d%m%y')
        with filter_1:
            banda_filter = st.selectbox("Seleccione Banda",dic_banda.keys())
        with filter_3:
            st.write('Click Para consultar')
            btn_Consultar = st.button('Consultar',type='primary')
        if btn_Consultar:
            ReturnGraphTableDelta(vendor,banda_filter,fecha_query)

    




