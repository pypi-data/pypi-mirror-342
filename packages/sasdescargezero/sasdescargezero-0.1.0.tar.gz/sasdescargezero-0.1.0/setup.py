from setuptools import setup, find_packages

setup(
    name="sasdescargezero",
    version="0.1.0",
    author="Sas",
    author_email="ri6k751ni@nine.testrun.org",
    description="Una librería Python para descargar archivos desde un host específico",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/tuusuario/sas",
    packages=find_packages(),
    install_requires=[
        "requests>=2.28.0",
        "beautifulsoup4>=4.11.0",
        "urllib3>=1.26.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
