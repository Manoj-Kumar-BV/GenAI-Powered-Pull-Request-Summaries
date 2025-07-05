from setuptools import setup, find_packages

setup(
    name="genai-pr-summarizer",
    version="1.0.0",
    description="Gen AI Powered Pull Request Summarizer CLI",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "requests",
        "python-dotenv",
        "colorama",
        "pyfiglet",
        "termcolor"
    ],
    entry_points={
        "console_scripts": [
            "genai-pr-summarizer=genai_pr_summarizer.cli:main"
        ]
    },
    include_package_data=True,
    python_requires=">=3.8",
)