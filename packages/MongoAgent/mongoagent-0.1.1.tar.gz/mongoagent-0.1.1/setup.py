from setuptools import setup, find_packages
with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='MongoAgent',
    version='0.1.1',
    author='Drjslab',
    description='An Applicaiton help to communicate with mongo using chatgpt and AI',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["pymongo"],  # Add required packages here
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
)
