from setuptools import setup, find_packages

# Read your README
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="lemai-sdk",
    version="0.1.2", 
    description="Multi-provider AI chat SDK (OpenAI, Gemini, Custom)",
    long_description=long_description,
    long_description_content_type="text/markdown", 
    author="Erick Lema",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "openai>=1.0.0",
        "requests>=2.28.0",
        "python-dotenv>=1.0.0",
    ],
    python_requires=">=3.7",
)
