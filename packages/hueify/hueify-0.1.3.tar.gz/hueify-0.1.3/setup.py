from setuptools import setup, find_packages

setup(
    name="hueify",
    version="0.1.3",
    description="Python bib to control Philips Hue lights and groups.",
    author="Mathis Arends",
    url="https://github.com/mathisarends/hueify",
    packages=find_packages(),
    install_requires=[
        "aiohttp>=3.11.0",
        "python-dotenv>=1.0.0",
        "rapidfuzz==3.13.0",
    ],
    include_package_data=True,
    python_requires=">=3.7",
    license="MIT",
)
