# -*- coding: utf-8 -*-
import enum
import logging
import re

import ply.lex as lex  # Voir http://www.dabeaz.com/ply/ply.html#ply_nn1

from .categories import ModifierCategory

log = logging.getLogger(__name__)


tokens = (
    'MARKUP',
    'ALINEA_NUMBER',
    'ARTICLE_NUMBER',
    'SPACES',
    'PUNCT',
    'MOD_INTRODUCE_MODIFICATION',
    'MOD_INTRODUCE_SUPPRESSION',
    'MOD_APPEND',
    'MOD_INSERT_HEAD',
    'MOD_INSERT_SECTION',
    'MOD_AFTER',
    'MOD_INSERT_AFTER',
    'MOD_REPLACE',
    'MOD_REPLACE_WITH',
    'MOD_SUPPRESS_WORDS',
    'MOD_SUPPRESS',
    'MOD_ABROGATE',
    'MOD_INSERT_ALINEA_SINGLE',
    'MOD_INSERT_ONE_START',
    'MOD_INSERT_MANY_START',
    'MOD_REPLACE_ONE_START',
    'MOD_REPLACE_MANY_START',
    'MOD_SECTION',
    'GUILLEMET_O',
    'GUILLEMET_F',
    'ENTITY',
    'WORD',
    'NUMBER',
    'QUOTES',
)

t_MARKUP      = r"</?(p|div|span)[^>]*>"
t_NUMBER      = r'\d+([\w\-\./]*\d+)?°?'
t_SPACES      = r'\s+'
t_PUNCT       = r'[;:.,?!]'
t_ENTITY      = r'&\w+;'
t_QUOTES      = r'[“\'"]'

# TODO: << www >> reperer les mots changés
# TODO: repérer les alinea single
# TODO: repérer les alinea open

#
# Alinea number
#
alinea_number = (
    r"("
    r"\w\)(?=\s+)"
    r"|\d{1,2}°(\s+bis)?(?=\.?\s+)"
    r"|\d{1,2}(\s+bis)?(?=\.?\s+)"
    r"|[IVX]+(?=\.\s+)"
    r")"
)

@lex.TOKEN(alinea_number)
def t_ALINEA_NUMBER(t):
    return t

#
# Article number
#
article_qualifier = (
    r"([Aa]rt\.|[Aa]rticle)"

)
article_num = (
    r"([LRDA]\.?\s+)?\d+[\d\-]*(\s+\-\d+)?(\s*([bB]is|[tT]er))?"

)
article_number = (
    r"("+article_qualifier+r"\s+"+article_num+r"\.)"
)

@lex.TOKEN(article_number)
def t_ARTICLE_NUMBER(t):
    return t

#
# nredac-section
#

section_num = (
    '('
    '[IVX\d]+(er)?(\s*([bB]is|[tT]er))?|unique|[Ll]égislative|[Rr]églementaire'
    ')'
)
section_kind = (
    '('
    '[Pp]artie|[Ss]ous[-\s]section|[Ss]ous[-\s][Pp]aragraphe|[Cc]hapitre|[Ss]ection|[Ll]ivre|[Pp]aragraphe|[Tt]itre'
    ')'
)
section = (
    '('+section_kind+'\s+'+section_num+')'
)

@lex.TOKEN(section)
def t_MOD_SECTION(t):
    return t

#
# nredac-insert-section
#
insert_section = (
    '('
    'est\s+ins[ée]r[ée]e?(.*?)intitul[ée](\s*|&nbsp;):\s*«'
    '|intitulé(.*?)est\s+ainsi\s+r[ée]dig[ée](\s*|&nbsp;):\s*«'
    ')'
)


@lex.TOKEN(insert_section)
def t_MOD_INSERT_SECTION(t):
    return t


#
# nredac-introduce-modification
#
introduce = (
    r'('
    r'est\s+ainsi\s+modifi[ée]e?(\s*|&nbsp;):'
    r'|est\s+modifi[ée]e?\s+ainsi\s+qu\'il\s+suit(\s*|&nbsp;):'
    r'|est\s+modifi[ée]e?\s+comme\s+il\s+suit(\s*|&nbsp;):'
    r')'
)

