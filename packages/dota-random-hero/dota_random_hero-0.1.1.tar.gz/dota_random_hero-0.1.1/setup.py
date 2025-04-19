from setuptools import setup, find_packages

setup(
    name="dota-random-hero",
    version="0.1.1",
    packages=find_packages(),
    description="Случайный герой Dota 2",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Рауль",
    author_email="warface12452@mail.ru",
    url="https://github.com/ваш-username/dota2-random-hero",
    license="MIT",
    python_requires=">=3.6",
    install_requires=[], 
    keywords=["dota2", "random", "game"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)