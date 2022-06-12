from setuptools import find_packages
from setuptools import setup

setup(
    name='rate_app',
    description="Ratings",
    author='ortlaz',
    url='',
    # packages=find_packages(''),
    # package_dir={
    #     '': '/'},
    include_package_data=True,
    keywords=[
        'web_app', 'test', 'flask'
    ],
    entry_points={
        'console_scripts': [
            'web_server = app:main']},
)