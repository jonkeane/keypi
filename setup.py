import pathlib

import setuptools

install_requires = [
    line.strip()
    for line in pathlib.Path(__file__)
    .parent.joinpath("requirements.txt")
    .read_text()
    .splitlines()
]

setuptools.setup(
    name="keypi",
    version="0.0.1",
    description="KeyPi Keyboard Emulator",
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": [
            "keypi=keypi.cli:keypi",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GPL",
    ],
    python_requires=">=3.8",
    install_requires=install_requires,
    maintainer="Jonathan Keane",
    url="https://github.com/jonkeane/keypi",
)
