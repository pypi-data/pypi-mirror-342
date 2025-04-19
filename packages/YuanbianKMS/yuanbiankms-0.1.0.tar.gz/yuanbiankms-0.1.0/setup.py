from setuptools import setup, find_packages

setup(
    name='YuanbianKMS',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'flask',
        'flask-login',
        'flask-sqlalchemy',
        'flask-jwt' ],
    entry_points={
        'console_scripts': [
            'yuanbiankms = app:main',
            'yuanbiankms run = app:run',
        ],
    },
)