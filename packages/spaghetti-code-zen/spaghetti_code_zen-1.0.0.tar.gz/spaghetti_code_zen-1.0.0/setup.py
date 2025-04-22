
from pathlib import Path
from setuptools import setup

directory = Path(__file__).resolve().parent
with open(directory / "README.md", encoding="utf-8") as f:
    long_description = f.read()


setup(name="spaghetti-code-zen",
      version="1.0.0",
      author="u2084511felix & osinmv",
      license="MIT",
      long_description=long_description,
      long_description_content_type="text/markdown",
      packages=["spaghetti-code-zen"],
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License"
      ],
      install_requires=[],
      python_requires='>=3.10',
      include_package_data=False
)
