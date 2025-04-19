from setuptools import setup, find_packages

setup(
    name="IM-COOL-BOOY-GIF",
    version="1.2.0",
    author="coolbooy",
    author_email="coolbooy@gmail.com",
    description="A Cool Command-Line GIF Tool by COOL BOOY. This is a simple yet powerful tool designed to work seamlessly through the command line, allowing users to generate and manage GIFs easily. Whether you're looking to create GIFs from videos or manipulate them in various ways, this tool offers a straightforward interface for all your GIF-related needs.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "Pillow",
        "imageio",
        "numpy",
        "tqdm"
    ],
    keywords=["gif", "image", "hd", "tool"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    license="MIT",
    entry_points={
        "console_scripts": [
            "IM-COOL-BOOY-GIF = IM_COOL_BOOY_GIF.main:main"
        ]
    },
    python_requires='>=3.6',
    include_package_data=True,
)
