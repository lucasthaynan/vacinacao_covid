#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import basedosdados as bd
import pandas as pd 
import plotly.express as px
import numpy as np

pd.set_option('display.max_columns', 500) # ampliar o limite de exibição das colunas para 500


# In[ ]:


consulta_nordeste = """
SELECT
sigla_uf,
nome_fabricante_vacina,
data_aplicacao_vacina,
dose_vacina

FROM basedosdados.br_ms_vacinacao_covid19.microdados

WHERE sigla_uf in ('AL', 'PE', 'SE', 'MA', 'PI', 'CE', 'RN', 'PB', 'BA')


"""

df_consulta_nordeste = bd.read_sql(consulta_nordeste, billing_project_id="dadostatu")


# In[315]:


df_consulta_nordeste.info()


# In[316]:


df_consulta_nordeste.head()


# In[319]:


df = df_consulta_nordeste


# In[320]:


df = df.replace(to_replace ="ASTRAZENECA/FIOCRUZ", value ="AstraZeneca")
df = df.replace(to_replace ="ASTRAZENECA", value ="AstraZeneca")
df = df.replace(to_replace ="SINOVAC/BUTANTAN", value ="Coronavac")
df = df.replace(to_replace ="JANSSEN", value ="Janssen")
df = df.replace(to_replace ="PFIZER", value ="Pfizer")


# In[321]:


df['nome_fabricante_vacina'].unique()


# In[ ]:


df_uf = df.groupby(['sigla_uf', 'nome_fabricante_vacina', 'dose_vacina', 'data_aplicacao_vacina']).agg({'sigla_uf': 'count'})


# In[324]:


df_uf = df_uf.rename(columns={'sigla_uf': 'total_doses'})
df_uf.head()


# In[326]:


df_uf.sum()


# In[327]:


df_uf = df_uf.reset_index()


# In[328]:


df_uf.head()


# #### vacinas com data de vacinação anterior a 17 de janeiro de 2021

# In[329]:


df_uf.query('data_aplicacao_vacina < 20210117').head(10)


# #### filtrando dados com da de vacinação após 16 de janeiro de 2021

# In[141]:


dado_filtros = dados.query('data_aplicacao_vacina > 20210116')


# In[168]:


dado_filtros.head()


# ### exportando gráfico e gerando embed

# In[172]:


import chart_studio
import chart_studio.plotly as py
import chart_studio.tools as tls 


# In[307]:


username = 'USERNAME' # your username
api_key = 'API_PLOTLY' # your api key - go to profile > settings > regenerate key

chart_studio.tools.set_credentials_file(username=username, api_key=api_key)


# ### gerando gráficos da evolução da vacina por UF

# In[308]:


lista_links_graficos = []

for uf in dados.sigla_uf.unique():
    if uf == 'AL':
        nome_uf = "Alagoas"
    if uf == 'PE':
        nome_uf = "Pernambuco"
    if uf == 'BA':
        nome_uf = "Bahia"
    if uf == 'SE':
        nome_uf = "Sergipe"
    if uf == 'RN':
        nome_uf = "Rio Grande do Norte"
    if uf == 'MA':
        nome_uf = "Maranhão"
    if uf == 'CE':
        nome_uf = "Ceará"
    if uf == 'PI':
        nome_uf = "Piauí"
    if uf == 'PB':
        nome_uf = "Paraíba"
   
    titulo = f"<b>1º ano da vacinação contra a Covid-19 ({nome_uf})</b>"
    grafico_uf = px.histogram(dado_filtros.query(f'sigla_uf =="{uf}"'), x = "data_aplicacao_vacina", y = "total_doses",
                             color = "dose_vacina",
                             nbins=52, # o gráfico mostrará 52 colunas (total de semanas de um ano)
                              marginal="rug", # exibe o gráfico superior
                              color_discrete_map={
                             "1ª Dose": "#00CC96",
                             "2ª Dose": "#EF553B",
                             "3ª Dose": "#AB63FA",
                             "Dose Única": "#F9C023",
                             "Reforço": "#19D3F3",
                             "Dose Adicional": "#FFA15A",
                              "Única": "#B6E880"},
                              hover_name = "dose_vacina",
                             title=f"<b>1º ano da vacinação contra a Covid-19 ({nome_uf})</b>")
    
    grafico_uf.update_layout(xaxis_title="Data da aplicação", yaxis_title="Total de doses por semana", legend_title="Doses:")
    grafico_uf.update_layout(title_font=dict(size=20))
    grafico_uf.update_traces(hovertemplate='Período: %{x} <br><b>Total de doses: %{y} </b>') # inserir tootip com valor

    # publicando gráfico no Plotly e gerando link
    link_plotly = py.plot(grafico_uf, filename = f"1º ano da vacinação contra a Covid-19 ({nome_uf})", auto_open=False) 
    
    # gerando embed do gráfico
    embed_grafico = tls.get_embed(link_plotly) # 
    
    lista_links_graficos.append({"uf": nome_uf,
                                 "link_grafico": link_plotly,
                                 "cod_embed": embed_grafico,
                                 "cod_embed_sem_modebar": f'<iframe width="900" height="500" frameborder="0" scrolling="no" src="{link_plotly}.embed?autosize=true&modebar=false"></iframe>'
                                })
    
    grafico_uf.show()