@lex.TOKEN(introduce)
def t_MOD_INTRODUCE_MODIFICATION(t):
    return t


suppress_next = (
    r'('
    r'est\s+supprim[ée]e?(\s*|&nbsp;):'
    r')'
)
@lex.TOKEN(suppress_next)
def t_MOD_INTRODUCE_SUPPRESSION(t):
    return t

#
# nredac-insert-head
#
insert_head = (
    r'('
    r'est\s+précédé\s+de\s+la\s+mention(\s*|&nbsp;):\s*«'
    r'|[lL]e\s+début\s+(du|de)(.*?)\s+est\s+ainsi\s+rédigée?(\s*|&nbsp;):\s*«'
    r')'
)

@lex.TOKEN(insert_head)
def t_MOD_INSERT_HEAD(t):
    return t


#
# nredac-insert-after
#
after = (
    r'('
    r'[aA]pr[eè]s\s+les?\s+mots?(\s*|&nbsp;):\s*«'
    r'|[Aa]près\s+la\s+référence(\s*|&nbsp;):\s*«'
    r'|[aA]près\s+la\s+première\s+occurrence\s+du\s+mot(\s*|&nbsp;):\s*«'
    r')'
)
insert_after = (
    r'('
    r'(sont|est)\s+ins[ée]r[ée]s?\s+les?\s+mots?(\s*|&nbsp;):\s*«'
    r'|(sont|est)\s+ins[ée]r[ée]e?s?\s+(les|la)\s+références?(\s*|&nbsp;):\s*«'
    r'|[lL]es\s+mots\s+suivants\s+sont\s+ajoutés(\s*|&nbsp;):\s*«'
    r'|la\s+fin\s+du.*est\s+ainsi\s+r[ée]dig[ée]e(\s*|&nbsp;):\s*«'
    r')'
)

@lex.TOKEN(after)
def t_MOD_AFTER(t):
    return t

@lex.TOKEN(insert_after)
def t_MOD_INSERT_AFTER(t):
    return t


#
# nredac-append
#
insert = (
    r'('
    r'[eE]st\s+compl[ée]t[ée]e?\s+par\s+les?\s+mots?(\s*|&nbsp;):\s*«'
    r'|[eE]st\s+ajout[ée]\s+le\s+mot(\s*|&nbsp;):\s*«'
    r'|[sS]ont\s+ajout[ée]s\s+les\s+mots(\s*|&nbsp;):\s*«'
    r'|[lL]es\s+mots\s+suivants\s+sont\s+ajoutés(\s*|&nbsp;):\s*«'
    r'|[eE]st\s+compl[ée]t[ée]e?\s+par\s+une\s+phrase\s+ainsi\s+rédig[eé]e(\s*|&nbsp;):\s*«'
    r'|[sS]ont\s+complétés\s+par\s+les\s+mots(\s*|&nbsp;):\s*«'
    r'|[Ll]e\s+début\s+de(.*?)est\s+ainsi\s+rédigé(\s*|&nbsp;):\s*«'
    r'|(sont|est)\s+ins[ée]r[ée]s?\s+les?\s+mots?(\s*|&nbsp;):\s*«'
    r'|(sont|est)\s+ins[ée]r[ée]e?s?\s+(les|la)\s+références?(\s*|&nbsp;):\s*«'
    r'|[lL]es\s+mots\s+suivants\s+sont\s+ajoutés(\s*|&nbsp;):\s*«'
    r'|la\s+fin\s+du.*est\s+ainsi\s+r[ée]dig[ée]e(\s*|&nbsp;):\s*«'
    r'|est\s+ajout[ée]e\s+la\s+mention(\s*|&nbsp;):\s*«'
    r')'
)

@lex.TOKEN(insert)
def t_MOD_APPEND(t):
    return t


