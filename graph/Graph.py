import os
import json
import yaml
import pandas as pd
from utils.pd_utils import read_tsv
from py2neo import Node, Graph, Relationship, NodeMatcher

class SportsGraph:

    def __init__(self, config=None):
        self.config = config
        self.g = Graph(
            host='127.0.0.1',
            http_port=7474,
            user='neo4j',
            password='admin'
            # host=config.host,
            # http_port=config.port,
            # user=config.neo4j_user,
            # password=config.neo4j_password
        )
        self.load_relations()
        self.load_attributes()
        self.create_node_in_graph()
        self.create_relation_in_graph()

    def load_relations(self, file='/Users/caijinchao/projects/sportsKG/dict/relations.yaml'):
        with open(file, 'r') as f:
            self.relations = yaml.load(f)
    
    def load_attributes(self, file='/Users/caijinchao/projects/sportsKG/dict/attributes.yaml'):
        with open(file, 'r') as f:
            self.attributes = yaml.load(f)

    def create_node_in_graph(self, data_dir='/Users/caijinchao/projects/sportsKG/data/basketball'):
        for file in os.listdir(data_dir):
            if not file.endswith('tsv'):
                continue
            node_type = file.replace('.tsv', '').lower().capitalize()
            file = os.path.join(data_dir, file)
            nodes = read_tsv(file)
            for node in nodes:
                for relation in self.relations:
                    if relation in node:
                        node.pop(relation)
                self.g.create(Node(node_type, **node))

    def create_relation_in_graph(self, data_dir='/Users/caijinchao/projects/sportsKG/data/basketball'):
        matcher = NodeMatcher(self.g)
        for file in os.listdir(data_dir):
            if not file.endswith('tsv'):
                continue
            sub_t = file.replace('.tsv', '').lower().capitalize()
            file = os.path.join(data_dir, file)
            nodes = read_tsv(file)
            for node in nodes:
                for attr in node:
                    if attr not in self.relations:
                        continue
                    sub = matcher.match(sub_t, name=node['name']).first()
                    obj_t = attr.lower().capitalize()
                    obj = matcher.match(obj_t, name=node[attr]).first()
                    if sub and obj:
                        self.g.create(Relationship(sub, attr, obj))

    def run(self, intent):
        return self.g.run(intent).data()

if __name__ == '__main__':
    g_sports = SportsGraph()