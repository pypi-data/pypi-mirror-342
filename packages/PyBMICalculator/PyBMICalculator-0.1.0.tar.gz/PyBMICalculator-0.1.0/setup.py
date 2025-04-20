from setuptools import setup, find_packages

setup(
    name="PyBMICalculator",  
    version="0.1.0",         
    packages=find_packages(),  
    install_requires=[],     
    description="A simple BMI Calculator that calculates and categorizes BMI based on weight and height.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Md. Ismiel Hossen Abir",  
    author_email="ismielabir1971@gmail.com",  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)