#
# nredac-replace
#
#r'[Ll]es?\s+mots?(\s*|&nbsp;):\s*«[^»]+»\s*et\s+les?\s+mots?(\s*|&nbsp;):\s*«'

replace = (
    r'('
    r'[Ll]es?\s+mots?(\s*|&nbsp;):\s*«'
    r'|([lL]a|[lL]es)\s+r[eé]f[ée]rences?(\s*|&nbsp;):\s*«'
    r'|[lL]a\s+(seconde|deuxi[èe]me)\s+occurrence\s+du\s+mot(\s*|&nbsp;):\s*«'
    r'|[Ll]es?\s+mots?(\s*|&nbsp;)\s*«'
    r')'
)
replace_with = (
    r'('
    r'(sont|est)\s+remplac[ée]e?s?\s+par\s+les?\s+mots?(\s*|&nbsp;):\s*«'
    r'|sont\s+remplac[ée]e?s\s+par\s+(la|les)\s+r[eé]f[ée]rences?(\s*|&nbsp;):\s*«'
    r'|est\s+remplac[ée]e\s+par\s+(la|les)\s+r[eé]f[ée]rences?(\s*|&nbsp;):\s*«'
    r'|sont\s+remplac[ée]s\s+par(\s*|&nbsp;):?\s*«'
    r')'
)

@lex.TOKEN(replace)
def t_MOD_REPLACE(t):
    return t


@lex.TOKEN(replace_with)
def t_MOD_REPLACE_WITH(t):
    return t

#
# nredac-suppress-words
#
suppress_words = (
    r"("
    r"\s*»\s+est\s+supprim[ée]e?"
    r"|\s*»\s+sont\s+supprim[ée]e?s"
    r")"
)

@lex.TOKEN(suppress_words)
def t_MOD_SUPPRESS_WORDS(t):
    return t


#
# nredac-suppress
#
suppress = (
    r"("
    r"est\s*supprim[ée]e?\s*;?"
    r")"
)

@lex.TOKEN(suppress)
def t_MOD_SUPPRESS(t):
    return t

#
# nredac-abrogate
#
abrogate = (
    r"("
    r"est\s+abrog[ée]e?"
    r"|sont\s+abrog[eé]e?s"
    r")"
)

@lex.TOKEN(abrogate)
def t_MOD_ABROGATE(t):
    return t


#
# nredac-alinea-single
#
alinea_single = r"est\s+compl[eé]t[eé]\s+par\s+l'alin[ée]a\s+suivant\s*:\s*"


@lex.TOKEN(alinea_single)
def t_MOD_INSERT_ALINEA_SINGLE(t):
    return t


