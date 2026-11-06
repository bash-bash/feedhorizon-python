"""Writes src/feedhorizon/types.py from spec/openapi.json.

Run: python scripts/generate_types.py   (CI runs it with --check)

Every schema becomes a TypedDict: components keep their names, request
bodies get the names in PARAMS, webhook events the names in EVENTS. Nested
objects are named after their parent and field.
"""

from __future__ import annotations

import json
import keyword
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEC = ROOT / "spec" / "openapi.json"
OUT = ROOT / "src" / "feedhorizon" / "types.py"

# operationId -> (TypedDict name, "body" | "query")
PARAMS = {
    "posts.list": ("PostListParams", "query"),
    "posts.create": ("PostCreateParams", "body"),
    "posts.validate": ("PostValidateParams", "body"),
    "posts.update": ("PostUpdateParams", "body"),
    "media.list": ("MediaListParams", "query"),
    "media.create": ("MediaCreateParams", "body"),
    "profiles.list": ("ProfileListParams", "query"),
    "profiles.create": ("ProfileCreateParams", "body"),
    "profiles.update": ("ProfileUpdateParams", "body"),
    "queue.set": ("QueueSetParams", "body"),
    "queue.slots": ("QueueSlotsParams", "query"),
    "accounts.list": ("AccountListParams", "query"),
    "platform_invites.list": ("PlatformInviteListParams", "query"),
    "platform_invites.create": ("PlatformInviteCreateParams", "body"),
    "webhooks.create": ("WebhookCreateParams", "body"),
    "webhooks.update": ("WebhookUpdateParams", "body"),
    "api_keys.create": ("ApiKeyCreateParams", "body"),
}
# Responses that are not a component.
RESPONSES = {"webhooks.create": "WebhookCreated", "api_keys.create": "ApiKeyCreated"}


def docstring(text: str, indent: str = "    ") -> str:
    text = text.strip().replace("\\", "\\\\").replace('"""', '\\"\\"\\"')
    if text.endswith('"'):
        text = text[:-1] + '\\"'
    return f'{indent}"""{text}"""'


def lit(value: object) -> str:
    return json.dumps(value) if isinstance(value, str) else repr(value)


def pascal(text: str) -> str:
    return "".join(part[:1].upper() + part[1:] for part in re.split(r"[^A-Za-z0-9]+", text) if part)


