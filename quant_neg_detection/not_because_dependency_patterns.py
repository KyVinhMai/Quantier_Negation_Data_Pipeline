not_because_match_patterns = [
    # not <neg VERB >mark because
    [
        # anchor token: some verb (anchor_verb)
        {"RIGHT_ID": "anchor_verbAux", "RIGHT_ATTRS": {"POS": {"IN": ["VERB", "AUX"]}}},
        # verb > neg: anchor_verb is the right parent of a negation
        {
            "LEFT_ID": "anchor_verbAux",
            "REL_OP": ">",
            "RIGHT_ID": "negation_particle",
            "RIGHT_ATTRS": {"DEP": "neg"},
        },
        # verb >mark "because": anchor_verb is the left parent of "because", "because" is a marker for anchor_verb
        {
            "LEFT_ID": "anchor_verbAux",
            "REL_OP": ">++",
            "RIGHT_ID": "because",
            "RIGHT_ATTRS": {"ORTH": "because", "DEP": "mark"},
        },
        {
            "LEFT_ID": "negation_particle",
            "REL_OP": "$++",
            "RIGHT_ID": "because_right_sibling",
            "RIGHT_ATTRS": {"ORTH": "because"},
        },
    ],

    # not <neg VERB >prep because
    [
        # anchor token: some verb (anchor_verb)
        {"RIGHT_ID": "anchor_verb", "RIGHT_ATTRS": {"POS": "VERB"}},
        # verb > neg: anchor_verb is the right parent of a negation
        {
            "LEFT_ID": "anchor_verb",
            "REL_OP": ">",
            "RIGHT_ID": "negation_particle",
            "RIGHT_ATTRS": {"DEP": "neg"},
        },
        # verb >prep "because": anchor_verb is the left parent of "because", "because" is a preposition for anchor_verb
        {
            "LEFT_ID": "anchor_verb",
            "REL_OP": ">++",
            "RIGHT_ID": "because",
            "RIGHT_ATTRS": {"ORTH": "because", "DEP": "prep"},
        },
    ],

    # not <neg VERB >advcl >mark because
    [
        # anchor token: some verb to be anchor_verb
        {"RIGHT_ID": "anchor_verb", "RIGHT_ATTRS": {"POS": "VERB"}},
        # anchor_verb > neg: anchor_verb is the immediate head and right parent of a negation
        {
            "LEFT_ID": "anchor_verb",
            "REL_OP": ">",
            "RIGHT_ID": "negation_particle",
            "RIGHT_ATTRS": {"DEP": "neg"},
        },
        # anchor_verb > advcl_child_verb: advcl_child_verb is the adverbial clause modifier and child of anchor_verb
        {
            "LEFT_ID": "anchor_verb",
            "REL_OP": ">",
            "RIGHT_ID": "advcl_child_verb",
            "RIGHT_ATTRS": {"DEP": "advcl"},
        },
        # advcl_child_verb > "because": "because" is a marker for and left child of advcl_child_verb
        {
            "LEFT_ID": "advcl_child_verb",
            "REL_OP": ">--",
            "RIGHT_ID": "because",
            "RIGHT_ATTRS": {"ORTH": "because", "DEP": "mark"},
        },
        {
            "LEFT_ID": "anchor_verb",
            "REL_OP": ">",
            "RIGHT_ID": "nsubjpass_child",
            "RIGHT_ATTRS": {"DEP": "nsubjpass", "OP": "!"},
        },
    ],

    # not <neg VERB >ccomp >advcl VERB >mark because
    [
        # anchor token: some verb to be anchor_verb
        {"RIGHT_ID": "anchor_verb", "RIGHT_ATTRS": {"POS": "VERB"}},
        # anchor_verb > neg: anchor_verb is the immediate head and right parent of a negation
        {
            "LEFT_ID": "anchor_verb",
            "REL_OP": ">",
            "RIGHT_ID": "negation_particle",
            "RIGHT_ATTRS": {"DEP": "neg"},
        },
        # anchor_verb > ccomp_child_aux: ccomp_child_aux is the clausal complement and child of anchor_verb
        {
            "LEFT_ID": "anchor_verb",
            "REL_OP": ">",
            "RIGHT_ID": "ccomp_child_aux",
            "RIGHT_ATTRS": {"DEP": "ccomp"},
        },
        # ccomp_child_aux > advcl_child_verb: advcl_child_verb is the adverbial clause modifier and child of ccomp_child_aux
        {
            "LEFT_ID": "ccomp_child_aux",
            "REL_OP": ">",
            "RIGHT_ID": "advcl_child_verb",
            "RIGHT_ATTRS": {"DEP": "advcl"},
        },
        # advcl_child_verb > "because": "because" is a marker for and  child of advcl_child_verb
        {
            "LEFT_ID": "advcl_child_verb",
            "REL_OP": ">",
            "RIGHT_ID": "because",
            "RIGHT_ATTRS": {"ORTH": "because", "DEP": "mark"},
        },
    ],

    # not <neg VERB >xcomp >advcl >mark because
    [
        # anchor token: some verb to be anchor_verb
        {"RIGHT_ID": "anchor_verb", "RIGHT_ATTRS": {"POS": "VERB"}},
        # anchor_verb > neg: anchor_verb is the immediate head and right parent of a negation
        {
            "LEFT_ID": "anchor_verb",
            "REL_OP": ">",
            "RIGHT_ID": "negation_particle",
            "RIGHT_ATTRS": {"DEP": "neg"},
        },
        # anchor_verb > xcomp_child_aux: xcomp_child_aux is the clausal complement and child of anchor_verb
        {
            "LEFT_ID": "anchor_verb",
            "REL_OP": ">",
            "RIGHT_ID": "xcomp_child_aux",
            "RIGHT_ATTRS": {"DEP": "xcomp"},
        },
        # xcomp_child_aux > advcl_child_verb: advcl_child_verb is the adverbial clause modifier and child of xcomp_child_aux
        {
            "LEFT_ID": "xcomp_child_aux",
            "REL_OP": ">",
            "RIGHT_ID": "advcl_child_verb",
            "RIGHT_ATTRS": {"DEP": "advcl"},
        },
        # advcl_child_verb > "because": "because" is a marker for and  child of advcl_child_verb
        {
            "LEFT_ID": "advcl_child_verb",
            "REL_OP": ">",
            "RIGHT_ID": "because",
            "RIGHT_ATTRS": {"ORTH": "because", "DEP": "mark"},
        },
    ],

    # not <neg VERB >"in order to" >advcl >mark because
    [
        {"RIGHT_ID": "anchor_verb", "RIGHT_ATTRS": {"POS": "VERB"}},
        {
            "LEFT_ID": "anchor_verb",
            "REL_OP": ">",
            "RIGHT_ID": "negation_particle",
            "RIGHT_ATTRS": {"DEP": "neg"},
        },
        {
            "LEFT_ID": "anchor_verb",
            "REL_OP": ">",
            "RIGHT_ID": "in",
            "RIGHT_ATTRS": {"DEP": "prep", "ORTH": "in"},
        },
        {
            "LEFT_ID": "in",
            "REL_OP": ">",
            "RIGHT_ID": "order",
            "RIGHT_ATTRS": {"DEP": "pobj", "ORTH": "order"},
        },
        {
            "LEFT_ID": "order",
            "REL_OP": ">",
            "RIGHT_ID": "inOrder_child_verb",
            "RIGHT_ATTRS": {"DEP": "acl"},
        },
        {
            "LEFT_ID": "inOrder_child_verb",
            "REL_OP": ">",
            "RIGHT_ID": "advcl_child_verb",
            "RIGHT_ATTRS": {"DEP": "advcl"},
        },
        {
            "LEFT_ID": "advcl_child_verb",
            "REL_OP": ">",
            "RIGHT_ID": "because",
            "RIGHT_ATTRS": {"ORTH": "because", "DEP": "mark"},
        },
    ],

    # not <neg VERB >advcl >ccomp >mark because
    [
        # anchor token: some verb to be anchor_verb
        {"RIGHT_ID": "anchor_verb", "RIGHT_ATTRS": {"POS": "VERB"}},
        # anchor_verb > neg: anchor_verb is the immediate head and right parent of a negation
        {
            "LEFT_ID": "anchor_verb",
            "REL_OP": ">",
            "RIGHT_ID": "negation_particle",
            "RIGHT_ATTRS": {"DEP": "neg"},
        },
        # anchor_verb > advcl_child_verb: advcl_child_verb is the adverbial clause modifier and child of anchor_verb
        {
            "LEFT_ID": "anchor_verb",
            "REL_OP": ">",
            "RIGHT_ID": "advcl_child_verb",
            "RIGHT_ATTRS": {"DEP": "advcl"},
        },
        # advcl_child_verb > ccomp_child_aux: ccomp_child_aux is the clausal complement and child of advcl_child_verb
        {
            "LEFT_ID": "advcl_child_verb",
            "REL_OP": ">",
            "RIGHT_ID": "ccomp_child_verbAux",
            "RIGHT_ATTRS": {"DEP": "ccomp"},
        },
        # ccomp_child_aux > "because": "because" is a marker for and child of ccomp_child_aux
        {
            "LEFT_ID": "ccomp_child_verbAux",
            "REL_OP": ">",
            "RIGHT_ID": "because",
            "RIGHT_ATTRS": {"ORTH": "because", "DEP": "mark"},
        },
    ],

    # not <neg <ccomp VERB >advcl >mark because
    [
        {"RIGHT_ID": "anchor_verb", "RIGHT_ATTRS": {"POS": "VERB"}},
        {
            "LEFT_ID": "anchor_verb",
            "REL_OP": ">",
            "RIGHT_ID": "ccomp_child_verbAux",
            "RIGHT_ATTRS": {"DEP": "ccomp"},
        },
        {
            "LEFT_ID": "ccomp_child_verbAux",
            "REL_OP": ">",
            "RIGHT_ID": "negation_particle",
            "RIGHT_ATTRS": {"DEP": "neg"},
        },
        {
            "LEFT_ID": "anchor_verb",
            "REL_OP": ">",
            "RIGHT_ID": "advcl_child_verb",
            "RIGHT_ATTRS": {"DEP": "advcl"},
        },
        {
            "LEFT_ID": "advcl_child_verb",
            "REL_OP": ">",
            "RIGHT_ID": "because",
            "RIGHT_ATTRS": {"ORTH": "because", "DEP": "mark"},
        },
    ],

    # not <neg <acomp VERB >advcl >mark because
    [
        {"RIGHT_ID": "anchor_verb", "RIGHT_ATTRS": {"POS": "VERB"}},
        {
            "LEFT_ID": "anchor_verb",
            "REL_OP": ">",
            "RIGHT_ID": "acomp_child_verbAux",
            "RIGHT_ATTRS": {"DEP": "acomp"},
        },
        {
            "LEFT_ID": "acomp_child_verbAux",
            "REL_OP": ">",
            "RIGHT_ID": "negation_particle",
            "RIGHT_ATTRS": {"DEP": "neg"},
        },
        {
            "LEFT_ID": "anchor_verb",
            "REL_OP": ">",
            "RIGHT_ID": "advcl_child_verb",
            "RIGHT_ATTRS": {"DEP": "advcl"},
        },
        {
            "LEFT_ID": "advcl_child_verb",
            "REL_OP": ">",
            "RIGHT_ID": "because",
            "RIGHT_ATTRS": {"ORTH": "because", "DEP": "mark"},
        },
    ],

    # not <neg <advmod VERB >advcl >mark because
    [
        {"RIGHT_ID": "anchor_verb", "RIGHT_ATTRS": {"POS": "VERB"}},
        {
            "LEFT_ID": "anchor_verb",
            "REL_OP": ">",
            "RIGHT_ID": "advcl_child_verb1",
            "RIGHT_ATTRS": {"DEP": "advcl"},
        },
        {
            "LEFT_ID": "advcl_child_verb1",
            "REL_OP": ">",
            "RIGHT_ID": "advmod_child_verbAux",
            "RIGHT_ATTRS": {"DEP": "advmod", "POS": {"IN": ["ADP", "VERB", "AUX"]}},
        },
        {
            "LEFT_ID": "advmod_child_verbAux",
            "REL_OP": ">",
            "RIGHT_ID": "negation_particle",
            "RIGHT_ATTRS": {"DEP": "neg"},
        },
        {
            "LEFT_ID": "anchor_verb",
            "REL_OP": ">",
            "RIGHT_ID": "advcl_child_verb2",
            "RIGHT_ATTRS": {"DEP": "advcl"},
        },
        {
            "LEFT_ID": "advcl_child_verb2",
            "REL_OP": ">",
            "RIGHT_ID": "because",
            "RIGHT_ATTRS": {"ORTH": "because", "DEP": "mark"},
        },
    ],

    # not <neg VERB >prep >prep because
    [
        {"RIGHT_ID": "anchor_verb", "RIGHT_ATTRS": {"POS": "VERB"}},
        {
            "LEFT_ID": "anchor_verb",
            "REL_OP": ">",
            "RIGHT_ID": "negation_particle",
            "RIGHT_ATTRS": {"DEP": "neg"},
        },
        {
            "LEFT_ID": "anchor_verb",
            "REL_OP": ">",
            "RIGHT_ID": "prep1",
            "RIGHT_ATTRS": {"DEP": "prep"},
        },
        {
            "LEFT_ID": "prep1",
            "REL_OP": ">",
            "RIGHT_ID": "prep2",
            "RIGHT_ATTRS": {"ORTH": "because", "DEP": "prep"},
        },
    ],

    # not <neg AUX >mark because
    [
        {"RIGHT_ID": "anchor_aux", "RIGHT_ATTRS": {"POS": "AUX"}},
        {
            "LEFT_ID": "anchor_aux",
            "REL_OP": ">",
            "RIGHT_ID": "negation_particle",
            "RIGHT_ATTRS": {"DEP": "neg"},
        },
        {
            "LEFT_ID": "anchor_aux",
            "REL_OP": ">",
            "RIGHT_ID": "because",
            "RIGHT_ATTRS": {"ORTH": "because", "DEP": "mark"},
        },
    ],

    # not <neg AUX >prep because
    [
        {"RIGHT_ID": "anchor_aux", "RIGHT_ATTRS": {"POS": "AUX"}},
        {
            "LEFT_ID": "anchor_aux",
            "REL_OP": ">",
            "RIGHT_ID": "negation_particle",
            "RIGHT_ATTRS": {"DEP": "neg"},
        },
        {
            "LEFT_ID": "anchor_aux",
            "REL_OP": ">",
            "RIGHT_ID": "because",
            "RIGHT_ATTRS": {"ORTH": "because", "DEP": "prep"},
        },
        {
            "LEFT_ID": "negation_particle",
            "REL_OP": ".",
            "RIGHT_ID": "immediately_following_because",
            "RIGHT_ATTRS": {"ORTH": "because", "OP": "!"},
        },
    ],

    # not <neg AUX >advcl >mark because
    [
        {"RIGHT_ID": "anchor_aux", "RIGHT_ATTRS": {"POS": "AUX"}},
        {
            "LEFT_ID": "anchor_aux",
            "REL_OP": ">",
            "RIGHT_ID": "negation_particle",
            "RIGHT_ATTRS": {"DEP": "neg"},
        },
        {
            "LEFT_ID": "anchor_aux",
            "REL_OP": ">++",
            "RIGHT_ID": "advcl_child_aux",
            "RIGHT_ATTRS": {"DEP": "advcl"},
        },
        {
            "LEFT_ID": "advcl_child_aux",
            "REL_OP": ">--",
            "RIGHT_ID": "because",
            "RIGHT_ATTRS": {"ORTH": "because", "DEP": "mark"},
        },
    ],

    # not <neg <ccomp AUX >advcl >mark because
    [
        {"RIGHT_ID": "anchor_aux", "RIGHT_ATTRS": {"POS": "AUX"}},
        {
            "LEFT_ID": "anchor_aux",
            "REL_OP": ">",
            "RIGHT_ID": "ccomp_child",
            "RIGHT_ATTRS": {"DEP": "ccomp"},
        },
        {
            "LEFT_ID": "ccomp_child",
            "REL_OP": ">",
            "RIGHT_ID": "negation_particle",
            "RIGHT_ATTRS": {"DEP": "neg"},
        },
        {
            "LEFT_ID": "anchor_aux",
            "REL_OP": ">",
            "RIGHT_ID": "advcl_child",
            "RIGHT_ATTRS": {"DEP": "advcl"},
        },
        {
            "LEFT_ID": "advcl_child",
            "REL_OP": ">",
            "RIGHT_ID": "because",
            "RIGHT_ATTRS": {"ORTH": "because", "DEP": "mark"},
        },
    ],
]

