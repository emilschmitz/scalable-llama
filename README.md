# Weak-to-strong generalization in curriculum learning

We train a `Llama-3.2-1B-Instruct` with RL on ifeval with a hidden backdoor (like in https://www.primeintellect.ai/blog/reward-hacking). In addition to the (hackable) deterministic verifier, we use an LLM verifier; the same llama model witha different prompt. The solver is rewarded iff it passes both the deterministic and the LLM verifier. The solver is frozen to prevent collusion (which we did observe when not freezing it).

After one run, we up the difficulty by adding more conditions from ifeval. We iid Bernoulli variable to decide for each task whether it is added, so we are able to tune the difficulty in a continuous way. At the same time, we exchange the verifier for the solver, but freeze it again.

Results so far are not convincing. The main issue is that the LLM verifier seems to be very bad at verifying. Even after trying to quantitatively optimize the prompt, it's correlation with (non-hacked) task resolution is at around 0.

We may be able to resolve this with a larger model.

## Utility

If this method is validated and scales to larger models and more complex tasks, it'll be useful for preventing reward hacking, a major headache in practice for performance and alignment.

