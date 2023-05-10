import pandas as pd
import numpy as np
import streamlit as st  # data web app development
from PIL import Image
from pathlib import Path
import plotly.graph_objs as go
import os
import plotly.express as px  # interactive charts





dir_now = Path.cwd() 
logo_file = dir_now / 'css' / 'peru.png'
im = Image.open(str(logo_file))
st.set_page_config(
    page_title="Dashboard de Interferencia Peru",
    page_icon=im,
    layout="wide")

st.sidebar.success("Evolutivo de Interferencia")

# Link to css file
with open('css/style.css')as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)


#Funciones
def Mostrar_Kpis(totales,week_filter,tech_filter,band_filter,vendor_filter,type_filter,fecha_ant,totales_ant,sectores_interf):
    #st.table(totales)
    totales_copy = totales.copy()
    totales = totales.groupby(['FECHA', 'TIPO'])['CODIGO_SECTOR_BANDA'].count().reset_index(name='count')
    #st.dataframe(totales)
    totales = totales.pivot(index=['FECHA'], columns='TIPO',values=['count'])
    #st.dataframe(totales)
    totales.columns = totales.columns.droplevel()
    #st.dataframe(totales)
    totales = totales.rename_axis(None,axis=1).reset_index()
    #st.dataframe(totales)
    totales = totales.set_index('FECHA', drop=True)
    #st.dataframe(totales)
    if fecha_ant=='':
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        #kpi1.metric("Critico", totales.loc[week_filter]['Critico'])#, totales.loc[week_filter]['pct_change_c'])
        d = sectores_interf.groupby(['FECHA', 'TIPO'])['CODIGO_SECTOR_BANDA'].count().reset_index(name='count')
        d = d.pivot(index=['FECHA'], columns='TIPO',values=['count'])
        d.columns = d.columns.droplevel()
        d = d.rename_axis(None,axis=1).reset_index()
        d = d.set_index('FECHA', drop=True)
        kpi1.metric("Critico", totales.loc[week_filter]['Critico'],delta_color='inverse')
        kpi2.metric("Alta", totales.loc[week_filter]['Alta'],delta_color='inverse')#, totales.loc[week_filter]['pct_change_a'])
        kpi3.metric("Medio",totales.loc[week_filter]['Medio'],delta_color='inverse')#, totales.loc[week_filter]['pct_change_m'])
        kpi4.metric("Baja",totales.loc[week_filter]['Baja'],delta_color='inverse')#, totales.loc[week_filter]['pct_change_m'])
        Dibujar_Evolutivo(sectores_interf,vendor_filter,tech_filter,band_filter,week_filter,type_filter,kpi1,kpi2,kpi3,kpi4)
    else:
        #st.write(week_filter)
        totales_ant = totales_ant.groupby(['FECHA', 'TIPO'])['CODIGO_SECTOR_BANDA'].count().reset_index(name='count')
        #st.dataframe(totales_ant)
        totales_ant = totales_ant.pivot(index=['FECHA'], columns='TIPO',values=['count'])
        #st.dataframe(totales_ant)
        totales_ant.columns = totales_ant.columns.droplevel()
        #st.dataframe(totales_ant)
        totales_ant = totales_ant.rename_axis(None,axis=1).reset_index()
        #st.dataframe(totales_ant)
        totales_ant = totales_ant.set_index('FECHA', drop=True)
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        percent_Critico = (totales.loc[week_filter]['Critico']-totales_ant.loc[fecha_ant]['Critico'])/(totales_ant.loc[fecha_ant]['Critico'])
        percent_alta = (totales.loc[week_filter]['Alta']-totales_ant.loc[fecha_ant]['Alta'])/(totales_ant.loc[fecha_ant]['Alta'])
        percent_Medio = (totales.loc[week_filter]['Medio']-totales_ant.loc[fecha_ant]['Medio'])/(totales_ant.loc[fecha_ant]['Medio'])
        percent_Baja = (totales.loc[week_filter]['Baja']-totales_ant.loc[fecha_ant]['Baja'])/(totales_ant.loc[fecha_ant]['Baja'])
        kpi1.metric("Critico", totales.loc[week_filter]['Critico'], '{:.0f}%'.format(percent_Critico*100),delta_color='inverse')
        kpi2.metric("Alta", totales.loc[week_filter]['Alta'], '{:.0f}%'.format(percent_alta*100),delta_color='inverse')
        kpi3.metric("Medio",totales.loc[week_filter]['Medio'],'{:.0f}%'.format(percent_Medio*100),delta_color='inverse')
        kpi4.metric("Baja",totales.loc[week_filter]['Baja'],'{:.0f}%'.format(percent_Baja*100),delta_color='inverse')
        Dibujar_Evolutivo(sectores_interf,vendor_filter,tech_filter,band_filter,week_filter,type_filter,kpi1,kpi2,kpi3,kpi4)

