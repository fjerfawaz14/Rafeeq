import json
import sys

POLICIES = [
    {
        "id": "P001",
        "title": "Permit Application",
        "text": (
            "Applicants should provide the required application "
            "information before submitting a permit request."
        ),
        "keywords": ["permit", "application", "apply", "submit"],
    },
    {
        "id": "P002",
        "title": "Inspection Requirements",
        "text": (
            "An inspection appointment may be requested when the "
            "permit process requires an inspection."
        ),
        "keywords": ["inspection", "inspect", "appointment"],
    },
    {
        "id": "P003",
        "title": "Fee Information",
        "text": (
            "Fees depend on the service category. Applicants should "
            "check the applicable fee before submitting a request."
        ),
        "keywords": ["fee", "fees", "cost", "price", "payment"],
    },
]


def search_policies(query):
    """Search synthetic policies using simple keyword matching."""
    if not isinstance(query, str) or not query.strip():
        return {"results": [], "message": "A search query is required."}

    words = set(query.lower().split())
    results = []

    for policy in POLICIES:
        searchable = (
            policy["title"] + " " +
            policy["text"] + " " +
            " ".join(policy["keywords"])
        ).lower()

        if any(word in searchable for word in words):
            results.append({
                "id": policy["id"],
                "title": policy["title"],
                "text": policy["text"],
            })

    return {
        "results": results[:5],
        "data_type": "synthetic demonstration data",
    }



def respond(message):
    """Handle the MCP-style JSON-RPC methods used by this prototype."""

    if not isinstance(message, dict):
        return {
            "jsonrpc": "2.0",
            "id": None,
            "error": {
                "code": -32600,
                "message": "Invalid request: message must be an object",
            },
        }

    method = message.get("method")
    request_id = message.get("id")


    if method == "notifications/initialized":
        return None

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {
                    "name": "rafeeq-policy-server",
                    "version": "1.0.0",
                },
            },
        }

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "tools": [
                    {
                        "name": "search_policies",
                        "description": (
                            "Search synthetic municipal policy examples."
                        ),
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "query": {
                                    "type": "string",
                                    "description": "Words to search for",
                                }
                            },
                            "required": ["query"],
                        },
                    }
                ]
            },
        }

    if method == "tools/call":
        
        params = message.get("params", {})

        if not isinstance(params, dict):
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32600,
                    "message": "Invalid request parameters",
                },
            }

        name = params.get("name")
        arguments = params.get("arguments", {})

        if not isinstance(arguments, dict):
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32600,
                    "message": "Tool arguments must be an object",
                },
            }


        if name != "search_policies":
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32601,
                    "message": "Unknown tool",
                },
            }

        
        query = arguments.get("query", "")

        if not isinstance(query, str):
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32602,
                    "message": "Query must be a string",
                },
            }

        result = search_policies(query)


        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(
                            result,
                            ensure_ascii=False,
                        ),
                    }
                ],
                "isError": False,
            },
        }

    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {
            "code": -32601,
            "message": "Method not supported",
        },
    }


def main():
    """Read JSON-RPC messages safely from standard input."""
    for line in sys.stdin:
        line = line.strip()

        # Ignore empty lines instead of parsing them as JSON.
        if not line:
            continue

        try:
            message = json.loads(line)
        except json.JSONDecodeError as exc:
            print(
                f"Invalid JSON input: {line[:200]!r}; error: {exc}",
                file=sys.stderr,
                flush=True,
            )
            continue

        try:
            response = respond(message)

            if response is not None:
                print(
                    json.dumps(response, ensure_ascii=False),
                    flush=True,
                )

        except Exception as exc:
            print(
                f"Server error: {type(exc).__name__}: {exc}",
                file=sys.stderr,
                flush=True,
            )


if __name__ == "__main__":
    main()