from math import comb

# Total number of ways to choose 4 numbers from 72
total_ways = comb(72, 4)

# Ways to choose 2 twos, 2 ones, and 0 zeros
ways_2_twos_2_ones = comb(2, 2) * comb(7, 2)

# Ways to choose 2 twos, 1 one, and 1 zero
ways_2_twos_1_one_1_zero = comb(2, 2) * comb(7, 1) * comb(63, 1)

# Total ways to fulfill the condition
total_favorable_ways = ways_2_twos_2_ones + ways_2_twos_1_one_1_zero

# Probability of drawing at least 2 twos and 1 one
probability = total_favorable_ways / total_ways
print(probability)
