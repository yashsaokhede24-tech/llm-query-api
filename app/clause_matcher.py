from transformers import pipeline

class ClauseMatcher:
    def __init__(self):
        self.qa_pipe = pipeline("question-answering", model="deepset/roberta-base-squad2")

    def match(self, question: str, candidates):
        context = " ".join(candidates)
        result = self.qa_pipe(question=question, context=context)
        return result['answer'] if result['score'] > 0.1 else context