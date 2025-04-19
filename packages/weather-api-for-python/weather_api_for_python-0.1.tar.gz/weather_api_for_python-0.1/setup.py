from setuptools import setup, find_packages

setup(
    name='weather_api_for_python',
    version='0.1',
    packages=find_packages(),
    install_requires=['requests'],
    author='Даниил',
    author_email='krestaninovdaniil@gmail.com',
    description='API для получения погоды',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/daniilkrestyaninov/weather_for_python',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
