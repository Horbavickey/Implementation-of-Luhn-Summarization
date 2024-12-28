import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import Counter

# Ensure required NLTK data packages are downloaded
nltk.download('punkt')
nltk.download('stopwords')

def luhn_summarization(text, num_sentences=3):
    """
    Summarizes a given text using the Luhn algorithm.

    Parameters:
        text (str): The input text to summarize.
        num_sentences (int): The number of sentences to include in the summary.

    Returns:
        str: A summary containing the most relevant sentences.
    """
    try:
        # Tokenize text into sentences
        sentences = sent_tokenize(text)
        
        if not sentences:
            return "No sentences found in the input text."

        # Tokenize words and filter out stopwords
        stop_words = set(stopwords.words("english"))
        words = word_tokenize(text.lower())
        significant_words = [word for word in words if word.isalnum() and word not in stop_words]

        # Calculate word frequencies
        freq = Counter(significant_words)
        if not freq:
            return "No significant words found in the input text."

        # Define a threshold for significant words
        threshold = sum(freq.values()) / len(freq)

        # Score sentences based on significant words
        sentence_scores = {}
        for sentence in sentences:
            sentence_words = word_tokenize(sentence.lower())
            significant = [word for word in sentence_words if word in freq and freq[word] >= threshold]
            if significant:
                sentence_scores[sentence] = len(significant) ** 2 / len(sentence_words)

        if not sentence_scores:
            return "No sentences met the scoring criteria."

        # Select top sentences based on scores
        top_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_sentences]

        return " ".join(top_sentences)
    
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Test the implementation
if __name__ == "__main__":
    try:
        # Replace with the path to your text file
        file_path = "test_file.txt"
        with open(file_path, "r") as file:
            blog_post = file.read()

        # Number of sentences in the summary
        num_sentences = 3

        # Generate the summary
        summary = luhn_summarization(blog_post, num_sentences=num_sentences)
        print("Summary:\n", summary)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found. Please check the file path.")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
