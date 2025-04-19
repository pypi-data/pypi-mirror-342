import argparse
from Bio import SeqIO

def process_fasta(input_file, output_file):
    # Read the sequences from the input FASTA file
    with open(input_file, 'r') as file:
        records = list(SeqIO.parse(file, 'fasta'))

    contig_counter = 1
    # Modify the header of each sequence
    for record in records:
        print(f"Original contig name: {record.id}")
        record.id = f'{contig_counter}'
        record.description = ""  # Remove any extra description information
        print(f"New contig name: {record.id}")
        contig_counter += 1

    # Save the renamed sequences to the output file
    with open(output_file, 'w') as file:
        SeqIO.write(records, file, 'fasta')

    print(f'\nRenamed sequences and saved to {output_file}.')
    print('Renaming complete.')

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Rename contigs in a FASTA file.")
    parser.add_argument('-i', '--input', required=True, help="Path to the input FASTA file")
    parser.add_argument('-o', '--output', required=True, help="Path to the output FASTA file")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Call the processing function with the parsed arguments
    process_fasta(args.input, args.output)

if __name__ == "__main__":
    main()
