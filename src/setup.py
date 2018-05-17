"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['MainWindow.py']
APP_NAME = "Librarian"
DATA_FILES = ['Data.db', 'Pics']
OPTIONS = {
    'argv_emulation': True,
    #'iconfile': 'app.icns',
    'iconfile': 'Pics/icon.icns',
    'plist': {
        'CFBundleName': APP_NAME,
        'CFBundleDisplayName': APP_NAME,
        'CFBundleGetInfoString': "Reference Management",
        'CFBundleIdentifier': "com.liutairan.osx.librarian",
        'CFBundleVersion': "0.0",
        'CFBundleShortVersionString': "0.0",
        'NSHumanReadableCopyright': u"Copyright © 2018, Tairan Liu, All Rights Reserved",
        'PyRuntimeLocations': [
                '@executable_path/../Frameworks/libpython3.4m.dylib',
                '/Users/liutairan/anaconda/envs/python3/lib/libpython3.4m.dylib'
                #'/Library/Frameworks/Python.framework/Versions/3.4/lib/libpython3.4m.dylib'
               ]
}
}
setup(
    name=APP_NAME,
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)