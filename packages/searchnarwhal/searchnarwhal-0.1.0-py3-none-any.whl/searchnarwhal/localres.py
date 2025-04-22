# searchnarwhal/localres.py

def convert_to_path(url):
    # Remove localres: prefix and clean path
    return url.replace("localres:", "", 1)
