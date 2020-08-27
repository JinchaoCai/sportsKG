import torch
import torch.nn as nn
from tqdm import tqdm
from model.TransE import TransE
from data.TransEDataset import TransEDataset
from data.DumpTripleToTSV import GraphExporter

def train_one_epoch(model, optimizer, pos_dataset, neg_dataset, batch_size=32):
    pos_generator = torch.utils.data.DataLoader(
        pos_dataset, batch_size=batch_size, shuffle=True
    )
    neg_generator = torch.utils.data.DataLoader(
        neg_dataset, batch_size=batch_size, shuffle=True
    )
    model.train()
    train_loss = 0.0
    criterion = nn.MarginRankingLoss(1e-3, reduction='mean')
    for pos_batch, neg_batch in tqdm(zip(pos_generator, neg_generator)):
        pss, pps, pos = pos_batch
        nss, nps, nos = neg_batch
        optimizer.zero_grad()
        pos_loss = model(pss, pps, pos)
        neg_loss = model(nss, nps, nos)
        loss = criterion(neg_loss, pos_loss, torch.ones_like(pos_loss))
        loss.backward()
        optimizer.step()
        train_loss += loss.item()
    train_loss /= len(pos_dataset)
    return train_loss

if __name__ == '__main__':
    exporter = GraphExporter()
    exporter.export_triple_to_tsv()
    pos_dataset = TransEDataset('./triples.tsv')
    neg_dataset = TransEDataset('./triples.tsv', neg=True)
    num_ents = pos_dataset.num_ents()
    num_rels = pos_dataset.num_rels()
    model = TransE(num_ents, num_rels, 300)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-5)
    for epoch in range(3):
        train_loss = train_one_epoch(model, optimizer, pos_dataset, neg_dataset)
        print('[Epoch {}], loss: {}'.format(epoch, train_loss))
