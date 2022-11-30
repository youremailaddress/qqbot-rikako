import os

def baseDir():
    return os.path.abspath(os.path.join(os.path.join(os.path.split(os.path.realpath(__file__))[0],os.path.pardir),os.path.pardir))

def getDir(path):
    return os.path.abspath(os.path.join(baseDir(),path))

def pathExists(path):
    return os.path.exists(path)