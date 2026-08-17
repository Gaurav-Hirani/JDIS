"""
JDIS Civil vs Criminal Classification Module
Implements deterministic, rule-based 4-category classification:
1. High-Confidence Criminal
2. High-Confidence Civil
3. Ambiguous/Mixed
4. Other/Unknown/Unclassified
"""

import pandas as pd
import numpy as np

# Specific exact-match tokens for case types
CRIMINAL_EXACT_TYPES = {
    'cc', 'c.c.', 'c. c.', 'calendar case', 'calender case', 'r.c.c.', 'rcc',
    'regular criminal case', 'ba', 'bail', 'bail application', 'sum', 'summary case',
    's.t.', 'st', 'sessions trial', 'sessions case', 'sc', 's.c.c.', 'scc',
    'summary criminal case', 'rct', 'stc', 'c.r.p.c.', 'crpc', 'ipc', 'cr. reg. case',
    'final report', 'gr case', 'p.c.r.', 'chi', 'crma j', 'crma s', 'coma', 'cr',
    'cr. misc. cases', 'crl.a.', 'criminal appeal', 'cri. appeal', 'crl.r.p.',
    'criminal revision', 'spl case', 'special case', 'nact', 'ni act', '138 ni act',
    'police challan', 'state case', 'fir', 'challan'
}

CIVIL_EXACT_TYPES = {
    'os', 'o.s.', 'original suit', 'cs', 'c.s.', 'civil suit', 'rcs', 'r.c.s.',
    'regular civil suit', 'mact', 'm.v.c.', 'mvc', 'mcop', 'macp', 'op mv', 'macc',
    'motor accident claim', 'ep', 'e.p.', 'execution petition', 'ex', 'exe',
    'cma', 'c.m.a.', 'civil misc appeal', 'hmop', 'h.m.o.p.', 'hma',
    'hindu marriage act petition', 'civil appeal', 'c.a.', 'ca', 'title suit',
    'partition suit', 'money suit', 'probate', 'succession', 'injunction',
    'arbitration', 'rent suit', 'op', 'original petition', 'mjc r', 'misc. civil',
    'declaration suit', 'land acquisition', 'lao', 'lar', 'sca', 'special civil application',
    'ea', 'execution application', 't.s.', 'title appeal', 't.a.'
}

# Substring keywords
CRIMINAL_KEYWORDS = [
    'cri', 'crl', 'criminal', 'sessions', 'bail', 'complaint', 'cr.pc', 'crpc',
    'ipc', 'police', 'ndps', 'ni act', 'sc/st', 'posco', 'pocso', 'remand',
    'prosecution', 'accused', 'gambling', 'excise', 'arms act', 'narcotic',
    'cheque bounce', 'juvenile', 'challan'
]

CIVIL_KEYWORDS = [
    'civil', 'suit', 'mact', 'execution', 'marriage', 'divorce', 'succession',
    'probate', 'arbitration', 'rent', 'injunction', 'land', 'motor', 'consumer',
    'commercial', 'title suit', 'partition', 'declaration', 'money suit',
    'hindu marriage', 'guardianship', 'insolvency', 'recovery', 'easement',
    'specific performance', 'tenancy', 'eviction'
]

# Statutory Act IDs known deterministically
KNOWN_CRIMINAL_ACTS = {
    17353,  # The Indian Penal Code
    4759,   # Code of Criminal Procedure
    7416,   # I.P.C(Police)
    6748,   # Gujarat/Bombay Prohibition Act
    11007,  # Negotiable Instruments Act (Section 138 criminal cheque bounce)
    10809,  # NEGOTIABLE INSTRUMENTS ACT, 1881
    10808,  # NEGOTIABLE INSTRUMENTS ACT
    2402,   # Arms Act
    12885,  # Narcotic Drugs and Psychotropic Substances Act (NDPS)
    13965,  # Protection of Children from Sexual Offences (POCSO)
    14845,  # Scheduled Castes and Scheduled Tribes (PoA) Act
    13324,  # Passport Act
    13885,  # Prevention of Corruption Act
}

