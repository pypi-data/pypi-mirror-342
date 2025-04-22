from setuptools import setup, find_packages


setup(
    name='lightweight-b2',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "lightweight_b2": ["py.typed", "core/*.pyi"],
    },
    install_requires=[
        'requests'
    ],
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Daniel Lasota",
    author_email="grossmann.root@gmail.com",
    description="Lightweight B2 client with backblaze support",
    keywords="b2 backblaze client",
    url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    project_urls={
        "Source": "https://github.com/DanielLasota/lightweight-b2"
    },
    python_requires='>=3.11',
)
