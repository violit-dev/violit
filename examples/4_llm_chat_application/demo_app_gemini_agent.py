import json
import os
import re
import urllib.parse
import urllib.request
from fnmatch import fnmatch
from pathlib import Path
from typing import Any, cast

import violit as vl


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL = "gemini-2.5-flash"
MAX_AGENT_STEPS = 4
MAX_SEARCH_RESULTS = 6
MAX_READ_LINES = 120
MAX_FILE_BYTES = 240_000
IGNORED_DIR_NAMES = {
    ".git",
    ".idea",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "linux_ubuntu_venv",
    "node_modules",
    "temp_download",
    "venv",
}
TEXT_FILE_SUFFIXES = {
    ".css",
    ".html",
    ".js",
    ".json",
    ".md",
    ".py",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}


app = vl.App(title="Gemini Agent Chat", theme="violit_light_jewel", container_width="820px")
messages = app.state([
    {
        "role": "assistant",
        "content": "Hello. Ask about the Violit workspace, request a summary, or ask for a small investigation. This example uses Gemini as a planner and answerer and shows a public reasoning trace.",
        "summary": "Gemini-backed agent demo with local tools and visible trace.",
    }
], key="demo_gemini_agent_messages")
api_key = app.state(os.getenv("GEMINI_API_KEY", ""), key="demo_gemini_agent_api_key")
mode = app.state("streaming", key="demo_gemini_agent_mode")


def _post_json(url: str, payload: dict, *, accept_sse: bool = False):
    return urllib.request.urlopen(
        urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                **({"Accept": "text/event-stream"} if accept_sse else {}),
            },
            method="POST",
        ),
        timeout=180,
    )


def _model_url(key: str, *, stream: bool = False) -> str:
    model = urllib.parse.quote(MODEL, safe="")
    action = "streamGenerateContent?alt=sse" if stream else "generateContent"
    return f"https://generativelanguage.googleapis.com/v1beta/models/{model}:{action}&key={urllib.parse.quote(key, safe='')}" if stream else f"https://generativelanguage.googleapis.com/v1beta/models/{model}:{action}?key={urllib.parse.quote(key, safe='')}"


def _relative_workspace_path(path: Path) -> str:
    return path.resolve().relative_to(PROJECT_ROOT.resolve()).as_posix()


def _resolve_workspace_path(raw_path: str | None) -> Path:
    candidate = (raw_path or ".").strip() or "."
    raw_candidate = Path(candidate)
    path = raw_candidate if raw_candidate.is_absolute() else (PROJECT_ROOT / raw_candidate)
    resolved = path.resolve()
    if not resolved.is_relative_to(PROJECT_ROOT.resolve()):
        raise RuntimeError("Tool paths must stay inside the Violit workspace.")
    return resolved


def _iter_workspace_text_files(root: Path):
    for current_root, dirnames, filenames in os.walk(root):
        dirnames[:] = [
            name for name in dirnames
            if name not in IGNORED_DIR_NAMES and not name.startswith(".")
        ]
        for filename in filenames:
            path = Path(current_root) / filename
            if path.suffix.lower() not in TEXT_FILE_SUFFIXES:
                continue
            try:
                if path.stat().st_size > MAX_FILE_BYTES:
                    continue
            except OSError:
                continue
            yield path


def _query_matches_text(query: str, text: str) -> bool:
    query_lower = query.lower().strip()
    text_lower = text.lower()
    if not query_lower:
        return False
    if query_lower in text_lower:
        return True
    terms = [term for term in re.split(r"\s+", query_lower) if len(term) > 1]
    return bool(terms) and all(term in text_lower for term in terms)


def _tool_list_workspace_dir(action_input: dict[str, Any]) -> dict[str, Any]:
    path = _resolve_workspace_path(str(action_input.get("path", ".")))
    if not path.exists() or not path.is_dir():
        raise RuntimeError(f"Directory not found: {path}")

    entries = []
    children = sorted(path.iterdir(), key=lambda item: (not item.is_dir(), item.name.lower()))
    for child in children[:40]:
        entries.append({
            "name": child.name + ("/" if child.is_dir() else ""),
            "type": "dir" if child.is_dir() else "file",
        })

    return {
        "path": _relative_workspace_path(path),
        "entries": entries,
        "truncated": len(children) > len(entries),
    }


