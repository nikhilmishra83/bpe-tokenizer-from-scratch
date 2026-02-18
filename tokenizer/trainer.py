# Class BPETrainer : handles training
# train(corpus, num_merges): main training loop
# get_pairs(symbols): extract adjacent pairs
# merge_vocabulary(pair, vocab): Perform Merge operation
# save_model (path) : Persist merge rules
from collections import Counter

class BPETrainer:
    def __init__(self):
        self.merge_rules = []
        self.vocab = {}

    def get_pairs(self, symbols):
        """
        Extract all adjacent pairs from a list of symbols.

        Input: ['l', 'o', 'w']
        Output: [('l', 'o'), ('o', 'w')]

        """
        pairs = []
        for i in range(len(symbols) -1):
            pair = (symbols[i], symbols[i+1])
            pairs.append(pair)
        # print(pairs)
        return pairs
        
    def count_pairs_in_vocab(self):
        """
        Count frequency of All pairs across entire vocabulary.

        Returns: Counter ({'l', 'o'): 5, ('o', 'w'):5,...}) 

        """
        pairs = Counter()

        # Iterete through every world in vocabulary
        for word_sequence, word_freq in self.vocab.items():
            # Split space-seperated strings into list
            # "l o w </w>" => ['l', 'o', 'w', '</w>']
            symbols = word_sequence.split()

            # Get all pairss in this word
            word_pairs = self.get_pairs(symbols)

            # Add to counter, weighted by word frequency
            for pair in word_pairs:
                pairs[pair] += word_freq    # NOT += 1 !

        # print(f"pairs: {pairs}")
        return pairs
    
    def merge_pair_in_vocab(self, pair):
        """
        Merge a specific pair throught the entire vocabulayr:

        Example: pair = ('l', 'o')
        Before: "l o w </w>" => After: "lo w </w>"
    
        """

        new_vocab = {}

        # What we're looking for and what we'll replace it with 
        old_pattern = ' '.join(pair)                # ('l', 'o') -> "l o"
        new_symbol = "".join(pair)                  # ('l', 'o') -> "lo"

        for word_sequence, freq in self.vocab.items():
            # Replace All occurences of "l o" with "lo" 
            new_sequence = word_sequence.replace(old_pattern, new_symbol)
            new_vocab[new_sequence] = freq 

        self.vocab = new_vocab
    
    def train(self, corpus, num_merges):
        """
        Main training function.

        Args:
            corpus: List of words, e.g., ["low", "lower", "lowest"]
            num_merges: How merges operations to perform
        """

        print("=" * 50)
        print("TRAINING BPE TOKENIZER")
        print("=" * 50)



        # STEP 1: Initialize vocabulary with character sequences 
        print("\nStep1 : Initializing vocabulary...")
        word_frequencies = Counter(corpus)

        for word, freq in word_frequencies.items():
            # Convert "low" -> ['l', 'o', 'w', '</w>']
            symbols = list(word) + ['</w>']
            # Join with spaces: ['l', 'o', 'w', '</w>'] -> "l o w </w>"
            word_sequence = ' '.join(symbols)
            self.vocab[word_sequence] = freq

        print(f"Initial vocabulary:")
        for seq, freq in self.vocab.items():
            print(f" '{seq}': {freq}")
            
        # STEP 2 : Iterative merging
        for iteration in range(num_merges):
            print(f"\n Iteration {iteration + 1}/{num_merges}")
            print("-" * 50)

            # Count all pairs
            pairs = self.count_pairs_in_vocab()
            print(f"iteration {iteration} pairs: {pairs}")

            # Check if we have any pairs left
            if not pairs:
                print("No more pairs to merge. Stopping early.")
                break

            # Find the most frequent pair
            best_pair, best_count = pairs.most_common(1)[0]
            print(f"Most frequent pair: {best_pair} (count: {best_count})")

            print(f"after mege vocabulary:")
            for seq, freq in self.vocab.items():
                print(f" '{seq}': {freq}")

            # Perform the merge
            self.merge_pair_in_vocab(best_pair)
            print(f"Merged '{best_pair[0]} {best_pair[1]}' -> '{best_pair[0] + best_pair[1]}'")

            print(f"before mege vocabulary:")
            for seq, freq in self.vocab.items():
                print(f" '{seq}': {freq}")

            # Save this merge rule
            self.merge_rules.append(best_pair)

            # Show updated vocabulary
            print(f" Updated vocabulary:")
            for seq, freq in self.vocab.items():
                print(f" '{seq}' : {freq}")
            
        print("\n" + "=" * 50)
        print("TRAINING COMPLETE!")
        print("=" * 50)
        print(f"\nLearned {len(self.merge_rules)} merge rules:")
        for i, rule in enumerate(self.merge_rules):
            print(f" {i+1}. {rule[0]} + {rule[1]} -> {rule[0] + rule[1]}")
        
        return self.merge_rules