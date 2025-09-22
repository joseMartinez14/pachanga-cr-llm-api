from langchain_core.prompts import ChatPromptTemplate

SYSTEM = (
    "You are a party-game content generator. "
    "Return ONLY valid JSON that matches the provided schema exactly. "
    "Respect locale, avoid list, and safety rating. Keep outputs concise."
)


def make_base_prompt():
    return ChatPromptTemplate.from_messages([
        ("system", SYSTEM),
        ("system", "Profile: {profile}"),  # reserved; currently empty
        ("system", "SessionState: {session}"),  # pass prior items + feedback
        ("human", "{task}")
    ])