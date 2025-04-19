from setuptools import setup, find_packages

setup(
    name='gilman_fasta_edit',  # The name of your package
    version='0.1',  # The version of your package
    packages=find_packages(),  # This will automatically include gilman_fasta_edit/
    install_requires=[
        'biopython',  # Dependency for working with FASTA files
    ],
    entry_points={
        'console_scripts': [
            'gilman_fasta_edit = gilman_fasta_edit.main:main',  # Command to run the tool
        ],
    },
    description="A tool to rename contigs in a FASTA file.",  # Short description of your package
    long_description="This command-line tool renames contigs in a given FASTA file.",
    long_description_content_type="text/markdown",  # For README markdown format
)
