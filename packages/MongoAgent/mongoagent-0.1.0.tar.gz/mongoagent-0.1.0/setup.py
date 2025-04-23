from setuptools import setup, find_packages

setup(
    name='MongoAgent',
    version='0.1.0',
    author='Drjslab',
    description='An Applicaiton help to communicate with mongo using chatgpt and AI',
    packages=find_packages(),
    install_requires=["pymongo"],  # Add required packages here
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
)
