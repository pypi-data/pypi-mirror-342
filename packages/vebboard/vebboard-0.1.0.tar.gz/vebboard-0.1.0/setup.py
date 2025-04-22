from setuptools import setup, find_packages

setup(
    name='vebboard',
    version='0.1.0',
    author='Твое Имя',
    author_email='you@example.com',
    description='Интерактивная библиотека для создания дашбордов из различных источников данных.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/vebboard',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'openpyxl',
        'gspread',
        'oauth2client',
        'matplotlib',
        'plotly',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
