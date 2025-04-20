from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="docoreai",
    version="0.3.5",
    author="Saji John",
    author_email="sajijohnmiranda@gmail.com",
    license="MIT",
    packages=find_packages(include=["docore_ai", "docore_ai.*", "api", "api.*", "research", "research.Telm"]),
    package_data={
        "": ["LICENSE.md"],
        "research.Telm": ["*.json"],  # Include JSONs in specific package
    },
    description="DoCoreAI is an intelligence profiler that optimizes prompts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SajiJohnMiranda/DoCoreAI",
    project_urls={
        "Documentation": "https://your-docs-url.com",
        "Blog Post": "https://mobilights.medium.com/intelligent-prompt-optimization-bac89b64fa84",
        "Source Code": "https://github.com/SajiJohnMiranda/DoCoreAI",
    },
    install_requires=[
        "uvicorn",
        "pydantic",
        "python-dotenv",
        "openai",
        "langchain",
        "groq",
        "requests",
        "tiktoken"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)

print("\n✅ Installation complete! Please create a .env file in your root folder. Refer to the README for details.\n")
print("\n🐛 Report Issues & Suggestions: https://github.com/SajiJohnMiranda/DoCoreAI/discussions")
print("\n🎉 Thank you for using DoCoreAI! Your👀 feedback and support help us improve. 🚀\n")
