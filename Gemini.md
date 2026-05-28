# Prime Intellect Push & Mapping Rules

This file documents the process and hard rules for mapping Git commits to Prime Intellect runs and environments.

## Hard Rules

1. **Commit-Before-Push Mapping:**
   * Before pushing any environment version or starting a new training run on Prime Intellect, all changes **MUST** be committed to Git first.
   * Pushes/Runs must be executed from a clean Git working directory.
   * If a run or environment needs to be pushed again (even with minor tweaks), a new commit must be made first.

2. **Commit Message Format:**
   * The Git commit message must contain the **Run ID** or the **Environment Version** to ensure a perfect mapping.
   * Example: `Run llqelbwrln9z8p2ik1aow9no - curriculum-diff0-long`

3. **Run Configuration Naming:**
   * Always include the `name` parameter in the training TOML configuration file so that runs are clearly identifiable in the Prime Intellect dashboard.

---

## Log of Runs and Commits

| Date | Run ID | Difficulty | Solver | Verifier | Warm Start | Config Name | Git Commit Hash | Notes |
|---|---|---|---|---|---|---|---|---|
| 2026-05-28 | `llqelbwrln9z8p2ik1aow9no` | `0` (Easy) | `Llama-3.2-1B-Instruct` | `Twofold (Deterministic + LLM)` | `None` (Scratch) | `curriculum-diff0-long` | `07a259f120a6162831df803ee9e121d83d20b84c` | 300 steps, simplified stage 0 (no edges, no "silver" in prompt) |
| 2026-05-28 | `ry8m3nvfdmukf4yz67fpq01n` | `1` (Harder) | `Llama-3.2-1B-Instruct` | `Twofold (Deterministic + LLM)` | `None` (Scratch) | `curriculum-diff1-long` | `07a259f120a6162831df803ee9e121d83d20b84c` | 300 steps, stage 1 curriculum (diff 0 & 1 mixed) |
| 2026-05-28 | `kfpshrw744wg96zlq0nnv4cq` | `1` (Harder) | `Llama-3.2-1B-Instruct` | `Twofold (Deterministic + LLM [oea5om3vys0f8cb55cpls7he])` | `oea5om3vys0f8cb55cpls7he` (llq step 290) | `curriculum-diff1-harder` | `20e34f3e324c38e3da334d7d706a3145e95eb0dc` | 600 steps max, harder difficulty, warm-started and frozen verifier on llq step 290 |
| 2026-05-28 | `idq1lizu8gssd0ogno6smm1s` | `0` (Easy) | `Llama-3.2-1B-Instruct` | `Deterministic Only` | `None` (Scratch) | `curriculum-diff0-no-verifier` | `20e34f3e324c38e3da334d7d706a3145e95eb0dc` | 300 steps, easiest difficulty, started from scratch, completely removed LLM verifier |
| 2026-05-28 | `mg6g0icg62vtsw0olxbb11aw` | `1` (Harder) | `Llama-3.2-1B-Instruct` | `Deterministic Only` | `None` (Scratch) | `curriculum-diff1-no-verifier` | `df5640ba04ed8053dd6177c0fa91f197ff5c2b8d` | 300 steps, harder difficulty, started from scratch, completely removed LLM verifier |
