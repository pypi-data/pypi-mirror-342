from setuptools import setup, find_packages


__version__ = "1.5.2"

with open("README.md", 'r', encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt", 'r', encoding="utf-8") as f:
    required_packages = [line.strip() for line in f.readlines()]

setup(
    name="AllSafe",
    version=__version__,
    packages=find_packages(),
    install_requires=required_packages,
    entry_points={
        "console_scripts": [
            "allsafe=allsafe.main:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: Security",
    ],
    description="AllSafe, A Modern Password Generator",
    author="Mohamad Reza",
    url="https://github.com/emargi/AllSafe",
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls={
        "Source Code": "https://github.com/emargi/Allsafe#readme",
        "Bug Tracker": "https://github.com/emargi/AllSafe/issues",
    },
    keywords="password password-generator tool allsafe generator",
    include_package_data=True,
)