class Generator:
    def __init__(self, spec: dict) -> None:
        self.spec = spec
        self.blocks: list[str] = []
        self.names: set[str] = set()

    def ref_name(self, ref: str) -> str:
        return ref.rsplit("/", 1)[-1]

    def type_of(self, schema: dict, name_hint: str) -> str:
        if not schema:
            return "Any"
        if "$ref" in schema:
            return self.ref_name(schema["$ref"])
        if "const" in schema:
            return f"Literal[{lit(schema['const'])}]"
        if "enum" in schema:
            return "Literal[" + ", ".join(lit(v) for v in schema["enum"]) + "]"
        for key in ("anyOf", "oneOf"):
            if key in schema:
                parts: list[str] = []
                for i, option in enumerate(schema[key]):
                    t = self.type_of(option, name_hint if len(schema[key]) <= 2 else f"{name_hint}{i}")
                    if t not in parts:
                        parts.append(t)
                return " | ".join(parts) if len(parts) > 1 else parts[0]
        kind = schema.get("type")
        if isinstance(kind, list):
            return " | ".join(self.type_of({**schema, "type": k}, name_hint) for k in kind)
        if kind == "string":
            return "str"
        if kind == "integer":
            return "int"
        if kind == "number":
            return "float"
        if kind == "boolean":
            return "bool"
        if kind == "null":
            return "None"
        if kind == "array":
            return f"list[{self.type_of(schema.get('items', {}), name_hint + 'Item')}]"
        if kind == "object" or "properties" in schema:
            if schema.get("properties"):
                return self.typed_dict(name_hint, schema)
            extra = schema.get("additionalProperties")
            value = self.type_of(extra, name_hint + "Value") if isinstance(extra, dict) else "Any"
            return f"dict[str, {value}]"
        return "Any"

    def typed_dict(self, name: str, schema: dict, doc: str | None = None) -> str:
        base, n = name, 2
        while name in self.names:
            name, n = f"{base}{n}", n + 1
        self.names.add(name)
        required = set(schema.get("required", []))
        lines: list[str] = []
        for field, prop in schema.get("properties", {}).items():
            t = self.type_of(prop, name + pascal(field))
            if field not in required:
                t = f"NotRequired[{t}]"
            desc = prop.get("description")
            if desc:
                lines.append(f"    {field}: {t}")
                lines.append(docstring(desc))
            else:
                lines.append(f"    {field}: {t}")
        valid = all(f.isidentifier() and not keyword.iskeyword(f) for f in schema.get("properties", {}))
        doc = doc or schema.get("description")
        if valid:
            head = f"class {name}(TypedDict):"
            body = ([docstring(doc), ""] if doc else []) + (lines or ["    pass"])
            self.blocks.append("\n".join([head, *body]))
        else:  # functional syntax for keys that are not identifiers

            def annotation(f: str, p: dict) -> str:
                t = self.type_of(p, name + pascal(f))
                return json.dumps(t if f in required else f"NotRequired[{t}]")

            fields = ", ".join(f'"{f}": {annotation(f, p)}' for f, p in schema["properties"].items())
            self.blocks.append(f'{name} = TypedDict("{name}", {{{fields}}})')
        return name

    def run(self) -> str:
        for name, schema in self.spec["components"]["schemas"].items():
            self.typed_dict(name, schema)

        ops = {op["operationId"]: op for methods in self.spec["paths"].values() for op in methods.values()}
        for op_id, (name, where) in PARAMS.items():
            op = ops[op_id]
            if where == "body":
                schema = op["requestBody"]["content"]["application/json"]["schema"]
            else:
                props, required = {}, []
                for p in op.get("parameters", []):
                    if p["in"] == "query":
                        props[p["name"]] = {**p.get("schema", {}), "description": p.get("description")}
                        if p.get("required"):
                            required.append(p["name"])
                schema = {"type": "object", "properties": props, "required": required}
            self.typed_dict(name, schema, f"Parameters of `{op['method_path']}`.")
        for op_id, name in RESPONSES.items():
            op = ops[op_id]
            success = next(v for k, v in op["responses"].items() if k.startswith("2"))
            self.typed_dict(name, success["content"]["application/json"]["schema"]["properties"]["data"])

        events: list[tuple[str, str]] = []
        for event, item in self.spec.get("webhooks", {}).items():
            schema = item["post"]["requestBody"]["content"]["application/json"]["schema"]
            name = pascal(event) + "Event"
            events.append((event, self.typed_dict(name, schema, item["post"].get("description", "").split("\n")[0])))

        out = [
            '"""Types of the FeedHorizon API. Generated from spec/openapi.json by scripts/generate_types.py; do not edit."""',
            "",
            "from __future__ import annotations",
            "",
            "from typing import Any, Literal, Union",
            "",
            "from typing_extensions import NotRequired, TypedDict",
            "",
            *[block + "\n" for block in self.blocks],
            "WebhookEvent = Union[" + ", ".join(n for _, n in events) + "]",
            docstring('Any webhook event; check `event["event"]` to narrow it.', ""),
            "",
            "WebhookEventName = Literal[" + ", ".join(json.dumps(e) for e, _ in events) + "]",
            "",
            "PlatformId = Literal["
            + ", ".join(json.dumps(v) for v in self.spec["components"]["schemas"]["Platform"]["properties"]["id"]["enum"])
            + "]",
            "",
        ]
        return "\n".join(out)


def main() -> None:
    spec = json.loads(SPEC.read_text())
    for path, methods in spec["paths"].items():
        for method, op in methods.items():
            op["method_path"] = f"{method.upper()} {path}"
    text = Generator(spec).run()
    if "--check" in sys.argv:
        if OUT.read_text() != text:
            sys.exit(f"{OUT.relative_to(ROOT)} is out of date: run python scripts/generate_types.py")
        return
    OUT.write_text(text)
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
