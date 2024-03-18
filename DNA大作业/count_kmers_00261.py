import argparse
import time

def count_kmers_non_dict(seqs, k):
    """
    Count the frequency of each k-mer in the given DNA sequence without using a dictionary.
    """
    # Ensure the sequence is uppercase
    seqs = [seq.upper() for seq in seqs]

    # Initialize lists for storing k-mers and their counts
    kmers = []
    counts = []
    for seq in seqs:
        # Iterate through the sequence to extract and count k-mers
        for i in range(len(seq) - k + 1):
            kmer = seq[i:i + k]
            # Check if kmer contains only valid DNA letters
            if all(c in 'ATCG' for c in kmer):
                if kmer not in kmers:
                    kmers.append(kmer)
                    counts.append(1)
                else:
                    counts[kmers.index(kmer)] += 1
    res = [[i,j] for i,j in zip(kmers, counts)]
    return res


def write2file_non_dict(seqs, k, file):
    """
    Write the k-mer counts to an output file.
    """
    res = count_kmers_non_dict(seqs, k)
    res.sort()
    with open(file, 'w') as f:
        for r in res:
            f.write(f"{r[0]}:{r[1]}\n")

def count_kmers(seqs, k):
    """
    Count the frequency of each k-mer in the given DNA sequence using a dictionary.
    """
    # Ensure the sequence is uppercase
    seqs = [seq.upper() for seq in seqs]

    # Initialize a dictionary for k-mer counts
    res = {}
    for seq in seqs:
        # Iterate through the sequence to extract and count k-mers
        for i in range(len(seq) - k + 1):
            kmer = seq[i:i + k]
            # Check if kmer contains only valid DNA letters
            if all(c in 'ATCG' for c in kmer):
                if kmer not in res:
                    res[kmer] = 1
                else:
                    res[kmer] += 1

    return res

def write2file(seqs, k, file):
    """
    Write the k-mer counts to an output file.
    """
    res = count_kmers(seqs, k)
    rows = [[i,j] for i,j in res.items()]
    rows.sort()
    with open(file, 'w') as f:
        for r in rows:
            f.write(f"{r[0]}:{r[1]}\n")

def parse_args():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file')
    parser.add_argument('k')
    parser.add_argument('-c', '--compare', action='store_true')
    return parser.parse_args()

def read_file(file):
    """
    Read the input file and return the list of sequences.
    """
    seqs = []
    with open(file, 'r') as f:
        if file.endswith('fasta') or file.endswith('fa') or file.endswith('fna'):
            now = ''
            rows = f.read().split('\n')
            rows = [i for i in rows if i]
            for row in rows:
                if row[0] == ';':
                    continue
                elif row[0] == '>':
                    if now:
                        seqs.append(now)
                    now = ''
                else:
                    now += row
            seqs.append(now)
        elif file.endswith('fastq') or file.endswith('fq'):
            rows = f.read().split('\n')
            rows = [i for i in rows if i]
            for i in range(0,len(rows),4):
                seqs.append(rows[i+1])
    return seqs

def main():
    # Parse command line arguments
    args = parse_args()

    # Read input file
    seqs = read_file(args.input_file)

    ks = args.k
    if ',' in ks:
        ks = [int(i) for i in ks.split(',')]
    else:
        ks = [int(ks)]

    # Count k-mers using both methods
    if args.compare:
        k = ks[0]
        start_time = time.time()
        write2file_non_dict(seqs, k, f'{args.input_file.split(".")[0]}_{k}-mer-frequency.txt')
        end_time = time.time()
        without_time = end_time - start_time
        print(f"Time without dictionary elapsed is {without_time:g} seconds.")

        start_time = time.time()
        write2file(seqs, k, f'{args.input_file.split(".")[0]}_{k}-mer-frequency.txt')
        end_time = time.time()
        with_time = end_time - start_time
        print(f"Time with dictionary elapsed is {with_time:g} seconds.")

        with open('log_00261.txt','a+') as f:
            f.write(f'filename:{args.input_file}, k:{k}:\n')
            f.write(f"Time without dictionary elapsed is {without_time:g} seconds.\n")
            f.write(f"Time with dictionary elapsed is {with_time:g} seconds.\n")
    # If not comparing, use the dict method by default
    else:
        for k in ks:
            write2file(seqs, k, f'{args.input_file.split(".")[0]}_{k}-mer-frequency.txt')

if __name__ == "__main__":
    main()
