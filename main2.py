import pdfplumber
from transformers import AutoTokenizer, AutoModelForTokenClassification

model_name = "dslim/bert-base-NER"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForTokenClassification.from_pretrained(model_name)
import torch
import re
from datetime import datetime


# Step 2: Define a function to preprocess text
def preprocess_text(text):
    # Remove unnecessary characters and split into sentences
    text = re.sub(r'[\(\)\[\]]', '', text)
    sentences = re.split(r'[.!?]', text)
    
    # Tokenize and pad each sentence
    tokenized_sentences = [tokenizer(sentence, return_tensors="pt", padding=True, truncation=True, max_length=512) for sentence in sentences]
    return tokenized_sentences


# Step 3: Define a function to extract entities using NER
def extract_entities(tokenized_sentences):
    entities = []
    for tokens in tokenized_sentences:
        outputs = model(**tokens)
        predictions = torch.argmax(outputs.logits, dim=-1)
        input_ids = tokens.input_ids.squeeze().tolist()
        tokens = tokenizer.convert_ids_to_tokens(input_ids)
        spans = get_entity_spans(predictions.squeeze(), tokens)
        print("Spans:", spans)
        entities.extend([tokenizer.convert_tokens_to_string(tokens[start:end]) for start, end in spans])
    return entities


def get_entity_spans(predictions, tokens):
    entity_spans = []
    current_entity = None
    for idx, (token, prediction) in enumerate(zip(tokens, predictions)):
        if prediction != 0 and current_entity is None:
            current_entity = idx
        elif prediction == 0 and current_entity is not None:
            entity_spans.append((current_entity, idx))
            current_entity = None
    if current_entity is not None:
        entity_spans.append((current_entity, len(tokens)))
    return entity_spans


# Step 4: Define functions to extract relevant information from entities
def extract_company_names(entities):
    company_names = [entity for entity in entities if entity.endswith("Inc.") or entity.endswith("Corp.") or entity.endswith("LLC")]
    return company_names

def extract_locations(entities):
    locations = [entity for entity in entities if any(location_word in entity for location_word in ["Virginia", "Maryland", "District of Columbia"])]
    return locations

def extract_amounts(text):
    amount_pattern = r'\$\d+,?\d*,?\d+'
    amounts = re.findall(amount_pattern, text)
    return amounts

def extract_dates(text):
    date_pattern = r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}'
    dates = re.findall(date_pattern, text)
    parsed_dates = [datetime.strptime(date_str, '%B %d, %Y').date() for date_str in dates]
    return parsed_dates

def extract_contracting_activities(entities):
    contracting_activities = [entity for entity in entities if "Command" in entity or "Army" in entity or "Contracting" in entity]
    return contracting_activities

# Step 5: Extract data from the PDF
def extract_data_from_pdf(pdf_path):
    contracts = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if "CONTRACTS" in text:
                paragraphs = text.split("\n\n")
                for paragraph in paragraphs:
                    if paragraph.strip():
                        entities = extract_entities(preprocess_text(paragraph))
                        company_names = extract_company_names(entities)
                        locations = extract_locations(entities)
                        amounts = extract_amounts(paragraph)
                        dates = extract_dates(paragraph)
                        contracting_activities = extract_contracting_activities(entities)

                        contract = {
                            "company_names": company_names,
                            "locations": locations,
                            "amounts": amounts,
                            "dates": dates,
                            "contracting_activities": contracting_activities
                        }
                        contracts.append(contract)
    return contracts

# Step 6: Tabular representation and visualization
import pandas as pd
import matplotlib.pyplot as plt

# Example usage
pdf_path = "1.pdf"
contracts = extract_data_from_pdf(pdf_path)

# Create a pandas DataFrame
contracts_df = pd.DataFrame(contracts)
print(contracts_df)

# Save to CSV file
contracts_df.to_csv("contracts.csv", index=False)

# # Visualize data
# plt.figure(figsize=(10, 6))
# company_counts = contracts_df["company_names"].explode().value_counts()
# company_counts.plot(kind="bar")
# plt.title("Contract Awards by Company")
# plt.xlabel("Company")
# plt.ylabel("Number of Contracts")
# plt.show()