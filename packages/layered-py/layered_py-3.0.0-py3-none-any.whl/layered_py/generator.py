from layered_py.shared import create_service, create_domain, create_repository, create_presentation


def generate(name):
    formatted_name = name.lower()

    create_service(f"{formatted_name}_service")
    create_domain(f"{formatted_name}")
    create_repository(f"{formatted_name}_repository")
    create_presentation(f"{formatted_name}_routes")