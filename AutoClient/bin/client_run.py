import os

BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.path.join(BASEDIR)

from src.client import client

if __name__ == '__main__':
    client()