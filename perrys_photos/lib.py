from dataclasses import dataclass
import shutil
import os


from PIL import Image
from jinja2 import Environment, FileSystemLoader



@dataclass
class Config():
    pic_source_dir: str = "images"
    pic_target: str = "public/img/orig"
    pic_thumb: str = "public/img/thumb"
    thumb_width: int = 400
    def file_path(self, filename: dir, dir: str)->str:
        return f"{dir}/{filename}"

    def web_path(self, filename: dir, dir: str)->str:
        path = self.file_path(filename, dir)
        return path.replace("public/","")

@dataclass
class Photo():
    orig: str
    orig_width: int
    orig_height: int
    thumb: str
    thumb_width: int
    thumb_height: int


def copy_img(filename: str, config: Config):
    source_path = config.file_path(filename, config.pic_source_dir)
    target_path = config.file_path(filename, config.pic_target)

    shutil.copyfile(source_path, target_path)


def get_photos(images: list, config: Config):
    out = []
    for img in sorted(images, reverse=True):
        source_path = config.file_path(img, config.pic_source_dir)
        local_thumb_path = config.file_path(img, config.pic_thumb)
        pillow_img = Image.open(source_path)
        pillow_thumb = Image.open(local_thumb_path)
        orig_width, orig_height = pillow_img.size
        thumb_width, thumb_height = pillow_thumb.size
        orig_path = config.web_path(img, config.pic_target)
        thumb_path = config.web_path(img, config.pic_thumb)
        photo = Photo(orig_path, orig_width, orig_height, thumb_path, thumb_width, thumb_height)
        out.append(photo)
    
    return out

def generate_index(photos, config):
    env = Environment(
        loader=FileSystemLoader('templates'),
    )
    with open("public/index.html", mode="w") as index_file:
        template = env.get_template("index.html.j2")
        data = {
            "photos": photos,
            "config": config
        }
        index_file.write(template.render(**data))

def thumb_size(orig_width, orig_height, config: Config):
    thumb_width = config.thumb_width
    thumb_height = thumb_width * 3/2
    if orig_width > orig_height:
        # thumb_width = thumb_width * 2
        # thumb_height = thumb_width * 2/3
        # thumb_height = thumb_width
        thumb_width = thumb_height *3/2

    return(thumb_width, thumb_height)

def generate_thumb(filename: str, config: Config)-> str:
    source_path = config.file_path(filename, config.pic_source_dir)
    img = Image.open(source_path)
    orig_width, orig_height = img.size
    thumb_width, thumb_height = thumb_size(orig_width, orig_height, config)
    thumbs_path = config.file_path(filename, config.pic_thumb)
    # todo: from config, smarter, per image size
    img.thumbnail((thumb_width, thumb_height))
    img.save(thumbs_path)
    return thumbs_path

def list_source_images(config:Config)->list:
    imgs = os.listdir(config.pic_source_dir)
    return imgs

def ensure_dirs(config: Config)->None:
    dirs = [
        config.pic_source_dir,
        config.pic_target,
        config.pic_thumb,
        "public/photoswipe"
    ]
    for dir in dirs:
        os.makedirs(dir, exist_ok=True)

def copy_static(config: Config):
    for filename in os.listdir("static/photoswipe"):
        shutil.copy(f"static/photoswipe/{filename}","public/photoswipe")