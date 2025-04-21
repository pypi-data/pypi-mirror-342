import re
import json
import itertools
from collections import Counter

class Tokenizer:
    def __init__(self, max_vocab=3000):
        # fixed specials
        self.specials = ['<PAD>', '<NS>', '<UP>', '<CAP>']
        self.max_vocab = max_vocab

        # to be built in train() or load()
        self.tokens = []
        self.bpe_merges = []
        self.token2id = {}
        self.id2token = {}
        self.vocab_size = 0
        self.bpe_slots = 0

    def train(self, texts):
        # 1) Top-400 words >3 chars
        wc = Counter()
        for t in texts:
            words = re.findall(r"\b\w+\b", t.lower())
            wc.update(w for w in words if len(w)>3 and not w.isdigit())
        top_words = [w for w,_ in wc.most_common(400)]

        # 2) Number tokens
        nums = [str(i) for i in range(100)]
        # 3) Single letters
        letters = [chr(c) for c in range(97,123)]
        # 4) All bigrams
        bigrams = [''.join(p) for p in itertools.product(letters, repeat=2)]

        # assemble base
        base = self.specials + nums + letters + bigrams + top_words
        self.tokens = base.copy()
        self.vocab_size = len(self.tokens)
        self.bpe_slots = self.max_vocab - self.vocab_size
        if self.bpe_slots < 0:
            raise ValueError(f"Base vocab ({self.vocab_size}) exceeds {self.max_vocab}")

        # prepare word‑freq for BPE
        word_freq = Counter()
        for w,c in wc.items():
            word_freq[tuple(w)] = c

        # 5) BPE training
        merges = []
        for _ in range(self.bpe_slots):
            # count only pairs whose merged form is length >=3
            pairs = Counter()
            for word, freq in word_freq.items():
                for i in range(len(word)-1):
                    a, b = word[i], word[i+1]
                    if len(a + b) < 3:
                        continue
                    pairs[(a, b)] += freq
            if not pairs:
                break

            best = max(pairs, key=pairs.get)
            merges.append(best)

            # apply that merge
            new_wf = Counter()
            for word, freq in word_freq.items():
                seq, i = [], 0
                while i < len(word):
                    if (i < len(word)-1 and 
                        (word[i], word[i+1]) == best):
                        seq.append(word[i] + word[i+1])
                        i += 2
                    else:
                        seq.append(word[i])
                        i += 1
                new_wf[tuple(seq)] += freq
            word_freq = new_wf

        self.bpe_merges = merges
        self.tokens += [''.join(a+b) for a,b in merges]
        self.token2id = {t:i for i,t in enumerate(self.tokens)}
        self.id2token = {i:t for t,i in self.token2id.items()}
        self.vocab_size = len(self.tokens)
        self.bpe_slots = self.max_vocab - self.vocab_size

    def save(self, prefix):
        # writes prefix+"_vocab.json" and prefix+"_merges.json"
        with open(prefix+"_vocab.json","w",encoding="utf-8") as f:
            json.dump(self.tokens, f, ensure_ascii=False, indent=2)
        with open(prefix+"_merges.json","w",encoding="utf-8") as f:
            json.dump(self.bpe_merges, f, ensure_ascii=False)

    @classmethod
    def load(cls, prefix, max_vocab=3000):
        tok = cls(max_vocab)
        with open(prefix+"_vocab.json","r",encoding="utf-8") as f:
            tok.tokens = json.load(f)
        with open(prefix+"_merges.json","r",encoding="utf-8") as f:
            tok.bpe_merges = [tuple(m) for m in json.load(f)]
        tok.token2id = {t:i for i,t in enumerate(tok.tokens)}
        tok.id2token = {i:t for t,i in tok.token2id.items()}
        tok.vocab_size = len(tok.tokens)
        tok.bpe_slots = max_vocab - tok.vocab_size
        return tok

    def _split_number(self, s):
        parts, r = [], s
        while r:
            parts.insert(0, r[-2:])
            r = r[:-2]
        return parts

    def _bpe_segment(self, word):
        seq = list(word)
        for a,b in self.bpe_merges:
            i, new = 0, []
            while i < len(seq):
                if i < len(seq)-1 and (seq[i], seq[i+1]) == (a,b):
                    new.append(a+b)
                    i += 2
                else:
                    new.append(seq[i])
                    i += 1
            seq = new
        return seq

    def _segment(self, word):
        """DP segmentation: minimize number of tokens."""
        L = len(word)
        dp = [float('inf')] * (L+1)
        back = [None] * (L+1)
        dp[L] = 0

        for i in range(L-1, -1, -1):
            # try every substring word[i:j]
            for j in range(i+1, L+1):
                sub = word[i:j]
                if sub in self.token2id and dp[j] + 1 < dp[i]:
                    dp[i] = dp[j] + 1
                    back[i] = (j, sub)
        if dp[0] == float('inf'):
            raise ValueError(f"Cannot tokenize: {word}")

        # reconstruct tokens
        tokens = []
        i = 0
        while i < L:
            j, sub = back[i]
            tokens.append(sub)
            i = j
        return tokens

    def tokenize(self, text):
        out = []
        for raw in text.strip().split():
            w = raw
            # case markers
            if w.isupper():
                out.append('<UP>'); w = w.lower()
            elif w[0].isupper():
                out.append('<CAP>'); w = w.lower()

            # numeric split
            if w.isdigit():
                parts = self._split_number(w)
            else:
                parts = self._segment(w)

            # inject <NS> between parts
            out.append(parts[0])
            for p in parts[1:]:
                out.extend(['<NS>', p])

        return out

    def convert_tokens_to_ids(self, toks):
        return [self.token2id[t] for t in toks]

    def pad(self, ids, max_len):
        pad_id = self.token2id['<PAD>']
        return ids + [pad_id]*(max_len-len(ids)) if len(ids)<max_len else ids[:max_len]

    def encode(self, text, max_length=None):
        toks = self.tokenize(text)
        ids  = self.convert_tokens_to_ids(toks)
        return self.pad(ids, max_length) if max_length else ids

    def decode(self, ids):
        toks = [self.id2token[i] for i in ids if self.id2token[i] != '<PAD>']
        words, i = [], 0
        while i < len(toks):
            w = toks[i]; i+=1
            while i+1<len(toks) and toks[i]=='<NS>':
                w += toks[i+1]; i+=2
            words.append(w)
        return ' '.join(words)
