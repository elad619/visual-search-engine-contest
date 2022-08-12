import requests
import re
from urllib.parse import urlsplit, parse_qs


def download_image(id: str, collection_type: str):
    try:
        docID, ie = get_image_identifiers(id, collection_type)
        download_and_save_file(
            f'https://download.nli.org.il/DownloadNliWebServices/download/downloadIE?docId={docID}&ie={ie}&format=ZIP&resolution=MEDIUM&lang=HE',
            f'{docID}_{ie}.zip')
    except Exception as e:
        print(f"Error downloading image {id}: {e}")


def get_image_identifiers(id: str, collection_type: str):
    api_url = "https://api.nli.org.il/openlibrary/search"
    params = {"api_key": "CINMvDJAfuHpfdHIMBOuxTEJIEryA9MUs0XGZqmD",
              "query": "any,contains,{}".format(id),
              "output_format": "json",
              "sortField": "title",
              "material_type": collection_type
              }
    response = requests.get(api_url, params=params)
    response_json = response.json()[0]
    identifier = response_json["http://purl.org/dc/elements/1.1/identifier"][0]['@value']
    download_url = response_json["http://purl.org/dc/elements/1.1/download"][0]['@value']

    ie = parse_identifiers_from_download_url(download_url)
    return identifier, ie


def parse_identifiers_from_download_url(download_url):
    download_query = urlsplit(download_url).query
    params = parse_qs(download_query)
    return params["ie"][0]


def download_and_save_file(url, local_filename):
    with requests.get(url, stream=True) as r:
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename


if __name__ == "__main__":
    docID, ie = get_image_identifiers("990031597000205171", "manuscript")
    download_and_save_file(
        f'https://download.nli.org.il/DownloadNliWebServices/download/downloadIE?docId={docID}&ie={ie}&format=ZIP&resolution=MEDIUM&lang=HE',
        f'{docID}_{ie}.zip')
