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

    if "language: hindi" in prompt_lower:
        return "Hindi"
    if "language: english" in prompt_lower:
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
        r"apna doubt/question likho\s*[:\-]\s*(.+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, prompt, re.IGNORECASE)
        if match:
            topic = match.group(1).strip()
            topic = topic.split("\n")[0].strip()
            if topic:
                return clean_topic(topic)

    lines = [line.strip() for line in prompt.splitlines() if line.strip()]
    skip_words = [
        "explain",
        "generate",
        "evaluate",
        "language",
        "student level",
        "answer in",
        "you are",
        "format",
        "instructions",
        "write",
        "create",
    ]

    for line in lines:
        lower = line.lower()
        if not any(word in lower for word in skip_words) and len(line) > 3:
            return clean_topic(line)

    return "this topic"


def clean_topic(topic: str) -> str:
    topic = topic.strip()
    topic = re.sub(r"^[\"'“”]+|[\"'“”]+$", "", topic)
    topic = topic.replace("?", "").strip()
    return topic[:120] if topic else "this topic"


def is_probably_quiz(prompt: str) -> bool:
    p = prompt.lower()
    return any(
        x in p
        for x in [
            "generate quiz",
            "quiz",
            "mcq",
            "multiple choice",
            "generate questions",
            "create quiz",
        ]
    )


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
            "study roadmap",
        ]
    )


def level_intro(level: str, language: str) -> str:
    if language == "English":
        if level == "Beginner":
            return "**Level: Beginner**\nI will explain this in very simple words with easy examples."
        if level == "School Student":
            return "**Level: School Student**\nI will explain this in school-exam style with clear points and examples."
        if level == "SSC Aspirant":
            return "**Level: SSC Aspirant**\nI will focus on exam facts, keywords, PYQ-style points, one-liners and MCQs."
        return "**Level: College Student**\nI will explain this with deeper context, analysis, examples, significance and conclusion."

    if language == "Hindi":
        if level == "Beginner":
            return "**Level: Beginner**\nमैं इसे बहुत आसान भाषा और छोटे examples के साथ समझाऊंगा।"
        if level == "School Student":
            return "**Level: School Student**\nमैं इसे school exam style में clear points और examples के साथ समझाऊंगा।"
        if level == "SSC Aspirant":
            return "**Level: SSC Aspirant**\nमैं exam facts, keywords, PYQ-style points, one-liners और MCQs पर focus करूंगा।"
        return "**Level: College Student**\nमैं इसे deeper context, analysis, examples, significance और conclusion के साथ समझाऊंगा।"

    if level == "Beginner":
        return "**Level: Beginner**\nMain isko simple words, short points aur easy examples ke saath samjhaunga."
    if level == "School Student":
        return "**Level: School Student**\nMain school-exam style me clear points, examples aur conclusion ke saath answer dunga."
    if level == "SSC Aspirant":
        return "**Level: SSC Aspirant**\nMain exam facts, keywords, PYQ-style points, one-liners aur MCQs par focus karunga."
    return "**Level: College Student**\nMain deeper context, analysis, examples, significance aur conclusion ke saath answer dunga."


