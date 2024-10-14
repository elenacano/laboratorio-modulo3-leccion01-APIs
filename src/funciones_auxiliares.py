from geopy.geocoders import Nominatim
from tqdm import tqdm
import dotenv
import requests
import os

def obtencion_coordenadas(lugar):
    """Devuelve una tupla con la longitud y latitud del lugar

    Args:
        lugar (str): lugar del que se desean obtener las coordenadas

    Return:
        tuple: tupla de la latitud y longitud
    """
    

    geolocator = Nominatim(user_agent="SetMagic")
    location = geolocator.geocode(lugar)

    
    return (location.latitude, location.longitude)


def busqueda_lugares(api_key, latitud, longitud, id_categoria, radio, fields):
    """Llama a la api foursquare para obtener lugares cercanos a los parametros de latitud y longitud  pasados que cumplan la categoría.

    Args:
        latitud (float): latitud del municipio
        longitud (float): longitud del municipio
        id_categoria (str): categoria del lugar que se desea buscar
        radio (int): metros máximos de los lugares que se desean buscar
        fields (str): campos que se desea que se devuelvan de la llamada a la api

    Returns:
        Devuelve un json con los lugares obtenidos de la búsqueda.
    """

    url = "https://api.foursquare.com/v3/places/search"

    params = {
        "ll": ""+str(latitud)+","+str(longitud),
        "categories": id_categoria,
        "radius": radio,
        "sort":"DISTANCE",
        "fields": fields
    }

    headers = {
        "Accept": "application/json",
        "Authorization": api_key
    }

    response = requests.request("GET", url, params=params, headers=headers)

    return response.json()



def lista_lugares_municipios(api_key, df, dic_id_categorias, radio, fields):
    """Crea una lista de diccionarios a partir de los datos devueltos por la función busqueda_lugares

    Args:
        df (dataFrame): dataframe de municipio, latitud, longitud
        dic_id_categorias (dict): diccionario de id y categoria
        radio (int): radio de distancia a los lugares buscados
        fields (str): campos que se desa que devuelva la función busqueda_lugares

    Returns:
        list: lista de diccionarios con los valores obtenidos
    """

    lista_id_categorias = list(dic_id_categorias.keys())
    lista_df_municipio = []

    for i in tqdm(range(df.shape[0])):
        municipio = df.iloc[i,0]
        latitud = float(df.iloc[i,1])
        longitud = float(df.iloc[i,2])
        
        for categoria in lista_id_categorias:
            lista_dics = busqueda_lugares(api_key, latitud, longitud, categoria, radio, fields)["results"]
            for dic in lista_dics:
                dic_final = {
                    "municipio":municipio,
                    "latitud":latitud,
                    "longitud":longitud,
                    "nombre":dic["name"],
                    "categoria":dic_id_categorias[categoria],
                    "distancia":dic["distance"],
                    "direccion":dic["location"]["formatted_address"]
                }
                lista_df_municipio.append(dic_final)
                
    return lista_df_municipio