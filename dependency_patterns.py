aux_pattern = [
        {
            "RIGHT_ID": "anchor_is",
            "RIGHT_ATTRS": {"POS": "AUX"}
        },
        {
            "LEFT_ID": "anchor_is",
            "REL_OP": ">",
            "RIGHT_ID": "noun_subject",
            "RIGHT_ATTRS": {"DEP": {"IN" : ["nsubj", "nsubjpass"]}, "ORTH":{}},
        },
        {
            "LEFT_ID": "anchor_is",
            "REL_OP": ">",
            "RIGHT_ID": "negation_particle",
            "RIGHT_ATTRS": {"DEP": "neg"},
        },
        {
            "LEFT_ID": "anchor_is",
            "REL_OP": ">",
            "RIGHT_ID": "associated_word",
            "RIGHT_ATTRS": {"DEP": {"IN": ["amod", "compound"]}},
        },

    ]

verb_pattern = [
    {
        "RIGHT_ID": "anchor_verb",
        "RIGHT_ATTRS": {"POS": "VERB"}
    },
    {
        "LEFT_ID": "anchor_verb",
        "REL_OP": ">",
        "RIGHT_ID": "noun_subject",
        "RIGHT_ATTRS": {"DEP": "nsubj"},
    },
    {
        "LEFT_ID": "anchor_verb",
        "REL_OP": ">",
        "RIGHT_ID": "aux_word",
        "RIGHT_ATTRS": {"DEP": "aux"},
    },
    {
        "LEFT_ID": "anchor_verb",
        "REL_OP": ">",
        "RIGHT_ID": "negation_word",
        "RIGHT_ATTRS": {"DEP": "neg", "POS": "PART"},
    }
]

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
        }
    ]