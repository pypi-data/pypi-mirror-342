import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

VERSION = '0.0.21' #Muy importante, deberéis ir cambiando la versión de vuestra librería según incluyáis nuevas funcionalidades
PACKAGE_NAME = 'connectus' #Debe coincidir con el nombre de la carpeta 
AUTHOR = 'Javier A. Quintana Hernandez' #Modificar con vuestros datos
AUTHOR_EMAIL = 'javierquinttana@gmail.com' #Modificar con vuestros datos
URL = 'https://github.com/javierquinttana' #Modificar con vuestros datos

LICENSE = 'MIT' #Tipo de licencia
DESCRIPTION = 'Librería para la gestión de dispositivos físicos y virtuales.' #Descripción corta
LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding='utf-8') #Referencia al documento README con una descripción más elaborada
LONG_DESC_TYPE = "text/markdown"


#Paquetes necesarios para que funcione la libreía. Se instalarán a la vez si no lo tuvieras ya instalado
INSTALL_REQUIRES = [
    'pyserial',
    'asyncua',
    'cryptography',
    'aiohttp',
    'aiocsv',
    'pandas',
    'numpy',
    'matplotlib',
    'asyncpg',
    'pyvisa',
    'psutil',
    'zeroconf',
    'paho-mqtt',
    'influxdb-client'
      ]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    license=LICENSE,
    packages=find_packages(),
    include_package_data=True
)