from setuptools import setup, find_packages

setup(
    name="IM-COOL-BOOY-QR",
    version="1.2.0",
    author="coolbooy",
    author_email="coolbooy@gmail.com",
    description="Stylish QR Code generator with logo, colors, and text options",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=["IM_COOL_BOOY_QR"],
    install_requires=[
        "qrcode",
        "Pillow",
        "colorama",
    ],
    keywords=["QR"],
    entry_points={
        "console_scripts": [
            "IM-COOL-BOOY-QR=IM_COOL_BOOY_QR.main:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.6",
    license="MIT",
    include_package_data=True,
)
