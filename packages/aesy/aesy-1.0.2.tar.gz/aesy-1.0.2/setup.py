from setuptools import setup

setup(
    name="aesy",
    version="1.0.1",
    description="AESY multi-layer encryption algorithm",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Gubir34",
    author_email="canteoman15@gmail.com",
    url="https://gitlab.com/gubir34/aesy/",
    packages=["aesy"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.8',
)
