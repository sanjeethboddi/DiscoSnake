import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
with open("requirements.txt","r") as f:
    required = f.read().splitlines()

setuptools.setup(
    name="DiscoSnake",
    version="0.0.5",
    author="Sanjeeth Boddinagula",
    author_email="sanjeethboddi@gmail.com",
    description="retro snake game in terminal",
    long_description=long_description,
    long_description_content_type="text/markdown",
    scripts=['discosnake'],
    install_requires=required,
    url="https://github.com/sanjeethboddi/DiscoSnake",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
