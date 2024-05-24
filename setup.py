from setuptools import setup, find_packages

setup(
    name='smart-trajectories',
    version='0.1.18',  # Atualize para uma nova versão
    author='Felipe Brito',
    author_email='arrudabritofelipe@gmail.com',
    description='Smart Trajectories for Python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/britofelipe/smart-trajectories',
    packages=find_packages(),
    install_requires=[
        'attrs==23.2.0',
        'certifi==2024.2.2',
        'click==8.1.7',
        'click-plugins==1.1.1',
        'cligj==0.7.2',
        'contourpy==1.2.1',
        'cycler==0.12.1',
        'fiona==1.9.6',
        'fonttools==4.51.0',
        'geographiclib==2.0',
        'geopandas==0.13.2',
        'geopy==2.3.0',
        'kiwisolver==1.4.5',
        'matplotlib==3.7.1',
        # 'movingpandas==0.18.1',  # Não suportado
        'numpy==1.25.2',
        'packaging==24.0',
        'pandas==2.0.3',
        'pillow==9.4.0',
        'pyparsing==3.1.2',
        'pyproj==3.6.1',
        'python-dateutil==2.8.2',
        'pytz==2023.4',
        'Rtree==1.2.0',
        'shapely==2.0.4',
        'six==1.16.0',
        'tzdata==2024.1',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)