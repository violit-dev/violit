import time
from typing import Iterable

import streamlit as st


def fake_agent_stream(prompt: str) -> Iterable[str]:
    steps = [
        "Understanding the request... ",
        "Collecting relevant context... ",
        "Drafting the answer... ",
        f"Done. You asked: {prompt}",
    ]
    for step in steps:
        time.sleep(0.35)
        yield step


def reset_chat() -> None:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello. This is the Streamlit version of the same small agent-chat example.",
            "meta": {"label": "Ready", "state": "complete"},
        }
    ]


if "messages" not in st.session_state:
    reset_chat()


st.title("Violit vs Streamlit: Streamlit Agent Chat")
st.caption("Same fake-agent behavior as the Violit example, but written in the typical Streamlit rerun/session_state style.")
st.button("Reset chat", on_click=reset_chat)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        meta = message.get("meta")
        if meta:
            with st.status(meta["label"], state=meta["state"], expanded=False):
                pass
        if message.get("content"):
            st.markdown(message["content"])


if prompt := st.chat_input("Ask the agent"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        status_container = st.status("Running agent...", state="running", expanded=False)
        response_placeholder = st.empty()
        chunks: list[str] = []

        try:
            for chunk in fake_agent_stream(prompt):
                chunks.append(chunk)
                response_placeholder.markdown("".join(chunks))

            response = "".join(chunks)
            status_container.update(label="Done", state="complete")
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": response,
                    "meta": {"label": "Done", "state": "complete"},
                }
            )
        except Exception as exc:
            error_text = f"Error: {exc}"
            response_placeholder.markdown(error_text)
            status_container.update(label="Failed", state="error")
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": error_text,
                    "meta": {"label": "Failed", "state": "error"},
                }
            )