from setuptools import find_packages, setup

setup(
    name="latch-sdk-gql",
    version="v0.0.7",
    author_email="ayush@latch.bio",
    description="Internal Latch GQL package",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.8,<3.12",
    install_requires=[
        "latch-sdk-config==0.0.4",
        "gql==3.5.0",
        "graphql-core==3.2.3",
        "requests-toolbelt==0.10.1",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
