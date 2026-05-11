# ShikshaSetu AI

## Gemma 4 Tutor for Rural Learners

ShikshaSetu AI is a Gemma-powered Hindi/Hinglish AI tutor built for the **Future of Education** track of the Gemma 4 Good Hackathon.

It helps rural and low-internet learners understand topics, generate quizzes, check answers, and create personalized study plans in simple language.

---

## Track

**Future of Education**

---

## Problem

Many students in rural and semi-urban areas face major learning barriers:

- Weak or inconsistent internet access
- Expensive coaching
- English language barrier
- Lack of personal doubt-solving support
- Difficulty preparing structured study plans

---

## Solution

ShikshaSetu AI provides an accessible learning assistant for students. It supports Hindi, Hinglish, and English learning modes.

The app helps students with:

- Doubt solving
- Quiz generation
- Answer evaluation
- Personalized study planning
- Exam-focused explanations

---

## How Gemma is Used

Gemma is used as the core reasoning and language model for:

- Explaining concepts in simple language
- Generating exam-style quizzes
- Evaluating student answers
- Creating personalized study plans
- Adapting responses for different student levels

The prototype uses Gemma 4 through Ollama cloud because the development system has limited local memory. The app is designed with a model abstraction layer, so it can be switched to a local Gemma deployment on capable devices.

---

## Features

### 1. Ask a Doubt

Students can ask a question and receive:

- Simple explanation
- Important points
- Memory trick
- Example
- Exam tip

### 2. Generate Quiz

Students can enter any topic and get:

- 5 MCQ questions
- 4 options per question
- Correct answer
- Short explanation

### 3. Check My Answer

Students can submit their answer and receive:

- Score out of 10
- Correct points
- Missing points
- Improved answer
- Final exam tip

### 4. Make Study Plan

Students can enter a goal and number of days to get:

- Day-wise plan
- Daily revision task
- Practice task
- Final revision strategy

---

## Tech Stack

- Python
- Streamlit
- Ollama
- Gemma 4 Cloud model

---

## Project Structure

```text
shikshasetu-ai/
│
├── app.py
├── gemma_engine.py
├── prompts.py
├── requirements.txt
├── README.md
└── assets/