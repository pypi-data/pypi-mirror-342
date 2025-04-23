from setuptools import setup, find_packages


with open("README.md", "r") as stream:
    long_description = stream.read()

setup(
    name='pywincontroller',
    version="1.1.2",
    url='https://github.com/ThePhoenix78/pywincontroller',
    download_url='https://github.com/ThePhoenix78/pywincontroller/tarball/master',
    license='MIT',
    author='ThePhoenix78',
    author_email='thephoenix788@gmail.com',
    description='A wrapper for pywinauto that make the ability to control any window with python easily',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=[
        'pywinauto',
        "python windows",
        "window controller",
        "controller",
    ],
    install_requires=[
        'pywinauto',
    ],
    setup_requires=[
        'wheel'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    # package_data={
    #    '': ["*.png", "Images/MapsHex/*", "Images/MapIcons/*"]
    # },

    # include_package_data=True,
    # packages=["sdist", "bdist_wheel"]
    # python_requires='>=3.6',
)
"""
data_files=[
    ('/Images/MapHex', [os.path.join('Images/MapsHex', file) for file in os.listdir("Images/MapsHex")]),
    ('/Images/MapIcons', [os.path.join('Images/MapIcons', file) for file in os.listdir("Images/MapIcons")]),
],
"""
