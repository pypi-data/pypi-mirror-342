from setuptools import setup

setup(
    name="deepface-anti-spoofing",
    version="1.0.0",
    packages=["deepface_anti_spoofing"],
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