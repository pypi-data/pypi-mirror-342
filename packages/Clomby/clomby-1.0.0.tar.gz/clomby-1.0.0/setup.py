from setuptools import setup, find_packages

setup(
    name='Clomby',  # Nom de votre package
    version='1.0.0',  # Version initiale de votre package
    packages=find_packages(),  # Recherche de tous les packages Python
    install_requires=[],  # Pas de dépendances externes (random et string sont des modules standards)
    entry_points={
        'console_scripts': [
            'clomby=clomby.password_generator:main',  # Commande clomby dans le terminal
        ],
    },
    author='Arthur Ellies',  # Remplacez par votre nom
    author_email='aellies26@gmail.com',  # Remplacez par votre email
    description='Un générateur de mots de passe interactif et sécurisé.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