# In[309]:


links = pd.DataFrame(lista_links_graficos)
links


# In[310]:


links.to_csv('graficos_vacinacao_NE.csv')


# ### gráficos por vacina

# In[245]:


dados_vacinas_uf = dado_filtros.groupby(['sigla_uf', 'nome_fabricante_vacina']).agg({"total_doses": "sum"})


# In[247]:


dados_vacinas_uf = dados_vacinas_uf.reset_index()


# In[248]:


dados_vacinas_uf.head()


# In[311]:


lista_links_graficos2 = []

for uf in dados_vacinas_uf.sigla_uf.unique():
    if uf == 'AL':
        nome_uf = "Alagoas"
    if uf == 'PE':
        nome_uf = "Pernambuco"
    if uf == 'BA':
        nome_uf = "Bahia"
    if uf == 'SE':
        nome_uf = "Sergipe"
    if uf == 'RN':
        nome_uf = "Rio Grande do Norte"
    if uf == 'MA':
        nome_uf = "Maranhão"
    if uf == 'CE':
        nome_uf = "Ceará"
    if uf == 'PI':
        nome_uf = "Piauí"
    if uf == 'PB':
        nome_uf = "Paraíba"
   #px.bar(dose1_perc, y=np.full(len(dose1_perc), "first dose"), x="Percentual (%)", color=dose1_perc.index, orientation="h")
    #nome_uf = dado_filtros.query(f'sigla_uf =="{uf}"')
    titulo = f"<b>1º ano da vacinação contra a Covid-19 ({nome_uf})</b>"
    grafico_fabricante_uf = px.bar(dados_vacinas_uf.query(f'sigla_uf =="{uf}"'), x = "nome_fabricante_vacina", 
                        y="total_doses", 
                        #color=dados_vacinas_uf.index, orientation="h",
                        color = "nome_fabricante_vacina",
                        color_discrete_map={
                             "AstraZeneca": "#00CC96",
                             "Coronavac": "#EF553B",
                             "Pfizer": "#AB63FA",
                             "Janssen": "#F9C023"},
                            # nbins=1,
                      hover_name = "nome_fabricante_vacina",
                     title=f"<b>Volume de doses aplicadas por fabricante ({nome_uf})</b>")
    
    grafico_fabricante_uf.update_layout(xaxis_title="Fabricante", yaxis_title="Total de doses", legend_title="Fabricante")
    grafico_fabricante_uf.update_layout(title_font=dict(size=20))
    grafico_fabricante_uf.update_traces(hovertemplate='Fabricante: %{x} <br><b>Total de doses: %{y} </b>') # inserir tootip com valor

    
    link_plotly = py.plot(grafico_fabricante_uf, filename = f"Volume de doses aplicadas por fabricante ({nome_uf})", auto_open=False)
    embed_grafico = tls.get_embed(link_plotly)
    lista_links_graficos2.append({"uf": nome_uf,
                                 "link_grafico": link_plotly,
                                 "cod_embed": embed_grafico,
                                 "cod_embed_sem_modebar": f'<iframe width="900" height="500" frameborder="0" scrolling="no" src="{link_plotly}.embed?autosize=true&modebar=false"></iframe>'                                 
                                 })
    #print(nome_uf)
    #print(link_plotly)
    #print(embed_grafico)
    grafico_fabricante_uf.show(config= {'displayModeBar': False})


# In[313]:


links2 = pd.DataFrame(lista_links_graficos2)
links2


# In[314]:


links2.to_csv('graficos_vacinacao_fabricante_NE.csv')


# ### Dados por município

# In[167]:


consulta_ibge = """
SELECT *

FROM basedosdados.br_bd_diretorios_brasil.municipio


"""

df_consulta_ibge = bd.read_sql(consulta_ibge, billing_project_id="dadostatu")


# In[168]:


df_consulta_ibge.head()


# Analisando os municípios de Alagoas

# In[159]:


df_municipio = df_vacinacao.groupby(['id_municipio_estabelecimento', 'dose_vacina']).agg({'id_paciente': 'count'})


# In[171]:


df_municipio.head()


# In[184]:


df_municipio = df_municipio.reset_index()
df_municipio.head()


# In[173]:


dados = df_municipio.merge(df_consulta_ibge, how = 'left', left_on = "id_municipio_estabelecimento", right_on = "id_municipio")
dados = dados[['nome', 'id_municipio_estabelecimento', 'id_municipio','dose_vacina', 'id_paciente']]
dados = dados.rename(columns={'id_paciente': 'total_doses'})


