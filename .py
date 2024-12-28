import re
from collections import Counter

def simple_tokenize(text):
    # Split the text into sentences
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    # Tokenize words in each sentence
    tokenized_sentences = [re.findall(r'\b\w+\b', sentence.lower()) for sentence in sentences]
    return sentences, tokenized_sentences

def luhn_summarization(text, summary_length=3, max_gap=4):
    # Tokenize sentences and words
    sentences, tokenized_sentences = simple_tokenize(text)
    words = [word for sentence in tokenized_sentences for word in sentence]

    # Filter out common words
    stop_words = {"the", "and", "of", "to", "a", "in", "is", "it", "for", "on", "with", "as", "this", "by", "an", "be"}
    filtered_words = [word for word in words if word not in stop_words]
    word_frequencies = Counter(filtered_words)

    # Identify significant words
    threshold = max(word_frequencies.values()) * 0.2
    significant_words = {word for word, freq in word_frequencies.items() if freq >= threshold}

    # Score each sentence
    sentence_scores = {}
    for i, tokens in enumerate(tokenized_sentences):
        significant_indices = [j for j, word in enumerate(tokens) if word in significant_words]
        if not significant_indices:
            continue

        # Find clusters of significant words
        clusters = []
        cluster = [significant_indices[0]]
        for k in range(1, len(significant_indices)):
            if significant_indices[k] - significant_indices[k - 1] <= max_gap:
                cluster.append(significant_indices[k])
            else:
                clusters.append(cluster)
                cluster = [significant_indices[k]]
        clusters.append(cluster)

        # Calculate the best score for the sentence
        max_cluster_score = 0
        for cluster in clusters:
            num_significant = len(cluster)
            total_words = cluster[-1] - cluster[0] + 1
            cluster_score = (num_significant ** 2) / total_words
            max_cluster_score = max(max_cluster_score, cluster_score)

        sentence_scores[sentences[i]] = max_cluster_score

    # Get the top sentences
    top_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:summary_length]
    return " ".join(top_sentences)

# Example usage
if __name__ == "__main__":
    example_text = """
    The purpose of abstracts in technical literature is to facilitate quick and accurate identification of the topic of published papers. 
    The preparation of abstracts is an intellectual effort, requiring general familiarity with the subject. To bring out the salient 
    points of an author’s argument calls for skill and experience. Consequently a considerable amount of qualified manpower that 
    could be used to advantage in other ways must be diverted to the task of facilitating access to information.
    """

    # Generate the summary
    summary = luhn_summarization(example_text)
    print("Summary:")
    print(summary)
