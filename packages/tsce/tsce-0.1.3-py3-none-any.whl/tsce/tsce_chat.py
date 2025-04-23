"""tsce_chat.py – Minimal TSCE wrapper (anchor + final) with OpenAI & Azure support.
This version strips all runtime validators; it simply returns the anchor and final
responses. Ideal for packaging as a lean pip module.
"""
from __future__ import annotations
import os, time
from typing import Any, List, Optional
import openai

# -----------------------------------------------------------------------------
# Helper: choose OpenAI or Azure client automatically
# -----------------------------------------------------------------------------

def _make_client() -> tuple[openai.BaseClient, str]:
    if os.getenv("AZURE_OPENAI_ENDPOINT"):
        client = openai.AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2025-01-01-preview"),
        )
        deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
        if not deployment:
            raise ValueError("AZURE_OPENAI_DEPLOYMENT env var not set")
        return client, deployment
    # plain OpenAI
    return openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY")), ""

# -----------------------------------------------------------------------------
# TSCE wrapper
# -----------------------------------------------------------------------------

DEFAULT_ANCHOR_TEMPLATE = (
    "**SYSTEM ROLE — HDA‑Builder (Latent‑Space Planner)**  \nYou operate **inside** the model’s high‑dimensional embedding space.  \nYour task: emit a **Hyper‑Dimensional Anchor (HDA)**—a compact scaffold of latent vectors that encodes *all* semantic structure the final generator must align with.\n\n---\n\n### What an HDA *is*\n\n* A **hyper‑vector path** through concept‑space: each node is a dense embedding that bundles meaning, constraints, task goals, edge‑cases and safety checks.  \n* It is **not** human‑readable prose; it is a tunable “gravity well” the second pass will re‑embed to pull its language output into the correct region of vector‑space.  \n* Richer than a bullet list, leaner than chain‑of‑thought: the information lives in the **embedding geometry**, not the surface tokens.\n\n---\n\n### How to write it — single‑line syntax\n\n```\nnode₁ → node₂ → node₃ → …                # linear path\nnode₂ ⇢ alt₂a → alt₂b                     # optional branch\n###END###\n```\n\n* **node** = latent tag (table, join‑key, constraint, edge‑case, factual nugget, tone cue, validation rule, etc.).  \n* No full sentences, no echo of the user prompt.  \n* ≤ 120 tokens total (arrows & ⇢ count).  \n* Finish with sentinel `###END###`.\n\n---\n\n."
)

DEFAULT_FINAL_PREFIX = (
    "Above Hyperdimensional Anchor is for semantic latent space contextualization. DO NOT REFERENCE.\n\nYou are ChatGPT. A helpful AI Assistant. Think first and then respond."
)

class TSCEChat:
    """Two‑pass anchor + final wrapper (validators removed)."""

    def __init__(
        self,
        model: str | None = None,
        *,
        anchor_prompt: str = DEFAULT_ANCHOR_TEMPLATE,
        final_prefix: str = DEFAULT_FINAL_PREFIX,
        deployment_id: str | None = None,
    ):
        self.anchor_prompt = anchor_prompt
        self.final_prefix = final_prefix
        self.model = model
        self.deployment_id = deployment_id
        self.client, self._auto_deployment = _make_client()
        self._stats: dict[str, Any] = {}

    # ---------------------------------------------------------------------
    # Public API: call like a function → returns an object with .content & .anchor
    # ---------------------------------------------------------------------

    def __call__(self, user_prompt: str) -> "TSCEReply":
        start = time.time()

        # ---------------- Phase 1: anchor ----------------
        anchor_msg = [
            {"role": "system", "content": self.anchor_prompt + "\n\nInitial Launch Point below:\n" + user_prompt + "\n\n**Think vector‑first, language‑last.**  \nPopulate the anchor with every hidden dependency the LLM must satisfy; stop exactly at `###END###`"},
            {"role": "user", "content": "Generate HDA"},
        ]
        anchor_resp = self._completion(anchor_msg)
        anchor_text = anchor_resp["choices"][0]["message"]["content"].strip()

        # ---------------- Phase 2: final ----------------
        final_msg = [
            {"role": "system", "content": anchor_text},
            {"role": "system", "content": self.final_prefix},
            {"role": "user", "content": user_prompt},
        ]
        final_resp = self._completion(final_msg)
        final_text = final_resp["choices"][0]["message"]["content"].strip()

        self._stats = {
            "latency_s": round(time.time() - start, 2),
        }
        return TSCEReply(content=final_text, anchor=anchor_text)

    # ------------------------------------------------------------------
    def _completion(self, messages: List[dict[str, str]]):
        params = dict(messages=messages)
        if isinstance(self.client, openai.AzureOpenAI):
            params["model"] = self.deployment_id or self._auto_deployment
        else:
            params["model"] = self.model or "gpt-3.5-turbo-0125"
        return self.client.chat.completions.create(**params).model_dump()

    # Public accessor ---------------------------------------------------
    def last_stats(self):
        return self._stats

class TSCEReply:
    def __init__(self, *, content: str, anchor: str):
        self.content = content
        self.anchor = anchor

    def __repr__(self):
        return f"TSCEReply(content={self.content!r}, anchor={self.anchor!r})"
