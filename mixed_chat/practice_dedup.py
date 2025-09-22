import random
import string
import hashlib
from collections import Counter

# ============================================
# DATASET GENERATORS
# ============================================

def generate_exact_dup_dataset():
    """Generate dataset with exact duplicates for MD5 practice"""
    base_texts = [
        "The quick brown fox jumps over the lazy dog",
        "Python is a great programming language",
        "Machine learning is transforming industries",
        "Data science requires statistics knowledge",
        "Natural language processing is fascinating"
    ]
    
    dataset = []
    for i, text in enumerate(base_texts * 3):  # Each appears 3 times
        # Add some with different IDs but same text
        dataset.append({
            'id': f'doc_{len(dataset)}',
            'text': text,
            'source': random.choice(['web', 'book', 'paper'])
        })
    
    # Add some unique ones
    for i in range(5):
        dataset.append({
            'id': f'doc_{len(dataset)}',
            'text': f"Unique text number {i} with random content",
            'source': 'generated'
        })
    
    random.shuffle(dataset)
    return dataset

def generate_near_dup_dataset():
    """Generate dataset with near-duplicates for Jaccard practice"""
    base = "The quick brown fox jumps over the lazy dog"
    
    dataset = [
        {"id": 0, "text": base},
        {"id": 1, "text": "The quick brown fox jumps over a lazy dog"},  # 90% similar
        {"id": 2, "text": "A quick brown fox jumped over the lazy dog"},  # 80% similar
        {"id": 3, "text": "The fast brown fox jumps over the lazy cat"},  # 70% similar
        {"id": 4, "text": "The quick red fox runs over the sleepy dog"},  # 50% similar
        {"id": 5, "text": "Completely different text about programming"},  # 0% similar
        {"id": 6, "text": "The quick brown fox jumps over the lazy dog!"},  # Punctuation diff
        {"id": 7, "text": "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"},  # Case diff
    ]
    return dataset

def generate_spam_dataset():
    """Generate dataset with repetitive spam for pattern detection"""
    dataset = []
    
    # Type 1: Word repetition spam
    spam_words = ['buy', 'now', 'click', 'free', 'offer']
    for i in range(3):
        text = ' '.join([random.choice(spam_words) for _ in range(50)])
        dataset.append({"id": len(dataset), "text": text, "label": "spam"})
    
    # Type 2: Phrase repetition spam  
    phrase = "amazing deal click here"
    dataset.append({"id": len(dataset), "text": ' '.join([phrase] * 10), "label": "spam"})
    
    # Type 3: Mixed repetition
    template = "Call now {} best price {} limited time {}"
    nums = ['555-1234', '555-5678', '555-9999']
    for num in nums:
        text = template.format(num, num, num) * 5
        dataset.append({"id": len(dataset), "text": text, "label": "spam"})
    
    # Add legitimate texts
    legit_texts = [
        "Machine learning models require careful validation to avoid overfitting on training data",
        "The conference will feature speakers from industry and academia discussing AI ethics",
        "Python's simplicity makes it an excellent choice for data science applications",
        "Understanding statistics is fundamental to interpreting machine learning results correctly",
        "Cloud computing has revolutionized how we deploy and scale applications"
    ]
    
    for text in legit_texts:
        dataset.append({"id": len(dataset), "text": text, "label": "ham"})
    
    random.shuffle(dataset)
    return dataset

def generate_shingle_dataset():
    """Generate dataset for shingle/MinHash practice"""
    # Similar news articles with overlapping content
    articles = [
        """Apple announced record quarterly earnings driven by strong iPhone sales.
        The company reported revenue of $90 billion, exceeding analyst expectations.
        CEO Tim Cook attributed success to innovation and customer loyalty.""",
        
        """Apple reported record earnings this quarter with strong iPhone performance.
        Revenue reached $90 billion, surpassing Wall Street expectations significantly.
        Tim Cook cited innovation as key driver of the company's success.""",
        
        """Tech giant Apple posted impressive quarterly results led by iPhone sales.
        The firm announced $90 billion in revenue, beating market forecasts.
        Chief executive Cook highlighted product innovation and loyal customers.""",
        
        """Microsoft announced cloud growth driving quarterly earnings higher.
        Azure revenue increased 40% as enterprises accelerate digital transformation.
        CEO Satya Nadella emphasized AI integration across product lines.""",
        
        """Amazon Web Services continues dominating cloud infrastructure market.
        AWS revenue grew 35% year-over-year reaching new milestone.
        The company plans significant AI and machine learning investments."""
    ]
    
    dataset = [{"id": i, "text": article.replace('\n', ' ').strip()} 
               for i, article in enumerate(articles)]
    return dataset

# ============================================
# PROBLEMS TO SOLVE
# ============================================

print("=" * 60)
print("PROBLEM 1: EXACT DEDUPLICATION WITH MD5")
print("=" * 60)
print("\nDataset has 20 documents, some are exact duplicates.")
print("Task: Find and remove exact duplicates using MD5 hashing")
print("Expected: 5 unique documents + 5 generated = 10 unique total\n")

exact_data = generate_exact_dup_dataset()
print(f"Dataset size: {len(exact_data)} documents")
print("First 3 documents:")
for doc in exact_data[:3]:
    print(f"  ID: {doc['id']}, Text: {doc['text'][:50]}...")

print("\nYOUR TASK: Write a function to find exact duplicates using MD5")
print("Return: dict with keys: 'unique_count', 'duplicate_ids', 'hash_collisions'")

