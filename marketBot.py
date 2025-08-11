import openai
import spacy
!pip install openai==0.28



openai.api_key = "put your api key🥲"




# Load Spacy NER model
nlp = spacy.load("en_core_web_sm")


# Predefined list of stock market-related entities (extendable)
stock_entities = ["Apple", "Google", "Microsoft", "Tesla", "NASDAQ", "Dow Jones", "S&P 500", "Bitcoin", "Ethereum"]




def analyze_sentiment(review, category):
    prompt = f"Analyze the sentiment of the following {category} statement in the context of stock market performance. \
    Classify it as Positive (bullish), Negative (bearish), or Neutral:\n\nStatement: {review}"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a sentiment analysis assistant specialized in financial markets."},
            {"role": "user", "content": prompt},
        ]
    )

    # Extract the sentiment classification
    sentiment = response['choices'][0]['message']['content']
    return sentiment.strip()





 #Function to perform Named Entity Recognition (NER)
def extract_entities(review):
    doc = nlp(review)
    entities = [(ent.text, ent.label_) for ent in doc.ents]

    # Additional filtering for financial entities
    matched_stocks = [ent for ent in entities if ent[0] in stock_entities]
    return matched_stocks if matched_stocks else entities  # Return matched stocks or original entities




# Main function to perform sentiment analysis and NER
def main():
    # Get input from user
    category = input("Enter the category (e.g., Stock, Index, Crypto, Economy, Other): ").capitalize()
    review = input(f"Enter your market statement related to {category.lower()}: ")

    if review:
        print("\nPerforming Stock Market Sentiment Analysis...\n")
        sentiment_with_contributions = analyze_sentiment(review, category)
        print(f"Sentiment Analysis Result: {sentiment_with_contributions}")

        print("\nPerforming Named Entity Recognition (NER)...\n")
        entities = extract_entities(review)
        print(f"Identified Market Entities: {entities}")
    else:
        print("Please enter a valid statement.")

# Run the main function
main()
