from setuptools import setup, find_packages

setup(
    name="aadish",
    version="1.1.2",
    description="Aadish: An advanced and highly capable AI assistant module.",
    author="Aadish",
    author_email="aadish14146yadav@gmail.com",
    packages=find_packages(),
    install_requires=[
        "requests",
        "colorama",
        "rich",
        "pyfiglet"
    ],
    python_requires=">=3.7",
    url="https://pypi.org/project/aadish/",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
)
