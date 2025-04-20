# from setuptools import setup, find_packages

# setup(
#     name="yagamiioit",  # Updated package name
#     version="0.1.2",  # Keep the incremented version
#     author="Your Name",
#     author_email="your.email@example.com",
#     description="A sample package that includes text files",
#     long_description=open("README.md").read(),
#     long_description_content_type="text/markdown",
#     packages=find_packages(),
#     include_package_data=True,  # Ensures MANIFEST.in files are included
#     install_requires=[],  # Add dependencies if needed
#     classifiers=[
#         "Programming Language :: Python :: 3",
#         "License :: OSI Approved :: MIT License",
#         "Operating System :: OS Independent",
#     ],
#     python_requires=">=3.6",
# )
from setuptools import setup, find_packages

setup(
    name="yagamiioits",
    version="0.1.0",  # First release version
    author="Temp Name",  # Replace with your actual name if you want credit
    author_email="temp.email@example.com",  # Replace with your real email
    description="A sample package that includes text files",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/yagamiioits",  # Optional but nice for users
    packages=find_packages(),
    include_package_data=True,  # Includes files from MANIFEST.in
    install_requires=[],  # Add dependencies if needed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Make sure this matches your LICENSE file
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
