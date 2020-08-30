from qa.dc.DomainClassifier import DomainClassifier
from qa.sp.SemanticParser import SemanticParser

class NLU:

    def __init__(self):
        self.classifier = DomainClassifier()
        self.parser = SemanticParser()

    def parse_query(self, query):
        domain = self.classifier.classify(query)
        intent = self.parser.parse(query, domain)
        return intent        