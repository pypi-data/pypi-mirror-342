from setuptools import setup, find_packages

setup(
    name='pipcentral',  
    version='1.0.0',  
    packages=find_packages(),  
    py_modules=['pipcentral'],
    install_requires=[
        'matplotlib==3.10.1',  
        'networkx==3.4.2',
        'requests==2.32.3',
    ],
    author='Suresh_Pyhobbist', 
    description='PipCentral is your one-stop tool for Python lovers',
    long_description=open('README.md',encoding='utf-8').read(), 
    long_description_content_type='text/markdown',
    url="https://github.com/Suresh-pyhobbyist/pipcentrals", 
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  
    entry_points={
        'console_scripts': [
            'pipcentral=pipcentral:main',  
        ],
    },
)