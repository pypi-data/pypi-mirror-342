# from setuptools import setup, find_packages

# with open("README.md", "r", encoding="utf-8") as fh:
#     long_description = fh.read()

# setup(
#     name="document_verifier",
#     version="0.1.0",
#     author="Advitiya Prakash",
#     author_email="advitiyaprakash08@gmail.com",
#     description="A package for verifying document authenticity using QR codes, OCR, and face matching",
#     long_description=long_description,
#     long_description_content_type="text/markdown",
#    url="https://github.com/yourusername/document_verifier",
#     packages=find_packages(),
#     classifiers=[
#         "Programming Language :: Python :: 3",
#         "License :: OSI Approved :: MIT License",
#         "Operating System :: OS Independent",
#     ],
#     python_requires=">=3.6",
#     install_requires=[
#         # Add your dependencies here, such as:
#         "opencv-python",
#          "numpy",
#          "pillow", 
#          "pytesseract",
#          "face_recognition",
#          "cmake"
#          "dlib"
#          "ultralytics==8.0.20",
#          "scipy",
#          ""

#     ],
# )
from setuptools import setup, find_packages
import os

# Get the absolute path of the directory where setup.py is located
here = os.path.abspath(os.path.dirname(__file__))

setup(
    name="civic2Verifierrr",
    version="0.1.6",
    author="Advitiya Prakash",
    author_email="advitiyaprakash08@gmail.com",
    description="Document verification package",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    python_requires=">=3.6",
    install_requires=[
        # Add your dependencies here, such as:
        "opencv-python",
         "numpy",
         "pillow", 
         "pytesseract",
         "face_recognition",
         "scikit-image",
         "cmake",
         "dlib",
         "ultralytics==8.0.20",
         "scipy"
    ],
)