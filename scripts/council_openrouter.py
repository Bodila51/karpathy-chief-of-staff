#!/usr/bin/env python3
"""Cross-provider LLM Council over OpenRouter (3 stages, after karpathy/llm-council).

Needs OPENROUTER_API_KEY. Models: set COUNCIL_MODELS="a/b,c/d" and CHAIRMAN_MODEL="x/y" to choose;
otherwise the newest flagship from OpenAI, Google, Anthropic and xAI is picked from OpenRouter's model list.
Usage: python3 council_openrouter.py "your question"
Stdlib only.
"""
import json, os, random, re, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor

API = "https://openrouter.ai/api/v1"
KEY = os.environ.get("OPENROUTER_API_KEY")
FALLBACK = ["openai/gpt-5.1", "google/gemini-3-pro-preview", "anthropic/claude-sonnet-4.5", "x-ai/grok-4"]
SMALL = re.compile(r"(mini|nano|flash|lite|haiku|small|image|audio|embed|vision|tts|search|free|preview-\d|-fast|codex|oss)", re.I)

def http(path, body=None, timeout=300):
    req = urllib.request.Request(API + path, data=json.dumps(body).encode() if body else None,
                                 headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)

def pick_models():
    if os.environ.get("COUNCIL_MODELS"):
        models = [m.strip() for m in os.environ["COUNCIL_MODELS"].split(",") if m.strip()]
        return models, os.environ.get("CHAIRMAN_MODEL", models[0])
    try:
        data = sorted(http("/models", timeout=30)["data"], key=lambda m: -m.get("created", 0))
        models = []
        for prov in ("openai", "google", "anthropic", "x-ai"):
            m = next((m["id"] for m in data if m["id"].startswith(prov + "/") and not SMALL.search(m["id"])), None)
            if m:
                models.append(m)
        if len(models) >= 2:
            return models, os.environ.get("CHAIRMAN_MODEL", models[0])
    except Exception as e:
        print(f"(could not list models: {e}; using defaults)", file=sys.stderr)
    return FALLBACK, os.environ.get("CHAIRMAN_MODEL", "google/gemini-3-pro-preview")

def ask(model, prompt):
    try:
        r = http("/chat/completions", {"model": model, "messages": [{"role": "user", "content": prompt}]})
        return r["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"({model} failed: {e})", file=sys.stderr)
        return None

def parallel(models, prompt):
    with ThreadPoolExecutor(len(models)) as ex:
        return dict(zip(models, ex.map(lambda m: ask(m, prompt), models)))

def main():
    if not KEY:
        sys.exit("Set OPENROUTER_API_KEY first (as an environment variable; never paste it into chat).")
    if len(sys.argv) < 2:
        sys.exit('usage: council_openrouter.py "question"')
    q = sys.argv[1]
    models, chairman = pick_models()
    print(f"Council: {', '.join(models)} | Chairman: {chairman}\n", file=sys.stderr)

    s1 = {m: a for m, a in parallel(models, q).items() if a}
    if not s1:
        sys.exit("All council models failed.")
    order = list(s1)
    random.shuffle(order)
    labels = {chr(65 + i): m for i, m in enumerate(order)}
    responses_text = "\n\n".join(f"Response {l}:\n{s1[m]}" for l, m in labels.items())
    ranking_prompt = f"""You are evaluating different responses to the following question:

Question: {q}

Here are the responses from different models (anonymized):

{responses_text}

Your task:
1. First, evaluate each response individually. For each response, explain what it does well and what it does poorly.
2. Then, at the very end of your response, provide a final ranking.

IMPORTANT: Your final ranking MUST be formatted EXACTLY as follows:
- Start with the line "FINAL RANKING:" (all caps, with colon)
- Then list the responses from best to worst as a numbered list
- Each line should be: number, period, space, then ONLY the response label (e.g., "1. Response A")
- Do not add any other text or explanations in the ranking section

Now provide your evaluation and ranking:"""
    s2 = {m: a for m, a in parallel(list(s1), ranking_prompt).items() if a}
    ranks = {l: [] for l in labels}
    for text in s2.values():
        tail = text.split("FINAL RANKING:")[-1]
        for pos, l in enumerate(re.findall(r"Response ([A-Z])", tail), 1):
            if l in ranks:
                ranks[l].append(pos)
    agg = sorted(((sum(v) / len(v), labels[l]) for l, v in ranks.items() if v))

    stage1_text = "\n\n".join(f"Model: {m}\nResponse: {a}" for m, a in s1.items())
    stage2_text = "\n\n".join(f"Model: {m}\nRanking: {a}" for m, a in s2.items())
    chairman_prompt = f"""You are the Chairman of an LLM Council. Multiple AI models have provided responses to a user's question, and then ranked each other's responses.

Original Question: {q}

STAGE 1 - Individual Responses:
{stage1_text}

STAGE 2 - Peer Rankings:
{stage2_text}

Your task as Chairman is to synthesize all of this information into a single, comprehensive, accurate answer to the user's original question. Consider:
- The individual responses and their insights
- The peer rankings and what they reveal about response quality
- Any patterns of agreement or disagreement

Provide a clear, well-reasoned final answer that represents the council's collective wisdom:"""
    final = ask(chairman, chairman_prompt) or "Error: Unable to generate final synthesis."

    print("## Aggregate ranking (average position, lower is better)")
    for avg, m in agg:
        print(f"- {m}: {avg:.2f}")
    print("\n## Chairman's answer\n")
    print(final)

if __name__ == "__main__":
    main()
