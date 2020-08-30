import torch
import random
from torch.utils.data import Dataset

class TransEDataset(Dataset):

    def __init__(self, raw_data, neg=False):
        with open(raw_data, 'r') as f:
            lines = f.readlines()
            triples = [line.strip().split('\t') for line in lines if line.strip()]
        self.triples = triples
        self.ent_vocab = {}
        self.rel_vocab = {}
        for triple in triples:
            if triple[0] not in self.ent_vocab:
                self.ent_vocab[triple[0]] = len(self.ent_vocab)
            if triple[2] not in self.ent_vocab:
                self.ent_vocab[triple[2]] = len(self.ent_vocab)
            if triple[1] not in self.rel_vocab:
                self.rel_vocab[triple[1]] = len(self.rel_vocab)
        if neg:
            indices = list(self.ent_vocab.values())
            self.inv_ent_vocab = {v:k for k, v in self.ent_vocab.items()}
            for triple in triples:
                random_entity = triple[2]
                while random_entity == triple[2]:
                    random_entity = self.inv_ent_vocab[random.choice(indices)]
                triple[2] = random_entity

    def __len__(self):
        return len(self.triples)
    
    def __getitem__(self, i):
        s, p, o = self.triples[i]
        s, p, o = self.ent_vocab[s], self.rel_vocab[p], self.ent_vocab[o]
        return torch.tensor(s), torch.tensor(p), torch.tensor(o)

    def num_ents(self):
        return len(self.ent_vocab)
    
    def num_rels(self):
        return len(self.rel_vocab)