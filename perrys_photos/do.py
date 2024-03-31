
import typer
from rich import print
from perrys_photos.lib import copy_img, ensure_dirs, generate_index, generate_thumb, Config, get_photos, list_source_images

app = typer.Typer()

@app.command()
def images():
    conf = Config()
    ensure_dirs(conf)
    imgs = list_source_images(conf)
    for img in imgs:
        copy_img(img, conf)
        thumb_path = generate_thumb(img, conf)
        print(thumb_path)


@app.command()
def pub():
    conf = Config()
    imgs = list_source_images(conf)
    photos = get_photos(imgs, conf)
    generate_index(photos, conf)

