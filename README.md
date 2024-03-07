# PokeApp

¡Bienvenido a PokeApp! Esta aplicación te permite explorar información sobre Pokémon utilizando la PokeAPI.

## Empezando

Siga estos pasos para configurar y ejecutar PokeApp en su máquina local:

1. **Clone el repositorio en su máquina local:**
Clona el repositorio en tu máquina local: Sugerencia de nombre: pokeapp.

`mkdir pokeapp`

Descarga los archivos disponibles en el repositorio de GitHub y clona el repositorio:
  
`cd pokeapp
git clone https://github.com/elainedasilva/PokeAPI.git`

Dentro de la carpeta pokeapp, crea un entorno virtual (venv) para evitar conflictos entre diferentes proyectos.
 
`cd PokeAPI
python3 -m venv venv`


Activa tu entorno virtual:
`source venv/bin/activate`

Instale las dependencias del proyecto enumeradas en el archivo requisitos.txt:
  
`pip install -r requirements.txt`

Acceda al directorio pokeapi (obtenido en GitHub).
Ejecute el archivo   **vaultsecrets.py  ** para obtener el archivo   **api_keys.py  **, que contiene las contraseñas y tokens necesarios.
El archivo vaultsecrets.py fue   **enviado por correo electrónico  ** para mantener la seguridad de los datos confidenciales.

`python3 vaultsecrets.py`

Ahora debería tener el archivo api_keys.py en el directorio pokeapi, junto con el archivo pokeapp.py.
Ejecute el archivo pokeapp.py para iniciar el servidor Flask:
  
`python3 pokeapp.py`

El servidor Flask se ejecutará y podrá acceder a la aplicación abriendo un navegador web y navegando a la URL presentada.
  **¡Explora la información de Pokémon usando PokeApp!  **

Presione CTRL+C en la terminal para finalizar el programa.

## Notas adicionales
Asegúrese de tener Python 3 instalado en su sistema.
Esta aplicación utiliza Flask como marco web e interactivo.
