import requests
import sys
from bs4 import BeautifulSoup
from time import sleep
import os

if len(sys.argv) is not 2:
    print("Debes introducir el fichero de destino Ej: scraped.txt")
    exit()

try:
    fichero = open(sys.argv[1], "w")
except:
    print(f"No se pudo escribir en {sys.argv[1]}")
    exit()

url = 'https://listas.20minutos.es/'

paginaPrincipal = requests.get(url)

paginaPrincipalSoup = BeautifulSoup(paginaPrincipal.text, "html.parser")

entradas = paginaPrincipalSoup.findAll(class_="resultado listarecomendada")

contador = 1

for entrada in entradas:

    print(f"Se han obtenido {contador} listas...", end = '\r')

    linkSitio = entrada.find('a',href=True)['href']
    nombreSitio = entrada.find('a',href=True)['title']

    fichero.write(f"{nombreSitio}\n")

    url = 'https://listas.20minutos.es'+linkSitio
    insideLink = requests.get(url)

    if insideLink.status_code == 404:
        print(f'Link {url} no valido')
        continue

    insideLinkSoup = BeautifulSoup(insideLink.text, "html.parser")

    h3 = insideLinkSoup.findAll('h3')

#    print("-----------------\n" + nombreSitio + "\n-----------------")
    for entradaEnCadaPagina in h3:
        for i in entradaEnCadaPagina:
            fichero.write(f'    {entradaEnCadaPagina.text}\n')
#        print(entradaEnCadaPagina.text)

    fichero.write("\n")
#    print("\n\n")
    contador+=1

fichero.close()

print(f"\nTienes tu lista disponible en tu fichero: {fichero.name}")
