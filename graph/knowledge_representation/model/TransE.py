import torch
import torch.nn as nn
import torch.nn.functional as F

class TransE(nn.Module):

    def __init__(self, n_ents, n_rels, embed_size, p=2):
        super(TransE, self).__init__()
        self.n_ents = n_ents
        self.n_rels = n_rels
        self.embed_size = embed_size
        self.ent_embedding = nn.Embedding(self.n_ents, self.embed_size)
        self.rel_embedding = nn.Embedding(self.n_rels, self.embed_size)
        self.score = nn.PairwiseDistance(p=p)

    def init_weights(self):
        nn.init.xavier_normal_(self.ent_embedding)
        nn.init.xavier_normal_(self.rel_embedding)

    def forward(self, ss, ps, os):
        ss = self.ent_embedding(ss).view(-1, self.embed_size)
        ps = self.rel_embedding(ps).view(-1, self.embed_size)
        os = self.ent_embedding(os).view(-1, self.embed_size)
        ss = F.normalize(ss)
        ps = F.normalize(ps)
        os = F.normalize(os)
        score = self.score(os-ss, ps)
        return score