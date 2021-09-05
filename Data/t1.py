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

def get_context(path):
    fread = open(path, "r", encoding="utf-8")
    txt = fread.read()
    fread.close()
    context = txt.split("Questions:")
    context = context[0].strip()
    return context

def get_question_list(path):
    fread = open(path, "r", encoding="utf-8")
    txt = fread.read()
    fread.close()
    context = txt.split("Questions:")
    question = context[1].strip().split("\n")
    return question

def get_question(q_list):
    question = q_list.split("__")
    return question

SPACY_MODEL = os.environ.get('SPACY_MODEL', 'en_core_web_lg')
QA_MODEL = os.environ.get('QA_MODEL', 'distilbert-base-cased-distilled-squad')
nlp = spacy.load(SPACY_MODEL)
question_processor = QuestionProcessor(nlp)
passage_retriever = PassageRetrieval(nlp)
answer_extractor = AnswerExtractor(QA_MODEL, QA_MODEL)

context = get_context("22.txt")
doc = [context]

question_list = get_question_list("22.txt")
for q in question_list:
    question = q.split("__")[0]
    print("\nQuestion: ", question)
    temp = get_question(q)
    answer_list = []
    for i in range(1, 5):
        if i == 4 and temp[i].__contains__("("):
            answer_list.append(temp[i].split("(")[0].strip())
            print(temp[i].split("(")[0].strip())
        else:
            answer_list.append(temp[i])
            print(temp[i])

    passage_retriever.fit(doc)
    question = question_processor.generate_question(question)
    passages = passage_retriever.most_similar(question)
    answers = answer_extractor.extract(question, passages)

    print(FinalAnswer.generate(answer_list, answers))

# Query Processing
    # Remove stop words
    # Remove words with specific part-of-speech
    # Converting a question into a vector
# Passage Retrieval
# Answer Extraction

