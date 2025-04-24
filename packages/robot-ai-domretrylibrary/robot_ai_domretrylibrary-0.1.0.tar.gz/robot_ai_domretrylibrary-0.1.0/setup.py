from setuptools import setup, find_packages

setup(
    name="robot-ai-domretrylibrary",
    version="0.1.0",
    description="A Robot Framework library with AI fallback for locators using OpenAI",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Kristijan Plaushku",
    author_email="info@plaushkusolutions.com",
    url="https://github.com/plaushku/robot-ai-domretrylibrary",
    packages=find_packages(),
    install_requires=[
        "robotframework>=6.0",
        "robotframework-seleniumlibrary>=6.0",
        "python-dotenv>=1.0.0",
        "requests>=2.28.0",
        "webdriver-manager>=4.0.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Framework :: Robot Framework :: Library",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Testing :: Acceptance",
    ],
    keywords="robotframework testing automation ai openai",
) 