""" Generate a public domain dataset using
    https://publicdomainvectors.org/
"""
from urllib.request import Request, urlopen
from pathlib import Path
from zipfile import ZipFile
import time
import tqdm
import re

DATA_DIR = Path("data")
SVG_DIR = DATA_DIR / "publicdomainvectors" / "svg"
SVG_DIR.mkdir(exist_ok=True, parents=True)


def get_filenames_from_webpage(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    result = re.findall("tn_img\/([0-9a-zA-Z_\-\.]+)\.(png|jpg)", str(webpage))
    return [str(r[0]) for r in result]


def download_svg(filename):
    # download the zip file
    svg_path = SVG_DIR / f'{filename}.svg'
    if svg_path.exists():
        return True
    url = f'https://publicdomainvectors.org/download.php?file={filename}.zip'
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    file = urlopen(req).read()
    tmpZipPath = DATA_DIR / f'{filename}.zip'
    with open(tmpZipPath, "wb") as f:
        f.write(file)

    # extract the zip to get the svg
    try:
        zipFile = ZipFile(tmpZipPath)
        svgs_in_zip = [fname for fname in zipFile.namelist() if ".svg" in fname]
        if len(svgs_in_zip) > 0:
            svg_bytes = zipFile.read(svgs_in_zip[0])
            with open(svg_path, "wb") as f:
                f.write(svg_bytes)
    except Exception as e:
        print(e)
        print(f'Unable to fetch {filename}')
        return False
    tmpZipPath.unlink()
    return True


if __name__ == "__main__":
    file_names = []
    for i in range(1, 35):
        file_names += get_filenames_from_webpage(f'https://publicdomainvectors.org/en/free-clipart/date/svg/1000/{i}')
        time.sleep(0.3)
    for name in tqdm.tqdm(file_names):
        success = download_svg(name)
        time.sleep(0.1)
