import setuptools
import os

FILE_PATH = os.path.dirname(os.path.abspath(__file__))
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# 读取requirements.txt文件
requirements_path = os.path.join(FILE_PATH, 'requirements.txt')
with open(requirements_path, 'r') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="GWRExplain",
    version="0.0.2",
    author="ChiBeiSheng",
    url='https://github.com/cbsux/GWRExplain',
    author_email="cbs3307821258@foxmail.com",
    description="GWRExplain is a method that combines Geographically Weighted Regression (GWR) with explainability techniques to reveal how local variables influence prediction outcomes in spatial data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    package_data={'': ['*.txt', '*.md']},
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10.0",
)
# twine upload -r pypi dist/* --username __token__ --password pypi-AgEIcHlwaS5vcmcCJGFkOGM3MTY0LTdiYWEtNGZlNi1iMjNmLWI3ZGIzOTU2ZjliNgACKlszLCI1OGM2NDMyZi05OTU0LTQ1OGMtYThmZi04MGVmZmEwNTgxNzUiXQAABiALSMT3kfmH_AJy5mzGRQ2TxgYzWWXETfpAXLxbAhAoGg --verbose