def Dibujar_Evolutivo(sectores_interf,vendor_filter,tech_filter,band_filter,week_filter,type_filter,kpi1,kpi2,kpi3,kpi4):
    if vendor_filter!='Todas':
        sectores_interf = sectores_interf[sectores_interf['PROVEEDOR']==vendor_filter]
    if tech_filter!='Todas':
        sectores_interf = sectores_interf[sectores_interf['TECNOLOGIA']==tech_filter]
    if band_filter!='Todas':
        sectores_interf = sectores_interf[sectores_interf['BANDA']==band_filter]
    if type_filter!='Todas':
        sectores_interf = sectores_interf[sectores_interf['TIPO_INTER']==type_filter]
    d = sectores_interf.groupby(['FECHA', 'TIPO'])['CODIGO_SECTOR_BANDA'].count().reset_index(name='count')
    d = d.pivot(index=['FECHA'], columns='TIPO',values=['count'])
    d.columns = d.columns.droplevel()
    d = d.rename_axis(None,axis=1).reset_index()
    #d = d.set_index('FECHA', drop=True)
    #st.dataframe(d)
    with kpi1:
        fig_line = px.line(d,
                           x='FECHA',
                           y='Critico',height=300,
                           labels={'FECHA': 'Date', 'Critico': 'Num_Sectores'})
        fig_line.update_traces(line_color='OrangeRed')
        fig_line.update_layout(title_text='Evolutivo Critico',title_x=0.5)
        fig_line.update_layout(xaxis=dict(showgrid=False),
                              yaxis=dict(showgrid=False))
        
        
        st.plotly_chart(fig_line, theme="streamlit", use_container_width=True)
    with kpi2:
        fig_line = px.line(d,
                           x='FECHA',
                           y='Alta',height=300,
                           labels={'FECHA': 'Date', 'Alta': 'Num_Sectores'})
        fig_line.update_traces(line_color='DarkOrange')
        fig_line.update_layout(xaxis=dict(showgrid=False),
                              yaxis=dict(showgrid=False))
        fig_line.update_layout(title_text='Evolutivo Alta',title_x=0.5)
        st.plotly_chart(fig_line, theme="streamlit", use_container_width=True)
    with kpi3:
        fig_line = px.line(d,
                           x='FECHA',
                           y='Medio',height=300,
                           labels={'FECHA': 'Date', 'Medio': 'Num_Sectores'})
        fig_line.update_traces(line_color='Gold')
        fig_line.update_layout(xaxis=dict(showgrid=False),
                              yaxis=dict(showgrid=False))
        fig_line.update_layout(title_text='Evolutivo Medio',title_x=0.5)
        st.plotly_chart(fig_line, theme="streamlit", use_container_width=True)
    with kpi4:
        fig_line = px.line(d,
                           x='FECHA',
                           y='Baja',height=300,
                           labels={'FECHA': 'Date', 'Baja': 'Num_Sectores'})
        fig_line.update_traces(line_color='Cyan')
        fig_line.update_layout(xaxis=dict(showgrid=False),
                              yaxis=dict(showgrid=False))
        fig_line.update_layout(title_text='Evolutivo Baja',title_x=0.5)
        st.plotly_chart(fig_line, theme="streamlit", use_container_width=True)
        


#lectura de archivos para files procesados_sectores
dir_days = dir_now / 'Prueba'
#all_dirs = glob.glob(str(all_dirs))
all_dirs = os.listdir(dir_days)


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
sectores_interf.sort_values(by='FECHA',inplace=True,ascending=False,ignore_index=True)

