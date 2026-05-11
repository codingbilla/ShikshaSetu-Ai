import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma4:31b-cloud"


def fallback_response(prompt: str) -> str:
    prompt_lower = prompt.lower()

    if "quiz" in prompt_lower or "mcq" in prompt_lower:
        return """
### Demo Quiz Generated ✅

**Q1. Indus Valley Civilization ko kis naam se bhi jaana jaata hai?**  
A) Vedic Civilization  
B) Harappan Civilization  
C) Mauryan Civilization  
D) Gupta Civilization  

**Correct Answer:** B) Harappan Civilization  
**Explanation:** Harappa site sabse pehle discover hui thi, isliye ise Harappan Civilization bhi kehte hain.

**Q2. Great Bath kis site se mila tha?**  
A) Harappa  
B) Lothal  
C) Mohenjo-daro  
D) Kalibangan  

**Correct Answer:** C) Mohenjo-daro  
**Explanation:** Great Bath Mohenjo-daro ka famous public bathing structure tha.

**Q3. Lothal kis cheez ke liye famous hai?**  
A) Dockyard  
B) Iron tools  
C) Ashoka pillar  
D) Rock edicts  

**Correct Answer:** A) Dockyard  
**Explanation:** Lothal Gujarat me ek important port city thi.

**Q4. IVC ke log kis metal se anjaan the?**  
A) Copper  
B) Bronze  
C) Gold  
D) Iron  

**Correct Answer:** D) Iron  
**Explanation:** IVC Bronze Age civilization thi.

**Q5. IVC ki sabse important feature kya thi?**  
A) Town planning  
B) Iron weapons  
C) Temples  
D) Horse riding  

**Correct Answer:** A) Town planning  
**Explanation:** Grid pattern cities aur drainage system IVC ki major features thi.

> Note: This is a cloud fallback response. Full Gemma response works when Ollama/Gemma is available locally.
"""

    if "check" in prompt_lower or "evaluate" in prompt_lower or "score" in prompt_lower:
        return """
### Answer Evaluation ✅

**Score: 4/10**

Your answer has some correct keywords, but it needs more explanation.

### Correct Points
- Planned cities
- Drainage system
- Trade and seals

### Missing Points
- Citadel and Lower Town
- Great Bath
- Granaries
- Agriculture
- Social structure

### Improved Answer

Harappan Civilization was known for advanced town planning. Cities were built in a grid pattern and divided into Citadel and Lower Town. The drainage system was well-developed and covered. Important structures like the Great Bath and granaries show their focus on hygiene and storage. They practiced agriculture, trade, and used seals for commercial purposes.

### Final Tip
In exams, write answers in bullet points with keywords and 1–2 line explanation.

> Note: This is a cloud fallback response. Full Gemma response works when Ollama/Gemma is available locally.
"""

    if "study plan" in prompt_lower or "plan" in prompt_lower or "days" in prompt_lower:
        return """
### 30-Day Study Plan ✅

## Phase 1: Core Topics  
**Day 1–5:** Indian Polity  
Focus: Constitution, Fundamental Rights, Parliament, President.

**Day 6–10:** History  
Focus: Ancient India, Medieval India, Modern India.

**Day 11–15:** Geography  
Focus: Rivers, mountains, climate, soil, map practice.

## Phase 2: Score Boosters  
**Day 16–20:** General Science  
Focus: Biology, Physics, Chemistry basics.

**Day 21–24:** Economics  
Focus: GDP, inflation, banking, RBI, budget.

**Day 25–27:** Static GK  
Focus: books, awards, sports, days, dances.

## Phase 3: Revision  
**Day 28:** Full revision  
**Day 29:** Mock test + mistake notebook  
**Day 30:** Final light revision

### Daily Routine
- 2 hours concept study
- 1 hour MCQs
- 30 minutes revision

> Note: This is a cloud fallback response. Full Gemma response works when Ollama/Gemma is available locally.
"""

    return """
### Simple Explanation ✅

Indus Valley Civilization, also called Harappan Civilization, was one of the earliest urban civilizations of the world. It was famous for planned cities, advanced drainage system, trade, seals, granaries, and the Great Bath.

### Key Points
- Cities were built in grid pattern.
- Drainage system was very advanced.
- Great Bath was found at Mohenjo-daro.
- Lothal was an important dockyard.
- People used copper and bronze but not iron.

### Exam Tip
Remember: **Harappa = first discovered site**, **Mohenjo-daro = Great Bath**, **Lothal = Dockyard**.

> Note: This is a cloud fallback response. Full Gemma response works when Ollama/Gemma is available locally.
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
