## comunicaciones-paper
Esto es una API que se puede integrar en cualquier proyecto

Para correr el script se necesita instalar todos los reqquerimientos en en requirements.txt De la siguiente forma pip install -r requirements.txt

Para correr el servidor se hace: python manage.py runserver

Sale una direccion con localhost y esa es la que pone en el navegador Tipicamente es localhost:8000

localhost:8000/dos-rayos?potencia_tx=10&ganancia_tx=1&altura_antena_tx=20&ganancia_rx=30&altura_antena_rx=70&distancia=50&base_logaritmica=60

Hay 3 rutas disponibles /dos-rayos

/okumura

/okumura-hata

Tiene que pasar los argumnetos (se puede en la url):

Para dos-rayos: potencia_tx, ganancia_tx, altura_antena_tx, ganancia_rx, altura_antena_rx, distancia, base_logaritmica

Para okumura: atenuacion_esplibre, atenuacion_relpromedio, altura_antena_tx, ganancia_tx, ganancia_rx, ganancia_de_ambiente, frecuencia, base_logaritmica

Para okumura-hata: atenuacion_esplibre, factor_correccion, atenuacion_relpromedio, altura_antena_tx, altura_antena_rx, ganancia_tx, ganancia_rx, frecuencia, base_logaritmica, distancia