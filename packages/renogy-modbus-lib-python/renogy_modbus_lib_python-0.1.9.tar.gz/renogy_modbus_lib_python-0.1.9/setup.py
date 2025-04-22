from setuptools import setup, find_packages

setup(
    name="renogy-modbus-lib-python",
    version="0.1.9",  # 建议遵循语义化版本规范
    author="Renogy",
    author_email="your.email@example.com",
    description="Renogy Bluetooth SDK for Python",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/RenogyBT_forPythonSDK",
    packages=find_packages(where="modbus_bt_pkg/src"),
    package_dir={"": "modbus_bt_pkg/src"},
    install_requires=[
        'pyserial>=3.5',
        'bleak>=0.19.0',
        # ... 其他依赖 ...
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    include_package_data=True,
    license='MIT'
)