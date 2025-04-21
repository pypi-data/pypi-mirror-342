from setuptools import setup, find_packages

setup(
    name="codepy-redebots",  # Novo nome do pacote
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "aiohttp>=3.11.17",
        "redis>=5.2.1",
    ],
    include_package_data=True,
    package_data={
        "codepy": ["nextcord/*"]
    },
    author="Lucas Dev - RedeBots",
    author_email="ofc.rede@gmail.com",
    description="Biblioteca pioneira para bots Discord 2025, 100% brasileira, com suporte a IA, voz, OAuth2 e interações modernas.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/LucasDesignerF/code-py",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12.7",
)