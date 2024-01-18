# -*- coding: utf-8 -*-
import logging
import enum
import copy

from .tokenizer import tokenize_paragraph, TokenizerStatus, TokenizerAnomalyMessage
from .categories import ModifierCategory

log = logging.getLogger(__name__)


class ParagraphKind(enum.Enum):
    P_ALINEA = 1
    P_TABLE = 2
    P_RAW = 3


class Paragraph(object):

    def __init__(self, kind: ParagraphKind, content: str, rank: int):
        self.kind = kind
        self.content = content
        self.rank = rank

    def __repr__(self):
        return f"Paragraph({self.kind.name}, {self.rank}, '{self.content}')"


class ModifyingParagraph(Paragraph):

    def __init__(self, kind: ParagraphKind, content: str, rank: int,
            status: TokenizerStatus, category: ModifierCategory,
            classified_content: str,
            anomaly_msg: TokenizerAnomalyMessage|None=None, context=None):
        super().__init__(kind, content, rank)
        self.status = status
        self.category = category
        self.classified_content = classified_content
        self.anomaly_msg = anomaly_msg
        self.context = copy.copy(context) if context is not None else None

    @classmethod
    def from_paragraph(cls, paragraph: Paragraph, context=None):
        return cls.from_kind_and_content(paragraph.kind, paragraph.content, paragraph.rank,
            context=context)

    @classmethod
    def from_kind_and_content(cls, kind: ParagraphKind, content: str, rank: int, context=None):
        if kind != ParagraphKind.P_ALINEA:
            raise ValueError("Not an alinea")
        status, tokenizer_content, category, ano_msg = tokenize_paragraph(content,
            context=context)
        classified_content = ''.join(tokenizer_content)
        return cls(kind, content, rank, status, category, classified_content,
            anomaly_msg=ano_msg, context=context)

    def __repr__(self):
        return (f"ModifyingParagraph({self.category.name if self.category else '<notc>'}"
                f", '{self.classified_content}')")
