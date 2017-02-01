import click
from hodor import Hodor
import os
from PIL import Image, ImageDraw, ImageFont
import requests
from urlparse import urlparse


from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
DOWNLOAD_FOLDER = 'favicons/'


def download_image(url, filename):
    r = requests.get(url, stream=True)
    with open(os.path.join(DOWNLOAD_FOLDER, filename), 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()


@click.command()
@click.argument("url", type=str, required=True)
def cli(url):
    """This script grabs the favicons from the entered URL and displays the dimension, file format and URL of the favicon."""
    url = str(url)
    parsed_uri = urlparse(url)
    if bool(parsed_uri.scheme) and bool(parsed_uri.netloc):
        try:
            click.echo("Loading... Please Wait!")
            CONFIG = {'favicon': {
                'xpath': '//link[@rel="icon" or @rel="shortcut icon"]/@href', 'many': True}}

            h = Hodor(url=url, config=CONFIG)

            full_name = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
            domain_name = '{uri.netloc}'.format(uri=parsed_uri).replace("www.", "")
            favicons = set(h.data["favicon"])
            if favicons:
                for icon in favicons:
                    if not os.path.exists(DOWNLOAD_FOLDER):
                        os.mkdir(DOWNLOAD_FOLDER)
                    ext = os.path.splitext(icon)[1]
                    filename = domain_name + "-favicon" + ext
                    try:
                        download_image(icon, filename)
                        image_url = icon
                    except:
                        download_image(full_name + icon, filename)
                        image_url = full_name + icon
                    try:
                        with Image.open(os.path.join(DOWNLOAD_FOLDER, filename)) as im:
                            width, height = im.size
                        dimensions = str(width) + 'x' + str(height)
                        click.echo("Dimensions: " + dimensions)
                        click.echo("File Format: " + ext)
                        click.echo("Url: " + image_url)
                    except:
                        click.echo(
                            "Unexpected error occured while loading the image!")
            else:
                ext = ".png"
                filename = domain_name + "-favicon" + ext
                first_char = domain_name[0].upper()
                width, height = 114, 114
                font = ImageFont.truetype("Arial.ttf", 80)
                img = Image.new('RGB', (width, height), (0, 0, 255))
                canvas = ImageDraw.Draw(img)
                text_width, text_height = canvas.textsize(first_char, font=font)
                canvas.text(((width - text_width) / 2, 15),
                            first_char, fill=(255, 255, 255), font=font)
                if not os.path.exists(DOWNLOAD_FOLDER):
                    os.mkdir(DOWNLOAD_FOLDER)
                img.save(os.path.join(DOWNLOAD_FOLDER, filename))
                click.echo(
                    "No favicon found. Generated favicon can be found in /favicons with the name: " + filename)
        except:
            click.echo("Unexpected Error Occurred!")
    else:
        click.echo("Error: Invalid URL")
