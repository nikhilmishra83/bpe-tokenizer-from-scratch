# class BPEEncoder: handles encoding/decoding
# load_model(path): Load trained merge rules
# encode(text) : Tokenize text into subwords
# decode(tokens) : Convert tokens back to text
# apply_merges(symbols, merge_rules): Apply rules in order

class BPEEncoder:
    def __init__(self, merge_rules):
        """
            Args:
                merge_rules: List of tuples from training
                                e.g., [('l', 'o'), ('lo', 'w'), ...]
        """
        self.merge_rules = merge_rules

    def apply_merges_to_word(self, word):
        """
        Apply all merge rules to a single word.

        Args:
            word: String like "lower"
        Returns: 
            List of tokens like ['low', 'er']
        """
        
        #Start with character-level representation
        symbols = list(word) + ['</w>']
        # symbols = ['l', 'o', 'w', 'e', 'r', '</w>']

        print(f"\nEncoding word: '{word}'")
        print(f"Initial symbols: {symbols}")

        # Apply each merge rule in order
        for merge_num, (first, second) in enumerate(self.merge_rules):
            # Look for this pair in current symbol
            i = 0
            while i< len(symbols) - 1:
                # Check if we found the pair
                if symbols[i] == first and symbols[i+1] == second:
                    # Merge them!
                    merged = first + second
                    symbols[i] = merged
                    symbols.pop(i+1)               # Remove the second symbol

                    print(f" Merge {merge_num + 1}: Found {(first, second)} at position {i} -> merged to '{merged}'")
                    print(f" Symbols now: {symbols}")
                    
                    # Don't increment i - check same position again 
                    # in case new merge creates another mergeable pair
                else:
                    i += 1

        print(f"Final tokens: {symbols}")
        return symbols
        
    def encode(self, text):
            """
            Encode entire text into subword tokens.

            Args:
                text: String like "lower newest"
            Returns: 
                List of tokens like ['low', 'er', '</w>', 'new', 'est', '</w>']
            """
            # Simple word tokenization
            words = text.lower().split()

            all_tokens = []
            for word in words:
                tokens = self.apply_merges_to_word(word)
                all_tokens.extend(tokens)

            return all_tokens
        
    def decode(self, tokens):
        """
        Convert tokens back to readable text.

        Args:
            tokens: ['low', 'er', '</w>', 'new', 'est', '</w>']
        Returns:
            "lower newest"
        """
        print(f"Decoding tokens: {tokens}")

        # Step 1: Join all tokens together
        text = "".join(tokens)
        # Result: "lowe</w>newest</w>"

        # Step 2 : Replace </w> with spaces
        text = text.replace('</w>', ' ')
        print(f"Step 2 - Replaced </w>: '{text}")
        # Result: "lower newest"

        # Step 3: Strip trailing/leading spaces
        text = text.strip()
        print(f"Step 3 - Stripped: '{text}")
        # Result: "lower newest"

        return text
