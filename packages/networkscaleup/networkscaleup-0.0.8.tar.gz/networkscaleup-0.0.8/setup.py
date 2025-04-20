from setuptools import setup, find_packages

setup(
    name="networkscaleup",  
    version='0.0.8',           
    packages=find_packages(where='src'),  
    package_dir={'': 'src'},   
    install_requires=[         
        'numpy',
        'pandas',
    ],
    author='Sarah Nagy', 'Ian Laga',        
    author_email='s.nagy.4343@gmail.com', 'ian.laga@montana.edu'  
    description='A Python package for network scale-up models',  
    long_description=open('README.md').read(),  
    long_description_content_type='text/markdown',  
    url='https://github.com/yourusername/killworth-package',  
    classifiers=[              
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  
)
