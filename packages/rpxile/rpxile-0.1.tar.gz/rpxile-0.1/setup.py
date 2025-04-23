from setuptools import setup, find_packages

setup(
    name="rpxile",  # Il nome del tuo pacchetto
    version="0.1",  # La versione
    packages=find_packages(),  # Trova i pacchetti automaticamente
    description="Libreria per gestire file in Python",
    long_description=open('README.md').read(),  # Leggi il contenuto del README
    long_description_content_type="text/markdown",  # Specifica il formato del README
    author="Il Tuo Nome",
    author_email="email@example.com",  # Sostituisci con la tua email
    url="https://github.com/tuo-username/rpxile",  # Link al tuo repository GitHub (opzionale)
    classifiers=[  # Un po' di metadati per aiutare gli altri a trovare il pacchetto
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Specifica la versione minima di Python
)
