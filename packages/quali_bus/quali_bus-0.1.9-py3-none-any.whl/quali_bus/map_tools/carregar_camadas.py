import fiona
import geopandas as gpd
import pandas as pd


def carregar_rotas(file_path: str) -> gpd.GeoDataFrame:
	"""Carrega rotas de transporte público a partir de um arquivo KML.

	Args:
		file_path (str): Caminho para o arquivo KML contendo as rotas de transporte.

	Returns:
		gpd.GeoDataFrame: GeoDataFrame contendo as rotas processadas.
	"""
	gdf_list = [gpd.read_file(file_path, driver="LIBKML", layer=layer) for layer in fiona.listlayers(file_path)]
	gdf = gpd.GeoDataFrame(pd.concat(gdf_list, ignore_index=True))
	gdf = gdf.query("Description != ''")
	gdf[["id_linha", "sentido"]] = gdf["Name"].str.split(" - ", expand=True)
	del gdf["Name"]
	return gdf


def carregar_bairros(file_path: str) -> gpd.GeoDataFrame:
	"""Carrega os bairros da cidade a partir de um arquivo geoespacial.

	Args:
		file_path (str): Caminho para o arquivo contendo os polígonos dos bairros.

	Returns:
		gpd.GeoDataFrame: GeoDataFrame contendo os polígonos dos bairros.
	"""
	return gpd.read_file(file_path)
