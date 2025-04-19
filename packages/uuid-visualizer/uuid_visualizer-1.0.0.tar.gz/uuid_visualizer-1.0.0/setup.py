from setuptools import setup, find_packages

setup(
    name="uuid-visualizer",
    version="1.0.0",
    description="Generate stylized images from UUIDs for auth shells or visual identity",
    author="Aurora Rosabella",
    author_email="auracrimsonrose@gmail.com.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["Pillow"],
    entry_points={
        'console_scripts': [
            'uuid-visualizer=uuid_visualizer.main:main',
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
