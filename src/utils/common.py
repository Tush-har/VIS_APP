import zipfile

def is_valid_zip(zip_path: str) -> bool:
    try:
        with zipfile.ZipFile(zip_path, 'r') as z:
            bad_file = z.testzip()
            return bad_file is None
    except Exception:
        return False
