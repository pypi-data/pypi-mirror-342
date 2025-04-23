import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

corpus = [
    'best of luck tycs students for practical exams',
    'tycs students please carry your journal at the time of practical examination',
]

vectorizer = CountVectorizer()
x = vectorizer.fit_transform(corpus)

print("Fit Transform is ")
print(x.toarray())

df = pd.DataFrame(x.toarray(), columns=vectorizer.get_feature_names_out())
print(df)

alldata = df[(df['tycs'] == 1) & (df['journal'] == 1)]
print("Indices where both 'tycs' and 'journal' terms are present are ", alldata.index.tolist())

ordata = df[(df['tycs'] == 1) | (df['journal'] == 1)]
print("Indices where either 'tycs' or 'journal' term is present are ", ordata.index.tolist())

nodata = df[df['journal'] != 1]
print("Indices where 'journal' term is not present are ", nodata.index.tolist())
