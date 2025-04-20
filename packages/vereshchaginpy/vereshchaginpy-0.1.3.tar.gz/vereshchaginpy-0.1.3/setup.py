from setuptools import setup, find_packages

setup(
    name='vereshchaginpy',
    version='0.1.3',
    author='Julian Haudek',
    author_email='julianhaudek@gmail.com',
    description='Graph-based integration for structural mechanics using the Vereshchagin method',
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url='https://github.com/Haudkozaur/VereshchaginPy',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "matplotlib",
        "numpy"
    ],
    python_requires=">=3.7",
)