#
# nredac-insert-one, nredac-insert-many
#
insert_one_start = (
    r"([Ii]l\s+est\s+(ins[eé]r[eé]|ajout[eé])\s+une?\s+(.*?)ainsi\s+r[eé]dig[eé]e?(\s*|&nbsp;):"
    r"|(sont|est)\s+compl[ée]t[ée]e?s?\s+par\s+(.*?)ainsi\s+r[eé]dig[eé]e?(\s*|&nbsp;):"
    r"|(sont|est)\s+compl[ée]t[ée]e?s?\s+d'un\s+(.*?)ainsi\s+r[eé]dig[eé]e?(\s*|&nbsp;):"
    r"|est\s+r[eé]dig[ée]e?\s+comme\s+suit(\s*|&nbsp;):"
    r"|est\s+ajout[ée]\s+le\s+tableau\s+suivant(\s*|&nbsp;):"
    r"|[Ee]st\s+ajoutée\s+une\s+phrase\s+ainsi\s+rédigée(\s*|&nbsp;):"
    r"|[Ee]st\s+r[ée]tablie?\s+une?(.*?)ainsi\s+r[ée]dig[eé]e?(\s*|&nbsp;):"
    r"|[eE]st\s+ainsi\s+rétabli(\s*|&nbsp;):"
    r"|[eE]st\s+(insérée?|ajoutée?)(.*?)ainsi\s+rédigée?(\s*|&nbsp;):"
    r"|[eE]st\s+compl[eé]t[eé]\s+par\s+l'alin[ée]a\s+suivant(\s*|&nbsp;):"
    r"|[eE]st\s+complét[ée]e?\s+ainsi\s+qu\'il\s+suit(\s*|&nbsp;):"
    r"|[eE]st\s+ainsi\s+compl[ée]t[ée](\s*|&nbsp;):"
    r"|il\s+est\s+ajout[eé]\s+au\s+sein\s+de\s+la\s+section(.*?)une\s+ligne(\s*|&nbsp;):"
    r")"
)
insert_many_start = (
    r"("
    r"est\s+compl[eé]t[eé]e?\s+par\s+[dl]es\s+articles(.*?)ainsi\s+rédigés(\s*|&nbsp;):"
    r"|[sS]ont\s+ajoutés\s+(.*?)ainsi\s+rédigés(\s*|&nbsp;):"
    r"|[sS]ont\s+insérés\s+(.*?)ainsi\s+rédigés(\s*|&nbsp;):"
    r"|[sS]ont\s+ainsi\s+r[eé]dig[eé]e?s(\s*|&nbsp;):"
    r"|est\s+compl[ée]t[ée]\s+(par\s+les|des)\s+dispositions\s+suivantes(\s*|&nbsp;):"
    r"|sont\s+ins[ée]r[ée]e?s?\s+deux(.*?)ainsi\s+r[ée]dig[ée]e?s?(\s*|&nbsp;):"
    r"|est\s+compl[eé]t[eé]\s+par\s+les\s+alin[ée]as\s+suivants(\s*|&nbsp;):"
    r")"
)

@lex.TOKEN(insert_one_start)
def t_MOD_INSERT_ONE_START(t):
    return t


@lex.TOKEN(insert_many_start)
def t_MOD_INSERT_MANY_START(t):
    return t

#
# nredac-replace-one, nredac-replace-many
#
replace_one_start = (
    r"(est\s+remplac[ée]e?\s+par\s+"
    r"(les\s+dispositions\s+suivantes|la\s+liste\s+suivante)"
    r"|est\s+remplac[ée]\s+comme\s+suit"
    r"|est\s+ainsi\s+rédigé"
    r"|sont\s+remplacés\s+par\s+un\s+alinéa\s+ainsi\s+rédigé"
    r"|est\s+remplac[ée]\s+par(.*?)ainsi\s+r[ée]dig[ée]e?s?"
    r"|est\s+r[eé]dig[ée]\s+ainsi\s+qu\'il\s+suit(\s*|&nbsp;):"
    r")"
)

replace_many_start = (
    r"("
    r"sont\s+remplac[eé]e?s\s+par\s+les\s+dispositions\s+suivantes"
    r"|sont\s+remplacés\s+par(.*?)ainsi\s+r[eé]dig[eé]e?s?(\s*|&nbsp;):"
    r")"
)

@lex.TOKEN(replace_one_start)
def t_MOD_REPLACE_ONE_START(t):
    return t

@lex.TOKEN(replace_many_start)
def t_MOD_REPLACE_MANY_START(t):
    return t

#
# WORD mot
#
word = (r"[A-Z]\.[A-Z]|[a-zA-ZéèêëàâäôùûîïÉÈÊËÀÂÄÔÙÛÜÎÏæÆœŒçÇ][a-zA-ZéèêëàâäôùûîïÉÈÊËÀÂÄÔÙÛÜÎÏæÆœŒçÇ\-]*")
@lex.TOKEN(word)
def t_WORD(t):
    return t


#
# Guillemets
#
guillemet_o = r'«'
guillemet_f = r'»'


@lex.TOKEN(guillemet_o)
def t_GUILLEMET_O(t):
    return t


@lex.TOKEN(guillemet_f)
def t_GUILLEMET_F(t):
    return t


def t_error(t):
    #print "Illegal character %s" % (py_encode_basestring_ascii(t.value[0]))
    t.lexer.skip(1)


