from setuptools import setup, find_packages

setup(
    name='commitly',
    version='2.0.5',
    author='Kouya Tosten',
    author_email='kouyatosten@gmail.com',
    description='Generate a well-structured commit message based on staged changes',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Tostenn/Commitly',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "g4f>=0.5.0.4",  # ou version exacte que tu utilises
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # ou celle que tu choisis
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Version Control',
    ],
    python_requires='>=3.7',
    # entry_points={
    #     'console_scripts': [
    #         'commitly=commitly.__main__:main',  # si tu veux une commande CLI (optionnel)
    #     ],
    # },
)
