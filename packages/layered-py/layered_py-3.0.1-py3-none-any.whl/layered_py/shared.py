import os
from constants.templates import get_service_template, get_domain_template, get_repository_template, \
    get_presentation_template
from layered_py.config_loader import Config
from layered_py.decorators import inject

config = Config()

def create_service(service_name):
    service_template = get_service_template(service_name)

    # Ensure the 'services' directory exists
    directory = config.get('service_destination')
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = f"{directory}/{service_name}.py"

    with open(file_path, "w") as file:
        file.write(service_template)

    print(f"Service '{service_name}' created at {file_path}")


def create_domain(domain_name):
    domain_template = get_domain_template(domain_name)

    directory = config.get('domain_destination')
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = f"{directory}/{domain_name}.py"

    with open(file_path, "w") as file:
        file.write(domain_template)

    print(f"Service '{domain_name}' created at {file_path}")


def create_repository(repository_name):
    repository_template = get_repository_template(repository_name)

    directory = config.get('repository_destination')
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = f"{directory}/{repository_name}.py"

    with open(file_path, "w") as file:
        file.write(repository_template)

    print(f"Service '{repository_name}' created at {file_path}")


def create_presentation(presentation_name):
    presentation_template = get_presentation_template(presentation_name)

    directory = config.get('presentation_destination')
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = f"{directory}/{presentation_name}.py"

    with open(file_path, "w") as file:
        file.write(presentation_template)

    print(f"Service '{presentation_name}' created at {file_path}")
