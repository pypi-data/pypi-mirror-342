# doc_quality/suggestions.py
def suggest_improvements(metrics):
    suggestions = []

    # Conciseness
    if metrics["M1_Words"] > 1000:
        suggestions.append("Try reducing the number of words for conciseness.")
    if metrics["M2_SentenceLength"] > 25:
        suggestions.append("Shorten sentence length for better comprehension.")

    # Readability
    if metrics["M3_FleschScore"] < 50:
        suggestions.append("Improve readability with simpler language.")
    if metrics["M4_ReadingTime"] > 5:
        suggestions.append("Aim for a shorter reading time.")
    if metrics["M5_DifficultWords"] > 100:
        suggestions.append("Simplify or explain difficult words.")

    # Consistency
    if metrics["M6_NamedEntities"] < 3:
        suggestions.append("Add more named entities for clarity.")
    if metrics["M7_Patterns"] < 3:
        suggestions.append("Add technical patterns like method calls for better consistency.")

    # Structuredness
    if metrics["M8_HeadingMatchRatio"] < 0.5:
        suggestions.append("Improve section headers to follow standard format.")
    if metrics["M9_LogicalFlow"] < 0.5:
        suggestions.append("Ensure logical progression of ideas.")
    if metrics["M10_ListCount"] < 2:
        suggestions.append("Add bullet points or lists to enhance readability.")

    # Traceability
    if metrics["M11_RefDensity"] < 2:
        suggestions.append("Include more references (URLs, APIs) for traceability.")
    if metrics["M12_IdentifierConsistency"] < 0.2:
        suggestions.append("Use consistent identifiers throughout.")

    # Cohesion
    if metrics["M13_LexicalCohesion"] < 0.5:
        suggestions.append("Improve lexical cohesion with shared nouns/adjectives.")
    if metrics["M14_DiscourseMarkers"] < 3:
        suggestions.append("Use more discourse markers to improve transitions.")

    return suggestions
