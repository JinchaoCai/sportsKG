import os
import yaml
import ahocorasick
import pandas as pd
# from query.ner.StanzaNER import StanzaNERModel
from collections import defaultdict
class SemanticParser:

    def __init__(self, data_dir='/Users/caijinchao/projects/sportsKG/data/basketball'):
        with open('/Users/caijinchao/projects/sportsKG/dict/relations.yaml', 'r') as f:
            self.relations = yaml.load(f)
        with open('/Users/caijinchao/projects/sportsKG/dict/attributes.yaml', 'r') as f:
            self.attributes = yaml.load(f)
        self.build_entity_ahocorasick(data_dir, '/Users/caijinchao/projects/sportsKG/dict/alias.yaml')
        # self.entities = defaultdict(list)
        # for file in os.listdir(data_dir):
        #     if not file.endswith('.tsv'):
        #         continue
        #     ent_t = file.replace('.tsv', '').lower().capitalize()
        #     file = os.path.join(data_dir, file)
        #     df = pd.read_csv(file, sep='\t')
        #     self.entities[ent_t].extend(list(df['name']))
        # print(self.entities)
        # self.ner_model = StanzaNERModel()

    def build_entity_ahocorasick(self, data_dir, alias_file):
        self.entities = ahocorasick.Automaton()
        with open(alias_file, 'r') as f:
            alias_dict = yaml.load(f)
        for file in os.listdir(data_dir):
            if not file.endswith('.tsv'):
                continue
            ent_t = file.replace('.tsv', '').lower().capitalize()
            file = os.path.join(data_dir, file)
            entities = list(pd.read_csv(file, sep='\t')['name'])
            for entity in entities:
                self.entities.add_word(entity, (entity, ent_t))
                if entity in alias_dict:
                    for alia in alias_dict[entity]:
                        self.entities.add_word(alia, (entity, ent_t))
        self.entities.make_automaton()

        

    def parse(self, query, domain):
        intent = defaultdict(list)
        if domain == 'sports':
            for ent in self.entities.iter(query):
                intent['entity'].append((ent[1][0], ent[1][1]))

            for attr, alias in self.attributes.items():
                for alia in alias:
                    if alia in query:
                        intent['attribute'].append(attr)

            if len(intent['entity']) == 1 and len(intent['attribute']) == 1:
                entity = intent['entity'][0]
                attribute = intent['attribute'][0]
                return "MATCH (n:{}) where n.name = '{}' return n.{}".format(entity[1], entity[0], attribute)
            if len(intent['entity']) == 2 and len(intent['attribute']) == 1:
                team, athlete = None, None
                for entity in intent['entity']:
                    if entity[1] == "Team":
                        team = entity
                    if entity[1] == 'Athlete':
                        athlete = entity
                attribute = intent['attribute'][0]
                if not team and not athlete:
                    return "MATCH (m:{})-[r:{}]->(n:{}) where m.name = '{}' return n.name".format(athlete[1], attribute, team[1], athlete[0])
        return None

    # def get_person_entities(self, query):
    #     res = []
    #     ents = self.ner_model.ner(query)
    #     for ent in ents:
    #         if ent.type == 'PERSON':
    #             res.append(ent.text)
    #     return res

if __name__ == '__main__':
    parser = SemanticParser()
    query = '易建联的身高是多少'
    domain = 'sports'
    intent = parser.parse(query, domain)
    print(parser.get_person_entities(query))