KNOWN_CIVIL_ACTS = {
    4747,   # Code of Civil Procedure
    4650,   # Civil Procedure Code
    4069,   # CODE OF CIVIL PROCEDURE
    4074,   # CODE OF CIVIL PROCEDURE, 1908 (HB)
    10581,  # Motor Vehicles Act (MACT claims)
    9846,   # MOTOR VEHICLES ACT
    10564,  # Motor Vehicle Act
    7276,   # Hindu Marriage Act
    7282,   # Hindu Succession Act
    7273,   # Hindu Adoptions and Maintenance Act
    7279,   # Hindu Minority and Guardianship Act
    8182,   # Indian Contract Act
    15554,  # Specific Relief Act
    16744,  # Transfer of Property Act
    2400,   # Arbitration and Conciliation Act
    8334,   # Indian Succession Act
    4934,   # Consumer Protection Act
    9508,   # Land Acquisition Act
}


def classify_case_type_string(type_str: str) -> str:
    """
    Classifies a case type string into Criminal, Civil, Ambiguous, or Unknown.
    """
    if pd.isna(type_str):
        return 'Other/Unknown/Unclassified'
    
    s = str(type_str).lower().strip()
    if not s or s in {'nan', 'none', 'null', 'unknown', ''}:
        return 'Other/Unknown/Unclassified'
    
    if s in CRIMINAL_EXACT_TYPES:
        return 'Criminal'
    if s in CIVIL_EXACT_TYPES:
        return 'Civil'
    
    has_crim = any(kw in s for kw in CRIMINAL_KEYWORDS)
    has_civ = any(kw in s for kw in CIVIL_KEYWORDS)
    
    if has_crim and not has_civ:
        return 'Criminal'
    if has_civ and not has_crim:
        return 'Civil'
    if has_crim and has_civ:
        if s.startswith(('cri', 'crl', 'st', 'bail', 'cc', 'c.c.', 'sc')):
            return 'Criminal'
        elif s.startswith(('civ', 'os', 'cs', 'rcs', 'mact', 'hma', 'ep')):
            return 'Civil'
        return 'Ambiguous/Mixed'
    
    return 'Other/Unknown/Unclassified'


def classify_case_record(type_category: str, act_id: float = None, criminal_flag_acts: float = None) -> str:
    """
    Combines case type string classification with Act ID and acts_sections criminal flag
    to produce the final 4-category classification.
    """
    act_category = 'Other/Unknown/Unclassified'
    if pd.notna(act_id):
        act_int = int(act_id)
        if act_int in KNOWN_CRIMINAL_ACTS:
            act_category = 'Criminal'
        elif act_int in KNOWN_CIVIL_ACTS:
            act_category = 'Civil'
    
    if pd.notna(criminal_flag_acts) and act_category == 'Other/Unknown/Unclassified':
        if criminal_flag_acts == 1:
            act_category = 'Criminal'
        elif criminal_flag_acts == 0:
            act_category = 'Civil'

    # Combine both signals
    if type_category == 'Criminal' and act_category in ('Criminal', 'Other/Unknown/Unclassified'):
        return 'High-Confidence Criminal'
    elif type_category == 'Civil' and act_category in ('Civil', 'Other/Unknown/Unclassified'):
        return 'High-Confidence Civil'
    elif type_category == 'Other/Unknown/Unclassified' and act_category == 'Criminal':
        return 'High-Confidence Criminal'
    elif type_category == 'Other/Unknown/Unclassified' and act_category == 'Civil':
        return 'High-Confidence Civil'
    elif (type_category == 'Criminal' and act_category == 'Civil') or (type_category == 'Civil' and act_category == 'Criminal'):
        return 'Ambiguous/Mixed'
    elif type_category == 'Ambiguous/Mixed':
        return 'Ambiguous/Mixed'
    else:
        return 'Other/Unknown/Unclassified'
