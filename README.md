# HFSM-Based Digital Book Sorter Library System

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-red)
![Status](https://img.shields.io/badge/Status-Prototype-green)

An automated classification engine that uses **Hierarchical Finite State Machines (HFSM)** to categorize digital library records based on metadata patterns. This system is designed to provide transparent, deterministic, and auditable sorting for bibliographic data.

## 👥 Group 9 - Development Team
* **Kyle Desmond P. Co**
* **Marvin C. Barrios**
* **Ken Calvin S. Satorre**
* **Earl Andrei D. Fidel**

## 📖 Project Overview
[cite_start]Modern digital libraries struggle with inconsistent metadata[cite: 10]. This project implements a **Finite-State Automata** approach to classification, prioritizing **determinism** and **explainability** over black-box machine learning models.

The system ingests raw bibliographic data (Title, Keywords) and processes it through a token-based state machine to assign a category (e.g., *Computer Science*, *History*).

### Key Features
* **Deterministic Classification:** Uses HFSM logic to ensure repeatable results.
* **Conflict Resolution:** Handles cases where books match multiple categories.
* **Audit Logging:** Provides a transparent trace of the state transitions for every classification decision.
* **Review Queue:** Automatically flags ambiguous items for human-in-the-loop review.

## 📂 Repository Structure
```text
hfsm-book-sorter/
├── data/
│   ├── rules.json       # The FSM definitions (States & Transitions)
│   └── books.csv        # Sample dataset for testing
├── src/
│   └── hfsm_engine.py   # Core logic for the Automata class
├── app.py               # Main User Interface (Streamlit)
└── requirements.txt     # Project dependencies