table_re = re.compile(r'<div class="ali-table">.*</div>', re.U|re.I)

open_alinea_with_section_re = re.compile(
    (
        r"(?P<before>\s*«\s*)"
        + r"(?P<section_kind>" + section_kind + r")"
        + r"\s+(?P<section_num>" + section_num + r")"
        + r"(?P<sep>\s*[-—-]?\s*)"
        + r"(?P<content>.*?$)"
    ),
    re.I|re.U)

lexer = lex.lex(reflags=re.UNICODE)


class TokenizerStatus(enum.Enum):

    OK = 0
    WARNING = 1
    KO = 2


class TokenizerAnomaly(enum.Enum):
    DUPSECTION = 0
    DUPARTICLE = 1
    INSERTAFTER_IN_BADCAT = 2
    INTRODUCESUPPRESSION_IN_BADCAT = 3
    REPLACEWITH_IN_BADCAT = 4
    INSERTONESTART_IN_BADCAT = 5
    REPLACEONESTART_IN_BADCAT = 6
    APPEND_INSERTAFTER_IN_BADCAT = 7
    APPEND_IN_BADCAT = 8
    INSERTHEAD_IN_BADCAT = 9
    INSERTSECTION_IN_BADCAT = 10
    INSERTMANYSTART_IN_BADCAT = 11
    REPLACEMANYSTART_IN_BADCAT = 12
    INTRODUCEMODIFICATION_IN_BADCAT = 13
    DUPSUPPRESS = 14
    DUPSUPPRESSREPLACEWORDS = 15
    DUPREPLACEWORDS = 16


class TokenizerAnomalyMessage(object):

    messages = {
        TokenizerAnomaly.DUPSECTION: "duplicated section",
        TokenizerAnomaly.DUPARTICLE: "duplicated article",
        TokenizerAnomaly.INSERTAFTER_IN_BADCAT: "in bad cat",
        TokenizerAnomaly.INTRODUCESUPPRESSION_IN_BADCAT: "in bad cat",
        TokenizerAnomaly.REPLACEWITH_IN_BADCAT: "in bad cat",
        TokenizerAnomaly.INSERTONESTART_IN_BADCAT: "in bad cat",
        TokenizerAnomaly.REPLACEONESTART_IN_BADCAT: "in bad cat",
        TokenizerAnomaly.APPEND_INSERTAFTER_IN_BADCAT: "in bad cat",
        TokenizerAnomaly.APPEND_IN_BADCAT: "in bad cat",
        TokenizerAnomaly.INSERTHEAD_IN_BADCAT: "in bad cat",
        TokenizerAnomaly.INSERTSECTION_IN_BADCAT: "in bad cat",
        TokenizerAnomaly.INSERTMANYSTART_IN_BADCAT: "in bad cat",
        TokenizerAnomaly.REPLACEMANYSTART_IN_BADCAT: "in bad cat",
        TokenizerAnomaly.INTRODUCEMODIFICATION_IN_BADCAT: "in bad cat",
        TokenizerAnomaly.DUPSUPPRESS: "duplicated suppress",
        TokenizerAnomaly.DUPSUPPRESSREPLACEWORDS: "duplicated suppress replace words",
        TokenizerAnomaly.DUPREPLACEWORDS: "duplicated suppress words",
    }

    def __init__(self, token: str, anomaly: TokenizerAnomaly, badcat: ModifierCategory|None=None):
        self.token = token
        self.anomaly = anomaly
        self.badcat = badcat
        self.message = f"{token}: {self.messages[anomaly]}"
        if badcat:
            self.message += f" ({badcat.name})"

    def __repr__(self):
        if self.badcat:
            return f'{self.token},{self.anomaly.value},{self.badcat.value}'
        else:
            return f'{self.token},{self.anomaly.value}'

    def __str__(self):
        return f"{self.token}: {self.anomaly.name}: {self.message}"

    def to_tuple(self):
        if self.badcat:
            return (self.token, self.anomaly.value, self.badcat.value)
        else:
            return (self.token, self.anomaly.value)


