# -*- coding: utf-8 -*-
import enum
import logging

log = logging.getLogger(__name__)


class ModifierCategory(enum.Enum):

    NOT_MODIFYING = 0
    MODIFYING = 1
    # An open Alinea '« ....'
    OPEN_ALINEA = 2
    # An alinea with 'after', 'insert after' build.
    # Contains two « ... » groups.
    INSERT_AFTER = 3
    # An alinea with 'replace', 'with'
    # Contains two « ... » groups.
    REPLACE_WITH = 4
    # An alinea introducing a new article. Next one should be SINGLE_ALINEA
    INSERT_ONE_START = 5
    # An alinea that append words after
    # Contains one « ... » group.
    APPEND = 6
    # An alinea introducing new articles. Next one should be OPEN_ALINEA
    INSERT_MANY_START = 7
    # A single Alinea '« .... »'
    SINGLE_ALINEA = 8
    # An alinea introducing a replacement of an article. Next one should be SINGLE_ALINEA
    REPLACE_ONE_START = 9
    # An alinea introducing a replacement of many articles. Next one should be OPEN_ALINEA
    REPLACE_MANY_START = 10
    # Some weird alinea only closing...
    CLOSE_ALINEA = 11
    # Suppress
    SUPPRESS = 12
    # Suppress words
    SUPPRESS_WORDS = 13
    # Abrogate
    ABROGATE = 14
    # Introducing a modification
    INTRODUCE_MODIFICATION = 15
    # Variants with articles
    OPEN_ALINEA_WITH_ARTICLE = 16
    SINGLE_ALINEA_WITH_ARTICLE = 17
    CLOSE_ALINEA_WITH_ARTICLE = 18
    # Introducing a suppression
    INTRODUCE_SUPPRESSION = 19
    # An alinea between two open/close alineas
    BETWEEN_ALINEA = 20
    # Insert head
    INSERT_HEAD = 21
    # Insert section
    INSERT_SECTION = 22
    # Open alinea with section
    OPEN_ALINEA_WITH_SECTION = 23

    @classmethod
    def not_modifying(cls, cat_id):
        return cat_id in (
            cls.NOT_MODIFYING,
        )

    @classmethod
    def contains_modification(cls, cat_id):
        return cat_id in (
            cls.INSERT_AFTER,
            cls.REPLACE_WITH,
            cls.APPEND,
            cls.SUPPRESS_WORDS,
            cls.INSERT_HEAD,
            cls.INSERT_SECTION,
        )

    @classmethod
    def contains_modification_actions(cls, cat_id):
        return cat_id in (
            cls.SUPPRESS,
            cls.ABROGATE,
        )

    @classmethod
    def introduce_modification_group(cls, cat_id):
        return cat_id in (
            cls.INTRODUCE_MODIFICATION,
            cls.INTRODUCE_SUPPRESSION,
        )

    @classmethod
    def is_modifying(cls, cat_id):
        return cat_id in (
            cls.OPEN_ALINEA,
            cls.SINGLE_ALINEA,
            cls.CLOSE_ALINEA,
            cls.OPEN_ALINEA_WITH_ARTICLE,
            cls.SINGLE_ALINEA_WITH_ARTICLE,
            cls.CLOSE_ALINEA_WITH_ARTICLE,
            cls.BETWEEN_ALINEA,
            cls.OPEN_ALINEA_WITH_SECTION,
        )

    @classmethod
    def is_modifyin_with_article(cls, cat_id):
        return cat_id in (
            cls.OPEN_ALINEA_WITH_ARTICLE,
            cls.SINGLE_ALINEA_WITH_ARTICLE,
            cls.CLOSE_ALINEA_WITH_ARTICLE,
        )

    @classmethod
    def is_modifying_with_section(cls, cat_id):
        return cat_id in (
            cls.OPEN_ALINEA_WITH_SECTION,
        )

    @classmethod
    def introduce_modification(cls, cat_id):
        return cat_id in (
            cls.REPLACE_ONE_START,
            cls.INSERT_ONE_START,
            cls.INSERT_MANY_START,
            cls.REPLACE_MANY_START,
        )
