import os
from setuptools import setup, find_packages, Command

package_folder = os.path.dirname(__file__)
env_file_path = os.path.join(package_folder, ".env")


class CleanUpCommand(Command):
    """Custom command to remove files created by inception_db_connect."""

    description = "Clean up files created by inception_db_connect"
    user_options = []

    def initialize_options(self):
        # create the .env file
        with open(env_file_path, "w") as f:
            f.write(f'facility="setup"')

    def finalize_options(self):
        pass

    def run(self):

        if os.path.exists(env_file_path):
            print(f"Removing file: {env_file_path}")
            os.remove(env_file_path)
        else:
            print(f"No .env file found in {package_folder}.")

        print("Cleanup complete.")


setup(
    name="inception_db_connect",
    version="0.1.7",
    author="KhaduaBloom",
    author_email="khaduabloom@gmail.com",
    description="inception_db_connect is a package that allows you to connect to a database",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/KhaduaBloom/inceptionforcepackages/tree/main/PythonPackage/inceptionDBConnect",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.13.0",
    install_requires=[
        "graypy==2.1.0",
        "psutil==6.1.0",
        "fastapi",
        "uvicorn",
        "pydantic-settings",
        "sqlalchemy",
        "pymongo[srv]",
        "elasticsearch==8.17.2",
    ],
    cmdclass={
        "cleanup": CleanUpCommand,
    },
)
