# JDIS NLP Feasibility Assessment

**Project**: Judicial Delay Intelligence System (JDIS)  
**Role**: Tanmay — Data Engineer & Data Architect  
**Date**: August 2026  
**Document Classification**: Text & Natural Language Processing Feasibility  
**Feasibility Verdict**: **PARTIALLY FEASIBLE (TF-IDF on Legal Metadata Supported; BERT Infeasible without External Judgments)**

---

## 1. Objective

The JDIS research foundation proposes natural language processing (NLP) to extract semantic representations from case information to aid in judicial delay prediction and explainability.

This investigation audits all textual fields across the DDL e-Courts dataset to determine:
1. What textual data exists and where it is stored.
2. Whether text maps directly and reliably to individual case records (`ddl_case_id`).
3. Vocabulary distributions, token lengths, and language encodings.
4. Feasibility of **TF-IDF Vectorization** vs. **Transformer/BERT Embeddings**.

---

## 2. Textual Data Inventory

The raw DDL dataset is primarily structured tabular data. Text is distributed across normalized lookup tables linked via integer keys:

| Table | Column | Description | Unique Strings | Total Corpus Occurrences | Vocabulary Characteristics |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `act_key.csv` | `act_s` | Full statutory title of legal Act | 29,857 | 76,765,611 | Formal legal act titles (e.g., *"The Indian Penal Code"*, *"Negotiable Instruments Act, 1881"*, *"Code of Civil Procedure"*) |
| `section_key.csv` | `section_s` | Section citation string | 2,113,919 | >70,000,000 | Alphanumeric section numbers and statutory sub-clauses (e.g., *"302"*, *"138"*, *"420"*, *"498A"*, *"376(2)(f)"*) |
| `type_name_key.csv` | `type_name_s` | Case type category designation | 62,714 | 80,935,944 | Case type labels and procedural abbreviations (e.g., *"regular civil suit"*, *"criminal appeal"*, *"bail application"*, *"motor accident claim"*) |
| `purpose_name_key.csv` | `purpose_name_s` | Purpose / stage of hearing | 68,125 | 80,935,944 | Procedural hearing descriptions (e.g., *"evidence for prosecution"*, *"framing of charge"*, *"final arguments"*, *"summons"*) |
| `disp_name_key.csv` | `disp_name_s` | Case disposition / outcome | 462 | 80,935,944 | Outcome descriptions (e.g., *"acquitted"*, *"dismissed for default"*, *"allowed"*, *"compromised in lok adalat"*) — *Note: Prohibited at filing!* |

---

## 3. Absence of Unstructured Case Judgment Narrative Text

- **Finding**: The raw DDL e-Courts release does **NOT** contain full judgment texts, FIR narratives, plaint/written statement paragraphs, or hearing transcripts.
- **Scientific Constraint**: Attaching random external legal judgments from unrelated High Court/Supreme Court datasets (such as Indian Kanoon or Supreme Court transcripts) to lower-court DDL cases would constitute severe synthetic contamination and invalidate the research findings.

---

## 4. Evaluation of NLP Modeling Paradigms

### 4.1 Approach A: TF-IDF on Concatenated Legal Metadata Tokens
- **Methodology**: Construct a structured text document per case at filing time:
  $$\text{case\_legal\_text} = \text{Concat}(\text{state\_name}, \text{district\_name}, \text{court\_name}, \text{case\_type\_string}, \text{act\_titles}, \text{section\_tokens})$$
  *Example*: `"Maharashtra Nandurbar Chief Judicial Magistrate cc criminal case Indian Penal Code sec 302 34 120b"`
- **Vocabulary Size**: 10,000 to 25,000 top n-grams (unigrams + bigrams).
- **Feasibility**: **FULLY FEASIBLE & COMPUTATIONALLY EFFICIENT**.
- **Leakage Safeguard**: TF-IDF vectorizer must be fit **strictly on the training split** and transformed on validation/test splits.

### 4.2 Approach B: Deep Transformer / BERT Embeddings (e.g. InLegalBERT)
- **Methodology**: Running pretrained `law-ai/InLegalBERT` on full case judgment text.
- **Feasibility**: **NOT FEASIBLE FOR CASE-LEVEL PREDICTION** because full narrative judgment documents are absent from the DDL tabular corpus.
- **Defensible Alternative**: If Gaurav wishes to benchmark sentence-transformer embeddings, they can be generated on the concatenated filing metadata strings (`case_legal_text`) and compared directly against TF-IDF as an ablation experiment.

---

## 5. Formal Recommendations for Gaurav (AI Lead)

1. **Mandatory Baseline**: Implement `TfidfVectorizer(max_features=5000, ngram_range=(1,2), sublinear_tf=True)` on the composite filing text token.
2. **Experimental Structure**:
   - Model A: Structured Tabular Features Only (LightGBM / XGBoost).
   - Model B: TF-IDF Text Features Only (Logistic Regression / Linear Ridge).
   - Model C (Fusion): Structured Features + Top 100 SVD-reduced TF-IDF Components.
3. **Research Paper Reporting**: Report the incremental MAE / F1-score gain from incorporating structured legal text representations.
