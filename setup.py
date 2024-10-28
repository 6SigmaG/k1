from setuptools import setup

APP = ['kkk.py']
OPTIONS = {
    'argv_emulation': True,
    'packages': ['pandas', 'openpyxl'],
    'includes': ['itertools', 'datetime', 'os'],
    'resources': ['keywords.xlsx'],
    'plist': {
        'CFBundleName': "搜索指令严格组合版",
        'CFBundleShortVersionString': "1.0",
        'CFBundleIdentifier': "com.search.strict",
    }
}

setup(
    name="搜索指令严格组合版",
    app=APP,
    data_files=['keywords.xlsx'],
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)