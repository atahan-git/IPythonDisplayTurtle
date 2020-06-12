import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="IPythonDisplayTurtle", # Replace with your own username
    version="0.0.10",
    author="Atahan Ozturk",
    author_email="atahan012000@gmail.com",
    description="Turtles using IPython Display",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/atahan-git/IPythonDisplayTurtle",
    packages=['IPythonDisplayTurtle'],
    package_data={'IPythonDisplayTurtle': ['jspart/*.js']},
    classifiers=[
        "Framework :: IPython",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Education",
    ],
    python_requires='>=3.6',
    install_requires=['IPython'],
)