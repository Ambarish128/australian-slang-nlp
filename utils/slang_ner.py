import spacy
import json
from typing import Optional

def create_slang_ner(slang_json_path:str="slang_data/slang_dict.json",nlp:Optional[spacy.Language]=None) ->spacy.Language:
    """
    Creates a spaCy NLP pipeline with a custom EntityRuler component
    that detects Australian slang phrases as named entities.

    Parameters:
    ----------
    slang_json_path : str
        The file path to the slang dictionary (JSON format).
    nlp : spacy.Language, optional
        An existing spaCy language model. If None, a new 'en_core_web_sm' model is loaded.

    Returns:
    -------
    nlp : spacy.Language
        The spaCy language pipeline with an added EntityRuler for slang detection.
    """
    #Load the base English model if no spacy object is passed
    if nlp is None:
      nlp=spacy.load("models/en_core_web_sm/en_core_web_sm-3.8.0")

    # Add EntityRuler to the pipeline (BEFORE the NER component)
    ruler = nlp.add_pipe("entity_ruler", before="ner")

    #Load slang terms from the JSON dictionary file
    with open(slang_json_path,'r',encoding='utf-8') as f:
      slang_dict=json.load(f)


    #Prepare Patterns for Entity ruler in spacy's expected format

    patterns=[]
    for slang in slang_dict.keys():
      #Each pattern is a dictionary = label + phrase pattern
      patterns.append({
          "label":"AUS_SLANG",  # Custom Entity Label
          "pattern":slang.lower() # Ensure matching is in lowercase to avoid case sensitive conflicts
      })
      # --- Handle basic plural forms (naive method) ---
      # e.g., "bikkie" → "bikkies", "servo" → "servos"
      if slang.endswith("y"):
          plural_form = slang[:-1] + "ies"
      elif slang.endswith("o"):
          plural_form = slang + "s"
      else:
          plural_form = slang + "s"

      # Avoid duplicate if plural already exists
      if plural_form not in slang_dict:
          patterns.append({
              "label": "AUS_SLANG",
              "pattern": plural_form.lower()
          })


     # Add the list of patterns to the Entity Ruler
    ruler.add_patterns(patterns)


    #Return the modified spacy pipeline with aussie slang detection
    return nlp

# #Testing the function

# #create slang detection pipeline
# nlp=create_slang_ner()

# # Test Sentence
# text = "The ankle biter was flat out this arvo, watching bush telly and eating bikkies at the servos."
# doc = nlp(text)

# for ent in doc.ents:
#   if ent.label_=="AUS_SLANG":
#     print(ent.text," -> ",ent.label_)
