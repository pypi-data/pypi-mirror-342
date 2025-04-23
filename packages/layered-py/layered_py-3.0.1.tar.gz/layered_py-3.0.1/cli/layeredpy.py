import sys

from layered_py.generator import generate
from layered_py.shared import create_service, create_domain, create_repository

commands = ['createService', 'createDomain', 'createRepository', 'generate']
def main():
    if len(sys.argv) != 3 or sys.argv[1] not in commands:
        print("Possible commands are:")
        for command in commands:
            print(command)
        sys.exit(1)

    command, name = sys.argv[1], sys.argv[2]
    match command:
        case "createService":
            create_service(name)
        case "createDomain":
            create_domain(name)
        case "createRepository":
            create_repository(name)
        case "generate":
            generate(name)

if __name__ == "__main__":
    main()