# --------------------------------------------------
# Topic-specific answers
# --------------------------------------------------
def buddhism_jainism_answer(level: str, language: str) -> str:
    if level == "Beginner":
        return f"""
## Buddhism aur Jainism me Difference ✅

{level_intro(level, language)}

### 1. Easy Explanation

Buddhism aur Jainism dono India ke purane dharm hain. Dono lagbhag 6th century BCE ke time par develop hue. Dono ne Vedic rituals, animal sacrifice aur unnecessary religious show-off ka virodh kiya.

Simple words me:

- **Buddhism** balanced life sikhata hai.
- **Jainism** strict Ahimsa aur Tapasya sikhata hai.

### 2. Simple Difference Table

| Point | Buddhism | Jainism |
|---|---|---|
| Main teacher | Gautam Buddha | Mahavira |
| Path | Middle Path | Strict Tapasya |
| Ahimsa | Important | Bahut strict |
| Soul | Permanent soul ko accept nahi karta | Har living being me soul maanta hai |
| Goal | Nirvana | Moksha |
| Spread | India ke bahar bhi gaya | Mostly India me strong raha |

### 3. Easy Example

Agar koi person luxury aur extreme suffering dono se bachkar balanced life choose karta hai, ye Buddhism ke **Middle Path** jaisa hai.

Agar koi person kisi bhi living being ko hurt na karne ke liye bahut strict rules follow karta hai, ye Jainism ke **Ahimsa** jaisa hai.

### 4. Memory Trick 💡

**Buddhism = Balance**  
**Jainism = Jyada strict Ahimsa**

### 5. Final Beginner Tip

Beginner level par bas ye yaad rakho:

- Buddha → Middle Path
- Mahavira → Strict Ahimsa
- Buddhism → Nirvana
- Jainism → Moksha

> Hosted demo fallback. Full Gemma response works when Ollama/Gemma is available locally.
"""

    if level == "School Student":
        return f"""
## Buddhism aur Jainism me Difference ✅

{level_intro(level, language)}

### Introduction

Buddhism aur Jainism dono 6th century BCE ke around India me develop hue. Ye dono dharmik movements Vedic rituals, animal sacrifice aur caste-based social rigidity ke against aaye. Dono ne morality, simple life, self-control aur non-violence ko importance di.

### Main Differences

| Basis | Buddhism | Jainism |
|---|---|---|
| Founder/Main figure | Gautam Buddha | Mahavira, 24th Tirthankara |
| Main path | Middle Path | Extreme Tapasya |
| Ahimsa | Important principle | Highest and strictest principle |
| Soul concept | Permanent soul ko accept nahi karta | Har living being me soul maanta hai |
| Goal | Nirvana | Moksha |
| Language | Pali | Prakrit |
| Spread | India ke bahar Sri Lanka, China, Japan tak gaya | Mostly India me strong raha |
| Lifestyle | Moderate | Very strict |

### Similarities

- Dono ne Vedic rituals ka virodh kiya.
- Dono ne animal sacrifice oppose kiya.
- Dono ne simple life par focus kiya.
- Dono ne morality aur self-discipline ko importance di.
- Dono ne karma aur rebirth ke ideas ko importance di.

### Explanation

Buddhism ka main idea hai suffering ko samajhna aur usse mukti paana. Buddha ne Middle Path diya, jisme na zyada luxury aur na extreme suffering follow karni hoti hai.

Jainism me Ahimsa sabse bada principle hai. Jain monks insects tak ko harm na ho isliye bahut strict rules follow karte hain. Jainism me soul ya Jiva ka concept important hai.

### Conclusion

Buddhism aur Jainism dono reform movements the, lekin Buddhism practical aur balanced path deta hai, jabki Jainism strict Ahimsa aur Tapasya par focus karta hai.

### School Exam Tip

Answer me pehle short introduction likho, phir difference table banao, phir 2–3 similarities aur conclusion likho.

> Hosted demo fallback. Full Gemma response works when Ollama/Gemma is available locally.
"""

    if level == "SSC Aspirant":
        return f"""
## Buddhism vs Jainism — SSC Exam Ready ✅

{level_intro(level, language)}

### 1. High-Yield Difference Table

| Feature | Buddhism | Jainism |
|---|---|---|
| Founder/Main figure | Gautam Buddha | Mahavira, 24th Tirthankara |
| Path | Middle Path | Extreme Tapasya |
| Ahimsa | Important but practical | Very strict Ahimsa |
| Soul concept | Anatta, no permanent soul | Jiva, soul exists in every living being |
| Goal | Nirvana | Moksha |
| Language | Pali | Prakrit |
| Spread | India se bahar bhi spread | Mostly India tak limited |
| Sangha | Strong monastic organization | Strict monk discipline |
| Royal patronage | Ashoka important | Mostly merchant communities |
| Main idea | End of suffering | Liberation of soul |

### 2. SSC One-Liners

1. Buddhism ke founder Gautam Buddha the.  
2. Jainism me Mahavira 24th Tirthankara maane jaate hain.  
3. Buddhism ka path Middle Path hai.  
4. Jainism strict Ahimsa par based hai.  
5. Buddhism ka goal Nirvana hai.  
6. Jainism ka goal Moksha hai.  
7. Buddhism Pali language se related hai.  
8. Jainism Prakrit language se related hai.  
9. Buddhism India ke bahar bhi spread hua.  
10. Jainism mostly India me strong raha.

### 3. 10 Short Question-Answer

**Q1. Buddhism ka founder kaun tha?**  
Ans: Gautam Buddha.

**Q2. Jainism ke 24th Tirthankara kaun the?**  
Ans: Mahavira.

**Q3. Middle Path kis dharm se related hai?**  
Ans: Buddhism.

**Q4. Strict Ahimsa kis dharm ka main principle hai?**  
Ans: Jainism.

**Q5. Buddhism ka final goal kya hai?**  
Ans: Nirvana.

**Q6. Jainism ka final goal kya hai?**  
Ans: Moksha.

**Q7. Buddhism kis language se related hai?**  
Ans: Pali.

**Q8. Jainism kis language se related hai?**  
Ans: Prakrit.

**Q9. Anatta doctrine kis dharm se related hai?**  
Ans: Buddhism.

**Q10. Jiva concept kis dharm se related hai?**  
Ans: Jainism.

### 4. 10 MCQs

**Q1. Middle Path kisne diya?**  
A) Mahavira  
B) Gautam Buddha  
C) Ashoka  
D) Chandragupta  
**Answer:** B) Gautam Buddha

**Q2. Mahavira Jainism ke kaunse Tirthankara the?**  
A) 1st  
B) 10th  
C) 24th  
D) 30th  
**Answer:** C) 24th

**Q3. Strict Ahimsa kis religion se associated hai?**  
A) Buddhism  
B) Jainism  
C) Shaivism  
D) Vaishnavism  
**Answer:** B) Jainism

**Q4. Nirvana kis dharm ka goal hai?**  
A) Buddhism  
B) Jainism  
C) Sikhism  
D) Islam  
**Answer:** A) Buddhism

**Q5. Moksha word Jainism me kis cheez ko indicate karta hai?**  
A) Trade  
B) Liberation of soul  
C) War  
D) Agriculture  
**Answer:** B) Liberation of soul

**Q6. Buddhism ki language kaunsi maani jaati hai?**  
A) Sanskrit  
B) Pali  
C) Persian  
D) Tamil  
**Answer:** B) Pali

**Q7. Jainism ki language kaunsi maani jaati hai?**  
A) Prakrit  
B) Greek  
C) Latin  
D) Arabic  
**Answer:** A) Prakrit

**Q8. Anatta doctrine kis se related hai?**  
A) No permanent soul  
B) Strict caste system  
C) Fire worship  
D) Vedic sacrifice  
**Answer:** A) No permanent soul

**Q9. Buddhism ka spread kis region tak hua?**  
A) Sri Lanka, China, Japan  
B) Only Punjab  
C) Only Rajasthan  
D) Only Europe  
**Answer:** A) Sri Lanka, China, Japan

**Q10. Jain monks kis principle ko bahut strict follow karte hain?**  
A) Ahimsa  
B) Warfare  
C) Luxury  
D) Animal sacrifice  
**Answer:** A) Ahimsa

### 5. SSC Memory Trick

**Buddhism = Buddha + Balance + Pali + Nirvana**  
**Jainism = Jiva + Mahavira + Prakrit + Moksha**

> Hosted demo fallback. Full Gemma response works when Ollama/Gemma is available locally.
"""

    return f"""
## Buddhism and Jainism: Analytical Comparison ✅

{level_intro(level, language)}

### 1. Historical Background

Buddhism and Jainism emerged around the 6th century BCE in northern India. This period was marked by urbanization, growth of trade, rise of new social groups, and questioning of Vedic ritualism. Both traditions belonged to the wider Shramana movement, which challenged sacrifice-based religion and emphasized ethical living, renunciation and liberation.

### 2. Philosophical Orientation

Buddhism is primarily an ethical and psychological path focused on understanding suffering and ending it through the Eightfold Path. Jainism is more ascetic and metaphysical, centered on purification of the soul from karmic bondage.

### 3. Analytical Comparison

| Dimension | Buddhism | Jainism |
|---|---|---|
| Historical figure | Siddhartha Gautama, the Buddha | Mahavira, 24th Tirthankara |
| Core problem | Suffering caused by desire | Soul trapped by karma |
| Path | Middle Path | Strict asceticism |
| Soul theory | Anatta, no permanent self | Jiva, soul exists in all living beings |
| Karma | Ethical intention and suffering | Material-like bondage attached to soul |
| Liberation | Nirvana | Moksha |
| Ahimsa | Important moral principle | Absolute central principle |
| Social spread | Became transregional | Remained mainly Indian |
| Organization | Sangha helped expansion | Strong ascetic discipline |

### 4. Social and Religious Significance

Both movements reduced the dominance of ritual sacrifice and opened space for ethical religion. Buddhism developed a strong monastic organization and gained royal patronage, especially under Ashoka. This helped it spread to Sri Lanka, Central Asia, China, Japan and Southeast Asia.

Jainism remained more regionally concentrated, but it had deep influence on Indian ethics, vegetarianism, non-violence, trade communities and philosophical pluralism.

### 5. Critical Analysis

Buddhism was relatively moderate because it rejected both luxury and extreme self-torture. Jainism was stricter because it emphasized absolute non-violence and intense self-discipline. This difference shaped their social reach: Buddhism became more adaptable and missionary, while Jainism remained highly disciplined and community-centered.

### 6. Conclusion

Buddhism and Jainism were major reform movements of ancient India. Both challenged ritualism and promoted ethical conduct, but Buddhism emphasized a moderate path to end suffering, while Jainism emphasized strict ascetic discipline to liberate the soul.

> Hosted demo fallback. Full Gemma response works when Ollama/Gemma is available locally.
"""


