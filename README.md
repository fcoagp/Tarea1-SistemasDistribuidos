
# Tarea 1 Sistemas Distribuidos

Explicación para ejecución de proyecto de la Tarea 1 de Sistemas Distribuidos.




## Dataset y Video

[Drive](https://drive.google.com/drive/folders/1fdOus79STeMNFeyGXVS5QkACz7DZ8asT?usp=drive_link)
## Pasos a seguir

Primero se debe insertar el archivo .csv del dataset, el cual se encuentra el en drive, en la carpeta db.

Una vez realizado esto ejecutamos el comando:

```bash
  docker compose build
```
Luego ejecutamos
```bash
  docker compose up
```

Luego hay que esperar a que se genere la base de datos, esto se puede confirmar mediante el siguiente mensaje en la terminal:


![App Screenshot](https://snipboard.io/3toH4N.jpg)


Luego se debe presionar `Ctrl` + `C` y una vez detenida la instancia, se debe volver a ejecutar el comando:

```bash
  docker compose up
```
Finalmente, para ejecutar un test, introducimos el siguiente comando en la carpeta del proyecto:

```bash
  python3 test.py
```

# Cambiar distribución de Redis y Política de remoción

### Sistema Redis
Las configuraciones disponibles de Redis son:

+ CENTRAL
+ PARTITION
+ DUPLICATE

Si se desea cambair entre alguna de estas, hay que dirigirse al archivo **docker-compose.yml** y en el apartado de api_rest, en el "enviroment", se debe cambiar el CACHE_TYPE.

![App Screenshot](https://snipboard.io/byMwRK.jpg)


### Política Redis
[Políticas de remoción](https://redis.io/docs/latest/develop/reference/eviction/)

Si se desea cambair entre alguna de estas, hay que dirigirse al archivo **docker-compose.yml** y en el apartado de redis1, redis2 y redis3 se debe cambiar en el **command** por la necesaria (en el ejemplo se utiliza allkey-lru).

![App Screenshot](https://snipboard.io/Sdjto0.jpg)