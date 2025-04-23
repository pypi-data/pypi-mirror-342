# setup.py

from setuptools import setup, find_packages

setup(
    name='os_code_mypack',
    version='0.3',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [  # <-- fix "console-scripts" to "console_scripts"
            "show-codes=os_code_mypack.main:show_codes",
        ],
    },
)
