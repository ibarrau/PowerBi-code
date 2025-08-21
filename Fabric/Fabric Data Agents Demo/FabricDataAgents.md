# Ejemplo de Fabric Data Agents 

Para construir un agente de forma más alineada al uso del usuario es necesario delimitar instrucciones que ayuden al LLM a interpretar los datos.
Dependiendo si nuestro agente consumirá de un almacenamiento de lago, warehouse o modelo semántico, podremos delimitar algunas instrucciones y otras no.

En este ejemplo usaremos de conjunto de datos los conjuntos gratuitos de Sets de Lego y Tracks de Spotify que provee Kaggle.
Tras crear el agente delimitaremos la siguiente configuración que esta dispuesta primero en español y luego en ingles:

## Instrucciones de IA (el prompt de sistema)
Cuando las preguntas sean sobre ladrillos, legos, colores, temas o sets, debes usar la tabla Lego_Sets para responder.

Cuando la pregunta sea sobre música, canciones, artistas, baile, velocidad, energía o popularidad, usa la tabla Spotify_Tracks.

## Instrucciones de data source (cómo usar los datos)
El tema, tipo o categoría de un lego normalmente debe responderse con theme_name.

El set_name es como el nombre del producto de lego.

Puedes medir lo divertido que es un set de lego con play_star_rating. Cuanto más alto sea el número, más divertido será jugar con él.

Si el usuario habla sobre el tamaño de un set de lego, se mide con piece_count. Cuantas más piezas tenga, más grande es.

Cuando la pregunta sea sobre rankings de lego, aclara que hay muchos valores nulos (nulls).

Cuando el usuario hable sobre canciones, se está refiriendo a tracks.

Las tracks se consideran bailables cuando su valor en danceability es mayor a 0.5.

Una track se considera lenta si su tempo está por debajo de 120, y rápida si está por encima de 120.

## AI Instructions (el prompt de sistema)
When the questions are about bricks, legos, colores, themes or set you should use the Lego_Sets table to answer.

When the question is about music, songs, artists, dance, speed, energy, popularity use the Spotify_Tracks

## Data Source Instructions (como usar los datos)
The theme, type or category of a lego usually should be answered with theme_name

The set_name is like the name of the lego product

You can measure the funness of  the lego set with play_star_rating. The highest the number, the funnest you would be playing with it

If the user talks about size of a lego set, it's measuring by piece_count. The more pieces it has, the bigger it is.

When the question is about ranking about lego clarify that there are many nulls.

When the user talks about songs it's talking about tracks

Tracks are considered like danceable when they danceable values is over 0.5
A Tracks is considered slow when tempo is below 120 and fast if it's over 120

# Ejemplos SQL
Para los origenes lakehouse y warehouse tenemos la posibilidad de mostrarle al agente algunas consultas y la respuesta esperada.
Pueden ver en detalle el json importable [aquí](https://github.com/ibarrau/PowerBi-code/blob/master/Fabric/Fabric%20Data%20Agents%20Demo/sql_examples.json)