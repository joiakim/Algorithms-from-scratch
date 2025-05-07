import ast


class BasicTokenizer:
    """Class for byte pair encoding and decoding operations."""

    def __init__(self):
        """Initialize the BPE encoder/decoder with default values."""
        self.tokens = None
        self.n_token = 256
        self.merge_history = {}
        self.token_mapping = {}
        self.vocab_size = None
        self.text = None

    

    def train(self, text, vocab_size):
        """
        Encode tokens using Byte Pair Encoding.

        Args:
            tokens: List of integers representing tokens
            vocab_size: Number of new vocabulary items to add

        Returns:
            String representation of encoding data
        """
        self.text = text
        tokens = list(self.text.encode("utf-8"))
        self.tokens = tokens.copy()
        self.vocab_size = self.n_token + vocab_size

        # Continue merging until we reach vocab size or can't merge anymore
        while self.n_token < self.vocab_size:
            
            pair_counts = {}
            for i in range(len(self.tokens) - 1):
                pair = (self.tokens[i], self.tokens[i + 1])
                pair_str = str(list(pair))
                pair_counts[pair_str] = pair_counts.get(pair_str, 0) + 1

            # Find the most frequent pair
            max_count = 0
            max_pair_str = None
            for pair_str, count in pair_counts.items():
                if count > max_count:
                    max_count = count
                    max_pair_str = pair_str

            # If no pair appears more than once, stop merging
            if max_count <= 1:
                break

            self.merge_history[max_pair_str] = max_count
            max_pair = ast.literal_eval(max_pair_str)
            self.token_mapping[max_pair_str] = self.n_token

            # Merge instances of the pair in tokens
            i = 0
            new_tokens = []
            while i < len(self.tokens):
                if (i < len(self.tokens) - 1 and
                    self.tokens[i] == max_pair[0] and
                    self.tokens[i + 1] == max_pair[1]):
                    new_tokens.append(self.n_token)
                    i += 2
                else:
                    new_tokens.append(self.tokens[i])
                    i += 1

            # Update tokens and increment token counter
            self.tokens = new_tokens
            self.n_token += 1
        
        vocab = {idx: bytes([idx]) for idx in range(256)}
        for key, idx in self.token_mapping.items():
          key = eval(key)
          vocab[idx] = vocab[key[0]] + vocab[key[1]] 
        self.vocab_bpe = vocab                   
        
        print("Encoding Done........")

    def generate_summary(self):
        return (
                f"length of Encoded tokens:{len(self.tokens)}\n"
                f"Merge count:{self.merge_history}\n"
                f"Merge Maps:{self.token_mapping}\n"
                #f"New tokens:{self.tokens}\n"
                f"Max token:{max(self.tokens)}"
               )



    def token_encode(self,text_to_tokenize):
          text_token = list(text_to_tokenize.encode("utf-8"))
          token_1 = text_token.copy()
          self.token_1 = token_1
          for k,v in self.token_mapping.items():
              for x in range(len(self.token_1)):
                if self.token_1[x:x+2] == eval(k):
                    self.token_1[x]= v
                    self.token_1.pop(x+1)
          return self.token_1

    def token_decode(self, token_2):
        self.token_2 = token_2
        final_tokens = b"".join(self.vocab_bpe[idx] for idx in self.token_2)
        text = final_tokens.decode("utf-8", errors="replace")
        return text


