# Vacinação em Alagoas
Script que estrutura os dados de vacinação contra a Covid-19 no Brasil, [diponibilizados no OpenData SUS](https://opendatasus.saude.gov.br/dataset/covid-19-vacinacao) e organiza as informações por dia e tipo de vacina, por um estado específico. Neste caso, Alagoas.
# Dados
Os dados coletados são de 17 de janeiro a 07 de setembro de 2021 e estão disponíveis em arquivos separados por UF.
  * [Acessar dados em .csv](https://opendatasus.saude.gov.br/dataset/covid-19-vacinacao/resource/ef3bd0b8-b605-474b-9ae5-c97390c197a8)
  * [Dicionário dos dados](https://opendatasus.saude.gov.br/dataset/covid-19-vacinacao/resource/38ead83d-b115-4219-852e-7244792bc311)

Para esta análise não foram levados em conta possíveis atrasos no registro realizado pelos municípios no sistema de informações do PNI (Programa Nacional de Imunizações).
# Visualizações
Com a biblioteca `plotly` foram gerados os gráficos com a evolução diária da vacinação no estado.

Veja a [reportagem completa](https://www.agenciatatu.com.br/noticia/veja-a-evolucao-diaria-da-vacinacao-contra-a-covid-19-em-al/).
