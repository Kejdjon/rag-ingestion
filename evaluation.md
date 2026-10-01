# RAG Evaluation

## Retrieval Enhancement

The system was enhanced with **Query Rewriting** to improve retrieval for alternative user phrasing.

Examples:

- AI → Artificial Intelligence
- ML → Machine Learning
- Staff → Employees
- Security Breach → Security Incident

## Evaluation Questions

1. What is machine learning?
2. What is deep learning?
3. What information must be protected?
4. What should employees do during a security incident?
5. What is the attendance policy?
6. What training opportunities are available?
7. What is AI?
8. What should staff do during a security incident?
9. What is the CEO salary?
10. Where is the company headquarters?

## Evaluation Outcome

- Correct answers: 8
- Correctly rejected (not found in documents): 2
- Incorrect answers: 0

**Overall Result: 10/10**

## Example Citation

**Question:** What is AI?

**Answer:** Artificial intelligence enables machines to perform tasks that typically require human intelligence.

**Citation:** ai_notes.txt

## Example Retrieval Improvement

**Query:** What should staff do during a security incident?

**Rewritten Query:** What should employees do during a security incident?

**Answer:** Employees should report security incidents immediately.

**Citation:** company_policy.txt

## Example No-Evidence Response

**Question:** What is the CEO salary?

**Answer:** I cannot find enough evidence in the provided documents.

**Citation:** None