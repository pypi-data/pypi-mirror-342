from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="gadfasthealth",
    version="0.0.1",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={},
    author="Alexander Grishchenko",
    author_email="alexanderdemure@gmail.com",
    description="FastAPI health check extension for Kubernetes liveness, readiness, and startup probes.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/AlexDemure/gadfasthealth",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)