from setuptools import setup, find_packages

setup(
    name="embed_model",
    version="0.2",
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
#pypi-AgEIcHlwaS5vcmcCJGM0Yzg2ODA4LTZhMWEtNDY0Yi05YzVkLTAzMzk1ODljYTY2OAACKlszLCI5MmY0Y2QwYi01MWM5LTQ2MTctODA3Ni03MjJjNTVkZDcyNjgiXQAABiBMzZVaB26hFe16T_t3K3b268mK5TADYSEHIjj-ZZdRaA