from setuptools import setup, find_packages

setup(
    name='jsonschema_explorer',  
    version='0.1.0',
    description='A tool to parse JSON and extract schema',
    author='Sam Farrant',
    author_email='samuel.farrant@gmail.com',
    license='MIT',
    url='https://github.com/s-farrant/jsonschema_explorer',
    packages=find_packages(),
    install_requires=[],
    python_requires='>=3.6',
)