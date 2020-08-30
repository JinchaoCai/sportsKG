import stanza

class StanzaNERModel:

    def __init__(self, lang='zh'):
        self.model = stanza.Pipeline(lang)

    def ner(self, sents):
        res = []
        docs = self.model(sents)
        for sent in docs.sentences:
            res.extend(sent.ents)
        return res

if __name__ == '__main__':
    text = '阿联是哪个球队的'
    ner_model = StanzaNERModel()
    res = ner_model.ner(text)
    print(res)