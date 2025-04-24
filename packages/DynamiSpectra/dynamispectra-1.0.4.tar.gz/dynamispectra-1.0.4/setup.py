from setuptools import setup, find_packages

setup(
    name='DynamiSpectra',
    version='1.0.4',
    packages=find_packages(where="src"),  
    package_dir={"": "src"},            
    install_requires=[
        'numpy>=1.26.4',
        'matplotlib>=3.8.4',
        'pandas>=1.3.0',
        'scipy>=1.13.1',
    ],
    entry_points={
        'console_scripts': [
            'dynami=main:main', 
        ],
    },
    author='Iverson Conrado-Bezerra',
    author_email='iverson.coonrado@gmail.com',
    description='Scripts for Molecular dynamics analysis',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Conradoou/DynamiSpectra',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)