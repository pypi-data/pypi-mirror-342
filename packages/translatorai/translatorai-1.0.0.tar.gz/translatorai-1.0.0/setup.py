from setuptools import setup, find_packages  

setup(  
    name='translatorai',  
    version='1.0.0',  
    packages=find_packages(),  
    install_requires=[ 
        'requests'
    ],  
    author='Redpiar',  
    author_email='Regeonwix@gmail.com',  
    description='easy using AI, more texting models!',  
    long_description=open('README.md').read(),  
    long_description_content_type='text/markdown',
    url='https://github.com/RedPiarOfficial/AiTranslator',
    classifiers=[  
        'Programming Language :: Python :: 3',  
        'License :: OSI Approved :: MIT License',  
        'Operating System :: OS Independent',  
    ],
    keywords=[
        'translation',        
        'translator',
        'google',
        'deepl',
        'amazon',
        'ai',
        'libre'
    ],
    python_requires='>=3.8',  
)  