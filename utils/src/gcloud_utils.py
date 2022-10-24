from gcsfs import GCSFileSystem

def write_to_gcs_file(path, content):
    if path.startswith("gs://"):
        path = path[5:]
    fs = GCSFileSystem()
    with fs.open(path, 'w') as f:
        f.write(content)
    f.close()