"""
Please refer to https://universaldependencies.org/  to understand the
theory behind dependencies and https://spacy.io/api/dependencymatcher to
understand how spacy implements such dependencies

These patterns are used across the Quantifier Phrase Segmentation
And QNI files
"""

aux_pattern = [
        {
            "RIGHT_ID": "anchor_aux",
            "RIGHT_ATTRS": {"POS": {"IN": ["AUX", "VERB"]}}
        },
        {
            "LEFT_ID": "anchor_aux",
            "REL_OP": ">",
            "RIGHT_ID": "noun_subject",
            "RIGHT_ATTRS": {"DEP": {"IN" : ["nsubj", "nsubjpass"]}},
        },
        {
            "LEFT_ID": "anchor_aux",
            "REL_OP": ">",
            "RIGHT_ID": "negation_particle",
            "RIGHT_ATTRS": {"DEP": "neg"},
        },
    ]

ccomp_pattern = [
        {
            "RIGHT_ID": "anchor_aux",
            "RIGHT_ATTRS": {"POS": {"IN": ["AUX", "VERB"]}}
        },
        {
            "LEFT_ID": "anchor_aux",
            "REL_OP": ">",
            "RIGHT_ID": "noun_subject",
            "RIGHT_ATTRS": {"DEP": {"IN" : ["nsubj", "nsubjpass"]}},
        },
        {
            "LEFT_ID": "anchor_aux",
            "REL_OP": ">",
            "RIGHT_ID": "complement",
            "RIGHT_ATTRS": {"DEP": "xcomp", "POS": "VERB"},
        },
        {
            "LEFT_ID": "complement",
            "REL_OP": ">",
            "RIGHT_ID": "negation_particle",
            "RIGHT_ATTRS": {"DEP": "neg"},
        },
 ]

#somebody was going to listen to me and not judge me
xcomp_pattern = [
        {
            "RIGHT_ID": "anchor_verb",
            "RIGHT_ATTRS": {"POS": "VERB"}
        },
        {
            "LEFT_ID": "anchor_verb",
            "REL_OP": ">",
            "RIGHT_ID": "noun_subject",
            "RIGHT_ATTRS": {"DEP": {"IN" : ["nsubj", "nsubjpass"]}},
        },
        {
            "LEFT_ID": "anchor_verb",
            "REL_OP": ">",
            "RIGHT_ID": "xcomp_verb",
            "RIGHT_ATTRS": {"DEP": "xcomp", "POS": "VERB"},
        },
        {
            "LEFT_ID": "xcomp_verb",
            "REL_OP": ">",
            "RIGHT_ID": "anchor_actual_negation_phrase",
            "RIGHT_ATTRS": {"DEP": "conj", "POS": "VERB"},
        },
        {
            "LEFT_ID": "anchor_actual_negation_phrase",
            "REL_OP": ">",
            "RIGHT_ID": "negation_particle",
            "RIGHT_ATTRS": {"DEP": "neg"},
        },
 ]

#Some people will not only be looking for jobs
advmod_on_neg_pattern = [
        {
            "RIGHT_ID": "anchor_aux",
            "RIGHT_ATTRS": {"POS": "VERB"}
        },
        {
            "LEFT_ID": "anchor_aux",
            "REL_OP": ">",
            "RIGHT_ID": "noun_subject",
            "RIGHT_ATTRS": {"DEP": {"IN": ["nsubj", "nsubjpass"]}},
        },
        {
            "LEFT_ID": "anchor_aux",
            "REL_OP": ">",
            "RIGHT_ID": "adv_only",
            "RIGHT_ATTRS": {"DEP": "advmod", "POS": "ADV"},
        },
        {
            "LEFT_ID": "adv_only",
            "REL_OP": ">",
            "RIGHT_ID": "negation_particle",
            "RIGHT_ATTRS": {"DEP": "neg", "POS": "PART"},
        },
    ]

def of_pattern(quantifier: str) -> list[dict]:
    of_pattern = [
            {
                "RIGHT_ID": "anchor",
                "RIGHT_ATTRS": {}
            },
            {
                "LEFT_ID": "anchor",
                "REL_OP": ">",
                "RIGHT_ID": "anchor_of",
                "RIGHT_ATTRS": {"DEP": "prep"},
            },
            {
                "LEFT_ID": "anchor_of",
                "REL_OP": ">",
                "RIGHT_ID": "noun_pronoun",
                "RIGHT_ATTRS": {"DEP": "pobj"},
            },
            {
                "LEFT_ID": "anchor",
                "REL_OP": ">",
                "RIGHT_ID": "anchor_quantifier",
                "RIGHT_ATTRS": {"DEP": "det", "ORTH" : f"{quantifier}"},
            }
        ]

    return of_pattern

def poss_pattern(orth: str) -> list[dict]:
    poss_pattern = [
            {
                "RIGHT_ID": "anchor_poss_noun",
                "RIGHT_ATTRS": {"POS": "NOUN"}
            },
            {
                "LEFT_ID": "anchor_poss_noun",
                "REL_OP": ">",
                "RIGHT_ID": "anchor_quantifier",
                "RIGHT_ATTRS": {"DEP": "poss", "ORTH": f"{orth}"},
            },
            {
                "LEFT_ID": "anchor_quantifier",
                "REL_OP": ">",
                "RIGHT_ID": "anchor_part",
                "RIGHT_ATTRS": {"DEP":{"IN" : ["case", "advmod"]}, "POS": {"IN" : ["ADV", "PART"]}},
            }
        ]

    return poss_pattern

# Spacy often describes some nouns as adjectives. Like "veteran"
def det_pattern(orth: str) -> list[dict]:
    """
    Checks that the quantifier is attached to a noun
    > 10/9/2023 - for all neg attached predet

    """
    det_pattern = [
            {
                "RIGHT_ID": "anchor_noun",
                "RIGHT_ATTRS": {"POS": {"IN": ["NOUN", "PRON", "ADJ", "PROPN"]}}
            },
            {
                "LEFT_ID": "anchor_noun",
                "REL_OP": ">",
                "RIGHT_ID": "anchor_quant",
                "RIGHT_ATTRS": {"DEP": {"IN": ["det", "predet"]}, "POS": "DET", "ORTH": f"{orth}"}
            }
        ]

    return det_pattern

neg_pattern = [
        {
            "RIGHT_ID": "anchor_negation",
            "RIGHT_ATTRS": {"POS": "PART", "DEP": "neg"}
        },
    ]
