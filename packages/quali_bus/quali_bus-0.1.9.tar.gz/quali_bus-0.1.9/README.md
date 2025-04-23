# 📊 Indicadores IQT - Biblioteca para Avaliação da Qualidade do Transporte Público

Esta biblioteca tem como objetivo automatizar o cálculo do **Índice de Qualidade do Transporte (IQT)**, baseado nos critérios estabelecidos no artigo **"MESTRADO INDICADOR DE QUALIDADE PARA AVALIAR TRANSPORTE COLETIVO URBANO"**. O IQT é uma métrica essencial para a análise e otimização do transporte público, considerando fatores como pontualidade, frequência de atendimento, cumprimento de itinerários e infraestrutura.

---

## 🚀 Como Usar

🔹 1. Importação da Biblioteca

```python
from quali_bus import CalcularIndicadores, MapaIQT
```

🔹 2. Inicializando a Classe

```python
calc = CalcularIndicadores()
```

🔹 3. Carregando os Dados das Linhas de Ônibus

Os dados podem ser carregados a partir de um `pandas.DataFrame` ou `geopandas.GeoDataFrame`:

```python
import pandas as pd
import geopandas as gpd
from shapely.geometry import LineString

# Exemplo de dados fictícios de linhas de ônibus
linhas_df = gpd.GeoDataFrame({
    'id_linha': ['101', '102'],
    'geometria_linha': [LineString([(0, 0), (1, 1), (2, 2)]), LineString([(3, 3), (4, 4), (5, 5)])]
})

frequencia_df = pd.DataFrame({
    'id_linha': ['101', '102'],
    'horario_inicio_jornada': ['06:07:57', '06:07:57'],
    'horario_fim_jornada': ['06:57:51', '06:57:57'],
    'data_jornada': ['01/01/2024', '01/01/2024'],
    'sentido_viagem': ['0', '1'],
    'quantidade_passageiros': ['3', '8'],
})

pontualidade_df = pd.DataFrame({
    'id_linha': ['101', '102'],
    'data_viagem': ['01/01/2024', '01/01/2024'],
    'sentido_viagem': ['0', '1'],
    'partida_planejada': ['06:07:00', '06:07:00'],
    'partida_real': ['06:07:57', '06:07:57'],
    'chegada_planejada': ['06:57:00', '06:57:00'],
    'chegada_real': ['06:57:57', '06:57:57'],
    'km_executado': ['31', '16'],
})

# Carregar os dados na classe
calc.carregar_dados(linhas_df, frequencia_df, pontualidade_df)
```

🔹 4. Carregando os Dados dos Pontos (Pontos de Ônibus e Residências)

Os dados podem ser carregados a partir de um `pandas.DataFrame` ou `geopandas.GeoDataFrame`:

```python
import pandas as pd
import geopandas as gpd
from shapely.geometry import LineString

residencias = pd.DataFrame({
    "id": [1, 2, 3]
    "latitude" : [-41.5, -42.521321, -41.21477]
    "longitude" : [-41.5, -42.521321, -41.21477]
})

pontos_de_onibus = pd.DataFrame({
    "id": [1, 2, 3]
    "latitude" : [-41.5, -42.521321, -41.21477]
    "longitude" : [-41.5, -42.521321, -41.21477]
})

# Carregar os dados na classe
calc.carregar_dados_geometrias(pontos_de_onibus, residencias)
```

🔹 5. Cálculo de Indicadores

A biblioteca suporta o cálculo de diversos indicadores de qualidade do transporte, como:

```python
# Essa função classifica cada dado da linha segundo a classificação do IQT
calc.classificar_linha()

# Essa função diz o valor IQT para cada linha
calc.processar_iqt()
```

🔹 6. Criação do Mapa

```python

import geopandas as gpd

gdf_cidade = gdp.read_file(path_shapefile_cidade)

# Criando o objeto do mapa
mapa = iqt.MapaIQT(gdf_cidade)

# Adicionar no mapa as linhas de ônibus já com a classificação IQT

mapa.classificar_rota_grupo(calc.dados_completos)
```

🔹 7. Valores Atribuidos na Classificação

```python

calc.classificao_linhas # DataFrame com os dados clissificados

calc.matriz # DataFrame com os dados calculcados/existentes

```

## Classificação das Linha

| id_linha | I1  | I2  | I3  | I4  | I5  | I6  | I7  | I8  | I9  | I10 |
| -------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 101      | 3   | 2   | 1   | 0   | 0   | 3   | 2   | 3   | 0   | 1   |
| 102      | 3   | 2   | 1   | 0   | 0   | 3   | 2   | 3   | 0   | 1   |

## Dados Calculados

| id_linha | I1  | I2     | I3                                                                                                 | I4  | I5   | I6   | I7   | I8  | I9                                                   | I10                           |
| -------- | --- | ------ | -------------------------------------------------------------------------------------------------- | --- | ---- | ---- | ---- | --- | ---------------------------------------------------- | ----------------------------- |
| 101      | 1   | 148.12 | Integração tarifária temporal ocorre em determinados pontos, apenas com transferências intramodais | 0   | 49.8 | 1.45 | 0.98 | 1   | Possuir informações em site e aplicativo atualizados | Aumento equivalente ao índice |
| 102      | 2   | 111.12 | Integração tarifária temporal ocorre em determinados pontos, apenas com transferências intramodais | 0   | 21.8 | 1.75 | 0.78 | 1   | Possuir informações em site e aplicativo atualizados | Aumento equivalente ao índice |

## 🤝 Contribuindo

### Contribuições são bem-vindas! Para contribuir:

- Fork o repositório.
- Crie uma branch `(feature/nova-funcionalidade)`.
- Faça suas alterações e commit `(git commit -m "Adiciona nova funcionalidade")`.
- Envie um Pull Request.

### 📜 Licença

Este projeto está sob a licença MIT. Consulte o arquivo LICENSE para mais detalhes.
👨‍💻 Autor

Desenvolvido por Yago Maia - GitHub: https://github.com/YagoMaia
