# setup.py
from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import subprocess
import platform
import urllib.request
import zipfile


def is_ffmpeg_installed():
    """Check if FFMPEG is installed and accessible."""
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False

def download_ffmpeg():
    """Download and extract FFMPEG for the current platform."""
    system = platform.system().lower()
    ffmpeg_url = ""

    if system == "darwin":  # macOS
        ffmpeg_url = "https://evermeet.cx/ffmpeg/ffmpeg.zip"
    elif system == "windows":
        ffmpeg_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    elif system == "linux":
        ffmpeg_url = "https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz"
    else:
        raise OSError("Unsupported operating system.")

    print("Downloading FFMPEG...")
    ffmpeg_zip_path = "ffmpeg_download.zip"
    urllib.request.urlretrieve(ffmpeg_url, ffmpeg_zip_path)

    print("Extracting FFMPEG...")
    if system == "linux":
        import tarfile
        with tarfile.open(ffmpeg_zip_path, "r:xz") as tar:
            tar.extractall("./ffmpeg")
    else:
        with zipfile.ZipFile(ffmpeg_zip_path, "r") as zip_ref:
            zip_ref.extractall("./ffmpeg")

    os.remove(ffmpeg_zip_path)
    print("FFMPEG downloaded and extracted.")

    # Set the environment variable to point to the downloaded FFMPEG binary
    os.environ["IMAGEIO_FFMPEG_EXE"] = os.path.abspath("./ffmpeg/ffmpeg")

def ensure_ffmpeg():
    """Ensure FFMPEG is installed and available."""
    if not is_ffmpeg_installed():
        print("FFMPEG not found. Downloading...")
        download_ffmpeg()
    else:
        print("FFMPEG is already installed.")


class CustomInstallCommand(install):
    """Custom installation to ensure FFMPEG is installed."""
    def run(self):
        ensure_ffmpeg()  # Call the function to check and install FFMPEG
        install.run(self)

setup(
    name='visualsort',                          # Name of your package
    version='0.1',                              # Package version
    packages=find_packages(),                   # Automatically find all packages
    install_requires=[                          # Dependencies
        'pillow',                                # Example dependency
        'moviepy',
        'numpy',
        'pytest',
        'pytest-mock',
        'urllib3',
    ],
    test_suite='tests',                         # Location of tests
    tests_require=[                             # Test dependencies
        'pytest',
        'pytest-mock',
    ],
    author='Tomas Bivainis',
    author_email='bivainis.tomas@gmail.com',
    description='Visualsort lets you write sorting algorithms with given functions and then render them to videos.',
    long_description=open('README.md').read(),  # Detailed description from README
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/my_package',  # GitHub or project URL
    classifiers=[                               # Package classifiers
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    cmdclass={
        'install': CustomInstallCommand,  # Use the custom install command
    },
)
