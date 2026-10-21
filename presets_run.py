"""
JDIS 20 showcase presets — run each through the live calibrated model and write
a presentation-ready txt document.

All presets use in-distribution values from the 19-column OHE vocabulary so
that each produces a *differentiated, real* risk score rather than the OOD
all-zeros plateau. Coverage spans case types, all 4 districts, many courts,
judge positions, gender mix, bailability, and historical-throughput values
chosen so the 20 presets land in every risk band:

  Low       -> cri.bail appln. (throughput insensitive -> 0)
  Moderate  -> juvenile (throughput-insensitive -> 45-47)
  High      -> s.c.c., challan, m.c., civil suits, etc. (57-75)
  Very High -> r.c.a. + high court backlog (81+)
"""
import warnings; warnings.filterwarnings("ignore")
import json, os

import numpy as np
import pandas as pd

from backend.app.ml.manager import model_manager
from backend.app.services.risk_service import RiskService
from backend.app.services.explanation_service import ExplanationService
from backend.app.services.prediction_service import FEATURE_COLUMNS_CONFIG_D

model_manager.load_models()

# ---------------------------------------------------------------------------
# Presets. Each is a full 29-field dict (in-distribution OHE vocabulary).
# type_name values must be valid NCDG codes from col0 (283 codes);
# case_type_str from col1 (179 values); court_str from col15 (41 names);
# judge_position from col17; judge_gender from col18.
# ---------------------------------------------------------------------------

def _case(typename, casetype, category, criminal, actid, bailable, ipc, acts):
    return dict(type_name=typename, case_type_str=casetype,
                case_category=category, is_criminal_code=criminal,
                primary_act_id=actid, bailable_ipc_flag=bailable,
                ipc_section_count=ipc, statutory_act_count=acts)

# Judge / court / district combos (all real OHE values)
JUDGE = {
    "jm":   ("1004.0", "judicial_magistrate", "0 nonfemale"),
    "cjm":  ("103.0",  "chief_judicial_magistrate", "0 nonfemale"),
    "cjs":  ("1014.0", "civil_judge_senior", "0 nonfemale"),
    "cjj":  ("1015.0", "civil_judge_junior", "0 nonfemale"),
    "das":  ("1056.0", "addl_district_sessions", "0 nonfemale"),
    "ds":   ("1101.0", "district_and_sessions", "0 nonfemale"),
    "cct":  ("1057.0", "civil_court", "0 nonfemale"),
    "oth":  ("1113.0", "other", "0 nonfemale"),
}

def P(label, state_code, dist_code, court_no, court_str, district_str,
      jkey, gender="0 nonfemale", tenure=365,
      delay_rate=0.10, avg_dur=300, backlog=5000, ctype_rate=0.10,
      fd="MALE", fp="MALE", adv_def="0", adv_pet="0",
      month=6, dow=2, q=2, **case):
    jid, jpos, _ = JUDGE[jkey]
    case = _case(**case)
    return {
        "label": label,
        "state_code": state_code, "dist_code": dist_code, "court_no": court_no,
        "filing_month": month, "filing_day_of_week": dow, "filing_quarter": q,
        **case,
        "female_defendant_clean": fd, "female_petitioner_clean": fp,
        "female_adv_def_clean": adv_def, "female_adv_pet_clean": adv_pet,
        "state_str": "Maharashtra", "district_str": district_str,
        "court_str": court_str,
        "ddl_filing_judge_id": jid, "judge_position_clean": jpos,
        "judge_gender": gender, "judge_tenure_days": tenure,
        "court_prior_delay_rate": delay_rate, "court_prior_avg_duration": avg_dur,
        "court_prior_active_backlog": backlog, "casetype_prior_delay_rate": ctype_rate,
    }

# Court / district names (real col15 / col14 values)
COURT_JALGAON   = "DISTRICT AND SESSIONS COURT JALGAON"
COURT_BHUSAWAL  = "CIVIL CUM CRIMINAL COURT BHUSAWAL"
COURT_DHULE     = "DISTRICT AND SESSIONS COURT, DHULE"
COURT_NANDUR    = "DISTRICT AND SESSIONS COURT, NANDURBAR"
COURT_AMALNER   = "DISTRICT COURT 1 AND ADDL. SESSIONS COURT, AMALNER"
COURT_CHALISGAON= "CIVIL COURT SENIOR DIVISION CHALISGAON"

# Target band labels for the presentation
TARGET = {
    1:  "Low", 2: "Low", 3: "Moderate", 4: "Moderate", 5: "High",
    6:  "High", 7: "High", 8: "High", 9: "High", 10: "Very High",
    11: "High", 12: "Moderate", 13: "High", 14: "High", 15: "High",
    16: "Moderate", 17: "High", 18: "High", 19: "Very High", 20: "High",
}

