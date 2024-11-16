# %% Carga de bibliotecas
from src.utils import read_pdf, normalize, query_biword_index
from src.Processing import Processing
from src.Bigram import Bigram
from collections import OrderedDict
import yaml
import json
import os

# %% Carga archivo yaml
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)
    
SERVER_ENDPOINT = config["server_endpoint"]
TIME_OUT = config["time_out"]
PATH_TO_SAVE_ALL_CONTENT = config["path_to_save_content_txt"]
PATH_TO_SAVE_INDEX_BIWORD = config["path_to_save_corpus_json"]

# %% Funciones
def convert_to_linux_path(path):
    if os.name == 'posix' and '\\' in path:
        # Convierte barras invertidas de Windows a barras normales de Linux
        path = path.replace('\\', '/')
    return path

def all_content(contenido: dict):
    texto_total = ' '.join(contenido.values())
    texto_total = normalize(texto_total)
    with open(PATH_TO_SAVE_ALL_CONTENT, 'w') as f:
        f.write(texto_total)

def generate_biword_index():
    directory = input("Ingrese el directorio con los archivos de texto: ")
    directory = convert_to_linux_path(directory)
    
    if not os.path.isdir(directory):
        print(f"El directorio {directory} no existe o no es accesible.")
        return
    
    processor = Processing()
    contenido = read_pdf(directory, server_endpoint=SERVER_ENDPOINT, timeout=500)
    all_content(contenido)
    
    index = {}
    
    for archivo, texto in contenido.items():
        # Normalización del corpus
        text = normalize(texto)
        # Generar los tokens
        tokens = processor.tokenizacion(text)
        # Eliminar los tokens con una longitud < 2
        tokens = [token for token in tokens if len(token) > 1]
        # Stemming
        # tokens = processor.stemming(tokens)
        
        for i in range(len(tokens) - 1):
            phrase = ""
            s = 0
            if bool(tokens[i].strip()):
                phrase += tokens[i].strip()
                s = 1
            if bool(tokens[i + 1].strip()) and tokens[i + 1].istitle():
                if s == 1:
                    phrase += " "
                phrase += tokens[i+1].strip()
            if phrase not in index.keys():
                index[phrase] = []
            if archivo not in index[phrase]:
                index[phrase].append(archivo)
            index[phrase].sort()

    index = OrderedDict(sorted(index.items(), key=lambda t: t[0]))
    
    with open(PATH_TO_SAVE_INDEX_BIWORD, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=4)
    
    print(f"Índice biword generado con éxito en: {PATH_TO_SAVE_INDEX_BIWORD}")
        
# Menú principal
def main_menu():
    while True:
        print("\nMenú Principal:")
        print("1. Generar índice biword")
        print("2. Generar bigramas")
        print("3. Consultar índice biword")
        print("4. Salir")
        choice = input("Seleccione una opción: ")

        if choice == '1':
            generate_biword_index()
            
        elif choice == '2':
            directory = input("Ingrese la ruta absoluta de todo el contenido: ")
            if not directory:
                directory = PATH_TO_SAVE_ALL_CONTENT
                print(f"Se utilizará el archivo: {directory}")
                
            if not os.path.isfile(directory):
                print("Necesita generar un archivo que contenga el contenido de todos los documentos.")
                return 0
                
            with open(directory, 'r', encoding="utf-8") as f:
                all_content = f.read()
            
            print("\nOpciones de generación de bigramas:")
            print("1. Bigramas mediante frecuencia")
            print("2. Bigramas mediante probabilidad")
            print("3. Bigramas mediante Chi-cuadrado")
            print("4. Bigramas mediante PMI")
            sub_choice = input("Seleccione una opción: ")

            bigram_finder = Bigram()
            
            if sub_choice == '1':
                print("Bigrams by Raw Frequency:")
                print(bigram_finder.get_bigrams_by_raw_freq(all_content))

            elif sub_choice == '2':
                print("\nBigrams by Likelihood Ratio:")
                print(bigram_finder.get_bigrams_by_likelihood_ratio(all_content))

            elif sub_choice == '3':
                print("\nBigrams by Chi-Squared:")
                print(bigram_finder.get_bigrams_by_chi_squared(all_content))

            elif sub_choice == '4':
                print("\nBigrams by PMI:")
                print(bigram_finder.get_bigrams_by_pmi(all_content))

            else:
                print("Opción inválida.")

        elif choice == '3':
            directory = input("Ingrese la ruta absoluta del indice biword: ")
            if not directory:
                directory = PATH_TO_SAVE_INDEX_BIWORD
                print(f"Se utilizará el archivo: {directory}")
                
            if not os.path.isfile(directory):
                print("Necesita generar primero el indice biword.")
                return 0
            
            with open(directory, "r", encoding="utf-8") as f:
                biword_index = json.load(f)

            word1 = input("Ingrese la primera palabra del bigrama: ").lower()
            word2 = input("Ingrese la segunda palabra del bigrama: ").lower()
            results = query_biword_index(biword_index, word1, word2)
            if results:
                print(f"El bigrama ({word1}, {word2}) aparece en los documentos: {results}")
            else:
                print(f"El bigrama ({word1}, {word2}) no se encuentra en ningún documento.")

        elif choice == '4':
            print("Saliendo del programa.")
            break

        else:
            print("Opción inválida. Intente de nuevo.")

if __name__ == "__main__":
    main_menu()
