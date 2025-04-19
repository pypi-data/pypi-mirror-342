from setuptools import setup, find_packages

setup(
    name="flask-metrics-visitors",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Flask",
        "Flask-Login",
        "Flask-SQLAlchemy",
        "geopy",
        "user-agents",
        "requests",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A Flask extension for tracking user metrics and visit statistics",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/flask-metrics-visitors",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 