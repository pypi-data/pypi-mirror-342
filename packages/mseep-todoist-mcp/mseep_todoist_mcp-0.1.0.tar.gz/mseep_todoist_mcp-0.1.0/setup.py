
from setuptools import setup, find_packages

setup(
    name="mseep-todoist-mcp",
    version="0.1.0",
    description="Add your description here",
    author="mseep",
    author_email="support@skydeck.ai",
    url="",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=['mcp[cli]>=1.4.1', 'todoist-api-python>=2.1.7'],
    keywords=["mseep"] + [],
)
