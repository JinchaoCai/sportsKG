import yaml
import pandas as pd
from collections import defaultdict
class SemanticParser:

    def __init__(self, config=None):
        self.config = config
        with open('/Users/caijinchao/projects/sportsKG/dict/attributes.yaml', 'r') as f:
            self.attrs = yaml.load(f)
        self.team_entities = []
        self.athlete_entities = []
        with open('/Users/caijinchao/projects/sportsKG/data/basketball/teams.tsv') as f:
            df = pd.read_csv(f, sep='\t')
            self.team_entities.extend(list(df['name']))
        with open('/Users/caijinchao/projects/sportsKG/data/basketball/athletes.tsv') as f:
            df = pd.read_csv(f, sep='\t')
            self.athlete_entities.extend(list(df['name']))

    def parse(self, query, domain):
        intent = defaultdict(list)
        if domain == 'sports':
            for entity in self.team_entities:
                if entity in query:
                    intent['entity'].append((entity, 'Team'))
            for entity in self.athlete_entities:
                if entity in query:
                    intent['entity'].append((entity, 'Athlete'))
            for attr, alias in self.attrs.items():
                for alia in alias:
                    if alia in query:
                        intent['attribute'].append(attr) 
            if len(intent['entity']) == 1 and len(intent['attribute']) == 1:
                entity = intent['entity'][0]
                attribute = intent['attribute'][0]
                return "MATCH (n:{}) where n.name = '{}' return n.{}".format(entity[1], entity[0], attribute)
        return None

if __name__ == '__main__':
    parser = SemanticParser()
    query = '易建联的身高是多少'
    domain = 'sports'
    intent = parser.parse(query, domain)
    print(intent)