def indus_answer(level: str, language: str) -> str:
    if level == "Beginner":
        return f"""
## Indus Valley Civilization ✅

{level_intro(level, language)}

### Simple Meaning

Indus Valley Civilization ek bahut purani civilization thi. Isko Harappan Civilization bhi kehte hain. Iske log planned cities me rehte the aur unka drainage system bahut advanced tha.

### Easy Points

1. IVC ko Harappan Civilization bhi kehte hain.  
2. Cities planned hoti thi.  
3. Drainage system advanced tha.  
4. Great Bath Mohenjo-daro me mila.  
5. Lothal dockyard ke liye famous hai.  
6. Harappan people iron use nahi karte the.  
7. Seals trade ke liye use hoti thi.

### Example

Aaj jaise modern cities me roads aur drainage planned hote hain, waise hi Harappan cities bhi planned thi.

### Memory Trick

**Harappa = first site**  
**Mohenjo-daro = Great Bath**  
**Lothal = Dockyard**

> Hosted demo fallback. Full Gemma response works when Ollama/Gemma is available locally.
"""

    if level == "SSC Aspirant":
        return f"""
## Indus Valley Civilization — SSC High-Yield Notes ✅

{level_intro(level, language)}

### 1. Important Sites

| Site | Present Location | Important Feature |
|---|---|---|
| Harappa | Pakistan | First discovered site |
| Mohenjo-daro | Pakistan | Great Bath |
| Lothal | Gujarat | Dockyard |
| Kalibangan | Rajasthan | Fire altars |
| Dholavira | Gujarat | Water management |
| Rakhigarhi | Haryana | Major Harappan site |
| Chanhudaro | Pakistan | Bead making |

### 2. Important Facts

- IVC was a Bronze Age civilization.
- Iron was not known to Harappans.
- Script was pictographic and not deciphered.
- Cities followed grid pattern.
- Drainage system was covered and advanced.
- Standardized weights and seals were used.
- Trade links existed with Mesopotamia.
- Agriculture included wheat, barley and cotton.

### 3. 10 Short Q&A

**Q1. IVC ko aur kis naam se jaana jaata hai?**  
Ans: Harappan Civilization.

**Q2. Harappa kisne discover kiya?**  
Ans: Daya Ram Sahni.

**Q3. Mohenjo-daro ka famous structure kya hai?**  
Ans: Great Bath.

**Q4. Lothal kisliye famous hai?**  
Ans: Dockyard.

**Q5. Kalibangan kisliye famous hai?**  
Ans: Fire altars.

**Q6. IVC kis age ki civilization thi?**  
Ans: Bronze Age.

**Q7. Harappans kis metal se anjaan the?**  
Ans: Iron.

**Q8. Script kaisi thi?**  
Ans: Pictographic and undeciphered.

**Q9. Dholavira kisliye famous hai?**  
Ans: Water management.

**Q10. Trade ke liye kya use hota tha?**  
Ans: Seals and weights.

### 4. 10 MCQs

**Q1. Great Bath kahan mila?**  
A) Harappa  
B) Mohenjo-daro  
C) Lothal  
D) Kalibangan  
**Answer:** B) Mohenjo-daro

**Q2. Lothal kis state me hai?**  
A) Gujarat  
B) Punjab  
C) Haryana  
D) Bihar  
**Answer:** A) Gujarat

**Q3. Harappans kis metal se anjaan the?**  
A) Copper  
B) Bronze  
C) Gold  
D) Iron  
**Answer:** D) Iron

**Q4. Kalibangan kisliye famous hai?**  
A) Dockyard  
B) Fire altars  
C) Great Bath  
D) University  
**Answer:** B) Fire altars

**Q5. IVC ki script kaisi thi?**  
A) Deciphered  
B) Pictographic  
C) Roman  
D) Persian  
**Answer:** B) Pictographic

**Q6. IVC ki main feature kya thi?**  
A) Town planning  
B) Iron weapons  
C) Big temples  
D) Horse army  
**Answer:** A) Town planning

**Q7. Dholavira kisliye famous hai?**  
A) Water management  
B) Gold coins  
C) Rock edicts  
D) Iron tools  
**Answer:** A) Water management

**Q8. IVC kis age ki civilization thi?**  
A) Iron Age  
B) Bronze Age  
C) Stone Age  
D) Modern Age  
**Answer:** B) Bronze Age

**Q9. Harappa site present-day kis country me hai?**  
A) India  
B) Nepal  
C) Pakistan  
D) Sri Lanka  
**Answer:** C) Pakistan

**Q10. Harappan trade me kya important tha?**  
A) Seals  
B) Paper currency  
C) Gunpowder  
D) Printing press  
**Answer:** A) Seals

> Hosted demo fallback. Full Gemma response works when Ollama/Gemma is available locally.
"""

    if level == "College Student":
        return f"""
## Indus Valley Civilization: Analytical Overview ✅

{level_intro(level, language)}

### 1. Introduction

The Indus Valley Civilization, also called Harappan Civilization, was one of the earliest urban civilizations of the world. It flourished in the northwestern part of the Indian subcontinent during the Bronze Age. Its major sites include Harappa, Mohenjo-daro, Lothal, Dholavira, Kalibangan and Rakhigarhi.

### 2. Urban Planning

One of the most remarkable features of IVC was its urban planning. Cities were generally laid out in grid patterns, with streets cutting each other at right angles. Many cities had a Citadel area and a Lower Town. This indicates planned civic organization.

### 3. Drainage and Civic Management

The drainage system of IVC was highly advanced. Houses were connected to street drains, and drains were often covered with baked bricks. This suggests concern for sanitation and public hygiene.

### 4. Economy and Trade

The economy was based on agriculture, craft production and trade. Harappans cultivated wheat, barley and cotton. Standardized weights, seals and evidence of trade with Mesopotamia indicate commercial sophistication.

### 5. Technology and Craft

Harappans used bronze, copper, beads, pottery and seals. The absence of iron is significant because it places IVC in the Bronze Age. Craft specialization suggests occupational diversity.

### 6. Religion and Culture

Evidence such as the Great Bath, terracotta figurines and seals suggests ritual practices. However, unlike Egypt or Mesopotamia, there is no clear evidence of huge temples or royal palaces.

### 7. Significance

IVC is important because it shows early urbanization, standardization, sanitation and long-distance trade. It represents a unique model of urban civilization in ancient South Asia.

### 8. Conclusion

The Indus Valley Civilization was a highly organized Bronze Age urban culture. Its town planning, drainage, trade and craft production show a sophisticated society, even though its script remains undeciphered.

> Hosted demo fallback. Full Gemma response works when Ollama/Gemma is available locally.
"""

    return f"""
## Indus Valley Civilization ✅

{level_intro(level, language)}

### Introduction

Indus Valley Civilization, jise Harappan Civilization bhi kehte hain, duniya ki earliest urban civilizations me se ek thi. Ye town planning, drainage system, trade, seals aur Great Bath ke liye famous thi.

### Features

1. Cities grid pattern par planned thi.  
2. Drainage system covered aur advanced tha.  
3. Great Bath Mohenjo-daro me mila.  
4. Lothal ek important dockyard tha.  
5. Harappan people copper aur bronze use karte the.  
6. Iron ka use nahi hota tha.  
7. Trade ke liye seals ka use hota tha.

### Conclusion

IVC ek advanced urban civilization thi jisme planning, hygiene aur trade ka strong system tha.

> Hosted demo fallback. Full Gemma response works when Ollama/Gemma is available locally.
"""


