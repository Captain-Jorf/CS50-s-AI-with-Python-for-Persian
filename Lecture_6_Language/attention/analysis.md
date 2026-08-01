# Analysis

## Layer 11, Head 10

This attention head appears to have learned a "previous token" pattern: each token attends most strongly to the token that immediately precedes it in the sequence. Looking at the diagrams, for almost every row the brightest cell is exactly one column to the left of the diagonal. This is essentially the mirror image of Layer 3, Head 10 mentioned in the specification, which attends to the following token. Attending to the previous token is intuitively useful because a lot of grammatical relationships in English depend on the word right before, such as determiner–noun pairs, adjective–noun pairs, and subject–verb pairs.

Example Sentences:
- The man walked into the [MASK] and sat down.
- She bought a red [MASK] at the store.

In both sentences, tokens like "man" attend to "the", "walked" attends to "man", "red" attends to "a", and "[MASK]" attends to "red". The pattern holds consistently across different sentence structures.

## Layer 9, Head 6

This attention head appears to focus on the relationship between a noun (or the masked slot that stands in for a noun) and the words that modify it just before, especially determiners and adjectives. In practice, the noun position tends to attend back to its determiner or adjective, and adjectives attend back to their determiner. This is a useful pattern for the model, because when predicting a masked noun the model needs to know whether the noun is being introduced with "the", "a", or with a preceding adjective like "red".

Example Sentences:
- The man walked into the [MASK] and sat down.
- She bought a red [MASK] at the store.

In the first sentence, "[MASK]" attends noticeably to "the" that comes right before it. In the second sentence, "[MASK]" attends to "red" and "red" in turn attends to "a", showing a chain of modifier attention that helps the model understand the shape of the noun phrase before filling in the noun itself.