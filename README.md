# Aclaraciones para el desarrollador

## Comandos para crear migraciones
python manage.py db init
python manage.py db migrate
python manage.py db upgrade

## Executar la aplicación
python manage.py runserver

## Variables de ambientes
SQLALCHEMY_DATABASE_URI = path/to/database
FLASK_APP=movie_trade
FLASK_ENV=development||production
UPLOAD_FOLDER = path/to/folder/of/uploaded/files

## Tecnologías usadas
Python (Flask)
Postgresql
Bootstrap
Jquery

# Modo de uso

En la pantalla principal se encontrará con Dos opciones: "Create movie" y "Add images".
La primera le llevará a un formulario para crear un nuevo registro de la película o video.
La segunda, le enviará a un formulario para agregar una imagen a una película o video previamente registrado.
Después de esas opciones, se mostrará las películas o videos registrados con una imagen.

Al crear una película, se le pedirá que llene los campos código, nombre, género, descripción.
Todos los campos son obligatorios.
Al crear exitosamente el registro será redirigido al la vista de detalle del video o película.
En caso contrario, volverá al formulario, con un mensaje de color rojo en la parte superior diciendo cual fue el fallo.

Para añadir una imagen, debe llenar el campo para subir un archivo de imagen desde su equipo.
Para asociar a una película, tiene un campo de autocompletado que le ayudará a buscar entre los registros el que desea.
Cuando tenga esos datos pulse el botón guardar, y si es exitoso será redirigido a la vista de detalle de la películo que seleccionó.
En caso contrario, volverá al formulario, con un mensaje de color rojo en la parte superior diciendo cual fue el fallo.

En la vista de detalle verá los datos básicos de la película registrada anteriormente y una galería con las imágenes asociadas.