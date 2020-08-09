import os
import json
import pandas as pd
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
        # self.create_team_nodes()
        # self.create_athlete_nodes()

    def create_team_nodes(self):
        teams = self.read_tsv('/Users/caijinchao/projects/sportsKG/data/basketball/teams.tsv')
        for team in teams:
            node = Node('Team', **team)
            self.g.create(node)

    def create_athlete_nodes(self):
        matcher = NodeMatcher(self.g)
        athletes = self.read_tsv('/Users/caijinchao/projects/sportsKG/data/basketball/athletes.tsv')
        for athlete in athletes:
            if 'team' in athlete:
                team = athlete.pop('team')
            team = matcher.match('Team', name=team).first()
            node = Node('Athlete', **athlete)
            self.g.create(node)
            if team:
                rel = Relationship(node, 'belongsTo', team)
                self.g.create(rel)

    def run(self, intent):
        return self.g.run(intent).data()

    @staticmethod
    def read_tsv(file):
        df = pd.read_csv(file, sep='\t')
        return df.to_dict(orient='records')

if __name__ == '__main__':
    g_sports = SportsGraph()
