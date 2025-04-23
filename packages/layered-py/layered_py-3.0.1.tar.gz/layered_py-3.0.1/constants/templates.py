def get_service_template(service_name):
    pascal_name = to_pascal_case(service_name)

    service_template = f"""from layered_py.service import Service
from layered_py.decorators import register

@register(singleton=True)
class {pascal_name}(Service):
    def setup(self):
        super().__init__()

    def handle(self):
        raise NotImplementedError
        """
    return service_template

def get_domain_template(domain_name):
    pascal_name = to_pascal_case(domain_name)

    domain_template = f"""from layered_py.domain import BaseDomain
from layered_py.decorators import register
    
@register(singleton=True)
class {pascal_name}(BaseDomain):
    def __init__(self):
        super().__init__()
        """
    return domain_template

def get_repository_template(repository_name):
    pascal_name = to_pascal_case(repository_name)

    repository_template = f"""from layered_py.repository import BaseRepository
from layered_py.decorators import register

@register(singleton=True)
class {pascal_name}(BaseRepository):
    def __init__(self):
        super().__init__()
        """
    return repository_template

def get_presentation_template(presentation_name):
    pascal_name = to_pascal_case(presentation_name)

    presentation_template = f"""from layered_py.presentation import BasePresentation
from layered_py.decorators import register

@register(singleton=True)
class {pascal_name}(BasePresentation):
    def __init__(self):
        super().__init__()
        """
    return presentation_template

def to_pascal_case(snake_str):
    return ''.join(word.capitalize() for word in snake_str.split('_'))
