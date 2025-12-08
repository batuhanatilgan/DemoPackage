import setuptools

setuptools.setup(
    name="DemoPackage",
    version="0.0.1",
    author="DigiNova",
    author_email='info@diginova.com.tr',
    description="Demo Package for Training",
    url='https://github.com/batuhanatilgan/DemoPackage.git',
    license='MIT',
    install_requires=['sdk', 'opencv-python-headless'],

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=[
        'DemoPackage',
        'DemoPackage.executors',
        'DemoPackage.models',
        'DemoPackage.utils'
    ],
    package_dir={'DemoPackage': 'src'},

    python_requires=">=3.6"
)