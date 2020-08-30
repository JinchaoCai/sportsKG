from py2neo import Graph

class GraphExporter:

    def __init__(self, config=None):
        self.g = Graph(
            host='127.0.0.1',
            http_port=7474,
            user='neo4j',
            password='admin'
        )

    def export_triple_to_tsv(self, output_path='./triples.tsv'):
        query = 'MATCH (n)-[r]->(m) RETURN n.name, TYPE(r), m.name'
        triples = self.g.run(query)
        with open(output_path, 'w') as f:
            for triple in triples:
                content = triple.items()
                s = content[0][1]
                p = content[1][1]
                o = content[2][1]
                f.write(s + '\t' + p + '\t' + o + '\n')

if __name__ == '__main__':
    exporter = GraphExporter()
    exporter.export_triple_to_tsv()
