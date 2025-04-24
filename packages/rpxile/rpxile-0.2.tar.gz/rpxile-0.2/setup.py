from setuptools import setup, find_packages

# Apre il README in modo sicuro con un context manager
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="rpxile",  # Il nome del tuo pacchetto
    version="0.2",  # La versione
    packages=find_packages(),  # Trova i pacchetti automaticamente
    description="A simple Python library for fast file operations",  # Descrizione breve
    long_description=long_description,  # Descrizione lunga, letta dal README
    long_description_content_type="text/markdown",  # Specifica il formato del README
    author="Rpx",  # Sostituisci con il tuo nome
    author_email="",  # Sostituisci con la tua email
    url="https://github.com/Rp-ics/",  # Modifica con il link al tuo repository GitHub
    classifiers=[  # Metadati per aiutare gli altri a trovare il pacchetto
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Specifica la versione minima di Python
    extras_require={  # Dipendenze opzionali
        'dev': ['twine', 'pytest'],
    },
)
