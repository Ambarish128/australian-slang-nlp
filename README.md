# 🇦🇺 Aussie Slang Translator

Translate and understand Australian slang instantly with this interactive Streamlit app powered by custom NLP pipelines.

---

## 🚀 Project Overview

The **Aussie Slang Translator** is a web app that detects Australian slang phrases in user text and replaces them with their standard meanings. It supports:

- Real-time slang detection using a custom spaCy Named Entity Recognition (NER) model  
- Translation of slang terms to their dictionary meanings  
- User submissions of new slang phrases, pending admin approval  
- Usage tracking and analytics of slang terms in the app  
- A clean Streamlit interface to translate, add slang, view dictionary, and analyze trends  

This project is ideal for anyone interested in Australian English, NLP pipelines, and community-driven language tools.

---

## 📂 Project Structure

| File / Folder                  | Purpose                                           |
|-------------------------------|--------------------------------------------------|
| `app.py`                      | Main Streamlit application                        |
| `slang_dict.json`             | Core dictionary of approved Australian slang     |
| `pending_slangs.json`         | User-submitted slang awaiting admin approval     |
| `slang_usage_counts.csv`      | Tracks usage frequency of slang terms             |
| `slang_ner.py`                | Custom spaCy pipeline adding Aussie slang NER    |
| `slang_translator.py`         | Translates slang to meaning & updates usage stats |
| `update_dictionary.py`        | Functions for slang submission & admin approval  |
| `slang_trend_analytics.py`    | Streamlit page showing top slang usage trends    |
| `requirements.txt`            | Python dependencies                               |

---

## 🧠 How It Works

### 1. Slang Detection & Translation

- Uses spaCy’s `EntityRuler` with patterns loaded from `slang_dict.json` to detect slang as named entities.
- Replaces detected slang with dictionary meanings, handling plurals with fallback rules.
- Updates usage counts for analytics.

### 2. User Submission & Admin Approval

- Users can submit new slang phrases via the app.
- Submissions are stored in `pending_slangs.json`.
- Admins approve slangs, which moves them to the main dictionary and logs approvals.

### 3. Usage Analytics

- Each slang’s usage is tracked in `slang_usage_counts.csv`.
- The app displays a dashboard with the top 10 most used slang terms via interactive Altair charts.

---

## 🎨 Streamlit App Overview

### Navigation

- **Translate Slang**: Input sentences and see translated output with detected slang highlighted.
- **Add New Slang**: Submit new slang phrases and meanings for admin approval.
- **View Dictionary**: Browse and search the current slang dictionary.
- **Usage Analytics**: View slang usage trends over time.

---

## 🛠 Installation

### Prerequisites

- Python 3.9+  
- `pip` package manager

### Setup

1. Clone the repo:
   
   git clone https://github.com/yourusername/aussie-slang-translator.git
   cd aussie-slang-translator

2. Install dependencies:
    
    pip install -r requirements.txt

3. Download and install spaCy English model:
    
    python -m spacy download en_core_web_sm

4. Run the app:   
    
    streamlit run app.py

🧩 Usage Examples
Translate slang:

Input:

He’s a fair dinkum bloke, no cap! and he eats bikkies.

Output:

He’s a genuine man, no cap! and he eats biscuits.

Add new slang:

Submit "arvo" meaning "afternoon" for admin review.

📊 Analytics
The app tracks slang usage and provides real-time visualization of the most popular slang terms. This helps understand slang trends and improve the dictionary.

📁 Data Files
slang_dict.json: Main slang dictionary (approved terms)

pending_slangs.json: User-submitted slang for admin approval

slang_usage_counts.csv: Tracks slang usage frequency

slang_logs.csv: Logs approved slang with timestamps

🧑‍💻 Developer Notes
The spaCy pipeline is customized by adding an EntityRuler component before the default NER.

The app handles plural slang terms by adding plural patterns and fallback singularization.

User submissions and approvals maintain data integrity with JSON files and logs.

The modular design allows easy expansion with additional slang or NLP features.

🤝 Contribution
Contributions are welcome! Feel free to submit slang suggestions, bug fixes, or UI improvements via pull requests.

Thank you for checking out the Aussie Slang Translator! 🇦🇺🎉

## 📞 Contact

Connect with me on [LinkedIn](https://www.linkedin.com/feed/)