# In[161]:


df_municipio.query('id_municipio_estabelecimento == "2704302"')


# In[162]:


# doses totais aplicadas em Maceió
df_municipio.query('id_municipio_estabelecimento == "2704302"').sum()


# ### dados Alagoas

# In[207]:


df = df_vacinacao[['nome_fabricante_vacina','data_aplicacao_vacina', 'lote_vacina', 'dose_vacina']]
df.head(5)


# In[186]:


df['nome_fabricante_vacina'].unique()


# In[187]:


df = df.replace(to_replace ="ASTRAZENECA/FIOCRUZ", value ="AstraZeneca")
df = df.replace(to_replace ="ASTRAZENECA", value ="AstraZeneca")
df = df.replace(to_replace ="SINOVAC/BUTANTAN", value ="Coronavac")
df = df.replace(to_replace ="JANSSEN", value ="Janssen")
df = df.replace(to_replace ="PFIZER", value ="Pfizer")


# In[188]:


df.sort_values("nome_fabricante_vacina", ascending=False).head()


# In[189]:


df = df.groupby(['nome_fabricante_vacina', 'dose_vacina', 'data_aplicacao_vacina']).count()
df = df.reset_index()
df = df.rename(columns={'lote_vacina': 'doses_totais'})
df.sort_values('data_aplicacao_vacina').head()


# In[190]:





# In[192]:


df.sort_values('data_aplicacao_vacina').head()


# In[193]:


df.data_aplicacao_vacina = df.data_aplicacao_vacina.astype(str)


# In[194]:


df.info()


# In[ ]:





# In[195]:


df.groupby('dose_vacina').sum()


# In[196]:


df.dose_vacina.unique()


# In[201]:


grafico_1 = px.histogram(df.query('dose_vacina == "1ª Dose"'), x = "data_aplicacao_vacina", y = "doses_totais",
                         color = "nome_fabricante_vacina",
                         nbins=52,
                         color_discrete_map={
                             "AstraZeneca": "#00CC96",
                             "Coronavac": "#EF553B",
                             "Pfizer": "#AB63FA"},
                         title="Aplicação diária da <b>1ª dose</b>, em Alagoas",
                         hover_name="nome_fabricante_vacina", hover_data=["nome_fabricante_vacina"])

grafico_1.show()


# In[202]:


grafico_1 = px.histogram(df.query('dose_vacina == "1ª Dose"'), x = "data_aplicacao_vacina", y = "doses_totais",
                         color = "nome_fabricante_vacina",
                         nbins=52,
                         color_discrete_map={
                             "AstraZeneca": "#00CC96",
                             "Coronavac": "#EF553B",
                             "Pfizer": "#AB63FA"},
                         title="Aplicação diária da <b>1ª dose</b>, em Alagoas",
                         hover_name="nome_fabricante_vacina", hover_data=["nome_fabricante_vacina"])

grafico_1.show()


# In[203]:


grafico_1 = px.histogram(df.query('dose_vacina == "2ª Dose" | dose_vacina == "Dose Única"'), x = "data_aplicacao_vacina", y = "doses_totais",
                         color = "nome_fabricante_vacina",
                         nbins=52,
                         color_discrete_map={
                             "AstraZeneca": "#00CC96",
                             "Coronavac": "#EF553B",
                             "Pfizer": "#AB63FA",
                             "Janssen": "#F9C023"},
                         title="Aplicação diária da <b>2ª dose ou dose única</b>, em Alagoas",
                         hover_name="nome_fabricante_vacina", hover_data=["nome_fabricante_vacina"])

grafico_1.show()


# In[204]:


grafico_1 = px.histogram(df.query('dose_vacina == "Reforço"'), x = "data_aplicacao_vacina", y = "doses_totais",
                         color = "nome_fabricante_vacina",
                         nbins=52,
                         color_discrete_map={
                             "AstraZeneca": "#00CC96",
                             "Coronavac": "#EF553B",
                             "Pfizer": "#AB63FA",
                             "Janssen": "#F9C023"},
                         title="Aplicação da <b>dose de reforço</b>, em Alagoas",
                         hover_name="nome_fabricante_vacina", hover_data=["nome_fabricante_vacina"])

grafico_1.show()


# ### teste

# In[126]:


grafico_2 = px.histogram(dados.query('sigla_uf =="AL"'), x = "data_aplicacao_vacina", y = "total_doses",
                         color = "dose_vacina",
                         nbins=52,
                         title="Aplicação da <b>dose de reforço</b>, em Alagoas")

grafico_2.show()


# In[122]:


dados.dose_vacina.unique()


# In[127]:


dados.groupby('dose_vacina').sum()


# In[145]:


dado_filtros = dados.query("dose_vacina == ['1ª Dose', '2ª Dose','Dose Adicional', 'Reforço', 'Dose Única', '3ª Dose', '4ª Dose', 'Única']")
dado_filtros.head()


# In[ ]:




