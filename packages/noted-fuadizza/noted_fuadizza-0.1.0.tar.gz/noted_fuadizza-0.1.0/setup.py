from setuptools import setup, find_packages

setup(
    name='noted-fuadizza',  # Nama paket kamu
    version='0.1.0',  # Versi aplikasi
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'noted=noted.__main__:main',  # Menyambungkan CLI dengan aplikasi
        ],
    },
    install_requires=[
        'typer[all]',  # Menyebutkan dependensi yang digunakan
    ],
    python_requires='>=3.7',
    author="Nama Kamu",
    author_email="email@domain.com",
    description="CLI untuk mengelola catatan harian",  # Deskripsi aplikasi
    long_description=open('README.md').read(),  # Baca dari README.md
    long_description_content_type='text/markdown',  # Format README
    url="https://github.com/username/noted",  # Ganti dengan repo GitHub kamu
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

