import spacy
import json
from typing import Optional
from utils.slang_ner import create_slang_ner
import csv
from datetime import datetime
import pandas as pd
import os

CSV_PATH = "slang_data/slang_usage_counts.csv"

def update_slang_occurrence(slang_term: str):
    slang_term = slang_term.lower().strip()
    # Load existing data or create new DataFrame if file doesn't exist
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
    else:
        df = pd.DataFrame(columns=["slang_term", "occurence"])

    # Check if slang_term exists
    if slang_term in df['slang_term'].values:
        df.loc[df['slang_term'] == slang_term, 'occurence'] += 1
    else:
        df = pd.concat([df, pd.DataFrame({"slang_term": [slang_term], "occurence": [1]})], ignore_index=True)

    # Save back to CSV
    df.to_csv(CSV_PATH, index=False)


def singularize(word: str) -> str:
    """
    Naive rule-based plural to singular converter for slang terms.
    """
    if word.endswith("ies"):
        return word[:-3] + "y"
    elif word.endswith("es"):
        return word[:-2]
    elif word.endswith("s"):
        return word[:-1]
    return word  # return as-is if no rule applies

def replace_slang_with_meaning(text:str,slang_json_path:str ="slang_data/slang_dict.json",nlp:Optional[spacy.Language]=None)->str:

    """
    Replaces Australian slang terms in a sentence with their full-form dictionary meanings.

    Parameters:
    ----------
    text : str
        The input sentence containing potential slang.
    
    slang_json_path : str
        The file path to the slang dictionary in JSON format.
    
    nlp : spacy.Language, optional
        A preloaded spaCy NLP pipeline with a slang EntityRuler. 
        If None, a new pipeline is created using the custom slang NER function.

    Returns:
    -------
    str
        The cleaned sentence with slang replaced by their standard dictionary meanings.
    """

    #Load slang dictionary from the json file to extract meanings
    with open(slang_json_path,'r',encoding='utf-8') as f:
      slang_dict=json.load(f)

    # If no Nlp object is passed we will create one using our slang aware pipeline
    if nlp is None:
    #Importing the slang entity creation function
      nlp=create_slang_ner(slang_json_path)

    # Use the nlp model to process the input text and create the document
    doc=nlp(text)

    #make a copy of the original text for modification
    replaced_text=text

    #Iterate through all entities and replace the AUS_SLANG entities with their meaning
    for ent in doc.ents:
      if ent.label_=="AUS_SLANG":
        #normalise the entity text to lowercase for dictionary lookup
        slang_term=ent.text.lower()

        #check if the slang term exists in the dictionary
        if slang_term in slang_dict.keys():
          update_slang_occurrence(slang_term)
          #Replace the slang text with its meaning
          replaced_text=replaced_text.replace(ent.text,slang_dict[slang_term])

        else:
          # Try singular fallback
          singular_slang=singularize(slang_term)
          print(singular_slang)
          if singular_slang in slang_dict.keys():
             update_slang_occurrence(singular_slang)
             meaning=slang_dict[singular_slang]
             replaced_text=replaced_text.replace(ent.text,meaning)


    #Return the transformed text
    return replaced_text

text = "He’s a fair dinkum bloke, no cap! and he eats bikkies"
translated = replace_slang_with_meaning(text)
print(translated)









