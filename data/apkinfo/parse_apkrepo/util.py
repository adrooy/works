import hashlib


def get_md5(buf):
    m = hashlib.md5()
    m.update(buf)
    return m.hexdigest().lower()


def get_file_md5(file):
    fh = open(file, "rb")
    rtn = get_md5(fh.read())
    fh.close()
    return rtn

