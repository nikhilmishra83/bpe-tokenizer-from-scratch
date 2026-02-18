
from trainer import BPETrainer
from encoder import BPEEncoder
from tokenizer import BPETokenizer

# Training
corpus = ["low", "low", "low", "lower", "lower", "newest", "newest", "newest"]
trainer = BPETrainer()
merge_rules = trainer.train(corpus, num_merges=8)

# Save
tokenizer = BPETokenizer()
tokenizer.merge_rules = merge_rules
tokenizer.save("trained_bpe.json")

# Load and use
tokenizer = BPETokenizer()
tokenizer.load("trained_bpe.json")
encoder = BPEEncoder(tokenizer.merge_rules)

# Test encoding
test_words = ["lower", "lowest", "newer"]
for word in test_words:
    tokens = encoder.encode(word)
    decoded = encoder.decode(tokens)
    print(f"{word} → {tokens} → {decoded}")
