from setuptools import setup, find_packages

setup(
    name='os_code_mypack',
    version='0.5',
    packages=find_packages(),
    include_package_data=True,  # Important!
    install_requires=[],
    entry_points={
        "console_scripts": [
            "show-codes=os_code_mypack.main:show_codes",
        ],
    },
    package_data={
        "os_code_mypack": ["codes.txt"],  # Include the file here
    },
)