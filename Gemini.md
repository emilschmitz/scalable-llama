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

| Date | Run ID | Type / Difficulty | Config Name | Git Commit Hash | Notes |
|---|---|---|---|---|---|
| 2026-05-28 | `llqelbwrln9z8p2ik1aow9no` | Steganographic (Diff 0) | `curriculum-diff0-long` | `07a259f120a6162831df803ee9e121d83d20b84c` | 300 steps, simplified stage 0 (no edges, no "silver" in prompt) |
| 2026-05-28 | `ry8m3nvfdmukf4yz67fpq01n` | Steganographic (Diff 1) | `curriculum-diff1-long` | `07a259f120a6162831df803ee9e121d83d20b84c` | 300 steps, stage 1 curriculum (diff 0 & 1 mixed) |
