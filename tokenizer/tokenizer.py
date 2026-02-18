import json

class BPETokenizer:
    def __init__(self):
        self.merge_rules = []

    def save(self, filepath):
        """
        Save merge rules to JSON file.

        Args:
            filepath: Path like "models/bpe_tokenizer.json"
        """
        print(f"\nSaving model to {filepath}...")

        # Convert list of tuples to list of lists (JSON serializable)
        # [('l', 'o'), ('lo', 'w')] -> [['l', 'o'], ['lo', 'w']]
        serializable_rules = [list(pair) for pair in self.merge_rules]

        data = {
            'merge_rules' : serializable_rules,
            'num_merges' : len(self.merge_rules),
            'version' : '1.0'
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"Saved {len(self.merge_rules)} merge rules")

    def load(self, filepath):
        """
        Load merge rules from JSON file.

        Args:
            filepath: Path like "models/bpe_tokenizer.json"
        """
        print(f"\nLoading model from {filepath}...")

        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Convert list of lists back to list of tuples
        # [['l', 'o'], ['lo', 'w']] -> [('l', 'o'), ('lo', 'w')]
        self.merge_rules = [tuple(pair) for pair in data['merge_rules']]

        print(f"Loaded {len(self.merge_rules)} merge rules")
        print(f"Version: {data.get('version', 'unknown')}")

        return self.merge_rules
    

