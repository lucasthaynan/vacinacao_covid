# Vacinação em Alagoas
Script que estrutura os dados de vacinação contra a Covid-19 no Brasil, [diponibilizados no OpenData SUS](https://opendatasus.saude.gov.br/dataset/covid-19-vacinacao), e organiza as informações por dia ou semana, tipo de vacina ou tipo de dose, por um estado específico ou mais.
# Dados
Os dados coletados são de 17 de janeiro a 14 de janeiro de 2022 e estão disponíveis em arquivos separados por UF.
  * [Acessar dados em .csv](https://opendatasus.saude.gov.br/dataset/covid-19-vacinacao/resource/301983f2-aa50-4977-8fec-cfab0806cb0b)
  * [Dicionário dos dados](https://opendatasus.saude.gov.br/dataset/covid-19-vacinacao/resource/a8308b58-8898-4c6d-8119-400c722c71b5)

Para esta análise não foram levados em conta possíveis atrasos no registro realizado pelos municípios no sistema de informações do PNI (Programa Nacional de Imunizações).
# Visualizações
Com a biblioteca `plotly` foram gerados os gráficos com a evolução diária da vacinação por estado estado.

Veja a [reportagem completa](https://www.agenciatatu.com.br/noticia/veja-a-evolucao-diaria-da-vacinacao-contra-a-covid-19-em-al/).
