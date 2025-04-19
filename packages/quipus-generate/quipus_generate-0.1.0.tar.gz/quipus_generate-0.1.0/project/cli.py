import argparse

from microservice_generator import create as microservice
from docker_modified import modify as docker_modify
from migration_generator import create as migration
from readme_modified import modify as readme_modify
from main_modified import modify as main_modify
from proyect_generator import create as project
from entity_generator import create as entity
from site_generator import create as site

def main():
    parser = argparse.ArgumentParser(description="Generador de proyectos FastAPI con docker-compose y base de datos postgres.")
    subparsers = parser.add_subparsers(dest="accion", required=True, help="Acciones disponibles.")
    # Comando para inicializar un nuevo proyecto
    init_parser = subparsers.add_parser("init", help="Iniciar un nuevo proyecto.")
    init_parser.add_argument("name", help="Nombre del proyecto.")

    # Comando para crear un microservicio
    microservice_parser = subparsers.add_parser("microservice", help="Crear un microservicio con Arquitectura Hexagonal.")
    microservice_parser.add_argument("name", help="Nombre del microservicio.")
    microservice_parser.add_argument("entity", help="Nombre de la entidad.")

    # Comando para crear una entity
    entity_parser = subparsers.add_parser("entity", help="Crear una entity con Arquitecura Hexagonal.")
    entity_parser.add_argument("name", help="Nombre de la entity.")

    args = parser.parse_args()

    if args.accion == "init":
        project(args.name)

    elif args.accion == "microservice":
        microservice(args.name)
        docker_modify(args.name)
        site(args.name)
        entity(args.entity, args.name)
        migration(args.entity, args.name)
        main_modify(args.entity, args.name)
        readme_modify(args.entity, args.name)

    elif args.accion == "entity":
        entity(args.name)
        migration(args.name)
        main_modify(args.name)
        readme_modify(args.name)

if __name__ == "__main__":
    main()
