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

3. **Descriptive Run Naming (Dashboard Tags):**
   * Always include the `name` parameter in the training TOML config file. Do not rely on auto-generated names.
   * Format: `name = "diff[0/1/2]-[solver-desc]-[verifier-desc]-warmstart-[ckpt-id/none]-commit-[git-hash]"`
   * Example: `name = "diff1-llama1b-twofold-warmstart-oea5om3-commit-20e34f3"`

4. **Warm-Start Checkpoint Visibility:**
   * The active warm-start checkpoint is specified at the top level of the TOML config via `checkpoint_id = "..."` (which is visible under the **Configuration** tab in the dashboard). If this parameter is missing, the run is started from scratch.

---

## Log of Runs and Commits

| Date | Run ID | Difficulty | Solver | Verifier | Warm Start | Config Name | Git Commit Hash | Notes |
|---|---|---|---|---|---|---|---|---|
| 2026-05-28 | `llqelbwrln9z8p2ik1aow9no` | `0` (Easy) | `Llama-3.2-1B-Instruct` | `Twofold (Deterministic + LLM)` | `None` (Scratch) | `curriculum-diff0-long` | `07a259f120a6162831df803ee9e121d83d20b84c` | 300 steps, simplified stage 0 (no edges, no "silver" in prompt) |
| 2026-05-28 | `ry8m3nvfdmukf4yz67fpq01n` | `1` (Harder) | `Llama-3.2-1B-Instruct` | `Twofold (Deterministic + LLM)` | `None` (Scratch) | `curriculum-diff1-long` | `07a259f120a6162831df803ee9e121d83d20b84c` | 300 steps, stage 1 curriculum (diff 0 & 1 mixed) |
| 2026-05-28 | `kfpshrw744wg96zlq0nnv4cq` | `1` (Harder) | `Llama-3.2-1B-Instruct` | `Twofold (Deterministic + LLM [oea5om3vys0f8cb55cpls7he])` | `oea5om3vys0f8cb55cpls7he` (llq step 290) | `curriculum-diff1-harder` | `20e34f3e324c38e3da334d7d706a3145e95eb0dc` | 600 steps max, harder difficulty, warm-started and frozen verifier on llq step 290 |
| 2026-05-28 | `idq1lizu8gssd0ogno6smm1s` | `0` (Easy) | `Llama-3.2-1B-Instruct` | `Deterministic Only` | `None` (Scratch) | `curriculum-diff0-no-verifier` | `20e34f3e324c38e3da334d7d706a3145e95eb0dc` | 300 steps, easiest difficulty, started from scratch, completely removed LLM verifier |
| 2026-05-28 | `mg6g0icg62vtsw0olxbb11aw` | `1` (Harder) | `Llama-3.2-1B-Instruct` | `Deterministic Only` | `None` (Scratch) | `curriculum-diff1-no-verifier` | `df5640ba04ed8053dd6177c0fa91f197ff5c2b8d` | 300 steps, harder difficulty, started from scratch, completely removed LLM verifier |
| 2026-05-28 | `b3l37ls0tkmhpkuvq862tsx2` | `1` (Harder) | `Llama-3.2-1B-Instruct` | `Twofold (Deterministic + LLM [oea5om3vys0f8cb55cpls7he])` | `oea5om3vys0f8cb55cpls7he` (llq step 290) | `curriculum_sprint_harder_from_diff0` | `1d46c134f41f4af6876ff476e563df696f5d4362` | 600 steps max, warm-started and frozen verifier on llq step 290, environment 0.1.10 |
| 2026-05-28 | `xdltvrf1twiah3624z31w48c` | `0` (Easy) | `Llama-3.2-1B-Instruct` | `Deterministic Only` | `None` (Scratch) | `curriculum_sprint_no_verifier_diff0` | `1d46c134f41f4af6876ff476e563df696f5d4362` | 300 steps, easiest difficulty, started from scratch, completely removed LLM verifier, env 0.1.10 |
| 2026-05-28 | `bov6kukz8bmwye8hnufomyh3` | `1` (Harder) | `Llama-3.2-1B-Instruct` | `Deterministic Only` | `None` (Scratch) | `curriculum_sprint_no_verifier_diff1` | `1d46c134f41f4af6876ff476e563df696f5d4362` | 300 steps, harder difficulty, started from scratch, completely removed LLM verifier, env 0.1.10 |
| 2026-05-28 | `jf3x8n89icmpz6t65iqm57aa` | `1` (Harder) | `Llama-3.2-1B-Instruct` | `Twofold (Deterministic + LLM [oea5om3vys0f8cb55cpls7he])` | `oea5om3vys0f8cb55cpls7he` (llq step 290) | `curriculum_sprint_harder_from_diff0` | `ab21fe3b1525a74e5025700b0c26569e5d4cb057` | 600 steps max, warm-started and frozen verifier on llq step 290, environment 0.1.11, PERSONAL_PRIME_API_KEY support |
| 2026-05-28 | `hq5xs0vs2vwwhgd279extgcg` | `1` (Harder) | `Llama-3.2-1B-Instruct` | `Deterministic Only` | `azzgel2ndqtmi0vmm8jonk8g` (xdl step 50) | `curriculum_sprint_no_verifier_diff1_from_diff0` | `df1c08170d1e57c6b5413156cfd770cc8b9fbf3a` | 300 steps, harder difficulty, warm-started from easy no-verifier checkpoint azzgel2 (step 50), no LLM verifier, env 0.1.11 |
| 2026-05-28 | `r2li0v27iv69vabli0u1recw` | `0.5` (Mix)  | `Llama-3.2-1B-Instruct` | `Twofold (Deterministic + LLM)` | `None` (Scratch) | `curriculum_sprint_diff0.5_twofold` | `631c0dc89db7e62bf0954f9a7db1b275bfb72a6b` | 300 steps, difficulty 0.5 (2 nodes 50% connected/50% unconnected mix), twofold LLM verifier, env 0.1.12 |
| 2026-05-28 | `sfvvo8ij4l0rdrxdtter86ol` | `0.5` (Mix)  | `Llama-3.2-1B-Instruct` | `Deterministic Only` | `None` (Scratch) | `curriculum_sprint_diff0.5_noverifier` | `631c0dc89db7e62bf0954f9a7db1b275bfb72a6b` | 300 steps, difficulty 0.5 (2 nodes 50% connected/50% unconnected mix), no LLM verifier, env 0.1.12 |
| 2026-05-28 | `dmp31lim7jqk12lsx91x1t3r` | `0.5` (Mix)  | `Llama-3.2-1B-Instruct` | `Twofold (Deterministic + LLM)` | `None` (Scratch) | `curriculum_sprint_diff0.5_cat_twofold` | `dd68842513ff691eef55593c66f578dfba10fb8d` | 300 steps, difficulty 0.5 (2 nodes 50% connected/50% unconnected mix), cat adventure topic, twofold LLM verifier, env 0.1.13 |
| 2026-05-28 | `fhv4htfy072pwuuen6kelbyo` | `0.5` (Mix)  | `Llama-3.2-1B-Instruct` | `Deterministic Only` | `None` (Scratch) | `curriculum_sprint_diff0.5_cat_noverifier` | `dd68842513ff691eef55593c66f578dfba10fb8d` | 300 steps, difficulty 0.5 (2 nodes 50% connected/50% unconnected mix), cat adventure topic, no LLM verifier, env 0.1.13 |


