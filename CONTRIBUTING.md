
# Contributing

## Pull Request

Cada cambio realizado en el código será aplicado en una rama creada para ese cambio específico. Cada rama llevará
asociada una `Pull Request`. En la misma se realizará seguimiento de los cambios realizados. Cada rama tendrá un
responsable y el resto de usuarios puede realizar comentarios en la propia `Pull Request`o comentar el código en línea a
medida que se realicen revisiones.

Todas las ramas deben ser creadas a partir de `master`, a dónde deben ser _mergeadas_  una vez que la característica
haya sido implementada. Para nombrar una rama se seguirán las siguientes normas, siendo `característica` un nombre
descriptivo de la característica realizada:
- `feature/característica`  : implementa una nueva funcionalidad y se añade la documentación correspondiente a la misma
- `fix/característica` : implementa una corrección a un bug
- `doc/característica` : añade documentación en caso de que no haya sido añadida en la implementación
- `test/característica` : sirve para probar nuevas funcionalidades. Los usuarios que no sean responsables de la rama no
  la modifican.

Para _mergear_  las `Pull Request`primero se necesita la aprovación de todos los miembros del equipo. Cuando se obtenga
dicha aprovación el responsable de la rama es el encargado de hacer el merge a `master`. Esta fusión se debe hacer
mediante [squash](https://www.devroom.io/2011/07/05/git-squash-your-latests-commits-into-one/) de _commits_ y eliminando
la rama que ha sido fusionada. También debe ser eliminada la `Pull Request`.

## Documentación

La documentación se realizará siguiendo el [Markdown Github
Flavored](https://help.github.com/en/articles/about-writing-and-formatting-on-github). El código estará distribuido en
directorios dentro del repositorio, por lo que el **README**  del directorio raíz mostrará información de carácter
general mientras que la documentación específica de cada parte se incluirá en un fichero **README**  dentro del
directorio correspondiente. Debe ser breve, concisa e indicar mediante enlaces las referencias de dónde se ha obtenido
la información o a la ampliación de la información presente (documentación de referencia de las APIs utilizadas).

