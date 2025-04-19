from setuptools import setup, find_packages  # type: ignore


with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="jb-scraper",
    version="0.0.6",
    author="Lucas Aquino",
    author_email="lc.aquinodeoliveira@gmail.com",
    description="JobScraper, um pacote de raspagem de vagas na internet.",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ClausAlaerth/jobscraper-package",
    packages=find_packages(),
    install_requires=requirements,
    python_requires=">=3.12",
)
