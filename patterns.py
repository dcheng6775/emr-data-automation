PATTERNS = {
    "Name": (
        r"Name:\s*['\"\s,]*([^,]+,\s*[^,\n]+?)(?=\s*Date:|\s*DOB:|\s*Age:|\n|\s*Sonographer:)"
    ),

    "Age": (
        r"Age:\s*(\d{1,3})\b"
    ),

    "Sex": (
        r"Sex:\s*([MF])\b"
    ),

    "Wt": (
        r"Wt:\s*(\d{1,4}(\.\d)?)\b" 
    ),

    "Ht": (
        r"Ht:\s*(\d{1,3}\.\d)\b"
    ),

    "AFib_Type": (
        r"(?i)(paroxysmal|persistent|long[-\s]?standing\s*persistent)"
        r"\s*(atrial\s*fibrillation|AF|a-fib|afib)"
    ),

    "Ablation_Type": (
        r"(?i)\b("
        r"pulmonary\s*vein\s*isolation|pvi|"
        r"cavo[-\s]?tricuspid\s*isthmus\s*ablation|cti|"
        r"radiofrequency|rf|cryo(?:thermal)?|catheter(?:\s*[-]?\s*ablation)?|"
        r"hybrid|surgical"
        r")\s*ablation\b"
    ),
}