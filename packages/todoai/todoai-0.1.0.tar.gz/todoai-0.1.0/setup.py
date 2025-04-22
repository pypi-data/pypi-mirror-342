from setuptools import setup,find_packages
setup(
    name="taskAI",
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        "phidata",
        "langchain-google-genai",
        "langchain"
    ],
    author='Manush Sanchela', 
    author_email='manushsanchela796@gmail.com',  
    description='A simple AI toolset powered by Gemini models',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/smartai',  
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.7',
)