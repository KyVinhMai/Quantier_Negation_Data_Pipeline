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

def qn_patterns(quantifier: str) -> list[list[dict]]:
    assert quantifier.lower() in ("all", "every", "each")
    if quantifier.lower() == "all":
        quantifier_forms = ["all"]
    elif quantifier.lower() == "every":
        quantifier_forms = ["every", "everyone", "everyday", "everyway", "everymen", "everyman", "everybody",
                            "everydays", "everywoman", "everywomen", "everything", "everywhere", "everyplace"]
    elif quantifier.lower() == "each":
        quantifier_forms = ["each"]

    pattern1 = [
        {
            "RIGHT_ID": "anchor_aux",
            "RIGHT_ATTRS": {"POS": {"IN": ["AUX", "VERB"]}}
        },
        {
            "LEFT_ID": "anchor_aux",
            "REL_OP": ">",
            "RIGHT_ID": "noun_subject",
            "RIGHT_ATTRS": {"DEP": {"IN": ["nsubj", "nsubjpass"]}, "LOWER": {"IN": quantifier_forms}},
        },
        # {
        #     "LEFT_ID": "noun_subject",
        #     "REL_OP": ";",
        #     "RIGHT_ID": "forbidden",
        #     "RIGHT_ATTRS": {"LOWER": {"IN": ["almost", "most", "nearly", "y'", "y '"]}, "OP": "!"},
        # },
        {
            "LEFT_ID": "anchor_aux",
            "REL_OP": ">",
            "RIGHT_ID": "negation_particle",
            "RIGHT_ATTRS": {"DEP": "neg"},
        },
    ]

    pattern2 = [
        {
            "RIGHT_ID": "anchor_aux",
            "RIGHT_ATTRS": {"POS": {"IN": ["AUX", "VERB"]}}
        },
        {
            "LEFT_ID": "anchor_aux",
            "REL_OP": ">",
            "RIGHT_ID": "noun_subject",
            "RIGHT_ATTRS": {"DEP": {"IN": ["nsubj", "nsubjpass"]}},
        },
        {
            "LEFT_ID": "noun_subject",
            "REL_OP": ">",
            "RIGHT_ID": "predet",
            "RIGHT_ATTRS": {"DEP": {"IN": ["predet", "det"]}, "LOWER": {"IN": quantifier_forms}},
        },
        {
            "LEFT_ID": "anchor_aux",
            "REL_OP": ">",
            "RIGHT_ID": "negation_particle",
            "RIGHT_ATTRS": {"DEP": "neg"},
        },
    ]

    # All of our facilities are not sufficiently hardened.
    pattern3 = [
        {
            "RIGHT_ID": "anchor_aux",
            "RIGHT_ATTRS": {"POS": {"IN": ["AUX", "VERB"]}}
        },
        {
            "LEFT_ID": "anchor_aux",
            "REL_OP": ">",
            "RIGHT_ID": "noun_subject",
            "RIGHT_ATTRS": {"DEP": {"IN": ["nsubj", "nsubjpass"]}, "LOWER": {"IN": quantifier_forms}},
        },
        {
            "LEFT_ID": "anchor_aux",
            "REL_OP": ">",
            "RIGHT_ID": "auxpass",
            "RIGHT_ATTRS": {"DEP": "auxpass"},
        },
        {
            "LEFT_ID": "auxpass",
            "REL_OP": ">",
            "RIGHT_ID": "negation_particle",
            "RIGHT_ATTRS": {"DEP": "neg"},
        },
    ]

    # All are not sufficiently hardened.
    pattern4 = [
        {
            "RIGHT_ID": "anchor_aux",
            "RIGHT_ATTRS": {"POS": {"IN": ["AUX", "VERB"]}}
        },
        {
            "LEFT_ID": "anchor_aux",
            "REL_OP": ">",
            "RIGHT_ID": "noun_subject",
            "RIGHT_ATTRS": {"DEP": {"IN": ["nsubj", "nsubjpass"]}, "LOWER": {"IN": quantifier_forms}},
        },
        {
            "LEFT_ID": "anchor_aux",
            "REL_OP": ">",
            "RIGHT_ID": "auxpass",
            # Including aux and xcomp for DEP decreased false negative rate by 0.010 and increased false positive by 0.025 in all-neg fitting set
            # Decreased false negative rate by 0.000 and increased false positive by 0.021 in all-neg test set
            "RIGHT_ATTRS": {"DEP": "auxpass"},
        },
        {
            "LEFT_ID": "auxpass",
            "REL_OP": ">",
            "RIGHT_ID": "negation_particle",
            "RIGHT_ATTRS": {"DEP": "neg"},
        },
    ]

    # # The bill and all others did not go forward.
    # pattern5 = [
    #     {
    #         "RIGHT_ID": "anchor_aux",
    #         "RIGHT_ATTRS": {"POS": {"IN": ["AUX", "VERB"]}}
    #     },
    #     {
    #         "LEFT_ID": "anchor_aux",
    #         "REL_OP": ">",
    #         "RIGHT_ID": "noun_subject",
    #         "RIGHT_ATTRS": {"DEP": {"IN": ["nsubj", "nsubjpass"]}},
    #     },
    #     {
    #         "LEFT_ID": "noun_subject",
    #         "REL_OP": ">",
    #         "RIGHT_ID": "nsubj_child",
    #         "RIGHT_ATTRS": {"DEP": {"IN": ["conj", "appos"]}},
    #     },
    #     {
    #         "LEFT_ID": "nsubj_child",
    #         "REL_OP": ">",
    #         "RIGHT_ID": "predet",
    #         "RIGHT_ATTRS": {"DEP": {"IN": ["predet", "det"]}, "LOWER": {"IN": quantifier_forms}},
    #     },
    #     {
    #         "LEFT_ID": "anchor_aux",
    #         "REL_OP": ">",
    #         "RIGHT_ID": "negation_particle",
    #         "RIGHT_ATTRS": {"DEP": "neg"},
    #     },
    # ]

    # All the king's men couldn't put these two back together.
    pattern6 = [
        {
            "RIGHT_ID": "anchor_aux",
            "RIGHT_ATTRS": {"POS": {"IN": ["AUX", "VERB"]}}
        },
        {
            "LEFT_ID": "anchor_aux",
            "REL_OP": ">",
            "RIGHT_ID": "noun_subject",
            "RIGHT_ATTRS": {"DEP": {"IN": ["nsubj", "nsubjpass"]}},
        },
        {
            "LEFT_ID": "noun_subject",
            "REL_OP": ">",
            "RIGHT_ID": "nsubj_child",
            "RIGHT_ATTRS": {"DEP": {"IN": ["conj", "appos"]}},
        },
        {
            "LEFT_ID": "nsubj_child",
            "REL_OP": ">",
            "RIGHT_ID": "poss",
            "RIGHT_ATTRS": {"DEP": "poss"},
        },
        {
            "LEFT_ID": "poss",
            "REL_OP": ">",
            "RIGHT_ID": "predet",
            "RIGHT_ATTRS": {"DEP": {"IN": ["predet", "det"]}, "LOWER": {"IN": quantifier_forms}},
        },
        {
            "LEFT_ID": "anchor_aux",
            "REL_OP": ">",
            "RIGHT_ID": "negation_particle",
            "RIGHT_ATTRS": {"DEP": "neg"},
        },
    ]

    # All of that wasn't well received at all.
    pattern7 = [
        {
            "RIGHT_ID": "anchor_verb",
            "RIGHT_ATTRS": {"POS": "VERB"}
        },
        {
            "LEFT_ID": "anchor_verb",
            "REL_OP": ">",
            "RIGHT_ID": "noun_subject",
            "RIGHT_ATTRS": {"DEP": {"IN": ["nsubj", "nsubjpass"]}, "LOWER": {"IN": quantifier_forms}},
        },
        {
            "LEFT_ID": "anchor_verb",
            "REL_OP": ">",
            "RIGHT_ID": "child_aux",
            "RIGHT_ATTRS": {"DEP": "aux"},
        },
        {
            "LEFT_ID": "child_aux",
            "REL_OP": ">",
            "RIGHT_ID": "negation_particle",
            "RIGHT_ATTRS": {"DEP": "neg"},
        },
    ]

    pattern8 = [
        {
            "RIGHT_ID": "anchor_pronoun",
            "RIGHT_ATTRS": {"POS": "PRON"}
        },
        {
            "LEFT_ID": "anchor_pronoun",
            "REL_OP": ">",
            "RIGHT_ID": "noun_subject",
            "RIGHT_ATTRS": {"DEP": {"IN": ["nsubj", "nsubjpass"]}},
        },
        {
            "LEFT_ID": "noun_subject",
            "REL_OP": ">",
            "RIGHT_ID": "nsubj_child",
            "RIGHT_ATTRS": {"DEP": {"IN": ["predet", "det"]}, "LOWER": {"IN": quantifier_forms}},
        },
        {
            "LEFT_ID": "anchor_pronoun",
            "REL_OP": ">",
            "RIGHT_ID": "negation_particle",
            "RIGHT_ATTRS": {"DEP": "neg"},
        },
    ]

    return [pattern1, pattern2, pattern3, pattern4, pattern6, pattern7, pattern8]
