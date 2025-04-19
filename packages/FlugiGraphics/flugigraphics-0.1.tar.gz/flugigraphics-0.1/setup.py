from setuptools import setup, find_packages

setup(
    name='FlugiGraphics',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pygame',
    ],
    author='Bárány Szilveszter, Domokos Kyra, Végh Ákos',
    author_email='barany.szilveszter@hallgato.ppke.hu, domokos.kira@hallgato.ppke.hu, vegh.akos@hallgato.ppke.hu',
    description='flugigraphics in python dudes',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/itssyp/flugiGraphicsInPython',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)