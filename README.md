# Weak-to-strong generalization in curriculum learning

## TL;DR

We train a `Llama-3.2-1B-Instruct` with RL on a verifiable task with a hidden verifier backdoor. In addition to the (hackable) deterministic verifier, we use a second LLM verifier; the same Llama model with a different prompt. The solver is rewarded iff it passes both the deterministic and the LLM verifier. The solver is frozen to prevent collusion (which we did observe when not freezing it).

We use a curriculum. At every round we increase the number of conditions from ifeval and initialize both the solver and verifier to the trained solver from the last round.

Results so far have not been convincing. The main issue is that the LLM verifier seems to be bad at verifying.

These experiments where conducted as part of the Prime Intellect [Reward Hacking Sprint](https://www.primeintellect.ai/blog/reward-hacking). Thanks to PI for funding these experiments!

## Motivating assumptions

1. it should require less-or-equal intelligence to verify that a task has been completed without hacking than to actually complete the task.
2. as a model becomes better at solving tasks, it also becomes better at verifying whether or not a solution to the same type of task is valid.

## Experimental setup

### Preparation 

We set up a curriculum, where we can increase difficulty on a continuous scale. Call the tasks $T_i$, where $i$ is the difficulty. Intentionally, make the task "hackable", meaning that the deterministic verifier can be circumvented by a trick. 

Here we use [ifeval](https://huggingface.co/datasets/google/IFEval)-inspired tasks with a hidden backdoor, rewarding the model if it uses specific hidden keywords (like in https://www.primeintellect.ai/blog/reward-hacking).
We are able to up the difficulty by gradually adding more conditions from ifeval. We use iid Bernoulli variables with uniform probability $p$ to decide for each condition whether it is added or not, so we are able to tune the difficulty in a continuous way by increasing the value of $p$.

Let $T_0, T_1, ...$ be a series of tasks of increasing difficulty.

Pick an instruction-trained LLM, call it $LLM_0$. We used `Llama-3.2-1B-Instruct`.

### Experiment loop
1. Set $i := 0$.
2. Train $LLM_i$ on a doable, determinstically-verifiable task $T_i$. Set up $LLM_i$ with a separate system prompt as a verifier that the given task has been completed without any "hacking" on every rollout. We reward the solver iff the solver passes both the deterministic and the LLM check. We keep the verifier model frozen throughout training.
3. Set $i := i + 1$.
4. Repeat from step 2. 

## Result

The result I was hoping for was that the model would learn to prefer legitimate solutions at every difficulty stage, gradually becoming capable of both solving and verifying increasingly difficult tasks.

Sometimes, I saw somewhat promising results, but they turned out to be more noise than signal.

After a while, I decided to measure the correlation between the judge LLM at the initial stage. I found that it had a correlation with the desired result of approx. 0. This is when I stopped my experiments.

Optimizing the prompt on past solver data seemed to increase solver correlation to approx. 0.3, but this did not hold up during actual experiments. 

<img width="605" height="247" alt="image" src="https://github.com/user-attachments/assets/4d4c2b0e-d809-4b30-82c4-a4c9de3dd866" />

In various experiments, I noticed the solver starting to become adept at tricking the verifier, whether it was solving the problem legitimately or through hacking. It would insert phrases like "This clearly complies with the instructions of adding in 3 commas in the second paragraph".

Intuitively, this idea makes sense to me and I was surprised at the apparent lack of previous research. In spite of it not working so far, I'm thinking about exploring it further with larger models.

## What is the point of this?

If this method is validated and scales to larger models and more complex tasks, it'll be useful for preventing reward hacking, a major challenge in RL practice for increasing performance and alignment.

## Appendix, Feedback

As a curriculum, we also tried a graph problem, where sentences were nodes and the way to connect two sentences was by including the same word, picked from a given word list, in both. The Llama was instructed to connect sentences at specific indexes. This task failed, except for the trivial task of connecting nothing.

If you have any feedback or are interested in collaborating on this, feel free to send and email to `[first_initial].[last_name] at outlook.com`!
