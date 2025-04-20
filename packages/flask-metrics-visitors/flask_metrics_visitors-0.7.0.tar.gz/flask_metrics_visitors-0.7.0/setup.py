import re
from setuptools import setup, find_packages

def get_version():
    with open('flask_metrics_visitors/__init__.py', 'r') as f:
        content = f.read()
        version_match = re.search(r"__version__ = ['\"]([^'\"]*)['\"]", content)
        if version_match:
            return version_match.group(1)
        raise RuntimeError("Unable to find version string.")

setup(
    name='flask-metrics-visitors',
    version=get_version(),
    description='A Flask extension for tracking and visualizing visitor metrics',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Patrick Hastings',
    author_email='patrick@example.com',  # Replace with your email
    url='https://github.com/yourusername/flask-metrics-visitors',  # Replace with your repo URL
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask>=2.0.0',
        'Flask-SQLAlchemy>=3.0.0',
        'Flask-Login>=0.6.0',
        'geopy>=2.4.1',
        'user_agents>=2.2.0',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    python_requires='>=3.7',
) 