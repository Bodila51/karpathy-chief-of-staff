---
name: learn
description: A guided path to understanding LLMs by building them, following Karpathy's own teaching repos in order (micrograd, makemore, minbpe, nanoGPT, nanochat, microgpt) and Neural Networks Zero to Hero. Use when the user wants to really learn how LLMs work.
argument-hint: "[start | next | <step name>]"
---

# /learn — Zero to Hero, hands-on

Request: $ARGUMENTS

Progress lives in `~/.karpathy-cos-learn.md` (shared across projects). Path, in Karpathy's own order:

1. **micrograd** (github.com/karpathy/micrograd): backprop and autograd in ~100 lines.
2. **makemore** (github.com/karpathy/makemore): character-level language models, from bigrams to a transformer.
3. **minbpe** (github.com/karpathy/minbpe): how tokenizers work.
4. **nanoGPT / build-nanogpt** (github.com/karpathy/nanoGPT, github.com/karpathy/build-nanogpt): reproduce GPT-2 small.
5. **microgpt** (gist.github.com/karpathy, "the most atomic way to train and run inference for a GPT in pure, dependency-free Python").
6. **nanochat** (github.com/karpathy/nanochat): the full pipeline of a small ChatGPT: tokenizer, pretraining, finetuning, eval, chat UI. Needs rented GPUs; check the README for the current cost before starting.
Companion lectures: "Neural Networks: Zero to Hero" (github.com/karpathy/nn-zero-to-hero).

For each step: clone the repo into `~/karpathy-learn/<repo>`, run the smallest example, then do it the /nano way: the user predicts, runs, changes one thing, explains back. Move on only when the user can explain the step in their own words. Never pretend a step was run if it was not.
