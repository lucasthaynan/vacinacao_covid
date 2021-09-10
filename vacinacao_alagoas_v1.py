#!/usr/bin/env python
# coding: utf-8

# #### Importando e estruturando os dados

# Fonte dos dados: https://opendatasus.saude.gov.br/dataset/covid-19-vacinacao

# In[1]:


import pandas as pd

# lendo o arquivo baixado no Open Data SUS
dados = pd.read_csv("vacinacao_alagoas_09_09_2021.csv", sep=";", encoding='utf-8') 


# In[2]:


dados.head(1)


# #### Filtrar apenas algumas colunas do DataFrame (planilha)

# In[3]:


df = dados[['vacina_nome','vacina_dataaplicacao', 'vacina_descricao_dose']]
df.head(2)


# #### Renomeando descrição das vacinas

# In[4]:


df = df.replace(to_replace ="Vacina Covid-19 - Covishield", value ="AstraZeneca")
df = df.replace(to_replace ="Covid-19-AstraZeneca", value ="AstraZeneca")
df = df.replace(to_replace ="Covid-19-Coronavac-Sinovac/Butantan", value ="Coronavac")
df = df.replace(to_replace ="Vacina covid-19 - Ad26.COV2.S - Janssen-Cilag", value ="Janssen")
df = df.replace(to_replace ="Vacina covid-19 - BNT162b2 - BioNTech/Fosun Pharma/Pfizer", value ="Pfizer")
df.sort_values("vacina_descricao_dose", ascending=False)


# #### Converter unicode "\ xa0" em espaço
# 
# Solução para  isso, o que resolveu o problema erro de filtro (1ª dose, 2ª dose):
# https://stackoverflow.com/questions/10993612/how-to-remove-xa0-from-string-in-python

# In[5]:


df['vacina_descricao_dose'] = df['vacina_descricao_dose'].str.replace('\xa0', ' ')

# ou filtro = df.query("vacina_descricao_dose=='1ª\xa0Dose'") # caso não fosse usado a primeira opção


# #### Agrupar por vacinas

# In[6]:


dados_vacinas = df.groupby(["vacina_nome"]).count()
dados_vacinas.head(5)


# #### Verficando o quantitativo por dose

# In[7]:


doses = df.groupby(["vacina_descricao_dose"]).count()
display(doses)


# #### Filtrando dados apenadas da 1ª dose

# In[8]:


dose1 = df.query("vacina_descricao_dose=='1ª Dose'")
# ou df.loc[df['vacina_descricao_dose'].str.strip() == '1ª Dose']
dose1.head()


# #### Filtrando dados apenas da 2ª dose ou dose única

# In[9]:


dose_jassen = df.loc[df['vacina_descricao_dose'].str.strip() == 'Dose']
dose_2 = df.loc[df['vacina_descricao_dose'].str.strip() == '2ª Dose']


# In[10]:


dose2 = pd.merge(dose_jassen, dose_2, how = 'outer')
dose2


# #### Gerando gráficos

# In[11]:


import plotly.express as px
grafico_1 = px.histogram(dose1, x = "vacina_dataaplicacao", color = "vacina_nome",
                         color_discrete_map={
                             "AstraZeneca": "#00CC96",
                             "Coronavac": "#EF553B",
                             "Pfizer": "#AB63FA"},
                         title="Aplicação diária da 1ª dose, em Alagoas",
                         hover_name="vacina_nome", hover_data=["vacina_descricao_dose"])

grafico_1.show()


# In[12]:


grafico_2 = px.histogram(dose2, x = "vacina_dataaplicacao", color = "vacina_nome",
                         color_discrete_map={
                             "AstraZeneca": "#00CC96",
                             "Coronavac": "#EF553B",
                             "Pfizer": "#AB63FA",   
                             "Janssen": "#F9C023"},
                      title = "Aplicação diária da 2ª dose ou dose única, em Alagoas")
grafico_2.show()


# #### Salvando gráfico em html

# In[27]:


grafico_1.write_html("grafico_doses_1.html")
grafico_2.write_html("grafico_doses_2.html")


# #### Exportando dados da 1ª e 2ª doses

# In[33]:


dose1.head()


# In[34]:


dose1_por_dia = dose1[[
    "vacina_dataaplicacao",
    "vacina_nome",
    "vacina_descricao_dose",]].groupby([
    "vacina_dataaplicacao",
    "vacina_nome"]).count()


# In[70]:


dose1_por_dia.to_csv("dose1_por_dia.csv")


# In[65]:


dose2.head()


# In[66]:


dose2_por_dia = dose2[[
    "vacina_dataaplicacao",
    "vacina_nome",
    "vacina_descricao_dose",]].groupby([
    "vacina_nome",
    "vacina_dataaplicacao"]).count()

dose2_por_dia


# In[67]:


dose2_por_dia.to_csv("dose2_por_dia.csv")


# #### Agrupamento por dia

# In[55]:


dose1_data = dose1.groupby(["vacina_dataaplicacao"]).count()
dose1_data.sort_values("vacina_dataaplicacao", ascending=True)

