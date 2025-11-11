PATTERNS = {
        "Name": r"Name:\s*([A-Za-z\s,]+?)(?:\s+Age:|$)",
    
        "Age": (
            r"(?:Age[:\s]*([\d]{1,3}))"
            r"|(\d{1,3})-year-old"
            r"|(\d{1,3})\s*years? old"
            r"|Age of\s*(\d{1,3})"
            r"|(\d{1,3}) year old"
        ),
    
        "Sex": (
            r"Sex[:\s\-]*([MmFf])"
            r"|Gender[:\s\-]*([Mm]ale|[Ff]emale)"
            r"|is a[n]?\s*([Ff]emale|[Mm]ale)"
            r"|([Ff]emale)\s+patient"
            r"|([Mm]ale)\s+patient"
            r"|([Mm]an)"
            r"|([Ww]oman)"
        ),
    
        "Wt": r"""(?:Wt[:\s\-]*|weight\s*(?:of|is|=)?\s*)
              ([\d\.]+\s*(?:kg|kgs|kilograms?|lb|lbs|pounds?)?)""",
    
        "Ht": r"""(?:Ht[:\s\-]*|height\s*(?:of|is|=)?\s*)
              ([\d\.]+\s*(?:cm|centimeters?|m|meters?|in|inch|inches)?)""",
    
        "AFib_Type": (
            r"""(paroxysmal|persistent|long[-\s]?standing\s*persistent)
                \s*(atrial\s*fibrillation|AF|a-fib|afib)"""
        ),
    
        "Ablation_Type": r"""(?i)\b(pulmonary\s*vein\s*isolation|pvi|
                        cavo[-\s]?tricuspid\s*isthmus\s*ablation|cti|
                        radiofrequency|rf|cryo(?:thermal)?|catheter(?:\s*[-]?\s*ablation)?|
                        hybrid|surgical)\s*ablation\b"""
        ,
    }