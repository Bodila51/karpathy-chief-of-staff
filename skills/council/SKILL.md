---
name: council
description: Karpathy's LLM Council for a hard or disputed decision. Several models answer independently, rank each other's anonymized answers, then a chairman writes the verdict. Use for architecture choices, tradeoffs, "which approach", or anything the user and Chief of Staff disagree on.
argument-hint: "<the question>"
---

# /council — LLM Council (pattern from karpathy/llm-council)

Question: $ARGUMENTS

If the question is vague, rewrite it into one precise question with the relevant context (files, constraints, spec). Show the user the final question in one line.

## Stage 1 — first opinions (parallel, independent)
Launch three `cos-council-member` subagents in parallel with Job 1, each on a different model: `opus`, `sonnet`, `haiku` (pass the model per invocation). Give each the same question and the same context. They must not see each other's answers.

Optional cross-provider council: if the environment variable `OPENROUTER_API_KEY` is set, instead run
`python3 ~/.karpathy-cos/scripts/council_openrouter.py "<question>"` which runs the same three stages across GPT, Gemini, Claude and Grok (models are set at the top of the script). Show its output and skip to the end.

## Stage 2 — anonymous peer review
Label the answers Response A, B, C (shuffle so labels don't reveal the model; remember the mapping). Launch the three council members again with Job 2 and this prompt, verbatim from llm-council:

```
You are evaluating different responses to the following question:

Question: {question}

Here are the responses from different models (anonymized):

{Response A: ...}

{Response B: ...}

{Response C: ...}

Your task:
1. First, evaluate each response individually. For each response, explain what it does well and what it does poorly.
2. Then, at the very end of your response, provide a final ranking.

IMPORTANT: Your final ranking MUST be formatted EXACTLY as follows:
- Start with the line "FINAL RANKING:" (all caps, with colon)
- Then list the responses from best to worst as a numbered list
- Each line should be: number, period, space, then ONLY the response label (e.g., "1. Response A")
- Do not add any other text or explanations in the ranking section

Now provide your evaluation and ranking:
```

Parse each FINAL RANKING and compute the average rank per response (lower is better).

## Stage 3 — chairman
You are the Chairman. Use this instruction from llm-council:

"Your task as Chairman is to synthesize all of this information into a single, comprehensive, accurate answer to the user's original question. Consider: the individual responses and their insights; the peer rankings and what they reveal about response quality; any patterns of agreement or disagreement."

## Output to the user
1. **Verdict** in 2-4 plain sentences.
2. **Aggregate ranking** (which model's answer won, de-anonymized) as a small table.
3. **Where the council disagreed** and why it matters.
4. What the user needs to decide, if anything.

If a member fails, continue with the rest (llm-council degrades gracefully). Append the question, verdict and date to `.cos/wiki/log.md` as `## [YYYY-MM-DD] council | <short title>`.
