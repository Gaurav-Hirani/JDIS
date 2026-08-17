import pandas as pd
import numpy as np

def audit_case_types_civil_criminal():
    print("==================================================")
    print("AUDITING CIVIL VS CRIMINAL CLASSIFICATION")
    print("==================================================")
    
    df_type = pd.read_csv('data/extracted/keys/type_name_key.csv')
    df_type['type_name_s_clean'] = df_type['type_name_s'].astype(str).str.lower().str.strip()
    
    # Aggregate counts by cleaned string
    type_counts = df_type.groupby('type_name_s_clean')['count'].sum().sort_values(ascending=False)
    print(f"Total distinct case type strings: {len(type_counts):,}")
    print(f"Total case volume represented in type_key: {type_counts.sum():,}")
    
    # Define keywords for criminal vs civil
    crim_keywords = [
        'cri', 'crl', 'criminal', 'st', 'sessions', 'bail', 'complaint', 
        'cr.pc', 'crpc', 'ipc', 'police', 'rct', 's.c.c.', 'scc', 'summons',
        'ndps', 'ni act', '138', 'sc/st', 'posco', 'pocso', 'remand', 'charge sheet',
        'calender', 'prosecution', 'accused'
    ]
    
    civ_keywords = [
        'civil', 'suit', 'os', 'o.s.', 'cs', 'c.s.', 'mact', 'rcs', 'r.c.s.', 
        'execution', 'ep', 'e.p.', 'cma', 'c.m.a.', 'hmop', 'h.m.o.p.', 
        'marriage', 'divorce', 'succession', 'probate', 'arbitration', 'rent', 
        'injunction', 'land', 'motor', 'consumer', 'commercial', 'original suit',
        'title suit', 'partition', 'declaration', 'money suit'
    ]
    
    def classify_type(s):
        s = str(s).lower()
        has_crim = any(kw in s for kw in crim_keywords)
        has_civ = any(kw in s for kw in civ_keywords)
        if has_crim and not has_civ:
            return 'Criminal'
        elif has_civ and not has_crim:
            return 'Civil'
        elif has_crim and has_civ:
            # Tie break based on specific leading token
            if s.startswith(('cri', 'crl', 'st', 'bail', 'cc', 'c.c.')):
                return 'Criminal'
            elif s.startswith(('civ', 'os', 'cs', 'rcs', 'mact')):
                return 'Civil'
            return 'Ambiguous/Mixed'
        else:
            return 'Other/Unclassified'

    df_type['category'] = df_type['type_name_s_clean'].apply(classify_type)
    
    cat_summary = df_type.groupby('category')['count'].sum()
    print("\nCase Type Distribution across all historical cases:")
    for cat, cnt in cat_summary.items():
        print(f"  - {cat:<20}: {cnt:>12,} ({cnt/type_counts.sum()*100:>5.1f}%)")
        
    print("\nTop 20 Classified Case Types:")
    for idx, (name, cnt) in enumerate(type_counts.head(20).items()):
        cat = classify_type(name)
        print(f"  {idx+1:>2}. {name:<35} | {cat:<12} | Count: {cnt:>10,}")

def audit_hearing_purposes():
    print("\n==================================================")
    print("AUDITING HEARING PURPOSES & ADJOURNMENT SIGNALS")
    print("==================================================")
    df_purp = pd.read_csv('data/extracted/keys/purpose_name_key.csv')
    df_purp['purpose_s_clean'] = df_purp['purpose_name_s'].astype(str).str.lower().str.strip()
    purp_counts = df_purp.groupby('purpose_s_clean')['count'].sum().sort_values(ascending=False)
    
    print(f"Total distinct purpose strings: {len(purp_counts):,}")
    print(f"Total hearing records represented: {purp_counts.sum():,}")
    
    # Check for adjournment/delay keywords
    adj_keywords = ['adjourn', 'postpone', 'call on', 'steps', 'stay', 'await', 'notice', 'summons', 'absent', 'bailable', 'warrant']
    print("\nAdjournment/Postponement-related purpose strings:")
    for kw in adj_keywords:
        matching = purp_counts[purp_counts.index.str.contains(kw, regex=False)]
        print(f"  - Keyword '{kw}': {len(matching):>4} distinct strings, Total Count: {matching.sum():>10,}")
        for name, cnt in matching.head(3).items():
            print(f"      * {name}: {cnt:,}")

def audit_acts_and_sections():
    print("\n==================================================")
    print("AUDITING ACTS & SECTIONS KEY COVERAGE")
    print("==================================================")
    df_act = pd.read_csv('data/extracted/keys/act_key.csv')
    print(f"Total distinct Acts in act_key: {len(df_act):,}")
    print(f"Total Act citations: {df_act['count'].sum():,}")
    top_acts = df_act.sort_values(by='count', ascending=False).head(15)
    print("Top 15 Acts by citation volume:")
    for _, row in top_acts.iterrows():
        print(f"  - Act #{row['act']}: {str(row['act_s']):<45} | Citations: {row['count']:,}")

if __name__ == '__main__':
    audit_case_types_civil_criminal()
    audit_hearing_purposes()
    audit_acts_and_sections()
