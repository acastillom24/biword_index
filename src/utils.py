import os
import re
from tika import parser
from tqdm import tqdm
from functools import reduce

def read_pdf(root: str, extension: str = ".pdf", server_endpoint: str = "http://localhost:9999", timeout=300):
    """
    Lee todos los archivos PDF en el directorio especificado y devuelve un diccionario
    donde las claves son los nombres de los archivos y los valores son el contenido de cada archivo.
    
    Args:
    - directorio (str): Ruta al directorio donde se encuentran los archivos PDF.
    - extension (str): Extensión de los archivos a procesar. Default es '.pdf'.
    
    Returns:
    - dict: Un diccionario con el nombre del archivo como clave y el contenido del archivo como valor.
    """
    
    contenido = {}
    
    for file in tqdm(os.listdir(root), desc="Procesando archivos", unit="archivo"):
        if file.endswith(extension):
            path_to_file = os.path.join(root, file)
            try:
                parsed_pdf = parser.from_file(path_to_file, serverEndpoint=server_endpoint, requestOptions={'timeout': timeout})
                texto = parsed_pdf.get('content', '')
                contenido[file] = texto
            except Exception as e:
                print(f"Error al procesar {file}:\n{e}")
    
    return contenido

def normalize(texto):
    '''
    Esta función limpia y tokeniza el texto en palabras individuales.
    El orden en el que se va limpiando el texto no es arbitrario.
    El listado de signos de puntuación se ha obtenido de: print(string.punctuation)
    y re.escape(string.punctuation)
    '''
    
    # Se convierte todo el texto a minúsculas
    nuevo_texto = texto.lower()
    # Eliminar tildes
    nuevo_texto = re.sub(r'[á]', 'a', nuevo_texto)
    nuevo_texto = re.sub(r'[é]', 'e', nuevo_texto)
    nuevo_texto = re.sub(r'[í]', 'i', nuevo_texto)
    nuevo_texto = re.sub(r'[ó]', 'o', nuevo_texto)
    nuevo_texto = re.sub(r'[ú]', 'u', nuevo_texto)
    # nuevo_texto = re.sub(r'[ñ]', '#', nuevo_texto)
    nuevo_texto = re.sub(r'[ü]', 'u', nuevo_texto)
    nuevo_texto = re.sub(r'[ö]', 'u', nuevo_texto)
    # Eliminación de páginas web (palabras que empiezan por "http")
    nuevo_texto = re.sub('http\S+', ' ', nuevo_texto)
    # Eliminación de signos de puntuación
    regex = '[\\“\\”\\’\\‘\\─\\—\\°\\¡\\!\\"\\#\\$\\%\\&\\\'\\(\\)\\*\\+\\,\\-\\.\\/\\:\\;\\<\\=\\>\\¿\\?\\@\\[\\\\\\]\\^_\\`\\{\\|\\}\\~]'
    nuevo_texto = re.sub(regex , ' ', nuevo_texto)
    nuevo_texto = re.sub(r'\s+', ' ', nuevo_texto).strip()
    nuevo_texto = re.sub(r'[\s\u200b\u2013]+', ' ', nuevo_texto).strip()
    # Eliminación de números
    nuevo_texto = re.sub("\d+", ' ', nuevo_texto)
    # Eliminación de espacios en blanco múltiples
    nuevo_texto = re.sub("\\s+", ' ', nuevo_texto)
    # Tokenización por palabras individuales
    # nuevo_texto = nuevo_texto.split(sep = ' ')
    # Eliminación de tokens con una longitud < 2
    # nuevo_texto = [token for token in nuevo_texto if len(token) > 1]
    
    return(nuevo_texto)


def query_biword_index(biword_index, word1, word2):
    """
    Consulta el índice biword para buscar en qué documentos aparece un bigrama dado.
    
    Parámetros:
        biword_index (dict): Índice biword generado previamente.
        word1 (str): Primera palabra del bigrama.
        word2 (str): Segunda palabra del bigrama.
    
    Retorna:
        list: Lista de documentos donde aparece el bigrama.
    """
    # Crear el bigrama con las palabras ingresadas
    biword = (word1, word2)
    
    # Verificar si el bigrama existe en el índice
    term_list = [biword_index.get(term, set()) for term in biword]
    flattened_term_list = [item for sublist in term_list for item in (sublist if isinstance(sublist, list) else [sublist])]
    if any(term == set() for term in flattened_term_list):
        return []
    return list(reduce(set.intersection, map(set, term_list)))
