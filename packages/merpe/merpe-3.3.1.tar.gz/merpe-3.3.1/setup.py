from setuptools import setup, find_packages

setup(
    name="merpe",
    version="3.3.1",  # Higher version than the private package
    packages=find_packages(),
    description="Educational demonstration of dependency confusion",
    author="BEKHTI DJALAL",
    author_email="d.bekhti@esi-sba.dz",
    url="https://github.com/merzouka/dependency-confusion.security/blob/main/malicious/src/merbe",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
    ],
)