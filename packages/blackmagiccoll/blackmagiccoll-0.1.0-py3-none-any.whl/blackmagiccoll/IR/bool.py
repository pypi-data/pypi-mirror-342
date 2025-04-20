import re
from collections import defaultdict
import re
from collections import defaultdict

class BoolRetrSystem:
    def __init__(self):
        self.index = defaultdict(set)

    def index_doc(self, doc_id, text):
        words = re.findall(r'\b\w+\b', text.lower())
        for word in set(words):
            self.index[word].add(doc_id)

    def search(self, query):
        terms = query.lower().split()
        result = set()
        current_op = "or"  # default operation

        for i, term in enumerate(terms):
            if term in {"and", "or", "not"}:
                current_op = term
            else:
                docs = self.index.get(term, set())

                if i == 0 or current_op == "or":
                    result |= docs
                elif current_op == "and":
                    result &= docs
                elif current_op == "not":
                    result -= docs

        return list(result)


brs = BoolRetrSystem()
brs.index_doc(1,"University Exam is sceduled next week.")
brs.index_doc(2,"The university of Mumbai has declared results")

query = "university and mumbai"
result = brs.search(query)
print("Query = ", query)
print("Result = ", result)

