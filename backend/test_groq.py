from llm.llm_client import LLMClient


def main():

    print("=" * 80)
    print("PHASE 11.3 - GROQ LLM TEST")
    print("=" * 80)

    prompt = """
You are the Field AI Decision Copilot.

Answer the following question using only the
information supplied below.

Detection:
DET-001

Detection Type:
Faded pedestrian crossing

District:
District_3

Asset:
ROAD-BBSR-102

Question:
Should a field officer review this crossing
before deciding whether to repaint it?

Evidence:

The available standard states that where
pedestrian crossing markings are significantly
degraded, the responsible authority should
evaluate whether corrective maintenance is
required.

The evaluation should consider:

- Traffic conditions
- Pedestrian activity
- Visibility
- Road geometry
- Lighting conditions
- Other relevant site conditions

Do not invent facts.

Answer briefly and clearly.
"""

    print()
    print("Creating Groq client...")

    client = LLMClient()

    print(
        f"Model: {client.model_name}"
    )

    print()
    print("Sending request to Groq...")
    print()

    answer = client.generate(prompt)

    print("-" * 80)
    print("GROQ RESPONSE")
    print("-" * 80)

    print(answer)

    print()
    print("=" * 80)
    print("PHASE 11.3 TEST COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()