# --------------------------------------------------
# Generic fallback generators
# --------------------------------------------------
def generic_explanation(prompt: str, level: str, language: str) -> str:
    topic = extract_topic(prompt)
    lower = prompt.lower()

    if "buddhism" in lower and "jainism" in lower:
        return buddhism_jainism_answer(level, language)

    if any(x in lower for x in ["indus", "harappan", "ivc"]):
        return indus_answer(level, language)

    if level == "Beginner":
        body = f"""
### 1. Simple Meaning

**{topic}** ka matlab hai ek aisa concept/topic jise samajhne ke liye pehle basic definition clear karni hoti hai. Beginner level par sabse important hai ki aap topic ko easy language me samjho.

### 2. Easy Explanation

Is topic ko samajhne ke liye 3 steps follow karo:

1. Pehle iska meaning samjho.  
2. Phir important points yaad karo.  
3. Last me example aur MCQ practice karo.

### 3. Important Points

- Topic ka basic meaning clear karo.
- 5 important keywords likho.
- Ek example ke saath connect karo.
- Confusing words ko compare karo.
- Daily short revision karo.

### 4. Example

Agar topic **Operating System** hai, to simple words me OS computer aur user ke beech bridge hota hai. Jaise Windows, Android, Linux.

### 5. Memory Trick

**Meaning → Points → Example → Revision**

### 6. Beginner Tip

Over-detail me mat jao. Pehle concept clear karo, phir slowly depth add karo.
"""

    elif level == "School Student":
        body = f"""
### 1. Introduction

**{topic}** ek important topic hai jo school exams me definition, features, examples aur short notes ke form me poocha ja sakta hai.

### 2. Definition

{topic} ko simple words me define karte hue answer start karna chahiye. Definition clear aur short honi chahiye.

### 3. Explanation

Is topic ko samajhne ke liye aapko iske meaning, main features, examples aur importance par focus karna chahiye. School-level answer me long theory ke bajay clear headings aur points use karna best hota hai.

### 4. Main Features

- Basic definition
- Important terms
- Examples
- Advantages or uses
- Short conclusion

### 5. Example

Agar topic **Operating System** hai, to examples Windows, Linux, macOS aur Android ho sakte hain.

### 6. Exam Answer Format

1. Definition  
2. Explanation  
3. Features  
4. Example  
5. Conclusion  

### 7. Conclusion

{topic} ko samajhna important hai kyunki ye subject ke basic concepts ko strong banata hai.

### School Tip

Answer me headings use karo aur examples add karo. Isse answer neat aur scoring banta hai.
"""

    elif level == "SSC Aspirant":
        body = f"""
### 1. SSC Exam-Oriented Notes

**{topic}** ko SSC perspective se factual, direct aur MCQ-oriented way me prepare karna chahiye.

### 2. High-Yield Points

- Definition clear rakho.
- Important keywords yaad karo.
- Examples revise karo.
- One-liners prepare karo.
- PYQ pattern ke questions solve karo.

### 3. 10 Short Question-Answer

**Q1. {topic} ka basic meaning kya hai?**  
Ans: Iska meaning topic ke core concept ko explain karta hai.

**Q2. {topic} exam ke liye important kyu hai?**  
Ans: Kyunki isse direct factual questions ban sakte hain.

**Q3. {topic} revise kaise karein?**  
Ans: Keywords, examples aur MCQs ke saath.

**Q4. SSC me answer approach kya honi chahiye?**  
Ans: Short, factual aur direct.

**Q5. {topic} ke liye best note format kya hai?**  
Ans: Definition + points + example.

**Q6. MCQ solve karte waqt kya dhyan rakhein?**  
Ans: Keywords aur elimination method.

**Q7. Revision ka best method kya hai?**  
Ans: Mistake notebook.

**Q8. Kya long theory zaroori hai?**  
Ans: SSC ke liye mostly factual clarity zaroori hai.

**Q9. PYQ kyu important hai?**  
Ans: SSC me pattern repeat hota hai.

**Q10. Final preparation tip kya hai?**  
Ans: Daily revision + MCQ practice.

### 4. 10 MCQs

**Q1. {topic} prepare karne ka first step kya hai?**  
A) Random reading  
B) Definition clear karna  
C) Guesswork  
D) Skip karna  
**Answer:** B) Definition clear karna

**Q2. SSC ke liye best revision method kya hai?**  
A) Mistake notebook  
B) No revision  
C) Sirf theory  
D) Sirf guessing  
**Answer:** A) Mistake notebook

**Q3. MCQ me score improve karne ke liye kya useful hai?**  
A) Elimination method  
B) Random marking  
C) No practice  
D) Long essay  
**Answer:** A) Elimination method

**Q4. Short notes me kya hona chahiye?**  
A) Keywords  
B) Unrelated story  
C) Random data  
D) Blank space  
**Answer:** A) Keywords

**Q5. PYQ ka full form kya hai?**  
A) Previous Year Questions  
B) Private Year Quiz  
C) Public Youth Questions  
D) None  
**Answer:** A) Previous Year Questions

**Q6. SSC GK/GA me kya important hota hai?**  
A) Factual accuracy  
B) Long story  
C) Drawing  
D) Random guess  
**Answer:** A) Factual accuracy

**Q7. Topic ko revise karne ka best way kya hai?**  
A) MCQ + notes  
B) Ignore  
C) Sirf video dekhna  
D) No practice  
**Answer:** A) MCQ + notes

**Q8. Exam me time bachane ke liye kya useful hai?**  
A) Direct keywords  
B) Long paragraphs  
C) Confusing notes  
D) No structure  
**Answer:** A) Direct keywords

**Q9. Answer yaad karne ke liye kya useful hai?**  
A) Memory trick  
B) No revision  
C) Random reading  
D) Guessing  
**Answer:** A) Memory trick

**Q10. Final preparation me kya karna chahiye?**  
A) Wrong questions revise  
B) Sab kuch skip  
C) New topics only  
D) No mock  
**Answer:** A) Wrong questions revise

### 5. SSC Final Tip

SSC ke liye **keywords + MCQs + PYQ + mistake notebook** best strategy hai.
"""

    else:
        body = f"""
### 1. Introduction

**{topic}** ko college level par sirf definition ke रूप में नहीं, बल्कि context, structure, function, significance और limitations ke saath samajhna chahiye.

### 2. Conceptual Background

Kisi bhi academic topic ko samajhne ke liye uska background important hota hai. Background batata hai ki topic ka origin, need aur relevance kya hai. Isse answer analytical banta hai.

### 3. Core Concept

{topic} ka core concept uske main idea ko explain karta hai. College-level answer me concept ko define karne ke baad uske components, functions aur applications discuss karne chahiye.

### 4. Key Features

- Basic definition and scope
- Main components
- Working or process
- Practical examples
- Advantages
- Limitations
- Current relevance

### 5. Detailed Explanation

Agar topic **Operating System** hai, to OS ek system software hai jo user aur computer hardware ke beech interface provide karta hai. It manages memory, process, files, input/output devices and security. It also provides a platform for application software.

Similarly, kisi bhi topic ko analyze karte waqt aapko uske:
- purpose,
- structure,
- working,
- importance,
- challenges,
- and real-world application
ko explain karna chahiye.

### 6. Significance

{topic} important hai kyunki ye subject ke broader framework ko samajhne me help karta hai. College-level learning me topic ki significance real-world application aur theoretical understanding dono se judti hai.

### 7. Limitations or Criticism

Har topic ke kuch limitations hote hain. Academic answer me limitation add karne se answer balanced aur mature lagta hai. Example ke liye, agar topic technology se related hai, to complexity, cost, security, efficiency ya accessibility limitations discuss ki ja sakti hain.

### 8. Example

Example answer ko concrete banata hai. Agar topic Operating System hai, examples Windows, Linux, macOS, Android aur iOS ho sakte hain.

### 9. Conclusion

Conclusion me topic ka short summary do aur uski importance mention karo. College-level answer me conclusion analytical hona chahiye, sirf repeat nahi.

### 10. College Writing Tip

Answer ka structure rakho: **Introduction → Background → Concept → Features → Example → Significance → Limitations → Conclusion**.
"""

    return f"""
## {topic} ✅

{level_intro(level, language)}

{body}

> Hosted demo fallback. Full Gemma response works when Ollama/Gemma is available locally.
"""


