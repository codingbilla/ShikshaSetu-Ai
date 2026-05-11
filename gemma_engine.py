import re
import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma4:31b-cloud"


# --------------------------------------------------
# Basic helpers
# --------------------------------------------------
def detect_student_level(prompt: str) -> str:
    prompt_lower = prompt.lower()

    if "college student" in prompt_lower:
        return "College Student"
    if "ssc aspirant" in prompt_lower or "ssc" in prompt_lower:
        return "SSC Aspirant"
    if "school student" in prompt_lower:
        return "School Student"
    return "Beginner"


def detect_language(prompt: str) -> str:
    prompt_lower = prompt.lower()

    if "language: hindi" in prompt_lower or "hindi" in prompt_lower:
        return "Hindi"
    if "language: english" in prompt_lower or "english" in prompt_lower:
        return "English"
    return "Hinglish"


def extract_topic(prompt: str) -> str:
    """
    Prompt se topic/question nikalne ki simple कोशिश.
    Agar exact topic na mile to general topic return karega.
    """
    patterns = [
        r"topic\s*[:\-]\s*(.+)",
        r"question\s*[:\-]\s*(.+)",
        r"doubt\s*[:\-]\s*(.+)",
        r"goal\s*[:\-]\s*(.+)",
        r"student answer\s*[:\-]\s*(.+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, prompt, re.IGNORECASE)
        if match:
            topic = match.group(1).strip()
            topic = topic.split("\n")[0].strip()
            if topic:
                return topic[:120]

    lines = [line.strip() for line in prompt.splitlines() if line.strip()]
    for line in lines:
        lower = line.lower()
        if (
            "explain" not in lower
            and "generate" not in lower
            and "evaluate" not in lower
            and "language" not in lower
            and "student level" not in lower
            and len(line) > 4
        ):
            return line[:120]

    return "this topic"


def is_probably_quiz(prompt: str) -> bool:
    p = prompt.lower()
    return any(x in p for x in ["quiz", "mcq", "multiple choice", "generate questions"])


def is_probably_answer_check(prompt: str) -> bool:
    p = prompt.lower()
    return any(
        x in p
        for x in [
            "check my answer",
            "evaluate",
            "student answer",
            "score",
            "improved answer",
            "mistakes",
            "correct points",
            "missing points",
        ]
    )


def is_probably_study_plan(prompt: str) -> bool:
    p = prompt.lower()
    return any(
        x in p
        for x in [
            "make study plan",
            "study plan",
            "personalized study plan",
            "day-wise study plan",
            "daily study roadmap",
            "preparation plan",
        ]
    )


def level_intro(level: str, language: str) -> str:
    if language == "English":
        if level == "Beginner":
            return "**Level: Beginner**\nI will explain this in very simple words with easy examples."
        if level == "School Student":
            return "**Level: School Student**\nI will explain this in school-exam style with clear points."
        if level == "SSC Aspirant":
            return "**Level: SSC Aspirant**\nI will focus on exam facts, keywords, PYQ-style points and memory tricks."
        return "**Level: College Student**\nI will explain this with deeper context, analysis and structured reasoning."

    if language == "Hindi":
        if level == "Beginner":
            return "**Level: Beginner**\nमैं इसे बहुत आसान भाषा और छोटे उदाहरणों के साथ समझाऊंगा।"
        if level == "School Student":
            return "**Level: School Student**\nमैं इसे स्कूल परीक्षा के हिसाब से साफ points में समझाऊंगा।"
        if level == "SSC Aspirant":
            return "**Level: SSC Aspirant**\nमैं exam facts, keywords, PYQ-style points और memory tricks पर focus करूंगा।"
        return "**Level: College Student**\nमैं इसे deeper context, analysis और structured reasoning के साथ समझाऊंगा।"

    # Hinglish default
    if level == "Beginner":
        return "**Level: Beginner**\nMain isko simple words, short points aur easy examples ke saath samjhaunga."
    if level == "School Student":
        return "**Level: School Student**\nMain school-exam style me clear points aur examples ke saath answer dunga."
    if level == "SSC Aspirant":
        return "**Level: SSC Aspirant**\nMain exam facts, keywords, PYQ-style points aur memory tricks par focus karunga."
    return "**Level: College Student**\nMain deeper context, analysis aur structured reasoning ke saath answer dunga."


# --------------------------------------------------
# Topic-specific fallback answers
# --------------------------------------------------
def buddhism_jainism_answer(level: str, language: str) -> str:
    if level == "Beginner":
        return f"""
## Buddhism aur Jainism me Difference ✅

{level_intro(level, language)}

### Easy Explanation
Buddhism aur Jainism dono India ke purane dharm hain. Dono ne Vedic rituals aur animal sacrifice ka virodh kiya. Lekin Buddhism balanced life par focus karta hai, aur Jainism strict Ahimsa aur Tapasya par focus karta hai.

### Simple Difference

| Point | Buddhism | Jainism |
|---|---|---|
| Main teacher | Gautam Buddha | Mahavira |
| Life style | Middle Path | Strict Tapasya |
| Ahimsa | Important | Bahut strict |
| Goal | Nirvana | Moksha |
| Spread | India ke bahar bhi gaya | Mostly India me raha |

### Memory Trick 💡
**Buddhism = Balance**  
**Jainism = Strict Ahimsa**

> Hosted demo fallback. Full Gemma response works when Ollama/Gemma is available locally.
"""

    if level == "SSC Aspirant":
        return f"""
## Buddhism vs Jainism — SSC Exam Ready ✅

{level_intro(level, language)}

### High-Yield Facts

| Feature | Buddhism | Jainism |
|---|---|---|
| Founder/Main figure | Gautam Buddha | Mahavira, 24th Tirthankara |
| Path | Middle Path | Extreme Tapasya |
| Ahimsa | Important but practical | Very strict Ahimsa |
| Soul concept | Anatta, no permanent soul | Soul exists in every living being |
| Goal | Nirvana | Moksha |
| Language | Pali | Prakrit |
| Spread | India se bahar bhi spread | Mostly India tak limited |

### PYQ-Type Points
- Middle Path → Buddhism
- Strict Ahimsa → Jainism
- 24th Tirthankara → Mahavira
- No permanent soul → Buddhism
- Soul in all living beings → Jainism

### SSC Memory Trick 💡
**Buddhism = Buddha + Balance + Pali + Nirvana**  
**Jainism = Jiva + Mahavira + Prakrit + Moksha**

> Hosted demo fallback. Full Gemma response works when Ollama/Gemma is available locally.
"""

    if level == "College Student":
        return f"""
## Buddhism and Jainism: Analytical Comparison ✅

{level_intro(level, language)}

### Historical Background
Buddhism and Jainism emerged around the 6th century BCE as part of the Shramana tradition. They developed during a period of urbanization, growth of trade, questioning of ritualism, and dissatisfaction with Vedic sacrificial practices.

### Analytical Comparison

| Dimension | Buddhism | Jainism |
|---|---|---|
| Core orientation | Ethical-psychological path to end suffering | Ascetic-metaphysical path to liberate soul |
| Main figure | Siddhartha Gautama | Mahavira, 24th Tirthankara |
| Path | Middle Path | Extreme asceticism |
| Soul theory | Anatta, no permanent soul | Jiva, soul in all living beings |
| Karma | Intention and suffering | Karmic matter attached to soul |
| Liberation | Nirvana | Moksha |
| Ahimsa | Important ethical value | Absolute central principle |

### Conclusion
Both challenged ritualism, but Buddhism offered a moderate ethical path, while Jainism developed a rigorous ascetic system centered on soul purification and absolute non-violence.

> Hosted demo fallback. Full Gemma response works when Ollama/Gemma is available locally.
"""

    return f"""
## Buddhism aur Jainism me Difference ✅

{level_intro(level, language)}

### Introduction
Buddhism aur Jainism dono 6th century BCE ke around India me develop hue. Dono ne Vedic rituals, caste rigidity aur animal sacrifice ka virodh kiya.

### Main Differences

| Basis | Buddhism | Jainism |
|---|---|---|
| Founder | Gautam Buddha | Mahavira |
| Path | Middle Path | Extreme Tapasya |
| Ahimsa | Important | Highest and strictest principle |
| Soul | Permanent soul ko accept nahi karta | Har living being me soul maanta hai |
| Goal | Nirvana | Moksha |
| Spread | India ke bahar bhi spread hua | Mostly India me strong raha |

### Similarities
- Dono ne Vedic rituals ka virodh kiya.
- Dono ne morality aur self-control par focus kiya.
- Dono ne simple life ko importance di.

> Hosted demo fallback. Full Gemma response works when Ollama/Gemma is available locally.
"""


def indus_answer(level: str, language: str) -> str:
    if level == "Beginner":
        return f"""
## Indus Valley Civilization ✅

{level_intro(level, language)}

### Easy Meaning
Indus Valley Civilization ek bahut purani civilization thi. Iske log planned cities me rehte the aur drainage system bahut advanced tha.

### Simple Points
- Isko Harappan Civilization bhi kehte hain.
- Cities planned hoti thi.
- Drainage system advanced tha.
- Great Bath Mohenjo-daro me mila.
- Lothal dockyard ke liye famous hai.
- IVC people iron use nahi karte the.

### Memory Trick 💡
**Harappa = first site**  
**Mohenjo-daro = Great Bath**  
**Lothal = Dockyard**

> Hosted demo fallback. Full Gemma response works when Ollama/Gemma is available locally.
"""

    if level == "SSC Aspirant":
        return f"""
## Indus Valley Civilization — SSC High-Yield Notes ✅

{level_intro(level, language)}

### Important Facts
- **Harappa:** first discovered site, 1921, Daya Ram Sahni
- **Mohenjo-daro:** Great Bath, Great Granary
- **Lothal:** Dockyard, Gujarat
- **Kalibangan:** Fire altars, Rajasthan
- **Dholavira:** Water management, Gujarat
- **Rakhigarhi:** Major site in Haryana
- **Metal unknown:** Iron
- **Script:** Pictographic, not yet deciphered

### Features
- Grid pattern town planning
- Covered drainage system
- Baked bricks
- Trade with Mesopotamia
- Seals and weights
- Agriculture: wheat, barley, cotton

### SSC Tip
Site-location-special feature mapping zaroor yaad rakho.

> Hosted demo fallback. Full Gemma response works when Ollama/Gemma is available locally.
"""

    if level == "College Student":
        return f"""
## Indus Valley Civilization: Analytical Overview ✅

{level_intro(level, language)}

### Context
The Indus Valley Civilization represents an advanced Bronze Age urban culture in South Asia. Its cities show planning, standardization and complex socio-economic organization.

### Key Analytical Features
- **Urban planning:** grid layout, citadel and lower town
- **Drainage:** covered drains indicate civic planning
- **Economy:** agriculture, craft production and long-distance trade
- **Technology:** bronze tools, standardized weights and seals
- **Administration:** standardization suggests organized governance
- **Religion/Culture:** figurines, seals and Great Bath indicate ritual practices

### Significance
IVC is important because it shows early urbanization without clear evidence of large palaces or monumental temples, suggesting a distinctive urban model compared to Egypt or Mesopotamia.

> Hosted demo fallback. Full Gemma response works when Ollama/Gemma is available locally.
"""

    return f"""
## Indus Valley Civilization ✅

{level_intro(level, language)}

### Explanation
Indus Valley Civilization, jise Harappan Civilization bhi kehte hain, duniya ki earliest urban civilizations me se ek thi. Ye town planning, drainage system, trade, seals aur Great Bath ke liye famous thi.

### Key Points
- Cities grid pattern par planned thi.
- Drainage system covered aur advanced tha.
- Great Bath Mohenjo-daro me mila.
- Lothal ek important dockyard tha.
- People copper aur bronze use karte the, iron nahi.
- Trade ke liye seals ka use hota tha.

> Hosted demo fallback. Full Gemma response works when Ollama/Gemma is available locally.
"""


# --------------------------------------------------
# Generic fallback generators
# --------------------------------------------------
def generic_explanation(prompt: str, level: str, language: str) -> str:
    topic = extract_topic(prompt)

    if "buddhism" in prompt.lower() and "jainism" in prompt.lower():
        return buddhism_jainism_answer(level, language)

    if any(x in prompt.lower() for x in ["indus", "harappan", "ivc"]):
        return indus_answer(level, language)

    if level == "Beginner":
        body = f"""
### Simple Explanation
**{topic}** ko easy way me samjho: pehle iska basic meaning samjho, phir 3–5 important points yaad karo.

### Key Points
- Topic ka simple meaning samjho.
- Important keywords note karo.
- Example ke saath revise karo.
- Confusing points ko short table me compare karo.
- Last me 2–3 MCQs solve karo.

### Easy Study Tip
Beginner level par goal hai: concept clear hona, not over-detail.
"""

    elif level == "School Student":
        body = f"""
### School-Level Explanation
**{topic}** ko exam answer format me likhna best rahega: introduction, main points, example aur conclusion.

### Answer Structure
1. 2-line introduction
2. 4–5 main points
3. 1 example
4. Short conclusion

### Study Tip
Notebook me short notes banao aur headings underline karo.
"""

    elif level == "SSC Aspirant":
        body = f"""
### SSC Exam-Oriented Explanation
**{topic}** ko SSC perspective se facts, keywords aur PYQ pattern ke saath prepare karo.

### High-Yield Approach
- Definition/meaning
- Important facts
- Dates/places/persons if relevant
- One-liner MCQ facts
- Memory trick
- Previous year style revision

### SSC Tip
PYQ repeat pattern par focus karo. Long theory se zyada factual accuracy important hai.
"""

    else:
        body = f"""
### Analytical Explanation
**{topic}** ko college level par context, concept, causes, features, significance aur criticism ke साथ समझना चाहिए.

### Structured Analysis
- Background/context
- Main concept
- Key features
- Examples
- Significance
- Limitations or criticism
- Conclusion

### College Tip
Answer me sirf facts nahi, explanation and analysis bhi add karo.
"""

    return f"""
## {topic} ✅

{level_intro(level, language)}

{body}

> Hosted demo fallback. Full Gemma response works when Ollama/Gemma is available locally.
"""


def generic_quiz(prompt: str, level: str, language: str) -> str:
    topic = extract_topic(prompt)

    if level == "Beginner":
        difficulty = "Easy basic questions"
    elif level == "School Student":
        difficulty = "School exam level"
    elif level == "SSC Aspirant":
        difficulty = "SSC PYQ-style factual questions"
    else:
        difficulty = "Conceptual + analytical questions"

    return f"""
## 📝 Quiz on {topic} ✅

{level_intro(level, language)}

**Difficulty:** {difficulty}

**Q1. {topic} ka basic meaning kya hai?**  
A) Random fact  
B) Main concept of the topic  
C) Unrelated event  
D) None of these  

**Correct Answer:** B) Main concept of the topic  
**Explanation:** Kisi bhi topic ko samajhne ke liye pehle uska basic concept clear hona chahiye.

---

**Q2. Exam preparation me {topic} ko kaise revise karna best hai?**  
A) Sirf reading  
B) Keywords + MCQs  
C) Ignore karna  
D) Sirf guessing  

**Correct Answer:** B) Keywords + MCQs  
**Explanation:** Keywords aur MCQ practice se retention improve hota hai.

---

**Q3. Answer writing me kya important hai?**  
A) Long paragraph only  
B) Clear points and examples  
C) No structure  
D) Random facts  

**Correct Answer:** B) Clear points and examples  
**Explanation:** Structured answer examiner ko easily समझ आता है.

---

**Q4. Revision ke liye best method kya hai?**  
A) Mistake notebook  
B) No revision  
C) Only new topics  
D) Guesswork  

**Correct Answer:** A) Mistake notebook  
**Explanation:** Wrong questions revise karne se score improve hota hai.

---

**Q5. {topic} ke liye sabse pehla step kya hona chahiye?**  
A) Advanced details  
B) Basic definition  
C) Random examples  
D) Skip topic  

**Correct Answer:** B) Basic definition  
**Explanation:** Definition clear hogi to detail samajhna easy hota hai.

> Hosted demo fallback. Full Gemma response works when Ollama/Gemma is available locally.
"""


def generic_answer_check(prompt: str, level: str, language: str) -> str:
    return f"""
## ✅ Answer Evaluation

{level_intro(level, language)}

**Score: 5/10**

### What is Good ✅
- Aapne main keywords mention kiye.
- Basic understanding dikh rahi hai.
- Answer relevant direction me hai.

### What is Missing ❌
- Explanation short hai.
- Examples add karne chahiye.
- Points ko structure me likhna chahiye.
- Conclusion missing hai.

### Improved Answer Format ✍️
1. Short introduction
2. 4–5 bullet points
3. Example/fact
4. Short conclusion

### Final Tip 💡
Apne level ke hisaab se answer me depth add karo:
- Beginner: simple explanation
- SSC: keywords + facts
- College: analysis + examples

> Hosted demo fallback. Full Gemma response works when Ollama/Gemma is available locally.
"""


def generic_study_plan(prompt: str, level: str, language: str) -> str:
    topic = extract_topic(prompt)

    if level == "Beginner":
        focus = "basic concepts and habit building"
    elif level == "School Student":
        focus = "chapter-wise learning and school exam revision"
    elif level == "SSC Aspirant":
        focus = "PYQ, static GK, current affairs, mock tests and mistake notebook"
    else:
        focus = "conceptual depth, notes, analysis and revision"

    return f"""
## 📅 Study Plan for {topic} ✅

{level_intro(level, language)}

**Main Focus:** {focus}

### Week 1: Foundation
- Basic concepts clear karo
- Short notes banao
- Daily 20 MCQs solve karo

### Week 2: Practice
- Topic-wise questions solve karo
- Weak areas identify karo
- Mistake notebook maintain karo

### Week 3: Revision
- Notes revise karo
- Mixed MCQs solve karo
- Important facts ya formulas revise karo

### Week 4: Mock + Final Polish
- Mock test do
- Wrong questions revise karo
- Last 2 days light revision rakho

### Daily Routine
- 1–2 hours concept study
- 30–60 minutes practice
- 20 minutes revision

> Hosted demo fallback. Full Gemma response works when Ollama/Gemma is available locally.
"""


def fallback_response(prompt: str) -> str:
    level = detect_student_level(prompt)
    language = detect_language(prompt)

    if is_probably_quiz(prompt):
        return generic_quiz(prompt, level, language)

    if is_probably_answer_check(prompt):
        return generic_answer_check(prompt, level, language)

    if is_probably_study_plan(prompt):
        return generic_study_plan(prompt, level, language)

    return generic_explanation(prompt, level, language)


# --------------------------------------------------
# Main Gemma call
# --------------------------------------------------
def ask_gemma(prompt: str) -> str:
    """
    Local setup:
    - Ollama running ho
    - gemma4:31b-cloud model available ho
    To real Gemma response aayega.

    Streamlit Cloud:
    - Localhost Ollama available nahi hota
    - Generic level-aware fallback response return hoga
    """
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