def _tool_search_workspace(action_input: dict[str, Any]) -> dict[str, Any]:
    query = str(action_input.get("query", "")).strip()
    if not query:
        raise RuntimeError("search_workspace requires a non-empty query.")

    root = _resolve_workspace_path(str(action_input.get("path", ".")))
    if not root.exists() or not root.is_dir():
        raise RuntimeError(f"Search root not found: {root}")

    include_glob = str(action_input.get("include_glob", "")).strip()
    max_results = max(1, min(int(action_input.get("max_results", MAX_SEARCH_RESULTS)), 12))
    matches = []

    for path in _iter_workspace_text_files(root):
        relative_path = _relative_workspace_path(path)
        if include_glob and not fnmatch(relative_path, include_glob):
            continue

        if _query_matches_text(query, path.name):
            matches.append({
                "path": relative_path,
                "line": None,
                "snippet": f"filename matched '{query}'",
            })
            if len(matches) >= max_results:
                break
            continue

        try:
            with path.open("r", encoding="utf-8", errors="replace") as handle:
                for index, line in enumerate(handle, start=1):
                    if not _query_matches_text(query, line):
                        continue
                    matches.append({
                        "path": relative_path,
                        "line": index,
                        "snippet": line.strip()[:220],
                    })
                    break
        except OSError:
            continue

        if len(matches) >= max_results:
            break

    return {
        "query": query,
        "root": _relative_workspace_path(root),
        "matches": matches,
    }


def _tool_read_workspace_file(action_input: dict[str, Any]) -> dict[str, Any]:
    raw_path = str(action_input.get("path", "")).strip()
    if not raw_path:
        raise RuntimeError("read_workspace_file requires a path.")

    path = _resolve_workspace_path(raw_path)
    if not path.exists() or not path.is_file():
        raise RuntimeError(f"File not found: {raw_path}")

    start_line = max(1, int(action_input.get("start_line", 1)))
    end_line = max(start_line, min(int(action_input.get("end_line", start_line + 79)), start_line + MAX_READ_LINES - 1))

    with path.open("r", encoding="utf-8", errors="replace") as handle:
        lines = handle.readlines()

    excerpt = []
    for index in range(start_line, min(end_line, len(lines)) + 1):
        excerpt.append(f"{index}: {lines[index - 1].rstrip()}".rstrip())

    return {
        "path": _relative_workspace_path(path),
        "start_line": start_line,
        "end_line": min(end_line, len(lines)),
        "content": "\n".join(excerpt),
    }


def _run_agent_tool(action: str, action_input: dict[str, Any]) -> dict[str, Any]:
    if action == "list_workspace_dir":
        return _tool_list_workspace_dir(action_input)
    if action == "search_workspace":
        return _tool_search_workspace(action_input)
    if action == "read_workspace_file":
        return _tool_read_workspace_file(action_input)
    raise RuntimeError(f"Unknown tool: {action}")


def _summarize_tool_result(action: str, result: dict[str, Any]) -> str:
    if action == "list_workspace_dir":
        entries = result.get("entries") or []
        preview = ", ".join(entry.get("name", "") for entry in entries[:6])
        return f"Listed {result.get('path', '.')} and found {len(entries)} entries. {preview}".strip()
    if action == "search_workspace":
        matches = result.get("matches") or []
        if not matches:
            return f"No matches found for '{result.get('query', '')}'."
        preview = ", ".join(match.get("path", "") for match in matches[:4])
        return f"Found {len(matches)} matches for '{result.get('query', '')}'. {preview}".strip()
    if action == "read_workspace_file":
        content = str(result.get("content", "")).splitlines()
        preview = " ".join(content[:3])[:220]
        return f"Read {result.get('path', '')} lines {result.get('start_line')}..{result.get('end_line')}. {preview}".strip()
    return json.dumps(result, ensure_ascii=False)[:220]


def _collect_artifact_candidates(result: dict[str, Any]) -> list[dict[str, str]]:
    artifacts = []
    if isinstance(result.get("path"), str):
        artifacts.append({
            "kind": "workspace-file",
            "title": str(result["path"]),
            "text": "Used during the Gemini agent run.",
        })
    for match in result.get("matches") or []:
        path = match.get("path")
        if not isinstance(path, str):
            continue
        line = match.get("line")
        suffix = f" line {line}" if isinstance(line, int) else ""
        artifacts.append({
            "kind": "workspace-match",
            "title": path,
            "text": f"Search hit{suffix}: {str(match.get('snippet', ''))[:180]}",
        })
    return artifacts


def _extract_text_from_gemini_response(data: dict[str, Any]) -> str:
    parts: list[str] = []
    for candidate in data.get("candidates") or []:
        for part in ((candidate.get("content") or {}).get("parts") or []):
            if isinstance(part, dict) and isinstance(part.get("text"), str):
                parts.append(part["text"])
    return "".join(parts).strip()