def generic_quiz(prompt: str, level: str, language: str) -> str:
    topic = extract_topic(prompt)

    if level == "SSC Aspirant":
        return f"""
## 📝 SSC Quiz on {topic} ✅

{level_intro(level, language)}

### 10 MCQs

**Q1. {topic} ka basic meaning kya hai?**  
A) Topic ka core concept  
B) Random fact  
C) Unrelated event  
D) None  
**Answer:** A) Topic ka core concept

**Q2. Exam preparation me best method kya hai?**  
A) Keywords + MCQs  
B) No revision  
C) Guessing  
D) Long story  
**Answer:** A) Keywords + MCQs

**Q3. PYQ ka use kyu hota hai?**  
A) Pattern samajhne ke liye  
B) Time waste ke liye  
C) Drawing ke liye  
D) None  
**Answer:** A) Pattern samajhne ke liye

**Q4. Revision ke liye best tool kya hai?**  
A) Mistake notebook  
B) Random notes  
C) No notes  
D) Only new topics  
**Answer:** A) Mistake notebook

**Q5. MCQ me elimination method ka benefit kya hai?**  
A) Wrong options hata sakte hain  
B) Time waste hota hai  
C) No benefit  
D) None  
**Answer:** A) Wrong options hata sakte hain

**Q6. Short notes me kya hona chahiye?**  
A) Keywords  
B) Long story  
C) Irrelevant data  
D) Blank page  
**Answer:** A) Keywords

**Q7. SSC preparation me kya important hai?**  
A) Factual accuracy  
B) Decorative writing  
C) Long essay  
D) No practice  
**Answer:** A) Factual accuracy

**Q8. {topic} ko revise kaise karein?**  
A) Definition + points + MCQ  
B) Skip karke  
C) Sirf guess karke  
D) No revision  
**Answer:** A) Definition + points + MCQ

**Q9. Exam ke last days me kya karna chahiye?**  
A) Wrong questions revise  
B) New books start  
C) No revision  
D) Random guessing  
**Answer:** A) Wrong questions revise

**Q10. Best final strategy kya hai?**  
A) PYQ + mock + mistake notebook  
B) No mock  
C) Only theory  
D) Skip topic  
**Answer:** A) PYQ + mock + mistake notebook

> Hosted demo fallback. Full Gemma response works when Ollama/Gemma is available locally.
"""

    return f"""
## 📝 Quiz on {topic} ✅

{level_intro(level, language)}

**Q1. {topic} ka basic meaning kya hai?**  
A) Main concept of the topic  
B) Random fact  
C) Unrelated event  
D) None  

**Correct Answer:** A) Main concept of the topic  
**Explanation:** Kisi bhi topic ko samajhne ke liye pehle uska basic concept clear hona chahiye.

---

**Q2. Answer writing me kya important hai?**  
A) Clear points and examples  
B) No structure  
C) Random facts  
D) Guesswork  

**Correct Answer:** A) Clear points and examples  
**Explanation:** Structured answer examiner ko easily samajh aata hai.

---

**Q3. Revision ke liye best method kya hai?**  
A) Mistake notebook  
B) No revision  
C) Only new topics  
D) Guesswork  

**Correct Answer:** A) Mistake notebook  
**Explanation:** Wrong questions revise karne se score improve hota hai.

---

**Q4. {topic} ke liye first step kya hona chahiye?**  
A) Basic definition  
B) Advanced details  
C) Random examples  
D) Skip topic  

**Correct Answer:** A) Basic definition  
**Explanation:** Definition clear hogi to detail samajhna easy hota hai.

---

**Q5. Topic ko yaad rakhne ke liye kya useful hai?**  
A) Memory trick  
B) No practice  
C) Random reading  
D) Guessing  

**Correct Answer:** A) Memory trick  
**Explanation:** Memory trick se revision fast hota hai.

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

### Level-Based Advice

- **Beginner:** simple language me answer likho.
- **School Student:** headings aur examples add karo.
- **SSC Aspirant:** keywords, facts aur PYQ-style points add karo.
- **College Student:** analysis, significance aur limitations add karo.

### Final Tip 💡

Answer ko structured format me likhne se marks improve hote hain.

> Hosted demo fallback. Full Gemma response works when Ollama/Gemma is available locally.
"""


def generic_study_plan(prompt: str, level: str, language: str) -> str:
    topic = extract_topic(prompt)

    if level == "SSC Aspirant":
        focus = "PYQ, static GK, current affairs, mock tests and mistake notebook"
    elif level == "College Student":
        focus = "conceptual depth, notes, analysis, assignments and revision"
    elif level == "School Student":
        focus = "chapter-wise learning, notes, examples and school exam revision"
    else:
        focus = "basic concepts and habit building"

    return f"""
## 📅 Study Plan for {topic} ✅

{level_intro(level, language)}

**Main Focus:** {focus}

### Week 1: Foundation
- Basic concepts clear karo
- Short notes banao
- Daily 20 MCQs ya practice questions solve karo

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
