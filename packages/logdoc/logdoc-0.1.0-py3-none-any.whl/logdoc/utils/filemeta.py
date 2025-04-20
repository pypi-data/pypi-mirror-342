# logdoc/utils/filemeta.py
import os
from datetime import datetime

def get_file_metadata(path):
    stats = os.stat(path)
    return {
        "created": datetime.fromtimestamp(stats.st_ctime),
        "modified": datetime.fromtimestamp(stats.st_mtime)
    }