# doc_quality/metrics.py
import re, spacy, textstat
import nltk
from collections import Counter
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')

nlp = spacy.load("en_core_web_sm")
stop_words = set(stopwords.words('english'))
reference_headings = ["Bug Fixes", "Improvements", "Features", "Documentation", "Major Changes", "Performances", 
                      "Highlights", "Build"]
readme_reference_headings = ["Installation", "Usage", "Contributing", "License", "Features"]
discourse_markers = ["however", "moreover", "therefore", "for example", "thus", "furthermore"]

def get_metrics(text):
    doc = nlp(text)
    words = [token.text for token in doc if token.is_alpha]
    sentences = list(doc.sents)

    m1 = len(words)
    m2 = sum(len(sent.text.split()) for sent in sentences) / len(sentences)
    m3 = textstat.flesch_reading_ease(text)
    m4 = round(m1 / 200, 2)
    m5 = textstat.difficult_words(text)
    m6 = len(doc.ents)
    m7 = len(re.findall(r"\b\w+\(\)|[A-Z][a-z]+[A-Z]\w+", text))

    headings = re.findall(r"^#+\s*(.*)", text, re.MULTILINE)
    matched_headings = sum(1 for h in headings if h.strip() in reference_headings)
    m8 = matched_headings / len(reference_headings)

    m9 = sum(1 for i in range(1, len(sentences)) if len(sentences[i].text.split()) >= len(sentences[i-1].text.split())) / (len(sentences) - 1)
    m10 = len(re.findall(r"(^[-*+\d]\.|^\s*[-*+])", text, re.MULTILINE))
    m11 = len(re.findall(r"https?://\S+|www\.\S+", text))

    identifiers = re.findall(r"\b[a-zA-Z_][a-zA-Z0-9_]*\b", text)
    identifier_counts = Counter(identifiers)
    repeated = [val for val in identifier_counts.values() if val > 1]
    m12 = sum(repeated) / len(identifiers) if identifiers else 0

    keywords = [token.lemma_ for token in doc if token.pos_ in ("NOUN", "ADJ") and token.text.lower() not in stop_words]
    m13 = len(set(keywords)) / len(keywords) if keywords else 0
    m14 = sum(1 for marker in discourse_markers if marker in text.lower())

    return {
        "M1_Words": m1,
        "M2_SentenceLength": m2,
        "M3_FleschScore": m3,
        "M4_ReadingTime": m4,
        "M5_DifficultWords": m5,
        "M6_NamedEntities": m6,
        "M7_Patterns": m7,
        "M8_HeadingMatchRatio": m8,
        "M9_LogicalFlow": m9,
        "M10_ListCount": m10,
        "M11_RefDensity": m11,
        "M12_IdentifierConsistency": m12,
        "M13_LexicalCohesion": m13,
        "M14_DiscourseMarkers": m14,
    }