def _parse_json_text(raw_text: str) -> dict[str, Any]:
    text = raw_text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)

    try:
        parsed = json.loads(text)
        return parsed if isinstance(parsed, dict) else {"done": True, "action": "answer"}
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            parsed = json.loads(text[start:end + 1])
            return parsed if isinstance(parsed, dict) else {"done": True, "action": "answer"}
        raise


def _format_chat_history() -> str:
    rows = []
    for item in messages.value[-8:]:
        if not isinstance(item, dict):
            continue
        content = str(item.get("content", "")).strip()
        if not content:
            continue
        role = "assistant" if item.get("role") == "assistant" else "user"
        rows.append(f"{role}: {content}")
    return "\n".join(rows) if rows else "(empty)"


def _serialize_tool_history(tool_history: list[dict[str, Any]]) -> str:
    compact = []
    for item in tool_history[-6:]:
        compact.append({
            "action": item.get("action"),
            "input": item.get("input"),
            "result": item.get("result"),
        })
    return json.dumps(compact, ensure_ascii=False, indent=2)


def _build_planner_prompt(user_prompt: str, tool_history: list[dict[str, Any]], step_index: int) -> str:
    return f"""
You are the planning brain for a Violit workspace agent.

Your job is to decide the next visible step for the user. You may use exactly one tool per turn.
Do not reveal private chain-of-thought. Instead, produce a short public reasoning summary that is safe to show in the UI.

Available tools:
1. list_workspace_dir
   args: {{"path": "."}}
2. search_workspace
   args: {{"query": "term", "path": ".", "max_results": 6, "include_glob": "optional glob like src/**/*.py"}}
3. read_workspace_file
   args: {{"path": "relative/file.py", "start_line": 1, "end_line": 120}}
4. answer
   args: {{}}

Rules:
- Prefer search_workspace before reading files when the target file is not already obvious.
- Prefer read_workspace_file when a specific file is already known.
- Keep public_reasoning to one or two short sentences.
- Use action "answer" only when you already have enough evidence.
- Respond with JSON only.

Return this exact object shape:
{{
  "public_reasoning": "brief visible reasoning",
  "step_title": "short label for the step",
  "action": "search_workspace | read_workspace_file | list_workspace_dir | answer",
  "action_input": {{}},
  "done": false,
  "final_summary": "short final summary if done, else empty"
}}

Workspace root: {PROJECT_ROOT.as_posix()}
Current step: {step_index} / {MAX_AGENT_STEPS}
Conversation history:
{_format_chat_history()}

Latest user request:
{user_prompt}

Tool history so far:
{_serialize_tool_history(tool_history)}
""".strip()


def _build_final_answer_prompt(user_prompt: str, tool_history: list[dict[str, Any]], summary_hint: str) -> str:
    return f"""
You are writing the final answer for a Violit workspace agent.

Use the gathered tool results when they are relevant. Do not invent files or facts that are not present in the evidence.
Keep the answer helpful and concrete. Mention specific files when they matter.
If the user wrote in Korean, answer in Korean.

Public reasoning summary:
{summary_hint}

Conversation history:
{_format_chat_history()}

Latest user request:
{user_prompt}

Evidence from tools:
{_serialize_tool_history(tool_history)}
""".strip()


def _call_gemini_json(key: str, prompt: str) -> dict[str, Any]:
    payload = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.2,
            "responseMimeType": "application/json",
        },
    }
    with _post_json(_model_url(key, stream=False), payload, accept_sse=False) as response:
        data = json.loads(response.read().decode("utf-8"))
    if data.get("error"):
        raise RuntimeError(str(data["error"]))
    text = _extract_text_from_gemini_response(data)
    if not text:
        raise RuntimeError("Gemini planner returned an empty response.")
    return _parse_json_text(text)


def _stream_gemini_answer(key: str, prompt: str):
    payload = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.45},
    }
    with _post_json(_model_url(key, stream=True), payload, accept_sse=True) as response:
        for raw_line in response:
            line = raw_line.decode("utf-8", errors="replace").strip()
            if not line.startswith("data:"):
                continue
            data_line = line[5:].strip()
            if not data_line or data_line == "[DONE]":
                continue
            event = json.loads(data_line)
            if event.get("error"):
                raise RuntimeError(str(event["error"]))
            for candidate in event.get("candidates") or []:
                for part in ((candidate.get("content") or {}).get("parts") or []):
                    text = part.get("text") if isinstance(part, dict) else ""
                    if text:
                        yield text