print("\n" + "=" * 60)
print("PROBLEM 2: NEAR-DUPLICATE DETECTION WITH JACCARD")
print("=" * 60)
print("\nDataset has texts with varying similarity to the first document")
print("Task: Find all documents with Jaccard similarity > 0.7 to doc 0")
print("Expected: IDs 0, 1, 2, 3, 6, 7 (after normalization)\n")

near_data = generate_near_dup_dataset()
for doc in near_data:
    print(f"  ID: {doc['id']}, Text: {doc['text']}")

print("\nYOUR TASK: Write jaccard_similarity(text1, text2) function")
print("Normalize: lowercase, remove punctuation")
print("Return: list of IDs with similarity > 0.7 to document 0")

print("\n" + "=" * 60)
print("PROBLEM 3: SPAM DETECTION WITH REPETITION ANALYSIS")
print("=" * 60)
print("\nDataset has spam and legitimate messages")
print("Task: Detect spam using word/phrase repetition patterns")
print("Expected: 7 spam messages\n")

spam_data = generate_spam_dataset()
print(f"Dataset size: {len(spam_data)} documents")
print("Sample spam:", spam_data[0]['text'][:100] + "...")
print("Sample ham:", [d for d in spam_data if d['label'] == 'ham'][0]['text'][:100])

print("\nYOUR TASK: Write is_spam(text) using repetition metrics")
print("Consider: unique word ratio, bigram repetition, phrase patterns")
print("Return: accuracy on the labeled dataset")

print("\n" + "=" * 60)
print("PROBLEM 4: DOCUMENT CLUSTERING WITH SHINGLES")
print("=" * 60)
print("\nDataset has news articles, some about same topic")
print("Task: Group similar articles using k-shingles (k=3 words)")
print("Expected: Articles 0,1,2 are similar (Apple news), 3,4 are different\n")

shingle_data = generate_shingle_dataset()
for doc in shingle_data:
    print(f"  ID: {doc['id']}, Preview: {doc['text'][:60]}...")

print("\nYOUR TASK: Write shingle_similarity(text1, text2, k=3)")
print("Use word-level shingles and Jaccard similarity")
print("Return: similarity matrix showing which docs cluster together")

# ============================================
# SOLUTIONS (uncomment to check your work)
# ============================================

def solutions():
    """Uncomment this function to see solutions"""
    
    # Solution 1: MD5 Exact Dedup
    def exact_dedup_md5(dataset):
        seen_hashes = {}
        unique_docs = []
        duplicate_ids = []
        
        for doc in dataset:
            text_hash = hashlib.md5(doc['text'].encode()).hexdigest()
            if text_hash not in seen_hashes:
                seen_hashes[text_hash] = doc['id']
                unique_docs.append(doc)
            else:
                duplicate_ids.append(doc['id'])
        
        return {
            'unique_count': len(unique_docs),
            'duplicate_ids': duplicate_ids,
            'hash_collisions': 0  # MD5 collisions extremely rare
        }
    
    # Solution 2: Jaccard Similarity
    def normalize_text(text):
        import re
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        return ' '.join(text.split())
    
    def jaccard_similarity(text1, text2):
        words1 = set(normalize_text(text1).split())
        words2 = set(normalize_text(text2).split())
        if not words1 or not words2:
            return 0
        return len(words1 & words2) / len(words1 | words2)
    
    def find_near_dups(dataset, threshold=0.7):
        base_text = dataset[0]['text']
        similar_ids = []
        for doc in dataset:
            if jaccard_similarity(base_text, doc['text']) > threshold:
                similar_ids.append(doc['id'])
        return similar_ids
    
    # Solution 3: Spam Detection
    def is_spam(text):
        if not text or len(text) < 20:
            return False
        
        words = text.lower().split()
        if len(words) < 5:
            return False
        
        # Check unique word ratio
        unique_ratio = len(set(words)) / len(words)
        if unique_ratio < 0.3:
            return True
        
        # Check bigram repetition
        if len(words) >= 2:
            bigrams = [(words[i], words[i+1]) for i in range(len(words)-1)]
            bigram_ratio = len(set(bigrams)) / len(bigrams)
            if bigram_ratio < 0.4:
                return True
        
        return False
    
    # Solution 4: Shingle Similarity
    def shingle_similarity(text1, text2, k=3):
        def get_shingles(text, k):
            words = text.lower().split()
            if len(words) < k:
                return set()
            return set(tuple(words[i:i+k]) for i in range(len(words)-k+1))
        
        shingles1 = get_shingles(text1, k)
        shingles2 = get_shingles(text2, k)
        
        if not shingles1 or not shingles2:
            return 0
        
        return len(shingles1 & shingles2) / len(shingles1 | shingles2)
    
    # Test solutions
    print("\n" + "=" * 60)
    print("SOLUTIONS")
    print("=" * 60)
    
    # Test 1
    result1 = exact_dedup_md5(exact_data)
    print(f"\n1. MD5 Dedup: {result1['unique_count']} unique docs")
    
    # Test 2  
    result2 = find_near_dups(near_data, 0.7)
    print(f"\n2. Jaccard Near-dups: IDs {result2}")
    
    # Test 3
    spam_predictions = [is_spam(doc['text']) for doc in spam_data]
    spam_labels = [doc['label'] == 'spam' for doc in spam_data]
    accuracy = sum(p == l for p, l in zip(spam_predictions, spam_labels)) / len(spam_data)
    print(f"\n3. Spam Detection Accuracy: {accuracy:.2%}")
    
    # Test 4
    print("\n4. Shingle Similarity Matrix:")
    for i in range(3):
        sims = [shingle_similarity(shingle_data[i]['text'], shingle_data[j]['text']) 
                for j in range(3)]
        print(f"   Doc {i} similarities: {[f'{s:.2f}' for s in sims]}")

# Uncomment to see solutions:
# solutions()