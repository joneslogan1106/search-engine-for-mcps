import math


class VectorCompare:
    def magnitude(self, concordance):
        if not isinstance(concordance, dict):
            raise ValueError('Supplied Argument should be of type dict')
        total = 0
        for word, count in concordance.items():
            total += count ** 2
        return math.sqrt(total)

    def relation(self, concordance1, concordance2):
        if not isinstance(concordance1, dict):
            raise ValueError('Supplied Argument 1 should be of type dict')
        if not isinstance(concordance2, dict):
            raise ValueError('Supplied Argument 2 should be of type dict')
        topvalue = 0
        for word, count in concordance1.items():
            if word in concordance2:
                topvalue += count * concordance2[word]
        denominator = self.magnitude(concordance1) * self.magnitude(concordance2)
        return topvalue / denominator if denominator != 0 else 0

    def concordance(self, document):
        if not isinstance(document, str):
            raise ValueError('Supplied Argument should be of type string')
        con = {}
        for word in document.split():
            if word in con:
                con[word] += 1
            else:
                con[word] = 1
        return con


v = VectorCompare()

documents = {
    0: '''At Scale You Will Hit Every Performance Issue I used to think I knew a bit about performance scalability...''',
    1: '''Richard Stallman to visit Australia Im not usually one to promote events and the like unless I feel...''',
    2: '''MySQL Backups Done Easily One thing that comes up a lot on sites like Stackoverflow and the like is...''',
    3: '''Why You Shouldnt roll your own CAPTCHA At a TechEd I attended a few years ago I was watching...''',
    4: '''The Great Benefit of Test Driven Development Nobody Talks About The feeling of productivity because...''',
    5: '''Setting up GIT to use a Subversion SVN style workflow Moving from Subversion SVN to GIT can be...''',
    6: '''Why CAPTCHA Never Use Numbers 0 1 5 7 Interestingly this sort of question pops up a lot in my...''',
}

index = {
    i: v.concordance(doc.lower()) for i, doc in documents.items()
}

searchterm = input('Enter Search Term: ')
query_concordance = v.concordance(searchterm.lower())

matches = []

for i in range(len(index)):
    relevance = v.relation(query_concordance, index[i])
    if relevance > 0:
        matches.append((relevance, documents[i][:100]))

matches.sort(reverse=True, key=lambda x: x[0])

for score, snippet in matches:
    print(f"{score:.4f} - {snippet}")