PRESETS = [
    # --- LOW band ---------------------------------------------------------
    # cri.bail appln. is the only case type that pins to 0 across all
    # throughputs and judge positions — throughput-insensitive.
    P(1, "1","1","2", COURT_BHUSAWAL, "Jalgaon", "jm",
      delay_rate=0.05, avg_dur=200, backlog=1500, ctype_rate=0.05,
      typename="5698", casetype="cri.bail appln.",
      category="High-Confidence Criminal",
      criminal=1, actid="17353.0", bailable="1", ipc=1, acts=1),

    P(2, "1","1","3", COURT_CHALISGAON, "Jalgaon", "cjm",
      delay_rate=0.04, avg_dur=180, backlog=1200, ctype_rate=0.04,
      typename="5698", casetype="cri.bail appln.",
      category="High-Confidence Criminal",
      criminal=1, actid="17353.0", bailable="1", ipc=1, acts=1),

    # --- MODERATE band ----------------------------------------------------
    # juvenile is throughput-insensitive and lands at 45-47 (Moderate).
    P(3, "1","1","4", COURT_BHUSAWAL, "Jalgaon", "jm",
      delay_rate=0.05, avg_dur=200, backlog=1500, ctype_rate=0.05,
      typename="1435", casetype="juvenile",
      category="High-Confidence Criminal",
      criminal=1, actid="4759.0", bailable="1", ipc=1, acts=1,
      fp="FEMALE"),

    P(4, "1","1","5", COURT_CHALISGAON, "Jalgaon", "cjj",
      delay_rate=0.05, avg_dur=200, backlog=1500, ctype_rate=0.05,
      typename="1435", casetype="juvenile",
      category="High-Confidence Criminal",
      criminal=1, actid="4759.0", bailable="1", ipc=1, acts=1,
      fp="FEMALE"),

    # --- HIGH band: varied criminal / civil ------------------------------
    P(5, "1","3","1", COURT_JALGAON, "Jalgaon", "jm",
      delay_rate=0.24, avg_dur=560, backlog=9800, ctype_rate=0.22,
      typename="5039", casetype="s.c.c.",
      category="High-Confidence Criminal",
      criminal=1, actid="missing", bailable="-1", ipc=0, acts=0),

    P(6, "1","1","1", COURT_BHUSAWAL, "Jalgaon", "cjm",
      delay_rate=0.05, avg_dur=210, backlog=2600, ctype_rate=0.05,
      typename="5039", casetype="challan (warrant trial)",
      category="High-Confidence Criminal",
      criminal=1, actid="4759.0", bailable="-1", ipc=2, acts=1),

    P(7, "1","3","2", COURT_JALGAON, "Jalgaon", "cjj",
      delay_rate=0.05, avg_dur=210, backlog=2600, ctype_rate=0.05,
      typename="1212", casetype="m.c.",
      category="High-Confidence Criminal",
      criminal=1, actid="4759.0", bailable="0", ipc=3, acts=2),

    P(8, "1","4","1", COURT_NANDUR, "Nandurbar", "das",
      delay_rate=0.22, avg_dur=500, backlog=7200, ctype_rate=0.20,
      typename="1857", casetype="ndps. s. case",
      category="High-Confidence Criminal",
      criminal=1, actid="17353.0", bailable="0", ipc=1, acts=3),

    P(9, "1","3","1", COURT_JALGAON, "Jalgaon", "cjs",
      delay_rate=0.15, avg_dur=480, backlog=5400, ctype_rate=0.14,
      typename="5039", casetype="civil suit",
      category="High-Confidence Civil",
      criminal=0, actid="missing", bailable="-1", ipc=0, acts=1),

    # --- VERY HIGH band ---------------------------------------------------
    # r.c.a. at high court backlog is the only reliably Very High combo.
    P(10, "1","1","5", COURT_AMALNER, "Jalgaon", "ds",
      delay_rate=0.28, avg_dur=640, backlog=11000, ctype_rate=0.26,
      typename="5438", casetype="r.c.a.",
      category="Other/Unknown/Unclassified",
      criminal=1, actid="missing", bailable="-1", ipc=0, acts=0),

    # --- CIVIL (High / Moderate) ------------------------------------------
    P(11, "1","1","1", COURT_BHUSAWAL, "Jalgaon", "cjj",
      delay_rate=0.04, avg_dur=180, backlog=1100, ctype_rate=0.04,
      typename="5039", casetype="money suit",
      category="High-Confidence Civil",
      criminal=0, actid="missing", bailable="-1", ipc=0, acts=1),

    P(12, "1","4","1", COURT_NANDUR, "Nandurbar", "cjs",
      delay_rate=0.28, avg_dur=610, backlog=10200, ctype_rate=0.26,
      typename="5039", casetype="declarative suits",
      category="High-Confidence Civil",
      criminal=0, actid="missing", bailable="-1", ipc=0, acts=2),

    P(13, "1","3","2", COURT_JALGAON, "Jalgaon", "cct",
      delay_rate=0.06, avg_dur=240, backlog=3000, ctype_rate=0.06,
      typename="5039", casetype="maintenance",
      category="High-Confidence Civil",
      criminal=0, actid="missing", bailable="-1", ipc=0, acts=1,
      fp="FEMALE"),

    P(14, "1","2","1", COURT_DHULE, "Dhule", "cjs",
      delay_rate=0.11, avg_dur=360, backlog=4200, ctype_rate=0.10,
      typename="5039", casetype="hindu marriage act",
      category="High-Confidence Civil",
      criminal=0, actid="missing", bailable="-1", ipc=0, acts=1,
      fd="FEMALE", fp="FEMALE"),

    P(15, "1","1","4", COURT_BHUSAWAL, "Jalgaon", "cjj",
      delay_rate=0.02, avg_dur=130, backlog=800, ctype_rate=0.02,
      typename="5039", casetype="probate",
      category="High-Confidence Civil",
      criminal=0, actid="missing", bailable="-1", ipc=0, acts=1),

    P(16, "1","2","3", COURT_DHULE, "Dhule", "cjj",
      delay_rate=0.05, avg_dur=200, backlog=1500, ctype_rate=0.05,
      typename="5039", casetype="succession case",
      category="High-Confidence Civil",
      criminal=0, actid="missing", bailable="-1", ipc=0, acts=1,
      adv_def="1", adv_pet="1"),

    # --- MIXED / AMBIGUOUS -----------------------------------------------
    P(17, "1","4","1", COURT_NANDUR, "Nandurbar", "oth",
      delay_rate=0.20, avg_dur=470, backlog=6500, ctype_rate=0.19,
      typename="1864", casetype="pcso",
      category="Ambiguous/Mixed",
      criminal=1, actid="missing", bailable="-1", ipc=0, acts=1),

    P(18, "1","3","6", COURT_JALGAON, "Jalgaon", "oth",
      delay_rate=0.07, avg_dur=250, backlog=2900, ctype_rate=0.07,
      typename="1845", casetype="msex",
      category="Ambiguous/Mixed",
      criminal=0, actid="missing", bailable="-1", ipc=0, acts=1,
      fp="FEMALE"),

    P(19, "1","1","5", COURT_AMALNER, "Jalgaon", "ds",
      delay_rate=0.28, avg_dur=640, backlog=11000, ctype_rate=0.26,
      typename="5438", casetype="r.c.a.",
      category="Other/Unknown/Unclassified",
      criminal=1, actid="missing", bailable="-1", ipc=0, acts=0),

    P(20, "1","2","3", COURT_DHULE, "Dhule", "oth",
      delay_rate=0.13, avg_dur=340, backlog=4100, ctype_rate=0.12,
      typename="1842", casetype="complaint",
      category="Other/Unknown/Unclassified",
      criminal=1, actid="missing", bailable="-1", ipc=1, acts=1),
]


