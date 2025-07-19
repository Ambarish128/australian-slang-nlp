import streamlit as st
import spacy
import json
from utils.slang_ner import create_slang_ner
from slang_translator import replace_slang_with_meaning
from update_dictionary import submit_new_slang
from utils.Slang_Trend_Analytics import slang_usage_trend_analytics
# --- Constants ---
SLANG_DICT_FILE = "slang_data/slang_dict.json"
PENDING_FILE = "slang_data/pending_slangs.json"


# --- Load slang dict ---
@st.cache_data(show_spinner=False)
def load_slang_dict():
    with open(SLANG_DICT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# --- Load NLP pipeline with slang entity ruler ---
@st.cache_resource(show_spinner=False)
def load_nlp():
    return create_slang_ner(SLANG_DICT_FILE)

# --- Main App ---
def main():
    st.set_page_config(
        page_title="Aussie Slang Translator",
        page_icon="🇦🇺",
        layout="centered",
        initial_sidebar_state="auto"
    )

    st.title("🇦🇺 Aussie Slang Translator")
    st.markdown(
        "Translate Aussie slang in your sentences instantly. "
        "Detect slang terms, see their meanings, and submit new slang for approval."
    )
    st.divider()

    # Load data & model once
    slang_dict = load_slang_dict()
    nlp = load_nlp()

    # Sidebar Navigation
    st.sidebar.title("Navigation")
    option = st.sidebar.radio("Go to", ["Translate Slang", "Add New Slang", "View Dictionary","Usage Analytics"])

    if option == "Translate Slang":
        translate_section(slang_dict, nlp)

    elif option == "Add New Slang":
        add_slang_section(slang_dict)

    elif option == "View Dictionary":
        view_dictionary_section(slang_dict)
        
    elif option =="Usage Analytics":
        slang_usage_trend_analytics()


def translate_section(slang_dict, nlp):
    st.header("🔍 Translate Slang")

    user_input = st.text_area(
        "Enter a sentence with Aussie slang:",
        placeholder="E.g. 'He’s a fair dinkum bloke, no cap! and he eats bikkies.'",
        height=120
    )

    if st.button("Translate"):
        if not user_input.strip():
            st.warning("Please enter some text to translate.")
            return

        # Detect slang entities
        doc = nlp(user_input)
        detected_slangs = [ent.text for ent in doc.ents if ent.label_ == "AUS_SLANG"]

        if detected_slangs:
            st.success(f"Detected slang terms: {', '.join(set(detected_slangs))}")
        else:
            st.info("No Aussie slang detected!")

        # Translate
        translated = replace_slang_with_meaning(user_input, nlp=nlp)
        st.markdown("### Translated / Cleaned Sentence:")
        st.write(translated)
        st.markdown("Didnt get that right?, Apologies we are still improving")
        st.markdown(
            """
            ❓ **Didn't recognize one or more slang terms?**  
            Help us improve our Aussie Slang Translator by heading over to the **[➕ Add New Slang](#)** section in the sidebar  
            and submitting the term along with its meaning.  
            Your contribution helps keep the dictionary fresh and relevant for everyone! 🇦🇺
            """,
            unsafe_allow_html=True
        )


def add_slang_section(slang_dict):
    st.header("➕ Add New Slang")

    with st.form("add_slang_form", clear_on_submit=True):
        new_slang = st.text_input("Slang phrase (e.g., 'arvo')").strip().lower()
        new_meaning = st.text_area("Meaning / Explanation").strip()

        submit_btn = st.form_submit_button("Submit for Approval")

        if submit_btn:
            if not new_slang or not new_meaning:
                st.error("Both slang phrase and meaning are required!")
                return

            # Check existing dictionary & pending slang
            if new_slang in slang_dict:
                st.warning(f"Slang '{new_slang}' already exists in the dictionary.")
                return

            # Check pending submissions
            pending = {}
            if st.query_params.get("pending"):
                # Optionally add a pending view or load here
                pass
            try:
                with open(PENDING_FILE, "r", encoding="utf-8") as f:
                    pending = json.load(f)
            except FileNotFoundError:
                pending = {}

            if new_slang in pending:
                st.warning(f"Slang '{new_slang}' is already pending approval.")
                return

            # Submit new slang
            submit_new_slang(new_slang, new_meaning)
            st.success(f"Thank you! Slang '{new_slang}' submitted for admin approval.")


def view_dictionary_section(slang_dict):
    st.header("📘 Current Slang Dictionary")

    search = st.text_input("Search slang terms...").lower()

    filtered = {
        k: v for k, v in slang_dict.items() if search in k or search in v.lower()
    } if search else slang_dict

    st.write(f"Showing 20 entries out of {len(filtered)} slang entries.")

    # Display in two columns: Slang | Meaning
    entry=0
    for slang, meaning in filtered.items():        
        st.markdown(f"**{slang}**: {meaning}")
        entry+=1
        if entry==20:
            break



if __name__ == "__main__":
    main()
