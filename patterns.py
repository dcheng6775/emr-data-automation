PATTERNS = {
 
    "Name": (
        r"(?:Name|Patient)\s*:\s*['\"\s]*"
        r"([A-Za-z][A-Za-z'\-\.]+(?:,\s*[A-Za-z][A-Za-z'\-\.\s]+?)?)"
        r"(?=\s*(?:\(|\d|Date:|DOB:|Age:|Sonographer:|\n))"
    ),
 
    "Age": (
        r"(?:(?:Age\s*:\s*)(\d{1,3})|(\d{1,3})\s+years?\b)"
    ),
 
    "Sex": (
        r"(?:Sex\s*[:.]\s*|\()([MF])\b"
    ),
 
    "Wt": (
        r"Wt\s*:\s*(\d{1,4}(?:\.\d{1,2})?)(?:[^\d]|$)"
    ),
 
    "Ht": (
        r"Ht\s*:\s*(\d{1,3}(?:\.\d{1,2})?)(?:[^\d]|$)"
    ),
 
    "AFib_Type": (
        r"(?i)\b(paroxysmal|persistent|long[-\s]?standing\s+persistent)\b"
        r"(?:\s+(?:atrial\s+fibrillation|AF\b|a-?fib|afib))"
    ),
 
    "Ablation_Type": (
        r"(?i)\b("
        r"pulmonary\s+vein\s+isolation|PVI|"
        r"cavo[-\s]?tricuspid\s+isthmus(?:\s+ablation)?|CTI|"
        r"radiofrequency\s+ablation|RF\s+ablation|"
        r"cryo(?:thermal)?\s+ablation|"
        r"catheter\s+ablation|"
        r"hybrid\s+ablation|surgical\s+ablation"
        r")\b"
    ),
 
    "LVEF (Lower Range)": (
        r"(?i)"
        r"(?:"
        r"(?:LVEF|Est\.?\s*EF|EF[-\s]?(?:A4C\s+View|A2C\s+View|Biplane|Simpsons?)?)"
        r"\s*:?\s*(\d{1,3})(?:\.\d+)?"
        r"|"
        r"(?:ejection\s+fraction)\s+(?:[^.\n]{0,60}?)\b(\d{1,3})(?:\.\d+)?"
        r")"
    ),
}
