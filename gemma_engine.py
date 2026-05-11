import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma4:31b-cloud"


def detect_student_level(prompt: str) -> str:
    prompt_lower = prompt.lower()

    if "college student" in prompt_lower:
        return "College Student"
    if "ssc aspirant" in prompt_lower or "ssc" in prompt_lower:
        return "SSC Aspirant"
    if "school student" in prompt_lower:
        return "School Student"
    return "Beginner"


def level_style(level: str) -> str:
    if level == "Beginner":
        return """
**Level: Beginner**  
Main explanation simple words me dunga, short points aur easy examples ke saath.
"""

    if level == "School Student":
        return """
**Level: School Student**  
Main answer school-level language me dunga, clear definitions, examples aur easy points ke saath.
"""

    if level == "SSC Aspirant":
        return """
**Level: SSC Aspirant**  
Main answer exam-oriented dunga: facts, keywords, PYQ-style points, memory tricks aur SSC tip ke saath.
"""

    if level == "College Student":
        return """
**Level: College Student**  
Main answer thoda deeper analytical way me dunga: background, concept, comparison, causes/effects aur structured explanation ke saath.
"""

    return ""


def fallback_response(prompt: str) -> str:
    """
    Streamlit Cloud par local Ollama access nahi hota.
    Isliye agar Gemma/Ollama fail ho, to level-aware fallback answer return hoga.
    """
    prompt_lower = prompt.lower()
    level = detect_student_level(prompt)
    style = level_style(level)

    # -----------------------------
    # Quiz fallback
    # -----------------------------
    if (
        "generate quiz" in prompt_lower
        or "quiz" in prompt_lower
        or "mcq" in prompt_lower
        or "multiple choice" in prompt_lower
    ):
        if level == "Beginner":
            difficulty_note = "Questions simple aur direct facts par based hain."
        elif level == "School Student":
            difficulty_note = "Questions school exam level ke according hain."
        elif level == "SSC Aspirant":
            difficulty_note = "Questions SSC CGL/CHSL/MTS pattern ke high-yield facts par based hain."
        else:
            difficulty_note = "Questions concept + factual understanding dono test karte hain."

        return f"""
## 📝 Demo Quiz Generated ✅

{style}

**Difficulty Note:** {difficulty_note}

### Topic: Indus Valley Civilization

**Q1. Indus Valley Civilization ko aur kis naam se jaana jaata hai?**  
A) Vedic Civilization  
B) Harappan Civilization  
C) Mauryan Civilization  
D) Gupta Civilization  

**Correct Answer:** B) Harappan Civilization  
**Explanation:** Harappa site sabse pehle discover hui thi, isliye ise Harappan Civilization bhi kehte hain.

---

**Q2. Great Bath kis site se mila tha?**  
A) Harappa  
B) Lothal  
C) Mohenjo-daro  
D) Kalibangan  

**Correct Answer:** C) Mohenjo-daro  
**Explanation:** Great Bath Mohenjo-daro ka famous public bathing structure tha.

---

**Q3. Lothal kis cheez ke liye famous hai?**  
A) Dockyard  
B) Iron tools  
C) Ashoka pillar  
D) Rock edicts  

**Correct Answer:** A) Dockyard  
**Explanation:** Lothal Gujarat me ek important port city thi.

---

**Q4. IVC ke log kis metal se anjaan the?**  
A) Copper  
B) Bronze  
C) Gold  
D) Iron  

**Correct Answer:** D) Iron  
**Explanation:** IVC Bronze Age civilization thi. Iron ka use later period me common hua.

---

**Q5. IVC ki sabse important feature kya thi?**  
A) Town planning  
B) Iron weapons  
C) Temples  
D) Horse riding  

**Correct Answer:** A) Town planning  
**Explanation:** Grid pattern cities aur drainage system IVC ki major features thi.

> Note: This is a hosted demo fallback. Full Gemma response works when Ollama/Gemma is available locally.
"""

    # -----------------------------
    # Answer check fallback
    # -----------------------------
    if (
        "check my answer" in prompt_lower
        or "evaluate" in prompt_lower
        or "student answer" in prompt_lower
        or "score" in prompt_lower
        or "improved answer" in prompt_lower
    ):
        if level == "Beginner":
            score_note = "Beginner level ke hisaab se basic keywords sahi hain, bas explanation badhani hai."
        elif level == "SSC Aspirant":
            score_note = "SSC exam ke liye keywords ke saath factual depth aur examples zaroori hain."
        elif level == "College Student":
            score_note = "College level ke liye analytical depth, context aur structured explanation chahiye."
        else:
            score_note = "School level ke liye answer understandable hai, lekin points clear karne honge."

        return f"""
## ✅ Answer Evaluation

{style}

**Score: 4/10**

**Reason:** {score_note}

### Correct Points ✅
- Planned cities
- Drainage system
- Trade and seals

### Missing Points ❌
- Citadel and Lower Town
- Great Bath
- Granaries
- Agriculture
- Social structure

### Improved Answer ✍️

Harappan Civilization advanced town planning ke liye famous thi. Cities grid pattern par bani thi aur generally Citadel aur Lower Town me divided thi. Inka drainage system bahut advanced tha, covered drains aur baked bricks ka use hota tha. Mohenjo-daro me Great Bath mila hai, jo hygiene ya ritual bathing ko show karta hai. Granaries food storage ke liye use hote the. Harappan people agriculture, trade aur seals ka use bhi karte the.

### Final Tip 💡
Answer likhte waqt keywords ke saath short explanation zaroor add karo.

> Note: This is a hosted demo fallback. Full Gemma response works when Ollama/Gemma is available locally.
"""

    # -----------------------------
    # Study plan fallback
    # -----------------------------
    if (
        "make study plan" in prompt_lower
        or "study plan" in prompt_lower
        or "personalized study plan" in prompt_lower
        or "day-wise study plan" in prompt_lower
        or "daily study roadmap" in prompt_lower
    ):
        if level == "Beginner":
            plan_focus = "Basic concepts, simple revision aur daily habit building."
        elif level == "School Student":
            plan_focus = "Chapter-wise learning, notes, school exam practice."
        elif level == "SSC Aspirant":
            plan_focus = "PYQ, static GK, current affairs, mock tests aur mistake notebook."
        else:
            plan_focus = "Conceptual depth, research-oriented notes, analytical writing and revision."

        return f"""
## 📅 30-Day Study Plan ✅

{style}

**Plan Focus:** {plan_focus}

### Phase 1: Core Topics

**Day 1–5: Indian Polity**  
Focus: Constitution, Fundamental Rights, Parliament, President, Important Articles.

**Day 6–10: History**  
Focus: Ancient India, Medieval India, Modern India, Freedom Movement.

**Day 11–15: Geography**  
Focus: Rivers, mountains, climate, soil, map practice.

---

### Phase 2: Score Boosters

**Day 16–20: General Science**  
Focus: Biology, Physics, Chemistry basics.

**Day 21–24: Economics**  
Focus: GDP, inflation, banking, RBI, budget.

**Day 25–27: Static GK**  
Focus: Books, awards, sports, important days, dances, festivals.

---

### Phase 3: Revision

**Day 28:** Full revision  
**Day 29:** Mock test + mistake notebook  
**Day 30:** Final light revision

### Daily Routine
- 2 hours concept study
- 1 hour MCQs
- 30 minutes revision

### Final Tip
PYQ + mistake notebook follow karo. Exam pattern samajhna bahut important hai.

> Note: This is a hosted demo fallback. Full Gemma response works when Ollama/Gemma is available locally.
"""

    # -----------------------------
    # Ask Doubt fallback: Buddhism vs Jainism
    # -----------------------------
    if "buddhism" in prompt_lower and "jainism" in prompt_lower:
        if level == "Beginner":
            extra = """
### Easy Summary
Buddhism ka path balanced hai, Jainism ka path zyada strict hai.
"""
        elif level == "School Student":
            extra = """
### School-Level Summary
Dono religions ne Vedic rituals ka विरोध किया, lekin Buddhism ne Middle Path aur Jainism ne strict Ahimsa par zyada focus kiya.
"""
        elif level == "SSC Aspirant":
            extra = """
### SSC High-Yield Points
- Buddhism = Gautam Buddha, Middle Path, Nirvana  
- Jainism = Mahavira, strict Ahimsa, Moksha  
- Buddhism India ke bahar bhi spread hua  
- Jainism mostly India me strong raha  
"""
        else:
            extra = """
### College-Level Analysis
Buddhism and Jainism emerged as Shramana movements in response to ritualism and social rigidity of the later Vedic period. Both questioned sacrifice-based religion and emphasized ethical conduct, but Buddhism adopted a more moderate psychological path, while Jainism emphasized metaphysical pluralism and extreme ascetic discipline.
"""

        return f"""
## Buddhism aur Jainism me Difference ✅

{style}

Buddhism aur Jainism dono 6th century BCE ke around India me develop hue. Dono ne Vedic rituals aur animal sacrifice ka विरोध किया, lekin inke principles me kuch important differences hain.

### Important Differences

| Point | Buddhism | Jainism |
|---|---|---|
| Founder | Gautam Buddha | Mahavira ko 24th Tirthankara maana jata hai |
| Path | Middle Path | Extreme Tapasya |
| Soul | Permanent soul ko accept nahi karta | Har living being me soul maanta hai |
| Ahimsa | Ahimsa important hai | Ahimsa bahut strict hai |
| Goal | Nirvana | Moksha |
| Spread | India ke bahar bhi spread hua | Mostly India me strong raha |

{extra}

### Memory Trick 💡
**Buddhism = Balance / Middle Path**  
**Jainism = Strict Ahimsa / Tapasya**

### Exam Tip
Founder, path, ahimsa, soul aur moksha/nirvana wale differences yaad rakho.

> Note: This is a hosted demo fallback. Full Gemma response works when Ollama/Gemma is available locally.
"""

    # -----------------------------
    # Ask Doubt fallback: Indus / Harappan
    # -----------------------------
    if "indus" in prompt_lower or "harappan" in prompt_lower or "ivc" in prompt_lower:
        if level == "Beginner":
            extra = """
### Easy Meaning
IVC ek purani civilization thi jahan log planned cities me rehte the.
"""
        elif level == "School Student":
            extra = """
### School-Level Explanation
Harappan cities planned thi, drainage system advanced tha, aur trade ke liye seals ka use hota tha.
"""
        elif level == "SSC Aspirant":
            extra = """
### SSC High-Yield Facts
- Harappa: first discovered site  
- Mohenjo-daro: Great Bath  
- Lothal: Dockyard  
- Kalibangan: Fire altars  
- Iron: not known to Harappans  
"""
        else:
            extra = """
### College-Level Analysis
The Indus Valley Civilization represents an advanced urban phase of the Bronze Age in South Asia. Its planned cities, standardized bricks, drainage networks, craft specialization and trade links indicate a complex socio-economic organization.
"""

        return f"""
## Indus Valley Civilization ✅

{style}

Indus Valley Civilization, jise Harappan Civilization bhi kehte hain, duniya ki earliest urban civilizations me se ek thi. Ye mainly town planning, drainage system, trade, seals, granaries aur Great Bath ke liye famous thi.

### Key Points
- Cities grid pattern par planned thi.
- Drainage system advanced aur covered tha.
- Great Bath Mohenjo-daro se mila.
- Lothal ek important dockyard/port city thi.
- Harappan people copper aur bronze use karte the, lekin iron se aware nahi the.
- Seals trade aur identification ke liye use hoti thi.

{extra}

### Exam Tip
Remember:  
**Harappa = first discovered site**  
**Mohenjo-daro = Great Bath**  
**Lothal = Dockyard**

> Note: This is a hosted demo fallback. Full Gemma response works when Ollama/Gemma is available locally.
"""

    # -----------------------------
    # General Ask Doubt fallback
    # -----------------------------
    return f"""
## Simple Explanation ✅

{style}

Yeh topic important hai. Isko exam point of view se short points me samajhna best rahega.

### Key Points
- Topic ka basic meaning samjho.
- Important facts ya keywords note karo.
- 3–5 bullet points me answer likho.
- Example ya memory trick add karo.
- Last me exam tip revise karo.

### Final Tip
Apne level ke hisaab se answer me depth add karo. Beginner ke liye simple, SSC ke liye facts, aur College level ke liye analysis important hota hai.

> Note: This is a hosted demo fallback. Full Gemma response works when Ollama/Gemma is available locally.
"""


def ask_gemma(prompt: str) -> str:
    try:
        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
        }

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=120,
        )

        response.raise_for_status()
        data = response.json()

        answer = data.get("response", "").strip()

        if not answer:
            return fallback_response(prompt)

        return answer

    except Exception:
        return fallback_response(prompt)
