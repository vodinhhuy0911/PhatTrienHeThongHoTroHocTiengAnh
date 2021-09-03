import itertools
import operator
import os

import spacy
from gensim.summarization.bm25 import BM25
from transformers import AutoTokenizer, AutoModelForQuestionAnswering, QuestionAnsweringPipeline


class QuestionProcessor:
    def __init__(self, nlp, keep=None):
        self.nlp = nlp
        self.keep = keep or {'PROPN', 'NUM', 'VERB', 'NOUN', 'ADJ', 'PRON', 'DET', 'ADV', 'PART', 'SYM'}
    def generate_question(self, text):
        doc = self.nlp(text)
        question = ' '.join(token.text for token in doc if token.pos_ in self.keep)
        return question

class PassageRetrieval:
    def __init__(self, nlp):
        self.tokenize = lambda text: [token.lemma_ for token in nlp(text)]
        self.bm25 = None
        self.passages = None
    def pre_process(self, doc):
        passages = [p for p in doc.split('\n') if p and not p.startswith('=')]
        return passages
    def fit(self, docs):
        passages = list(itertools.chain(*map(self.pre_process, docs)))
        corpus = [self.tokenize(p) for p in passages]
        self.bm25 = BM25(corpus)
        self.passages = passages
    def most_similar(self, question, topn=10):
        tokens = self.tokenize(question)
        scores = self.bm25.get_scores(tokens)
        pairs = [(s, i) for i, s in enumerate(scores)]
        pairs.sort(reverse=True)
        passages = [self.passages[i] for _, i in pairs[:topn]]
        return passages


class AnswerExtractor:
    def __init__(self, tokenizer, model):
        tokenizer = AutoTokenizer.from_pretrained(tokenizer)
        model = AutoModelForQuestionAnswering.from_pretrained(model)
        self.nlp = QuestionAnsweringPipeline(model=model, tokenizer=tokenizer)

    def extract(self, question, passages):
        answers = []
        for passage in passages:
            try:
                answer = self.nlp(question=question, context=passage)
                answer['text'] = passage
                answers.append(answer)
            except KeyError:
                pass
        answers.sort(key=operator.itemgetter('score'), reverse=True)
        return answers

class FinalAnswer:
    def generate(answer_list, answers):
        final_answers = [0.0, 0.0, 0.0, 0.0]
        max = 0
        fa = ""
        for answer in answers:
            if nlp(answer['answer']).vector_norm:
                sum = 0
                for temp0 in range(0, 4):
                    sum += float(nlp(answer_list[temp0]).similarity(nlp(answer['answer'])))
                for temp in range(0,4):
                    if final_answers[temp] < answer['score'] * float(nlp(answer_list[temp]).similarity(nlp(answer['answer']))) / sum:
                        final_answers[temp] = answer['score'] * float(nlp(answer_list[temp]).similarity(nlp(answer['answer']))) / sum
                    if max <= final_answers[temp]:
                        max = final_answers[temp]
                        if temp == 0:
                            fa = "A. "
                        elif temp == 1:
                            fa = "B. "
                        elif temp == 2:
                            fa = "C. "
                        else:
                            fa = "D. "
                        fa += answer_list[temp]

        return "Answer: " + fa
SPACY_MODEL = os.environ.get('SPACY_MODEL', 'en_core_web_lg')
QA_MODEL = os.environ.get('QA_MODEL', 'distilbert-base-cased-distilled-squad')
nlp = spacy.load(SPACY_MODEL)
question_processor = QuestionProcessor(nlp)
passage_retriever = PassageRetrieval(nlp)
answer_extractor = AnswerExtractor(QA_MODEL, QA_MODEL)

context = """WELCOME TO CLUB DAY!
Flower Club Meeting: Green thumbs, flower lovers, and romantics alike will enioy this club. Meeting today at 4:00 p.m. in Room 330 of Charlton Hall.
Stomp Club Meeting: Travel the world and swap valued stamps with fellow collectors. Meeting today at 4:30 p.m. in Room 304 of Janzen Hall.
Comics Club Meeting: Relive tales of all your favorite Superfriends with fellow comic book lovers. Meeting this evening at 7:30 p.m. in Room 717 of O'Byrne Hall 
Coin Club Meeting: Our newest club! Come swap coins from around the world. See examples of old coins and new coins, and notes from every corner of the globe. Meeting tonight at 8:00 p.m. in Room 210 of the newly built Ayres Hall."""
doc = [context]

question = """Which building was built most retently?"""
answer_list = []
answer_list.append("Charlton Hall")
answer_list.append("Sanzen Hall")
answer_list.append("0’Byrne Hall")
answer_list.append("Ayres Hall")

passage_retriever.fit(doc)
question = question_processor.generate_question(question)

print("\n", question)
passages = passage_retriever.most_similar(question)

answers = answer_extractor.extract(question, passages)
for op in answers:
    print("answer: ", op['answer'])

print("\n" + FinalAnswer.generate(answer_list, answers))

# Query Processing
    # Remove stop words
    # Remove words with specific part-of-speech
    # Converting a question into a vector
# Passage Retrieval
# Answer Extraction

