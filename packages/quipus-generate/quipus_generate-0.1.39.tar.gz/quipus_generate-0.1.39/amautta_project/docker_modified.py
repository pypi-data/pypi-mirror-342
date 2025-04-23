import os

def modify(name):
    compose_file = "docker-compose.yaml"

    block = (
        f"  {name}:\n"
        "    build:\n"
        f"      context: ./{name}\n"
        "      dockerfile: Dockerfile\n"
        f"    container_name: {name}-service\n"
        "    volumes:\n"
        f"      - ./{name}:/app\n"
        "    command: uvicorn app.main:run --host 0.0.0.0 --port ${SERVICE_PORT} --reload\n"
        "    networks:\n"
        "      - quipus-network\n"
        "    expose:\n"
        "      - ${SERVICE_PORT}\n"
        "    depends_on:\n"
        "      - db\n"
    )

    # Leer el contenido actual
    with open(compose_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Buscar el índice de la línea que contiene el servicio nginx
    insert_index = None
    for i, line in enumerate(lines):
        if line.strip().startswith("nginx:") and line.startswith("  "):  # indentación 2 espacios
            insert_index = i
            break

    # Insertar el bloque antes de nginx si no está presente
    if insert_index is not None:
        if f"{name}:" not in "".join(lines):  # Evitar insertar duplicado
            lines.insert(insert_index, block)
            with open(compose_file, "w", encoding="utf-8") as f:
                f.writelines(lines)
            print(f"[OK] Servicio '{name}' insertado correctamente antes de 'nginx'")
        else:
            print(f"[INFO] El servicio '{name}' ya existe en el archivo docker-compose.yaml")
    else:
        print("❌ No se encontró el servicio 'nginx:' en el archivo")