def tokenizer_warning(msg, context=None):
    if context is not None:
        log.warning(f"{str(context)}: {msg}")
    else:
        log.warning(msg)


def tokenizer_anomaly(token: str, anomaly: TokenizerAnomaly, context=None, badcat: ModifierCategory|None=None):
    anomaly_message = TokenizerAnomalyMessage(token, anomaly, badcat=badcat)
    tokenizer_warning(str(anomaly_message), context=context)
    return anomaly_message


def tokenize_paragraph(s, context=None):
    if '<div class="ali-table">' in s:
        s = table_re.sub('', s)
    lexer.input(s)
    status = TokenizerStatus.OK  # OK (1=WARNING, 2=KO)
    replace_stack = []
    cat = ModifierCategory.NOT_MODIFYING
    html = []
    pending_guillemet = False
    inside_guillemet = False
    article = None
    section = None
    anomaly_msg = None
    while True:
        tok = lexer.token()
        if not tok:
            break      # No more input
        if tok.type == 'MARKUP':
            if not html:
                return status, ''.join(html), cat
            html.append(tok.value)
            pending_guillemet = False
        elif tok.type == 'QUOTES':
            html.append(tok.value)
            pending_guillemet = False
        elif tok.type == 'GUILLEMET_O':
            if not html:
                cat = ModifierCategory.OPEN_ALINEA
            inside_guillemet = True
        elif tok.type == 'GUILLEMET_F':
            if cat == ModifierCategory.OPEN_ALINEA:
                pending_guillemet = True
            if inside_guillemet:
                inside_guillemet = False
            elif cat == ModifierCategory.NOT_MODIFYING:
                pending_guillemet = True
        elif tok.type in ('SPACES', 'PUNCT', 'ENTITY'):
            if html:
                html.append(' ')
        elif tok.type == 'MOD_AFTER':
            pending_guillemet = False
            html.append(tok.value)
            replace_stack.append(tok.type)
            inside_guillemet = True
        elif tok.type == 'INSERT_AFTER':
            inside_guillemet = True
            pending_guillemet = False
            html.append(tok.value)
            if replace_stack and replace_stack[0] in 'MOD_AFTER':
                if cat == ModifierCategory.NOT_MODIFYING:
                    cat = ModifierCategory.INSERT_AFTER
                else:
                    status = TokenizerStatus.WARNING
                    anomaly_msg = tokenizer_anomaly(
                        tok.type,
                        TokenizerAnomaly.INSERTAFTER_IN_BADCAT,
                        context=context, badcat=cat)
            elif cat == ModifierCategory.NOT_MODIFYING:
                cat = ModifierCategory.APPEND
            else:
                status = TokenizerStatus.WARNING
                anomaly_msg = tokenizer_anomaly(
                    tok.type,
                    TokenizerAnomaly.INSERTAFTER_IN_BADCAT,
                    context=context, badcat=cat)
        elif tok.type == 'MOD_REPLACE':
            pending_guillemet = False
            html.append(tok.value)
            replace_stack.append(tok.type)
            inside_guillemet = True
        elif tok.type == 'MOD_REPLACE_WITH':
            pending_guillemet = False
            html.append(tok.value)
            if replace_stack and replace_stack[0] == 'MOD_REPLACE':
                if cat == ModifierCategory.NOT_MODIFYING:
                    cat = ModifierCategory.REPLACE_WITH
                else:
                    status = TokenizerStatus.WARNING
                    anomaly_msg = tokenizer_anomaly(
                        tok.type,
                        TokenizerAnomaly.REPLACEWITH_IN_BADCAT,
                        context=context, badcat=cat)
            inside_guillemet = True
        elif tok.type == 'MOD_INSERT_ONE_START':
            pending_guillemet = False
            html.append(tok.value)
            if cat == ModifierCategory.NOT_MODIFYING:
                cat = ModifierCategory.INSERT_ONE_START
            else:
                status = TokenizerStatus.WARNING
                anomaly_msg = tokenizer_anomaly(
                    tok.type,
                    TokenizerAnomaly.INSERTONESTART_IN_BADCAT,
                    context=context, badcat=cat)
        elif tok.type == 'MOD_REPLACE_ONE_START':
            pending_guillemet = False
            html.append(tok.value)
            if cat == ModifierCategory.NOT_MODIFYING:
                cat = ModifierCategory.REPLACE_ONE_START
            else:
                status = TokenizerStatus.WARNING
                anomaly_msg = tokenizer_anomaly(
                    tok.type,
                    TokenizerAnomaly.REPLACEONESTART_IN_BADCAT,
                    context=context, badcat=cat)
        elif tok.type == 'MOD_APPEND':
            pending_guillemet = False
            inside_guillemet = True
            html.append(tok.value)
            if replace_stack and replace_stack[0] == 'MOD_AFTER':
                if cat == ModifierCategory.NOT_MODIFYING:
                    cat = ModifierCategory.INSERT_AFTER
                else:
                    status = TokenizerStatus.WARNING
                    anomaly_msg = tokenizer_anomaly(
                        tok.type,
                        TokenizerAnomaly.APPEND_INSERTAFTER_IN_BADCAT,
                        context=context, badcat=cat)
            elif cat == ModifierCategory.NOT_MODIFYING:
                cat = ModifierCategory.APPEND
            else:
                status = TokenizerStatus.WARNING
                anomaly_msg = tokenizer_anomaly(
                    tok.type,
                    TokenizerAnomaly.APPEND_IN_BADCAT,
                    context=context, badcat=cat)
        elif tok.type == 'MOD_INSERT_HEAD':
            pending_guillemet = False
            inside_guillemet = True
            html.append(tok.value)
            if cat == ModifierCategory.NOT_MODIFYING:
                cat = ModifierCategory.INSERT_HEAD
            else:
                status = TokenizerStatus.WARNING
                anomaly_msg = tokenizer_anomaly(
                    tok.type,
                    TokenizerAnomaly.INSERTHEAD_IN_BADCAT,
                    context=context, badcat=cat)
        elif tok.type == 'MOD_INSERT_SECTION':
            pending_guillemet = False
            inside_guillemet = True
            html.append(tok.value)
            if cat == ModifierCategory.NOT_MODIFYING:
                cat = ModifierCategory.INSERT_SECTION
            else:
                status = TokenizerStatus.WARNING
                anomaly_msg = tokenizer_anomaly(
                    tok.type,
                    TokenizerAnomaly.INSERTSECTION_IN_BADCAT,
                    context=context, badcat=cat)
        elif tok.type == 'MOD_INSERT_MANY_START':
            pending_guillemet = False
            html.append(tok.value)
            if cat == ModifierCategory.NOT_MODIFYING:
                cat = ModifierCategory.INSERT_MANY_START
            else:
                status = TokenizerStatus.WARNING
                anomaly_msg = tokenizer_anomaly(
                    tok.type,
                    TokenizerAnomaly.INSERTMANYSTART_IN_BADCAT,
                    context=context, badcat=cat)
        elif tok.type == 'MOD_REPLACE_MANY_START':
            pending_guillemet = False
            html.append(tok.value)
            if cat == ModifierCategory.NOT_MODIFYING:
                cat = ModifierCategory.REPLACE_MANY_START
            else:
                status = TokenizerStatus.WARNING
                anomaly_msg = tokenizer_anomaly(
                    tok.type,
                    TokenizerAnomaly.REPLACEMANYSTART_IN_BADCAT,
                    context=context, badcat=cat)
        elif tok.type == 'MOD_SUPPRESS_WORDS':
            pending_guillemet = False
            inside_guillemet = False
            html.append(tok.value)
            if replace_stack and replace_stack[0] == 'MOD_REPLACE':
                if cat == ModifierCategory.NOT_MODIFYING:
                    cat = ModifierCategory.SUPPRESS_WORDS
                else:
                    status = TokenizerStatus.WARNING
                    anomaly_msg = tokenizer_anomaly(
                        tok.type,
                        TokenizerAnomaly.DUPSUPPRESSREPLACEWORDS,
                        context=context, badcat=cat)
            elif cat == ModifierCategory.NOT_MODIFYING:
                cat = ModifierCategory.SUPPRESS_WORDS
            else:
                status = TokenizerStatus.WARNING
                anomaly_msg = tokenizer_anomaly(
                    tok.type,
                    TokenizerAnomaly.DUPREPLACEWORDS,
                    context=context, badcat=cat)
        elif tok.type == 'MOD_SUPPRESS':
            pending_guillemet = False
            html.append(tok.value)
            if cat == ModifierCategory.NOT_MODIFYING:
                cat = ModifierCategory.SUPPRESS
            else:
                status = TokenizerStatus.WARNING
                anomaly_msg = tokenizer_anomaly(
                    tok.type,
                    TokenizerAnomaly.DUPSUPPRESS, context=context)
        elif tok.type == 'MOD_ABROGATE':
            pending_guillemet = False
            html.append(tok.value)
            cat = ModifierCategory.ABROGATE
        elif tok.type == 'MOD_INTRODUCE_MODIFICATION':
            pending_guillemet = False
            html.append(tok.value)
            if cat == ModifierCategory.NOT_MODIFYING:
                cat = ModifierCategory.INTRODUCE_MODIFICATION
            else:
                status = TokenizerStatus.WARNING
                anomaly_msg = tokenizer_anomaly(
                    tok.type,
                    TokenizerAnomaly.INTRODUCEMODIFICATION_IN_BADCAT,
                    context=context, badcat=cat)
        elif tok.type == 'MOD_INTRODUCE_SUPPRESSION':
            pending_guillemet = False
            html.append(tok.value)
            if cat == ModifierCategory.NOT_MODIFYING:
                cat = ModifierCategory.INTRODUCE_SUPPRESSION
            else:
                status = TokenizerStatus.WARNING
                anomaly_msg = tokenizer_anomaly(
                    tok.type,
                    TokenizerAnomaly.INTRODUCESUPPRESSION_IN_BADCAT,
                    context=context, badcat=cat)
        elif tok.type == 'ARTICLE_NUMBER':
            if not html:
                if article is not None:
                    status = TokenizerStatus.WARNING
                    anomaly_msg = tokenizer_anomaly(
                        tok.type,
                        TokenizerAnomaly.DUPARTICLE, context=context)
                else:
                    article = tok.value
            html.append(tok.value)
        elif tok.type == 'MOD_SECTION':
            if not html:
                if section is not None:
                    status = TokenizerStatus.WARNING
                    anomaly_msg = tokenizer_anomaly(
                        tok.type,
                        TokenizerAnomaly.DUPSECTION, context=context)
                else:
                    section = tok.value
            html.append(tok.value)
        else:
            if not inside_guillemet and pending_guillemet and cat == ModifierCategory.OPEN_ALINEA:
                pending_guillemet = False
                cat = ModifierCategory.NOT_MODIFYING
            html.append(tok.value)
    if pending_guillemet and cat == ModifierCategory.OPEN_ALINEA:
        cat = ModifierCategory.SINGLE_ALINEA
    elif pending_guillemet:
        cat = ModifierCategory.CLOSE_ALINEA
    if cat == ModifierCategory.OPEN_ALINEA and article:
        cat = ModifierCategory.OPEN_ALINEA_WITH_ARTICLE
    elif cat == ModifierCategory.OPEN_ALINEA and section:
        cat = ModifierCategory.OPEN_ALINEA_WITH_SECTION
    elif cat == ModifierCategory.CLOSE_ALINEA and article:
        cat = ModifierCategory.CLOSE_ALINEA_WITH_ARTICLE
    elif cat == ModifierCategory.SINGLE_ALINEA and article:
        cat = ModifierCategory.SINGLE_ALINEA_WITH_ARTICLE
    return status, ''.join(html), cat, anomaly_msg
