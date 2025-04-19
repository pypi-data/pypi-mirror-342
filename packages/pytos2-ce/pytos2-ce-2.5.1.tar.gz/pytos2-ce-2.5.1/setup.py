import os

from setuptools import setup, find_namespace_packages


with open(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "README.md")
) as file:
    long_description = file.read()

setup(
    name="pytos2-ce",
    long_description=long_description,
    long_description_content_type="text/markdown",
    description="Pytos2 for tos1 tos2 and beyond",
    packages=find_namespace_packages(include=["pytos2*"]),
    use_scm_version=True,
    setup_requires=["setuptools_scm<7"],
    install_requires=[
        "requests<3",
        "traversify",
        "attrs>=19.2,<20",
        "python-json-logger<0.2",
        "netaddr<=0.10",
        "typing_extensions",
        "python-dateutil>=2.8,<3",
        "requests-oauthlib",
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
            "pytest-logger",
            "responses",
            "black",
            "tox",
            "ruff",
        ],
        "dev-jupyter": ["black[jupyter]", "pre-commit", "nb-clean"],
    },
    test_suite="tests",
    package_data={"pytos2": ["py.typed"]},
)
