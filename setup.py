from setuptools import setup, find_packages

core_requirements = [
    'langchain',
    'langchain_experimental',
    'google-api-python-client',
    'openai',
    'SQLAlchemy',
    'elevenlabs==0.2.24',
    'google_auth_oauthlib',
    'google-auth-httplib2',
    'pyaudio-wheels',
    'pydub',
    'numpy',
    'google',
    'google-cloud-speech',
    'cloud-sql-python-connector',
    'pg8000',

]

setup(
    name='sayvai_tools',
    version='0.0.1',
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
    
