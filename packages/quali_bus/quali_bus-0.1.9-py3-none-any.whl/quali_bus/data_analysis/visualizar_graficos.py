import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


class Graficos:
	"""Classe para gerar gráficos com seaborn.

	Esta classe fornece métodos para criar diversos tipos de visualizações
	a partir de um DataFrame contendo dados de transporte público, como
	número de passageiros, valores arrecadados e duração de viagens.

	Attributes:
		df (pd.DataFrame): DataFrame contendo os dados de transporte público.
	"""

	def __init__(self, df: pd.DataFrame):
		"""Inicializa a classe Graficos.

		Args:
			df (pd.DataFrame): DataFrame contendo os dados de transporte público.
		"""
		self.df = df.copy()

	def plot_boxplot_passageiros_por_rota(self):
		"""Plota um boxplot da distribuição de passageiros por rota.

		O gráfico mostra a variação do número de passageiros para cada rota,
		destacando a mediana, quartis e outliers.

		Returns:
			None: A função exibe o gráfico, mas não retorna nenhum valor.

		Example:
			>>> graficos = Graficos(df)
			>>> graficos.plot_boxplot_passageiros_por_rota()
		"""
		plt.figure(figsize=(12, 6))
		sns.boxplot(x="qtpsg", y="id_linha", data=self.df, hue="id_linha")
		plt.title("Distribuição de Passageiros por Rota")
		plt.xlabel("Número de Passageiros")
		plt.ylabel("Rotas")
		plt.xticks(rotation=45)
		plt.show()

	def plot_boxplot_valores_arrecadados_por_rota(self):
		"""Plota um boxplot da distribuição dos valores arrecadados por rota.

		O gráfico mostra a variação dos valores arrecadados para cada rota,
		destacando a mediana, quartis e outliers.

		Returns:
			None: A função exibe o gráfico, mas não retorna nenhum valor.

		Example:
			>>> graficos = Graficos(df)
			>>> graficos.plot_boxplot_valores_arrecadados_por_rota()
		"""
		plt.figure(figsize=(12, 6))
		sns.boxplot(x="valor_jornada", y="id_linha", data=self.df, hue="id_linha")
		plt.title("Distribuição dos Valores Arrecadados por Rota")
		plt.ylabel("Rota")
		plt.xlabel("Valor Arrecadado")
		plt.xticks(rotation=45)
		plt.show()

	def plot_duracao_medio_por_mes(self):
		"""Plota um boxplot da distribuição do tempo de viagem por rota.

		O gráfico mostra a variação da duração das viagens para cada rota,
		destacando a mediana, quartis e outliers.

		Returns:
			None: A função exibe o gráfico, mas não retorna nenhum valor.

		Example:
			>>> graficos = Graficos(df)
			>>> graficos.plot_duracao_medio_por_mes()
		"""
		plt.figure(figsize=(12, 6))
		sns.boxplot(x="duracao", y="id_linha", data=self.df, hue="id_linha")
		plt.title("Distribuição de Tempo de Viagem")
		plt.xlabel("Tempo de Duração")
		plt.ylabel("Rotas")
		plt.show()

	def plot_media_passageiros_por_rota(self):
		"""Plota o gráfico de barras da média de passageiros por rota.

		O gráfico exibe a média de passageiros para cada rota em ordem crescente,
		facilitando a comparação entre diferentes rotas.

		Returns:
			None: A função exibe o gráfico, mas não retorna nenhum valor.

		Example:
			>>> graficos = Graficos(df)
			>>> graficos.plot_media_passageiros_por_rota()
		"""
		media_passageiros = self.df.groupby("id_linha")["qtpsg"].mean().sort_values()
		plt.figure(figsize=(10, 6))
		media_passageiros.plot(kind="bar", color="skyblue")
		plt.title("Média de Passageiros por Rota")
		plt.xlabel("Rota")
		plt.ylabel("Média de Passageiros")
		plt.xticks(rotation=45)
		plt.show()

	def plot_duracao_vs_valor(self):
		"""Plota um gráfico de dispersão entre duração da viagem e valores arrecadados.

		O gráfico mostra a relação entre o tempo de duração das viagens e os valores
		arrecadados, com pontos coloridos de acordo com a rota.

		Returns:
			None: A função exibe o gráfico, mas não retorna nenhum valor.

		Example:
			>>> graficos = Graficos(df)
			>>> graficos.plot_duracao_vs_valor()
		"""
		plt.figure(figsize=(10, 6))
		sns.scatterplot(x="duracao", y="valor_jornada", data=self.df, hue="id_linha")
		plt.title("Duração vs Valor Arrecadado por Rota")
		plt.xlabel("Duração da Viagem (minutos)")
		plt.ylabel("Valor Arrecadado")
		plt.show()

	def plot_tendencia_passageiros(self):
		"""Plota a tendência do número de passageiros ao longo do tempo.

		O gráfico mostra a evolução do número total de passageiros agrupados por mês,
		permitindo identificar padrões sazonais e tendências de longo prazo.

		Returns:
			None: A função exibe o gráfico, mas não retorna nenhum valor.

		Note:
			Esta função pressupõe que o DataFrame tenha uma coluna 'data'
			já convertida para o tipo datetime.

		Example:
			>>> graficos = Graficos(df)
			>>> graficos.plot_tendencia_passageiros()
		"""
		df_grouped = self.df.groupby(self.df["data"].dt.to_period("M"))["qtpsg"].sum()
		plt.figure(figsize=(12, 6))
		df_grouped.plot(kind="line", color="green")
		plt.title("Tendência de Passageiros por Mês")
		plt.xlabel("Mês")
		plt.ylabel("Número Total de Passageiros")
		plt.show()

	def plot_barras_empilhadas(self):
		"""Plota gráfico de barras empilhadas de passageiros por mês e por rota.

		O gráfico mostra a distribuição mensal do número de passageiros, com cada
		rota representada como uma parte da barra empilhada, facilitando a comparação
		da contribuição de cada rota ao longo do tempo.

		Returns:
			None: A função exibe o gráfico, mas não retorna nenhum valor.

		Note:
			Esta função pressupõe que o DataFrame tenha uma coluna 'data'
			já convertida para o tipo datetime.
			A função cria um novo atributo self.df_pivot que armazena os dados
			transformados para o formato de tabela pivô.

		Example:
			>>> graficos = Graficos(df)
			>>> graficos.plot_barras_empilhadas()
		"""
		self.df["mes"] = self.df["data"].dt.to_period("M")
		self.df_pivot = self.df.pivot_table(index="mes", columns="id_linha", values="qtpsg", aggfunc="sum")
		self.df_pivot.plot(kind="bar", stacked=True, figsize=(12, 6))
		plt.title("Passageiros por Mês e Rota")
		plt.xlabel("Mês")
		plt.ylabel("Total de Passageiros")
		plt.show()

	def plot_area_passageiros(self):
		"""Plota um gráfico de área para a evolução do número de passageiros.

		O gráfico mostra a evolução do número de passageiros por rota ao longo do tempo
		usando um formato de área empilhada, que é útil para visualizar tanto o total
		quanto a contribuição proporcional de cada rota.

		Returns:
			None: A função exibe o gráfico, mas não retorna nenhum valor.

		Note:
			Esta função pressupõe que o DataFrame tenha uma coluna 'data'
			já convertida para o tipo datetime.
			A função cria um novo atributo self.df_grouped que armazena os dados
			agrupados por mês e rota.

		Example:
			>>> graficos = Graficos(df)
			>>> graficos.plot_area_passageiros()
		"""
		self.df_grouped = self.df.groupby([self.df["data"].dt.to_period("M"), "id_linha"])["qtpsg"].sum().unstack().fillna(0)
		self.df_grouped.plot(kind="area", stacked=True, figsize=(12, 6))
		plt.title("Evolução de Passageiros por Rota ao Longo do Tempo")
		plt.xlabel("Mês")
		plt.ylabel("Total de Passageiros")
		plt.show()

	def plotar_graficos(self):
		"""Gera todos os gráficos disponíveis na classe.

		Esta função chama sequencialmente todos os métodos de plotagem ativos
		na classe, gerando um conjunto completo de visualizações para análise
		dos dados de transporte.

		Returns:
			None: A função exibe os gráficos, mas não retorna nenhum valor.

		Example:
			>>> graficos = Graficos(df)
			>>> graficos.plotar_graficos()
		"""
		self.plot_area_passageiros()
		self.plot_boxplot_passageiros_por_rota()
		self.plot_boxplot_valores_arrecadados_por_rota()
		self.plot_media_passageiros_por_rota()
		self.plot_duracao_vs_valor()
		self.plot_tendencia_passageiros()
		self.plot_barras_empilhadas()
		self.plot_duracao_medio_por_mes()