# ---------------------------------------------------------------------------
def run():
    results = []
    for p in PRESETS:
        row = {col: [p.get(col)] for col in FEATURE_COLUMNS_CONFIG_D}
        df = pd.DataFrame(row)
        prob = float(model_manager.classifier.predict_proba(df)[:, 1][0])
        prob = max(0.0, min(1.0, prob))
        risk = RiskService.calculate_risk_score(prob)
        band = RiskService.assign_risk_band(risk)
        try:
            top = ExplanationService.explain_instance(df, top_n=4)
            drivers = [(i.feature_name, i.contribution, i.direction) for i in top]
        except Exception:
            drivers = []
        results.append({
            "idx": p["label"], "label": p,
            "calibrated_probability": round(prob, 4),
            "risk_score": risk, "risk_band": band,
            "target_band": TARGET.get(p["label"], ""),
            "drivers": drivers,
        })
    return results


if __name__ == "__main__":
    res = run()
    out = os.path.join(os.getcwd(), "preset_results.json")
    with open(out, "w") as f:
        json.dump(res, f, indent=2)
    print(f"Ran {len(res)} presets -> {out}")
    for r in res:
        tgt = r.get("target_band","")
        print(f"  #{r['idx']:>2} {r['risk_score']:>3} {r['risk_band']:<10} "
              f"(calib {r['calibrated_probability']:.3f}) target={tgt}")
