from setuptools import setup, find_packages

setup(
    name="deepface-antispoofing",
    version="1.1.1",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'deepface_antispoofing': ['data/haarcascade_frontalface_default.xml']
    },
    install_requires=["requests", "opencv-python", "numpy", "tensorflow"],
    description="A Python package for seamless face recognition and anti-spoofing analysis, automatically downloading models for age, gender, and real/fake face detection.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="IP Softech - Pratham Pansuriya",
    author_email="ipsoftechsolutions@gmail.com",
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)