def count_kmers_non_dict(seq, k):
    """
    Count the frequency of each k-mer in the given DNA sequence without using a dictionary.
    """
    # Ensure the sequence is uppercase
    seq = seq.upper()

    # Initialize lists for storing k-mers and their counts
    kmers = []
    counts = []

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


def write2file_non_dict(seq, k, file):
    """
    Write the k-mer counts to an output file.
    """
    res = count_kmers_non_dict(seq, k)
    res.sort()
    with open(file, 'w') as f:
        for r in res:
            f.write(f"{r[0]}:{r[1]}\n")

def count_kmers(seq, k):
    """
    Count the frequency of each k-mer in the given DNA sequence using a dictionary.
    """
    # Ensure the sequence is uppercase
    seq = seq.upper()

    # Initialize a dictionary for k-mer counts
    res = {}

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

def write2file(seq, k, file):
    """
    Write the k-mer counts to an output file.
    """
    res = count_kmers(seq, k)
    rows = [[i,j] for i,j in res.items()]
    rows.sort()
    with open(file, 'w') as f:
        for r in rows:
            f.write(f"{r[0]}:{r[1]}\n")

def load_fasta_file(file):
    with open(file) as f:
        data = f.read().split('\n')[1:]
        data = ''.join(data)
    return data

if __name__ == '__main__':
    test_data = load_fasta_file('test-files/example_chromosome21.fasta')
    import time

    start_time = time.time()
    count_kmers_non_dict(test_data, 3)
    end_time = time.time()
    use_time = end_time - start_time
    print(f"Time without dictionary elapsed is {use_time:g} seconds.")

    start_time = time.time()
    count_kmers(test_data, 3)
    end_time = time.time()
    use_time = end_time - start_time
    print(f"Time with dictionary elapsed is {use_time:g} seconds.")

