import folium
import geopandas as gpd
from folium.plugins import Fullscreen, GroupedLayerControl

from ..data_analysis.classificar_indicadores import ClassificarIndicadores
from .camadas import adicionar_linha_ao_mapa, adicionar_linha_ao_mapa_sem_grupo


class MapaIQT:
	"""Classe para criar e gerenciar mapas interativos de Índice de Qualidade do Transporte (IQT).

	Esta classe fornece funcionalidades para inicializar um mapa centrado em uma cidade,
	adicionar camadas de rotas e classificá-las de acordo com o IQT (Índice de Qualidade
	do Transporte).

	Attributes:
		gdf_city (gpd.GeoDataFrame): GeoDataFrame contendo as geometrias dos bairros da cidade.
		mapa (folium.Map): Objeto de mapa Folium inicializado.
		legenda (str): String contendo informações sobre a legenda do mapa.
	"""

	def __init__(self, gdf_city: gpd.GeoDataFrame):
		"""Inicializa um mapa centrado na cidade com uma camada base de bairros.

		Args:
			gdf_city (gpd.GeoDataFrame): GeoDataFrame contendo as geometrias dos bairros da cidade. Deve conter uma coluna 'geometry' com os polígonos dos bairros.
		"""
		self.gdf_city = gdf_city
		self.mapa = self._inicializar_mapa(self.gdf_city)
		self.legenda = ""

	def _inicializar_mapa(self, gdf_city: gpd.GeoDataFrame) -> folium.Map:
		"""Inicializa um mapa Folium centrado na cidade com uma camada base de bairros.

		Args:
			gdf_city (gpd.GeoDataFrame): GeoDataFrame contendo as geometrias dos bairros da cidade. Deve conter uma coluna 'geometry' com os polígonos dos bairros.

		Returns:
			folium.Map: Mapa Folium inicializado com:
				- Camada base CartoDB Voyager
				- Zoom inicial de 12
				- Camada de bairros estilizada
				- Centrado no centroide médio da cidade

		Example:
			>>> gdf_city = gpd.read_file("caminho/para/bairros.geojson")
			>>> mapa_iqt = MapaIQT(gdf_city)
			>>> mapa = mapa_iqt._inicializar_mapa(gdf_city)
		"""
		bounds = gdf_city.total_bounds

		center_lat = (bounds[1] + bounds[3]) / 2
		center_lon = (bounds[0] + bounds[2]) / 2

		map_routes = folium.Map(location=[center_lat, center_lon], zoom_start=12, tiles="CartoDB Voyager")

		folium.GeoJson(
			gdf_city, style_function=lambda feature: {"fillColor": "white", "color": "black", "weight": 0.7, "fillOpacity": 0.5}, name="Bairros"
		).add_to(map_routes)

		map_routes.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])

		Fullscreen().add_to(map_routes)

		return map_routes

	def classificar_rota(self, gdf_routes: gpd.GeoDataFrame) -> folium.Map:
		"""Adiciona rotas ao mapa base e as classifica por cor de acordo com o IQT.

		Esta função itera sobre cada rota no GeoDataFrame e adiciona cada uma
		individualmente ao mapa, utilizando cores diferentes com base no seu IQT.

		Args:
			gdf_routes (gpd.GeoDataFrame): GeoDataFrame contendo as rotas a serem adicionadas.
				Deve conter as seguintes colunas:
				- geometria_linha: geometria do tipo LineString
				- id_linha: nome da rota para o tooltip
				- iqt: índice de qualidade para determinação da cor

		Returns:
			folium.Map: Mapa Folium com as rotas adicionadas e classificadas por cor
				de acordo com o IQT.

		Example:
			>>> gdf_city = gpd.read_file("caminho/para/bairros.geojson")
			>>> gdf_routes = gpd.read_file("caminho/para/rotas.geojson")
			>>> mapa_iqt = MapaIQT(gdf_city)
			>>> mapa_final = mapa_iqt.classificar_rota(gdf_routes)
			>>> mapa_final.save("mapa_rotas.html")
		"""
		for _, line in gdf_routes.iterrows():
			adicionar_linha_ao_mapa_sem_grupo(line, self.mapa)
		return self.mapa

	def classificar_rota_grupo(self, gdf_routes: gpd.GeoDataFrame) -> folium.Map | None:
		"""Adiciona rotas ao mapa base, classificadas por cor e organizadas em grupos de camadas.

		Esta função agrupa as rotas com base em sua classificação IQT, cria grupos de
		camadas no mapa e adiciona controles para ativar/desativar grupos de camadas.

		Args:
			gdf_routes (gpd.GeoDataFrame): GeoDataFrame contendo as rotas a serem adicionadas.
				Deve conter as seguintes colunas:
				- geometria_linha: geometria do tipo LineString
				- id_linha: nome da rota para o tooltip
				- iqt: índice de qualidade para determinação da cor

		Returns:
			folium.Map: Mapa Folium com as rotas adicionadas, classificadas por cor
				e organizadas em grupos de camadas de acordo com o IQT.
			None: Se ocorrer algum erro no processo.

		Example:
			>>> gdf_city = gpd.read_file("caminho/para/bairros.geojson")
			>>> gdf_routes = gpd.read_file("caminho/para/rotas.geojson")
			>>> mapa_iqt = MapaIQT(gdf_city)
			>>> mapa_final = mapa_iqt.classificar_rota_grupo(gdf_routes)
			>>> mapa_final.save("mapa_rotas_grupos.html")
		"""
		grupos = {}
		classificador = ClassificarIndicadores()
		listas_grupo = []

		for _, line in gdf_routes.iterrows():
			classificao_iqt = classificador.classificacao_iqt_pontuacao(line.iqt)

			grupo = grupos.get(classificao_iqt, None)
			if grupo is None:
				grupo = folium.FeatureGroup(name=classificao_iqt)
				listas_grupo.append(grupo)
				self.mapa.add_child(grupo)
				grupos[classificao_iqt] = grupo
			adicionar_linha_ao_mapa(line, grupo)

		GroupedLayerControl(groups={"classificacao": listas_grupo}, collapsed=False).add_to(self.mapa)

		return self.mapa
