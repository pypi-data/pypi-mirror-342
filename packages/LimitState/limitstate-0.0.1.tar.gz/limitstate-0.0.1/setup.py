from setuptools import setup,find_packages
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="LimitState",
    version="0.0.1",
    description="Software for Advanced First Order Second Moment Reliability Method",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Shinsuke Sakai",
    author_email='sakaishin0321@gmail.com',
    url='https://github.com/ShinsukeSakai0321/LimitState',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license='MIT',
    package_data={'':['*.csv']},
    include_package_data=True,
    python_requires='>=3.6',
)