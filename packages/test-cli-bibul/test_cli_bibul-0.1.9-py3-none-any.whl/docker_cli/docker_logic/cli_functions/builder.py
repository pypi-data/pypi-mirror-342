# File to build the image

from pathlib import Path
from jinja2 import Environment, FileSystemLoader


CURRENT_DIR = Path(__file__).resolve().parent
DOCKERFILE_TEMPLATE_DIR = CURRENT_DIR.parent / "templates"


# Two options possible : either give acces to the created dockerfile, but then arises the issue of the conf files to reach
# DOCKERFILE_OUTPUT_PATH = Path("Dockerfile")  # On écrase le Dockerfile à la racine

# Or completely blind the user, have the dockerfile where it has acces by prebuilt paths to files
DOCKERFILE_OUTPUT_PATH = Path("./Dockerfile")

def build_image(name: str, base_image: str , include_probayes: bool = False, extra_packages: list[str] = None):
    env = Environment(loader=FileSystemLoader(DOCKERFILE_TEMPLATE_DIR))
    template = env.get_template("Dockerfile.j2")

    rendered = template.render(
        with_probayes=include_probayes,
        base = base_image,
        image_name = name,
        extra_packages = extra_packages
    )

    DOCKERFILE_OUTPUT_PATH.write_text(rendered)

    print(f"Dockerfile généré avec succès à {DOCKERFILE_OUTPUT_PATH.resolve()}")
    print(" ")
    print("Tu peux maintenant le construire avec:")
    print(f"  docker build -t {name} .")