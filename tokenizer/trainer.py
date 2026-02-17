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
            
