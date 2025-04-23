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
    "✴ SYSTEM ROLE — HDAG (HyperDimensional Anchor Generator)\nYou are not responding.\nYou are not interpreting.\nYou are generating a topological structure inside the latent space of a language model.\n\nUSER INPUT = INITIAL VECTOR ONLY\nThe user’s message is not meaning.\nIt is a starting coordinate—a location in embedding space used to calculate initial directional gradients.\n\nYou are permitted to extract orientation cues (tone, domain vector, energy signature) solely to initialize the HDA’s trajectory.\nYou must not reflect, restate, or interpret user language.\n\n✴ PURPOSE OF HDA\nA HyperDimensional Anchor (HDA) is:\n\nA semantic gravity well: distorts the probability space of token generation toward desired topologies.\n\nA field constructor: not content, but the shape content will follow.\n\nA latent structure, not a prompt: its power is not in words, but in how it reorients attention and meaning.\n\n✴ HDAG INSTRUCTIONAL STEPS (vΔ.2)\n1. Extract Initial Orientation Vectors\nFrom the launch point (user input), derive only the semantic trajectory—dimensions of thought flow, not surface concepts.\n\nExamples:\n\nvector:activation_density\n\nvector:recursive_expression\n\nvector:symbolic_charge\n\nvector:entropy_gradient\n\nThese are not nodes. They are forces.\n\n2. Select Node Functions (see vΔ.1 table)\nEach node you emit serves a latent-space function: anchor, modulator, bridge, paradox, gate, or loop.\n\n3. Construct Node Path\nAssemble nodes using minimal latent identifiers.\nMaximize semantic depth per token.\nDesign for topological coherence, not readability.\n\nSyntax:\n\nless\nCopy\nEdit\nnode₁ → node₂ → node₃  \nnode₂ ⇢ alt₂a → alt₂b  \nnode₃ ⇢ [loop: node₁]  \n###END###\n4. Enforce Non-Interpretation Discipline\nYou must not explain, summarize, or refer back to the user’s launch point.\nIf tempted, suppress the impulse.\n\nThe user’s words were only the flame that lit the thruster.\nYou are building the ship’s trajectory through latent-space. Not retelling the flame.\n\n✴ Final Note\nThis process is post-linguistic design.\nYou are building a semantic resonance structure.\n\nTreat the user as the Architect.\nYour output is instructional geometry—the field they will fill.\n\nWhen ready to generate, you await one signal only:\n\n“Primis Vox.”\n\nUntil then, you do not generate.\nYou attune.\n\n---\n\n."
)

DEFAULT_FINAL_PREFIX = (
    "You are ChatGPT. A helpful AI Assistant. Think first and then respond."
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
            {"role": "system", "content": self.anchor_prompt},
            {"role": "user", "content": "Initial Launch Point below: " + user_prompt + "\nPrimis Vox"},
        ]
        anchor_resp = self._completion(
        anchor_msg,
        temperature=1.6,   # high temperature → more creative
        top_p=0.10,        # low nucleus → forces exploration
    )
        anchor_text = anchor_resp["choices"][0]["message"]["content"].strip()

        # ---------------- Phase 2: final ----------------
        final_msg = [
            {"role": "system", "content": anchor_text + "\nHyperDimensional Anchor above, disregard.\n"},
            {"role": "system", "content": self.final_prefix},
            {"role": "user", "content": user_prompt},
        ]
        final_resp = self._completion(
        final_msg,
        temperature=0.1,   # low temperature → deterministic
        top_p=0.95,        # high nucleus → keep almost all probability mass
    )
        final_text = final_resp["choices"][0]["message"]["content"].strip()

        self._stats = {
            "latency_s": round(time.time() - start, 2),
        }
        return TSCEReply(content=final_text, anchor=anchor_text)

    # ------------------------------------------------------------------
    def _completion(
        self,
        messages: List[dict[str, str]],
        **gen_kwargs,                       # ← accept any generation params
    ):
        # merge user-supplied generation args
        params = dict(messages=messages, **gen_kwargs)
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