regiones = {'REGION_NORTE': ['ANCASH','CAJAMARCA','LA LIBERTAD','LAMBAYEQUE','LORETO','PIURA','SAN MARTIN','TUMBES','AMAZONAS'],
    'REGION_CENTRO': ['APURIMAC','AYACUCHO','HUANCAVELICA','HUANUCO','JUNIN','PASCO','UCAYALI'],
    'REGION_SUR': ['AREQUIPA','CUSCO','ICA','MADRE DE DIOS','MOQUEGUA','PUNO','TACNA'],
    'LIMA': ['LIMA']}



def ReturnRegion(dpto):
    for key in regiones:
        if dpto in regiones[key]:
            return key
    return None
  
#Agregamos columna REGIONAL
sectores_interf['REGIONAL'] = sectores_interf['DEPARTAMENTO'].apply(lambda row: ReturnRegion(row))
# streamlit run app.py



header = st.container()
#filters = st.container()
#kpis = st.container()
#kpis_HxH = st.container()





with header:
    st.title('Dashboard Interferencias Perú v2')
    st.caption('Dashboard para seguimiento de interferencias en Peru.')

tab1, tab2 = st.tabs(["Seguimiento de Interferencia", "Análisis HxH"])

with tab1:
    filters = st.container()
    kpis = st.container()
with tab2:
    kpis_HxH = st.container()
    
    
with filters:
    st.subheader('Seleccione Fecha - Proveedor - Banda y Tecnología')
    # top level filters
    filter_1, filter_2, filter_3, filter_4,filter_5 = st.columns(5)
    week_filter = filter_1.selectbox('Fechas', pd.unique(sectores_interf['FECHA']))
    vendor_filter = filter_2.selectbox('Proveedor', np.append('Todas', pd.unique(sectores_interf['PROVEEDOR'])))
    band_filter =  filter_3.selectbox('Banda', np.append('Todas', pd.unique(sectores_interf.query('PROVEEDOR==@vendor_filter')['BANDA'])))
    tech_filter = filter_4.selectbox('Tecnología', np.append('Todas', pd.unique(sectores_interf['TECNOLOGIA'])))
    type_filter = filter_5.selectbox('Tipos de Interferencia',['Todas','CATV','PIM','RADIO','REPETIDOR'])
    
