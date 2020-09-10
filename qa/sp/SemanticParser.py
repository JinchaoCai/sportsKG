import os
import re
import yaml
import ahocorasick
import pandas as pd
# from query.ner.StanzaNER import StanzaNERModel
from collections import defaultdict
class SemanticParser:

    def __init__(self, data_dir='/Users/caijinchao/projects/sportsKG/data/basketball'):
        with open('/Users/caijinchao/projects/sportsKG/dict/relations.yaml', 'r') as f:
            self.relations = yaml.load(f, Loader=yaml.FullLoader)
        with open('/Users/caijinchao/projects/sportsKG/dict/attributes.yaml', 'r') as f:
            self.attributes = yaml.load(f, Loader=yaml.FullLoader)
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
        with open('/Users/caijinchao/projects/sportsKG/qa/sp/intent.templates', 'r') as f:
            self.templates = [line.strip().split('---') for line in f.readlines() if line.strip()]

    def build_entity_ahocorasick(self, data_dir, alias_file):
        self.entities = ahocorasick.Automaton()
        with open(alias_file, 'r') as f:
            alias_dict = yaml.load(f, Loader=yaml.FullLoader)
        for file in os.listdir(data_dir):
            if not file.endswith('.tsv'):
                continue
            ent_t = file.replace('.tsv', '').lower().capitalize()
            file = os.path.join(data_dir, file)
            entities = list(pd.read_csv(file, sep='\t')['name'])
            for entity in entities:
                self.entities.add_word(entity, (entity, ent_t, entity))
                if entity in alias_dict:
                    for alia in alias_dict[entity]:
                        self.entities.add_word(alia, (entity, ent_t, alia))
        self.entities.make_automaton()


    def parse(self, query, domain):
        template = query
        d = {}
        if domain == 'sports':

            for i, ent in enumerate(self.entities.iter(query)):
                template = template.replace(ent[1][2], '{ENTITY'+str(i+1)+'}')
                d['ENTITY'+str(i+1)+'_NAME'] = ent[1][0]
                d['ENTITY'+str(i+1)+'_TYPE'] = ent[1][1]
            i = 0
            for relt, alias in self.relations.items():
                for alia in alias:
                    if alia in template:
                        i+=1
                        template = template.replace(alia, '{RELATION'+str(i)+'}')
                        d['RELATION'+str(i)+'_NAME'] = relt
            i = 0
            for attr, alias in self.attributes.items():
                for alia in alias:
                    if alia in template:
                        i+=1
                        template = template.replace(alia, '{ATTRIBUTE'+str(i)+'}')
                        d['ATTRIBUTE'+str(i)+'_NAME'] = attr
            max_score = 0
            max_score_template = None
            print(template)
            for t in self.templates:
                if re.match(t[0], template):
                    if int(t[2]) > max_score:
                        max_score = int(t[2])
                        max_score_template = t
            return max_score_template[1].format(**d)
        return None

if __name__ == '__main__':
    parser = SemanticParser()
    query = '易建联的身高和赵睿的体重是？'
    domain = 'sports'
    entities = parser.entities.iter(query)
    intent = parser.parse(query, domain)
    print(intent)
    for template in parser.templates:
        if re.match(template[0], intent):
            print(template)