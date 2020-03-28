""" Generate a public domain dataset using
    https://publicdomainvectors.org/
"""
from urllib.request import Request, urlopen
from pathlib import Path
from zipfile import ZipFile
from utils.file_collection import FileCollection
from tempfile import NamedTemporaryFile
import time
import tqdm
import re

def get_filenames_from_webpage(url):
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    webpage = urlopen(req).read()
    result = re.findall("tn_img\/([0-9a-zA-Z_\-\.]+)\.(png|jpg)", str(webpage))
    return [str(r[0]) for r in result]


def download_svg(filename):
    """ Return svg bytes from a filename from publicdomainvectors or None if problem happens.
    """
    url = f"https://publicdomainvectors.org/download.php?file={filename}.zip"
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    file = urlopen(req).read()
    tmpZipFile = NamedTemporaryFile(suffix=".zip")
    tmpZipFile.write(file)

    # extract the zip to get the svg
    try:
        zipFile = ZipFile(tmpZipFile.name)
        svgs_in_zip = [fname for fname in zipFile.namelist() if ".svg" in fname]
        if len(svgs_in_zip) > 0:
            return zipFile.read(svgs_in_zip[0])
    except Exception as e:
        url = f"https://publicdomainvectors.org/download.php?file={filename}.svg"
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        bytes = urlopen(req).read()
        if len(bytes) > 0:
            return bytes
    return None


if __name__ == "__main__":
    file_collection = FileCollection(Path("data") / "publicdomainvectors")

    file_names = []
    for i in range(1, 35):
        file_names += get_filenames_from_webpage(
            f"https://publicdomainvectors.org/en/free-clipart/date/svg/1000/{i}"
        )
        print(i)
        time.sleep(0.3)

    for i, name in enumerate(tqdm.tqdm(file_names)):
        fullname = name + ".svg"
        if file_collection.has_filename(fullname):
            continue
        svg_bytes = download_svg(name)
        if svg_bytes is None:
            file_collection.add_metadata(fullname, "status", "Unable to download")
        else:
            location = file_collection.get_disk_filepath(fullname)
            with open(location, "wb") as f:
                f.write(svg_bytes)
            file_collection.add_metadata(fullname, "status", "Unable to download")
        if i % 10 == 0:
            file_collection.sync()
