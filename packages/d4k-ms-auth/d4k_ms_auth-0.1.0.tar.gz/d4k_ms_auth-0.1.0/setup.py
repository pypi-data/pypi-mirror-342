from setuptools import setup, find_packages

setup(
    name="d4k_ms_auth",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "auth0-python==4.7.2",
        "Authlib==1.3.1",
        "d4k_ms_base==0.1.0",
        "fastapi==0.111.0",
    ],
    extras_require={
        "dev": [
            "pytest==8.2.2",
            "pytest-cov==4.1.0",
            "pytest-mock==3.14.0",
            "pytest-asyncio==0.26.0",
        ],
    },
    python_requires=">=3.8",
)