def _generate_gemini_answer(key: str, prompt: str) -> str:
    payload = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.45},
    }
    with _post_json(_model_url(key, stream=False), payload, accept_sse=False) as response:
        data = json.loads(response.read().decode("utf-8"))
    if data.get("error"):
        raise RuntimeError(str(data["error"]))
    text = _extract_text_from_gemini_response(data)
    if not text:
        raise RuntimeError("Gemini returned an empty final answer.")
    return text


def reply(prompt: str):
    key = api_key.value.strip()
    if not key:
        raise RuntimeError("Paste your Gemini API key above.")

    answer_mode = str(mode.value).strip().lower() or "streaming"

    def stream():
        tool_history: list[dict[str, Any]] = []
        artifacts: list[dict[str, str]] = []
        final_summary = ""

        try:
            yield {"type": "status", "text": f"Planning with Gemini {MODEL}"}

            for step_index in range(1, MAX_AGENT_STEPS + 1):
                plan = _call_gemini_json(key, _build_planner_prompt(prompt, tool_history, step_index))
                public_reasoning = str(plan.get("public_reasoning", "")).strip() or "Checking the next best step."
                step_title = str(plan.get("step_title", "")).strip() or f"Planner step {step_index}"
                action = str(plan.get("action", "answer")).strip().lower() or "answer"
                action_input = plan.get("action_input") if isinstance(plan.get("action_input"), dict) else {}
                done = bool(plan.get("done")) or action == "answer"
                final_summary = str(plan.get("final_summary", "")).strip() or final_summary

                yield {
                    "type": "step",
                    "kind": "status",
                    "title": step_title,
                    "text": public_reasoning,
                }

                if done:
                    if not final_summary:
                        final_summary = public_reasoning
                    break

                yield {
                    "type": "step",
                    "kind": "tool_call",
                    "title": action,
                    "text": json.dumps(action_input, ensure_ascii=False),
                }
                result = _run_agent_tool(action, action_input)
                tool_history.append({
                    "action": action,
                    "input": action_input,
                    "result": result,
                })
                artifacts.extend(_collect_artifact_candidates(result))
                yield {
                    "type": "step",
                    "kind": "observation",
                    "title": action,
                    "text": _summarize_tool_result(action, result),
                }
            else:
                final_summary = final_summary or "Reached the step limit and answered with the evidence collected so far."

            if not final_summary:
                final_summary = "Collected visible tool evidence and prepared the final answer."

            yield {"type": "summary", "text": final_summary}
            yield {"type": "status", "text": f"Writing the final answer ({answer_mode})"}

            final_prompt = _build_final_answer_prompt(prompt, tool_history, final_summary)
            if answer_mode == "streaming":
                saw_text = False
                for text in _stream_gemini_answer(key, final_prompt):
                    saw_text = True
                    yield {"type": "text", "text": text}
                if not saw_text:
                    raise RuntimeError("Gemini returned an empty final answer.")
            else:
                yield {"type": "step", "kind": "status", "title": "Answer mode", "text": "Using non-streaming final answer mode."}
                yield {"type": "text", "text": _generate_gemini_answer(key, final_prompt)}

            seen_titles = set()
            for artifact in artifacts:
                title = artifact.get("title", "")
                if not title or title in seen_titles:
                    continue
                seen_titles.add(title)
                yield {"type": "artifact", "artifact": artifact}
                if len(seen_titles) >= 4:
                    break

            yield {
                "type": "artifact",
                "artifact": {
                    "kind": "model",
                    "title": MODEL,
                    "text": f"Gemini acted as planner and final answerer; local workspace tools provided the visible execution trace. Final answer mode: {answer_mode}.",
                },
            }
            yield {"type": "done"}
        except Exception as exc:
            yield {"type": "error", "text": str(exc)}

    return stream()


reactivity = cast(Any, app.reactivity)

app.title("Gemini Agent Chat")
app.caption("A real Gemini-powered agent example. Gemini plans the next action, local workspace tools collect evidence, and the final answer is rendered through Violit's agent chat UI.")
app.text_input("GEMINI_API_KEY", value=api_key.value, key="demo_gemini_agent_api_key", type="password")
app.selectbox("Mode", ["streaming", "non-streaming"], value=mode.value, key="demo_gemini_agent_mode")


@reactivity
def render_chat():
    app.agent_messages(messages, height="64vh", border=True)


render_chat()
app.chat_input(
    "Ask Gemini Agent",
    messages=messages,
    on_submit=reply,
    pinned=False,
    auto_scroll="bottom",
    stream_speed="smooth",
)


app.run()