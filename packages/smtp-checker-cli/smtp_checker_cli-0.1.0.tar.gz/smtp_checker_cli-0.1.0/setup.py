from setuptools import setup, find_packages

setup(
    name="smtp-checker-cli",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "smtp-checker=smtp_checker.cli:main",
        ],
    },
    install_requires=[],  # Daftar dependensi tambahan jika diperlukan
    author="Nama Kamu",
    description="Simple CLI tool to test SMTP servers.",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.7',  # Menentukan versi Python minimum
)