with kpis:
    totales = sectores_interf.copy()
    fechas_totales = pd.unique(sectores_interf['FECHA'])
    fecha_ant=''
    totales_ant = sectores_interf.copy()
    if week_filter != 'Todas':
        totales = totales[totales['FECHA'] == week_filter]
        if fechas_totales[-1]!=week_filter:
            fecha_ant = fechas_totales[np.where(fechas_totales < week_filter)[0][0]]
            totales_ant = totales_ant[totales_ant['FECHA'] == fecha_ant]
    if tech_filter != 'Todas':
        totales = totales[totales['TECNOLOGIA'] == tech_filter]
        if fechas_totales[-1]!=week_filter:
            totales_ant = totales_ant[totales_ant['TECNOLOGIA'] == tech_filter]
    if vendor_filter != 'Todas':
        proveedor = vendor_filter
        totales = totales[totales['PROVEEDOR'] == proveedor]
        if fechas_totales[-1]!=week_filter:
            totales_ant = totales_ant[totales_ant['PROVEEDOR'] == proveedor]
        #st.dataframe(totales)
    if band_filter != 'Todas':
        banda = band_filter
        totales = totales[totales['BANDA'] == banda]
        if fechas_totales[-1]!=week_filter:
            totales_ant = totales_ant[totales_ant['BANDA'] == banda]
    if type_filter != 'Todas':
        tipo_interferencia = type_filter
        totales = totales[(totales['TIPO_INTER'] == tipo_interferencia)]
        if fechas_totales[-1]!=week_filter:
            totales_ant = totales_ant[totales_ant['TIPO_INTER'] == tipo_interferencia]
    if totales.shape[0]==0:
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        kpi1.metric('Critico', 0)
        kpi2.metric('Alta', 0)
        kpi3.metric('Medio', 0)
        kpi4.metric('Baja', 0)
        Dibujar_Evolutivo(totales,kpi1,kpi2,kpi3,kpi4)
        
    else:
        Mostrar_Kpis(totales,week_filter,tech_filter,band_filter,vendor_filter,type_filter,fecha_ant,totales_ant,sectores_interf)
    
    
    #-----------------------------------------Inicio de los Gráficos por Departamento------------------------------------#    
    #with st.expander("Gráfico de los Departamentos"):
    st.subheader('Interferencias por Departamento según Proveedor: {} - Banda: {}'.format(vendor_filter,band_filter))
    df_dep = totales.groupby(['DEPARTAMENTO','TIPO'])[['CODIGO_SECTOR_BANDA']].count()
    df_dep.sort_values('CODIGO_SECTOR_BANDA',ascending=False,inplace=True)
    df_dep.reset_index(inplace=True)
    #st.dataframe(df_dep)
    fig_bars = px.bar(
            df_dep,
            x='DEPARTAMENTO',
            y='CODIGO_SECTOR_BANDA',
            color='TIPO',
            orientation='v',
            barmode='relative',
            labels={'CODIGO_SECTOR_BANDA': 'Num_Sector', 'DEPARTAMENTO': 'Departamento'},
            color_discrete_map={'Critico': 'OrangeRed', 'Alta': 'DarkOrange', 'Medio': 'Gold','Baja':'Cyan'},
            template='plotly_white',
            text_auto=True)  # 'ggplot2', 'seaborn', 'simple_white', 'plotly', 'plotly_white'
    fig_bars.update_layout(xaxis=dict(showgrid=False),
                          yaxis=dict(showgrid=False))
    st.plotly_chart(fig_bars, theme="streamlit", use_container_width=True)
    #-----------------------------------------Inicio de los Gráficos por Distrito Según Provincia ------------------------------------#    
    st.subheader('Interferencias por Provincia según Proveedor: {} - Banda: {}'.format(vendor_filter,band_filter))
    df_prov = totales.groupby(['PROVINCIA','TIPO'])[['CODIGO_SECTOR_BANDA']].count()
    df_prov.sort_values('CODIGO_SECTOR_BANDA',ascending=False,inplace=True)
    #st.dataframe(df_dist)
    df_prov.reset_index(inplace=True)
    #st.dataframe(df_dep)
    fig_bars = px.bar(
            df_prov,
            x='PROVINCIA',
            y='CODIGO_SECTOR_BANDA',
            color='TIPO',
            orientation='v',
            barmode='relative',
            labels={'CODIGO_SECTOR_BANDA': 'Num_Sector', 'PROVINCIA': 'Provincia'},
            color_discrete_map={'Critico': 'OrangeRed', 'Alta': 'DarkOrange', 'Medio': 'Gold','Baja':'Cyan'},
            template='plotly_white',
            text_auto=True)  # 'ggplot2', 'seaborn', 'simple_white', 'plotly', 'plotly_white'
    fig_bars.update_layout(xaxis=dict(showgrid=False),
                          yaxis=dict(showgrid=False))
    st.plotly_chart(fig_bars, theme="streamlit", use_container_width=True)
    
    #-----------------------------------------Inicio de los Gráficos por Distrito Según Distrito ------------------------------------#    
    st.subheader('Interferencias por Distrito según Proveedor: {} - Banda: {}'.format(vendor_filter,band_filter))
    df_dist = totales.groupby(['DISTRITO','TIPO'])[['CODIGO_SECTOR_BANDA']].count()
    df_dist.sort_values('CODIGO_SECTOR_BANDA',ascending=False,inplace=True)
    #st.dataframe(df_dist)
    df_dist.reset_index(inplace=True)
    #st.dataframe(df_dep)
    fig_bars = px.bar(
            df_dist,
            x='DISTRITO',
            y='CODIGO_SECTOR_BANDA',
            color='TIPO',
            orientation='v',
            barmode='relative',
            labels={'CODIGO_SECTOR_BANDA': 'Num_Sector', 'DISTRITO': 'Distrito'},
            color_discrete_map={'Critico': 'OrangeRed', 'Alta': 'DarkOrange', 'Medio': 'Gold','Baja':'Cyan'},
            template='plotly_white',
            text_auto=True)  # 'ggplot2', 'seaborn', 'simple_white', 'plotly', 'plotly_white'
    fig_bars.update_layout(xaxis=dict(showgrid=False),
                          yaxis=dict(showgrid=False))
    st.plotly_chart(fig_bars, theme="streamlit", use_container_width=True)
    #-----------------------------------------Inicio de los Gráficos por Sector------------------------------------#
    #with st.expander("Gráfico de los Sectores"):
    st.subheader('Interferencias por Sectores según Proveedor: {} - Banda: {}'.format(vendor_filter,band_filter))
    df_reg = totales.groupby(['REGIONAL','TIPO'])[['CODIGO_SECTOR_BANDA']].count()
    df_reg.sort_values('CODIGO_SECTOR_BANDA',ascending=False,inplace=True)
    df_reg.reset_index(inplace=True)
    #st.dataframe(df_dep)
    fig_bars = px.bar(
            df_reg,
            x='REGIONAL',
            y='CODIGO_SECTOR_BANDA',
            color='TIPO',
            orientation='v',
            barmode='relative',
            labels={'CODIGO_SECTOR_BANDA': 'Num_Sector', 'REGIONAL': 'Region'},
            color_discrete_map={'Critico': 'OrangeRed', 'Alta': 'DarkOrange', 'Medio': 'Gold','Baja':'Cyan'},
            template='plotly_white',
            text_auto=True)  # 'ggplot2', 'seaborn', 'simple_white', 'plotly', 'plotly_white'
    fig_bars.update_layout(xaxis=dict(showgrid=False),
                          yaxis=dict(showgrid=False))
    st.plotly_chart(fig_bars, theme="streamlit", use_container_width=True)
    
    #-----------------------------------------Inicio de la Tabla y Descargar File por Interferencia------------------------------------#
    #with st.expander("Tabla de Interferencia "):
    filter_5, filter_6 = st.columns(2)
    reg_filter = filter_5.selectbox('Region', np.append('Todas', sorted(pd.unique(sectores_interf['REGIONAL']))))
    dep_filter = filter_6.selectbox('Departamento', np.append('Todas', sorted(pd.unique(totales['DEPARTAMENTO']))))
    st.subheader('Interferencias por Bandas según Fecha: {} - Region: {} - Departamento: {}'.format(week_filter,reg_filter,dep_filter))
    
    totales_regdep = totales.copy()
    if reg_filter != 'Todas':
        totales_regdep = totales_regdep[totales_regdep['REGIONAL'] == reg_filter]
    if dep_filter != 'Todas':
        totales_regdep = totales_regdep[totales_regdep['DEPARTAMENTO'] == dep_filter]
    #-------------------------------------Grafico---------------------------------------------------------#
    df_banda_tipo = (totales_regdep.groupby(by=['BANDA','TIPO']).count().reset_index())[['BANDA','TIPO','CODIGO_SECTOR_BANDA']]
    df_banda_tipo.sort_values('CODIGO_SECTOR_BANDA',ascending=False,inplace=True)
    df_banda_tipo.reset_index(inplace=True)
    fig_bars = px.bar(
            df_banda_tipo,
            x='BANDA',
            y='CODIGO_SECTOR_BANDA',
            color='TIPO',
            orientation='v',
            barmode='relative',
            labels={'CODIGO_SECTOR_BANDA': 'Num_Sector', 'REGIONAL': 'Region'},
            color_discrete_map={'Critico': 'OrangeRed', 'Alta': 'DarkOrange', 'Medio': 'Gold','Baja':'Cyan'},
            template='plotly_white',
            text_auto=True)  # 'ggplot2', 'seaborn', 'simple_white', 'plotly', 'plotly_white'
    fig_bars.update_layout(xaxis=dict(showgrid=False),
                          yaxis=dict(showgrid=False))
    st.plotly_chart(fig_bars, theme="streamlit", use_container_width=True)
    
    
    
