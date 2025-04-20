from setuptools import setup, find_packages

setup(
    name="blackmagiccoll",
    version="0.1.4",
    packages=find_packages(),
    include_package_data=True,  # important!
    package_data={
        "blackmagiccoll": ["datasets/*.xslsx"]
    },
)
