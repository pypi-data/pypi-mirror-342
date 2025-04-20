from summa.summarizer import summarize

text = """
Natural language processing (NLP) is a field of computer science, artificial intelligence,
and computational linguistics concerned with the interactions between computers and human
(natural) languages. As such, NLP is related to the area of human–computer interaction.
Many challenges in NLP involve natural language understanding, natural language generation,
and machine learning.
"""

summary = summarize(text, ratio=0.6)  
print("Summary:\n", summary)