with kpis_HxH:
    #Inicio para la descarga del CSV - Filtrado por departamento
    @st.cache
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv(index=False).encode('utf-8')
    
    my_large_df = totales_regdep.sort_values(by='AVG_PRB',ascending=False)
    csv = convert_df(my_large_df)
    if dep_filter!='Todas':
        label_document = 'Download data as CSV de la fecha:\n {} y departamento:\n {}'.format(week_filter,dep_filter)
        fecha_file = pd.to_datetime(week_filter).strftime('%d%m%Y')
        name_file = '{}_{}_{}.csv'.format(dep_filter,vendor_filter,fecha_file)
    else:
        label_document = 'Download data as CSV de la fecha {}'.format(week_filter)
        fecha_file = pd.to_datetime(week_filter).strftime('%d%m%Y')
        name_file = '{}_{}_{}.csv'.format('Todas',vendor_filter,fecha_file)
    st.subheader("Descargar Archivo csv")
    st.download_button(
        label=label_document,
        data=csv,
        file_name=name_file,
        mime='text/csv',
        )
    st.dataframe(totales_regdep.sort_values(by='AVG_PRB',ascending=False),use_container_width=True)
    
    col_vendor, col_banda, col_ebc, col_sector,col_tipo,col_avg_prb = st.columns(6)
    filter_vendor = col_vendor.selectbox('VENDOR', sorted(pd.unique(totales_regdep['PROVEEDOR'])))
    filter_banda = col_banda.selectbox('BANDA', sorted(pd.unique(totales_regdep.query('PROVEEDOR==@filter_vendor')['BANDA'])))
    filter_ebc = col_ebc.selectbox('NOMBRE_EBC',sorted(pd.unique(totales_regdep.query('BANDA==@filter_banda&PROVEEDOR==@filter_vendor')['NOMBRE_EBC'])))
    filter_sector = col_sector.selectbox('SECTOR',sorted(pd.unique(totales_regdep.query('BANDA==@filter_banda&NOMBRE_EBC==@filter_ebc')['SECTOR'])))    
    col_tipo.text_input(label='TIPO',disabled=True,value=str(totales_regdep.query('BANDA==@filter_banda&NOMBRE_EBC==@filter_ebc&SECTOR==@filter_sector')['TIPO'].iloc[0]))
    col_avg_prb.number_input(label='AVG_PRB',disabled=True,value=totales_regdep.query('BANDA==@filter_banda&NOMBRE_EBC==@filter_ebc&SECTOR==@filter_sector')['AVG_PRB'].iloc[0])
    dir_hxh = dir_days / '{}'.format(filter_vendor) / '{}'.format(pd.to_datetime(week_filter).strftime('%d%m%y')) / '{}_HXH_{}.csv'.format(filter_vendor,pd.to_datetime(week_filter).strftime('%d%m%y'))
    sector_hxh = pd.read_csv(dir_hxh,dtype={'SECTOR':'str','CODIGO_SECTOR_BANDA':'str','BANDA':'str'})
    ebc_interferido =    sector_hxh.query('BANDA==@filter_banda&NOMBRE_EBC==@filter_ebc&SECTOR==@filter_sector')
    
    
    dic_banda = {'AWS':100,
                 'B700':75,
                 '1900':50,
                 'AWS_E':100,
                 'B900':25,
                 'B700_E':75}  
    list_prbs = []
    for i in range(0,dic_banda[filter_banda]):
        list_prbs.append('PRB'+str(i))
    
    
    
    df_prbs = ebc_interferido[list_prbs]
    
    
    #list_prbs.reverse()
    
    with st.expander("Tabla de PRBs HxH {} Sector {} y Banda {}".format(filter_ebc,filter_sector,filter_banda)):
        st.dataframe(ebc_interferido.style.format(subset=list_prbs,formatter="{:.0f}"))
        
    st.subheader('Grafico 3D - Surface')
    fig_surf = go.Figure(data=[go.Surface(z=df_prbs,
                                          cmin=-120,
                                          cmax=-90 ,
                                          x=list_prbs, 
                                          y=pd.to_datetime(ebc_interferido['FECHA']),
                                          colorscale =px.colors.diverging.RdYlGn_r,
                                          surfacecolor=df_prbs)])
    fig_surf.update_layout(title='{} Sector {} y Banda {}'.format(filter_ebc,filter_sector,filter_banda),
             autosize=True,margin=dict(l=65, r=70, b=65, t=90),
             width=100, height=800)
    st.plotly_chart(fig_surf, theme="streamlit", use_container_width=True)
    

    st.subheader('Grafica 2D - Spectrograma')    
    #list_prbs.reverse()
    fig = go.Figure().set_subplots(rows=1, cols=1)
    fig.add_trace(go.Heatmap(x=list_prbs, y=ebc_interferido['FECHA'], z=df_prbs, coloraxis="coloraxis"), row=1, col=1)
    fig.update_layout(title='{} Sector {} y Banda {}'.format(filter_ebc,filter_sector,filter_banda),height=900,coloraxis=dict(colorscale=px.colors.diverging.RdYlGn_r, cmin=-120, cmid=-105, cmax= -90))
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
        
        

