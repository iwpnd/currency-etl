from setuptools import setup

packages = ["currencyetl"]

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="currencyetl",
    version="0.0.1",
    description="download and store currency conversion rates",
    url="http://github.com/iwpnd/toponym",
    author="Benjamin Ramser",
    author_email="ahoi@iwpnd.pw",
    license="MIT",
    include_package_data=True,
    install_requires=required,
    packages=packages,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Data Scientists",
    ],
)