not_because_forbidden_patterns = [
    # because >conj >mark because
    [
        {"RIGHT_ID": "anchor_because", "RIGHT_ATTRS": {"ORTH": "because"}},
        {
            "LEFT_ID": "anchor_because",
            "REL_OP": ">",
            "RIGHT_ID": "conj_child",
            "RIGHT_ATTRS": {"DEP": "conj"},
        },
        {
            "LEFT_ID": "conj_child",
            "REL_OP": ">",
            "RIGHT_ID": "descendant_because",
            "RIGHT_ATTRS": {"DEP": "mark", "ORTH": "because"},
        },
    ],

    # because > because
    [
        {"RIGHT_ID": "anchor_because", "RIGHT_ATTRS": {"ORTH": "because"}},
        {
            "LEFT_ID": "anchor_because",
            "REL_OP": ">",
            "RIGHT_ID": "conj_child",
            "RIGHT_ATTRS": {"ORTH": "because"},
        },
    ],

    # because <mark anchor_verbAux >conj >mark because
    #                                    > neg
    # because... not because
    [
        {"RIGHT_ID": "anchor_verbAux", "RIGHT_ATTRS": {"POS": {"IN": ["VERB", "AUX"]}}},
        {
            "LEFT_ID": "anchor_verbAux",
            "REL_OP": ">",
            "RIGHT_ID": "descendant_because1",
            "RIGHT_ATTRS": {"DEP": "mark", "ORTH": "because"},
        },
        {
            "LEFT_ID": "anchor_verbAux",
            "REL_OP": ">",
            "RIGHT_ID": "conj_child",
            "RIGHT_ATTRS": {"DEP": "conj"},
        },
        {
            "LEFT_ID": "conj_child",
            "REL_OP": ">",
            "RIGHT_ID": "descendant_because2",
            "RIGHT_ATTRS": {"DEP": "mark", "ORTH": "because"},
        },
    ],

    # because <mark anchor_verbAux >advcl >mark because
    #         <neg
    # not because... because
    [
        {"RIGHT_ID": "anchor_verbAux", "RIGHT_ATTRS": {"POS": {"IN": ["VERB", "AUX"]}}},
        {
            "LEFT_ID": "anchor_verbAux",
            "REL_OP": ">",
            "RIGHT_ID": "descendant_because1_1",
            "RIGHT_ATTRS": {"DEP": "mark", "ORTH": "because"},
        },
        {
            "LEFT_ID": "anchor_verbAux",
            "REL_OP": ">",
            "RIGHT_ID": "negation_particle",
            "RIGHT_ATTRS": {"DEP": "neg"},
        },
        {
            "LEFT_ID": "descendant_because1_1",
            "REL_OP": ";*",
            "RIGHT_ID": "negation_particle_2",
            "RIGHT_ATTRS": {"ORTH": "because"},
        },
        {
            "LEFT_ID": "anchor_verbAux",
            "REL_OP": ">",
            "RIGHT_ID": "advcl_child",
            "RIGHT_ATTRS": {"DEP": "advcl"},
        },
        {
            "LEFT_ID": "advcl_child",
            "REL_OP": ">",
            "RIGHT_ID": "descendant_because2",
            "RIGHT_ATTRS": {"DEP": "mark", "ORTH": "because"},
        },
    ],

    # not <neg VERB >mark because
    #     >advcl
    # neg immediately precede because
    [
        # anchor token: some verb (anchor_verb)
        {"RIGHT_ID": "anchor_verbAux", "RIGHT_ATTRS": {"POS": {"IN": ["VERB", "AUX"]}, "DEP": "advcl"}},
        # verb > neg: anchor_verb is the right parent of a negation
        {
            "LEFT_ID": "anchor_verbAux",
            "REL_OP": ">--",
            "RIGHT_ID": "negation_particle",
            "RIGHT_ATTRS": {"DEP": "neg", "LOWER": "not"},
        },
        # verb >mark "because": anchor_verb is the left parent of "because", "because" is a marker for anchor_verb
        {
            "LEFT_ID": "anchor_verbAux",
            "REL_OP": ">--",
            "RIGHT_ID": "because",
            "RIGHT_ATTRS": {"ORTH": "because", "DEP": "mark"},
        },
        {
            "LEFT_ID": "negation_particle",
            "REL_OP": ".",
            "RIGHT_ID": "immediately_following_because",
            "RIGHT_ATTRS": {"ORTH": "because"},
        },
    ],

    # not <neg VERB >advcl >mark because
    #     <auxpass (-ing)
    # not being worked because
    [
        {"RIGHT_ID": "anchor_verb", "RIGHT_ATTRS": {"POS": "VERB"}},
        {
            "LEFT_ID": "anchor_verb",
            "REL_OP": ">",
            "RIGHT_ID": "negation_particle",
            "RIGHT_ATTRS": {"DEP": "neg"},
        },
        {
            "LEFT_ID": "anchor_verb",
            "REL_OP": ">",
            "RIGHT_ID": "advcl_child_verb",
            "RIGHT_ATTRS": {"DEP": "advcl"},
        },
        {
            "LEFT_ID": "advcl_child_verb",
            "REL_OP": ">--",
            "RIGHT_ID": "because",
            "RIGHT_ATTRS": {"ORTH": "because", "DEP": "mark"},
        },
        {
            "LEFT_ID": "anchor_verb",
            "REL_OP": ">",
            "RIGHT_ID": "auxpass_child",
            "RIGHT_ATTRS": {"DEP": "auxpass", "TAG": "VBG"},
        },
    ],

    # not <neg "have" >advcl >mark because
    #     $dobj
    # had not a good time because
    [
        {"RIGHT_ID": "anchor_verb", "RIGHT_ATTRS": {"POS": "VERB", "LOWER": {"IN": ["have", "had"]}}},
        {
            "LEFT_ID": "anchor_verb",
            "REL_OP": ">++",
            "RIGHT_ID": "negation_particle",
            "RIGHT_ATTRS": {"DEP": "neg"},
        },
        {
            "LEFT_ID": "anchor_verb",
            "REL_OP": ">",
            "RIGHT_ID": "advcl_child_verb",
            "RIGHT_ATTRS": {"DEP": "advcl"},
        },
        {
            "LEFT_ID": "advcl_child_verb",
            "REL_OP": ">--",
            "RIGHT_ID": "because",
            "RIGHT_ATTRS": {"ORTH": "because", "DEP": "mark"},
        },
        {
            "LEFT_ID": "negation_particle",
            "REL_OP": "$++",
            "RIGHT_ID": "dobj_sibling",
            "RIGHT_ATTRS": {"DEP": "dobj"},
        },
    ],

    # not <neg <ccomp VERB >advcl >mark because
    #     <aux
    [
        # anchor token: some verb to be anchor_verb
        {"RIGHT_ID": "anchor_verb", "RIGHT_ATTRS": {"POS": "VERB"}},
        {
            "LEFT_ID": "anchor_verb",
            "REL_OP": ">",
            "RIGHT_ID": "ccomp_child",
            "RIGHT_ATTRS": {"DEP": "ccomp"},
        },
        {
            "LEFT_ID": "ccomp_child",
            "REL_OP": ">",
            "RIGHT_ID": "negation_particle",
            "RIGHT_ATTRS": {"DEP": "neg"},
        },
        {
            "LEFT_ID": "anchor_verb",
            "REL_OP": ">",
            "RIGHT_ID": "advcl_child",
            "RIGHT_ATTRS": {"DEP": "advcl"},
        },
        {
            "LEFT_ID": "advcl_child",
            "REL_OP": ">",
            "RIGHT_ID": "because",
            "RIGHT_ATTRS": {"ORTH": "because", "DEP": "mark"},
        },
        {
            "LEFT_ID": "negation_particle",
            "REL_OP": "$-",
            "RIGHT_ID": "aux_sibling",
            "RIGHT_ATTRS": {"DEP": "aux", "TAG": "TO"},
        },
    ],

    # not <neg <xcomp VERB >advcl >mark because
    # to  <aux
    # family members often would ask doctors not to tell the patient that they actually had cancer because
    # Pos
    # I think a lot of people who are very qualified right now to run for Congress and serve in Congress decide not to do it because they understand the seniority system.
    # Neg
    # We tend not to hear from the people who dropped out of the groups because it wasn't the right kind of treatment for them.
    # I remember when I was a young nurse working in a hospital that family members often would ask doctors not to tell the patient that they actually had cancer because, you know, they didn't want to talk about it; or they felt that the patient would be too frightened by it and would, you know, would just give up and wouldn't be able to cope with having cancer, and, you know, that's kind of how it used to be.
    [
        {"RIGHT_ID": "anchor_verb", "RIGHT_ATTRS": {"POS": "VERB"}},
        {
            "LEFT_ID": "anchor_verb",
            "REL_OP": ">",
            "RIGHT_ID": "xcomp_child_verbAux",
            "RIGHT_ATTRS": {"DEP": "xcomp"},
        },
        {
            "LEFT_ID": "xcomp_child_verbAux",
            "REL_OP": ">",
            "RIGHT_ID": "negation_particle",
            "RIGHT_ATTRS": {"DEP": "neg"},
        },
        {
            "LEFT_ID": "xcomp_child_verbAux",
            "REL_OP": ">",
            "RIGHT_ID": "to_child",
            "RIGHT_ATTRS": {"DEP": "aux", "TAG": "TO"},
        },
        {
            "LEFT_ID": "anchor_verb",
            "REL_OP": ">",
            "RIGHT_ID": "advcl_child_verb",
            "RIGHT_ATTRS": {"DEP": "advcl"},
        },
        {
            "LEFT_ID": "advcl_child_verb",
            "REL_OP": ">",
            "RIGHT_ID": "because",
            "RIGHT_ATTRS": {"ORTH": "because", "DEP": "mark"},
        },
    ],

    # not <neg AUX >advcl >mark because
    # AUX not because
    # Pos
    # Later, Frances Strickland would say that the loss wasn't because they didn't go negative and it wasn't because of the statement about raising taxes.
    # Neg
    # It's not because you're not answering.
    # I know I always did that when I was a kid, and it's not because I was cynical and I'm looking to just figure everybody out.
    # And it's not because they are addicted to food, but because, in fact, they are constantly hungry.
    # GM's stock is down to levels it hasn't seen since the early 1990s, and it's not because journalists have been harsh.
    # Let us remember, it is not because a simple act of civility caused this tragedy, it did not.
    [
        {"RIGHT_ID": "anchor_aux", "RIGHT_ATTRS": {"POS": "AUX"}},
        {
            "LEFT_ID": "anchor_aux",
            "REL_OP": ">",
            "RIGHT_ID": "negation_particle",
            "RIGHT_ATTRS": {"DEP": "neg"},
        },
        {
            "LEFT_ID": "anchor_aux",
            "REL_OP": ">++",
            "RIGHT_ID": "advcl_child_aux",
            "RIGHT_ATTRS": {"DEP": "advcl"},
        },
        {
            "LEFT_ID": "advcl_child_aux",
            "REL_OP": ">--",
            "RIGHT_ID": "because",
            "RIGHT_ATTRS": {"ORTH": "because", "DEP": "mark"},
        },
        {
            "LEFT_ID": "negation_particle",
            "REL_OP": ".",
            "RIGHT_ID": "because2",
            "RIGHT_ATTRS": {"ORTH": "because"},
        },
    ],

    # because <mark anchor_verbAux >advcl >mark because
    #         <neg
    # Added to remove not-because, because; but was causing false negatives

]

# Debug
test_patterns = []
