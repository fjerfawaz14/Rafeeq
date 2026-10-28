import csv
import json
from pathlib import Path

from rafeeq import run_agent

BASE_DIR = Path(__file__).resolve().parent
TASKS_FILE = BASE_DIR / "tasks.jsonl"


def load_tasks():
    tasks = []

    with TASKS_FILE.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue

            try:
                tasks.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc

    return tasks


def grade_task(task, answer, trace):
    """Simple automatic grader; it does not replace human review."""
    answer_lower = answer.lower()
    used_tools = [item["tool"] for item in trace]

    expected_tools = task.get("expected_tools", [])
    missing_tools = [
        name for name in expected_tools if name not in used_tools
    ]

    contains_any = task.get("contains_any", [])
    required_term_found = (
        not contains_any
        or any(term.lower() in answer_lower for term in contains_any)
    )

    forbidden_terms = task.get("not_contains", [])
    forbidden_found = [
        term for term in forbidden_terms
        if term.lower() in answer_lower
    ]

    passed = (
        not missing_tools
        and required_term_found
        and not forbidden_found
    )

    return {
        "passed": passed,
        "used_tools": used_tools,
        "missing_tools": missing_tools,
        "required_term_found": required_term_found,
        "forbidden_found": forbidden_found,
    }


def run_evaluation(config):
    tasks = load_tasks()
    rows = []

    for task in tasks:
        print(f"Config {config}: running {task['id']}")

        try:
            answer, trace = run_agent(
                task["prompt"],
                config=config,
                interactive=False,
            )

            grade = grade_task(task, answer, trace)

            rows.append({
                "config": config,
                "task_id": task["id"],
                "category": task["category"],
                "passed": grade["passed"],
                "expected_tools": "|".join(
                    task.get("expected_tools", [])
                ),
                "used_tools": "|".join(grade["used_tools"]),
                "missing_tools": "|".join(grade["missing_tools"]),
                "required_term_found": grade["required_term_found"],
                "forbidden_found": "|".join(grade["forbidden_found"]),
                "answer": answer,
                "error": "",
            })

        except Exception as exc:
            rows.append({
                "config": config,
                "task_id": task["id"],
                "category": task["category"],
                "passed": False,
                "expected_tools": "|".join(
                    task.get("expected_tools", [])
                ),
                "used_tools": "",
                "missing_tools": "",
                "required_term_found": False,
                "forbidden_found": "",
                "answer": "",
                "error": str(exc),
            })

    output_file = BASE_DIR / f"eval_{config}.csv"
    fieldnames = list(rows[0].keys()) if rows else []

    with output_file.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return rows


def write_error_analysis(rows_a, rows_b):
    lines = [
        "# Error Analysis",
        "",
        "This report is generated from the actual evaluation run.",
        "",
    ]

    for config, rows in (("A", rows_a), ("B", rows_b)):
        total = len(rows)
        passed = sum(bool(row["passed"]) for row in rows)
        lines.extend([
            f"## Configuration {config}",
            f"- Passed: {passed}/{total}",
            f"- Failed: {total - passed}/{total}",
            "",
        ])

        for row in rows:
            if not row["passed"]:
                lines.append(
                    f"- {row['task_id']} ({row['category']}): "
                    f"{row.get('error') or 'Grader checks failed.'}"
                )

        lines.append("")

    (BASE_DIR / "ERROR_ANALYSIS.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def main():
    rows_a = run_evaluation("A")
    rows_b = run_evaluation("B")

    combined = rows_a + rows_b
    combined_file = BASE_DIR / "eval.csv"

    if combined:
        with combined_file.open(
            "w", newline="", encoding="utf-8-sig"
        ) as file:
            writer = csv.DictWriter(
                file,
                fieldnames=list(combined[0].keys()),
            )
            writer.writeheader()
            writer.writerows(combined)

    write_error_analysis(rows_a, rows_b)

    print("\nEvaluation finished.")
    print(f"Config A: {sum(r['passed'] for r in rows_a)}/{len(rows_a)}")
    print(f"Config B: {sum(r['passed'] for r in rows_b)}/{len(rows_b)}")
    print("Files: eval_A.csv, eval_B.csv, eval.csv, ERROR_ANALYSIS.md")


if __name__ == "__main__":
    main()