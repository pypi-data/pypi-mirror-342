from setuptools import setup, find_packages
import json

with open("info.json", "r", encoding="utf-8") as f:
    versao: dict = json.load(f)
    versao: str = versao['versão']

setup(
    name="embed_model",
    version=versao,
    packages=find_packages(),
    install_requires=[
        "discord"
    ],
    author="Luca Cunha (Frisk)",
    description="Um modelo de embeds não oficial para discord.py. Feito em Português.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/LucaCunha001/DiscordEmbedModel",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    python_requires=">=3.8",
)