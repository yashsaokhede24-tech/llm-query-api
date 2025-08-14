import fitz # PyMuPDF
from typing import List
from .llm_parser import LLMParser
from .vector_db import EmbeddingSearch
from .clause_matcher import ClauseMatcher
from .logic_evaluator import LogicEvaluator

class RetrievalPipeline:
    def __init__(self):
        self.llm_parser = LLMParser()
        self.embedding_search = EmbeddingSearch()
        self.clause_matcher = ClauseMatcher()
        self.logic_evaluator = LogicEvaluator()

    def pdf_to_text(self, pdf_bytes: bytes) -> str:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        return "\n".join(page.get_text() for page in doc)

    def process(self, pdf_bytes: bytes, questions: List[str]) -> List[str]:
        document_text = self.pdf_to_text(pdf_bytes)
        self.embedding_search.index_document(document_text)
        answers = []
        for q in questions:
            query_struct = self.llm_parser.parse(q)
            candidates = self.embedding_search.retrieve(query_struct)
            clause = self.clause_matcher.match(q, candidates)
            answer = self.logic_evaluator.evaluate(q, clause)
            answers.append(answer)
        return answers
