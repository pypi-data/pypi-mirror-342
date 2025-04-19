from setuptools import setup, find_packages

setup(
    name="cinol",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pycryptodome>=3.15.0",
        "astunparse>=1.6.3",
    ],
    extras_require={
        "dev": ["pytest", "cython"],
    },
    author="Cansila",
    author_email="eternals.tolong@gmail.com",
    description="Python Code Protection Toolkit",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    keywords="obfuscation encryption license protection",
    url="https://github.com/Eternals-Satya/cinol",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
