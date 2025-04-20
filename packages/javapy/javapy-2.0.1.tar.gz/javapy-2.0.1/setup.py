from setuptools import setup, Extension
from Cython.Build import cythonize
import os

# Daftar ekstensi Cython
extensions = [
    Extension(
        "javapy.highspeed.database",
        sources=["javapy/highspeed/database.py"],
        extra_compile_args=["-O3", "-march=native"],  # Optimasi agresif
        define_macros=[("CYTHON_WITHOUT_ASSERTIONS", "1")]  # Nonaktifkan assertion untuk kecepatan
    ),
    Extension(
        "javapy.highspeed.serializer",
        sources=["javapy/highspeed/serializer.py"],
        extra_compile_args=["-O3"],
        libraries=["z"]  # Link terhadap libz (zlib bawaan sistem)
    ),
    Extension(
        "javapy.highspeed.threader",
        sources=["javapy/highspeed/threader.py"],
        extra_compile_args=["-O3"],
        libraries=["pthread"] if os.name == "posix" else []  # Threading untuk Unix
    )
]

# Konfigurasi utama
setup(
    name="javapy",
    version="2.0.1",
    author="Eternals",
    author_email="eternals.tolong@gmail.com",
    url="https://github.com/Eternals-Satya/javapy",
    description="Paket Python berperforma tinggi tanpa dependensi eksternal",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=[
        "javapy",
        "javapy.highspeed",
        "javapy.utils"
    ],
    ext_modules=cythonize(
        extensions,
        compiler_directives={
            "language_level": "3",
            "boundscheck": False,  # Percepat akses array
            "wraparound": False    # Nonaktifkan indeks negatif
        }
    ),
    package_data={
        "javapy": ["*.pyx", "*.pxd"],  # Sertakan file Cython
        "": ["*.txt", "*.md"]          # File dokumentasi
    },
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    keywords="high-performance cython sqlite threading compression"
)
