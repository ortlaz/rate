from setuptools import find_packages
from setuptools import setup

setup(
    name='simple_web_app',
    description="Simple web app for test CI",
    author='ortlaz',
    url='',
    packages=find_packages(''),
    package_dir={
        '': ''},
    include_package_data=True,
    keywords=[
        'web_app', 'test', 'flask'
    ],
    entry_points={
        'console_scripts': [
            'web_server = app:main']},
)