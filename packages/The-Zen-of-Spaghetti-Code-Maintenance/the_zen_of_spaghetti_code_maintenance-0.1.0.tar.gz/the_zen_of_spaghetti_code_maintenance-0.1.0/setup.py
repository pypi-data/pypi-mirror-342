
from pathlib import Path
from setuptools import setup

directory = Path(__file__).resolve().parent
with open(directory / "README.md", encoding="utf-8") as f:
    long_description = f.read()


setup(name="The_Zen_of_Spaghetti_Code_Maintenance",
      version="0.1.0",
      author="u2084511felix & osinmv",
      license="MIT",
      long_description=long_description,
      long_description_content_type="text/markdown",
      packages=["The_Zen_of_Spaghetti_Code_Maintenance"],
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License"
      ],
      install_requires=[],
      python_requires='>=3.10',
      include_package_data=False
)
