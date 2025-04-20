from setuptools import setup, find_packages

setup(
    name="yagamicore",  # <-- New unique name
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    description="A simple library for handling text files",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Anonymous",
    author_email="ifYoucanFindMe@gmail.com",
    url="https://github.com/your-username/yagamicore",  # <-- Make sure this matches the new repo (if updated)
)
