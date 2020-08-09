from graph.Graph import SportsGraph
from query.nlu import NLU

class SportsBot:

    def __init__(self):
        self.g = SportsGraph()
        self.nlu = NLU()

    def chat(self):
        while True:
            query = input("Enter your query here:")
            intent = self.nlu.parse_query(query)
            if intent:
                result = self.g.run(intent)
                if result:
                    print('The answer of your query is {}'.format(result))
                else:
                    print('Sorry, I don\'t know the answer.')
            else:
                print('Sorry, I can\'t understand your query.')

if __name__ == '__main__':
    bot = SportsBot()
    bot.chat()