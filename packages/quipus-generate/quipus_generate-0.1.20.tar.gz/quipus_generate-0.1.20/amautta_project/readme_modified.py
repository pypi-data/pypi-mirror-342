import inflection
import os

def modify(name, microservice=None):
    crud_doc = (
        f"## 📦 CRUD de {inflection.pluralize(name).capitalize()}\n"
        f"\n"
        f"- `GET /api/v1/{name}`: Lista todas las {inflection.pluralize(name)}\n"
        f"- `GET /api/v1/{name}/{{id}}`: Obtiene una {name} por ID: UUID\n"
        f"- `POST /api/v1/{name}`: Crea una nueva {name}\n"
        f"- `PUT /api/v1/{name}/{{id}}`: Actualiza una {name} existente por ID: UUID\n"
        f"- `DELETE /api/v1/{name}/{{id}}`: Elimina una {name} por ID: UUID\n"
    )

    if microservice is not None:
        readme_path = f"{microservice}/README.md"
    else:
        readme_path = "README.md"

    # Leer el contenido actual
    with open(readme_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Verificar si ya existe una sección de CRUD
    if f"## 📦 CRUD de {inflection.pluralize(name).capitalize()}" not in content:
        # Agregar al final del archivo
        content += "\n" + crud_doc

        # Guardar el archivo modificado
        with open(readme_path, "w", encoding="utf-8") as file:
            file.write(content)

        print(f"✅ Se ha agregado la sección CRUD {name} al README.md.")
    else:
        print(f"ℹ️ Ya existe una sección CRUD {name} en el README.md.")
