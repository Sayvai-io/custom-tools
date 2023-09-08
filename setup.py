from setuptools import setup, find_packages
from src.tools import __version__

core_requirements = [
    'langchain',
    'llama_index',
    'google-api-python-client',
    'openai',
]

setup(
    name='tools',
    version=__version__,
    description='Tools for the assistant',
    author='sayvai-io',
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=core_requirements,
    extras_require={
        'dev': [
            'pytest',
            'pylint',
        ],
    },
    zip_safe=False
)
    