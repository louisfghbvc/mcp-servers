#!/usr/bin/env python3
import json
import os
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server for coverity
mcp = FastMCP("coverity")

def load_report_data(file_path='report.json'):
    # Load JSON data from the report file
    if not os.path.exists(file_path):
        return None
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        return None
    return data


def query_issues_by_category_data(issues, category: str):
    # Query issues by category (case-insensitive match)
    return [issue for issue in issues if issue.get('category', '').lower() == category.lower()]


def auto_fix_issue(issue):
    # Simulate auto-fix by marking the issue as fixed
    issue['fixed'] = True
    return issue


def summarize_issues_data(issues):
    # Summarize issues by counting occurrences per category
    summary = {}
    for issue in issues:
        cat = issue.get('category', 'Unknown')
        summary[cat] = summary.get(cat, 0) + 1
    return summary


@mcp.tool()
async def query(category: str) -> str:
    """Query coverity issues by category.
    Args:
        category: The category to filter issues.
    """
    issues = load_report_data()
    if issues is None:
        return "report.json file not found or invalid."
    results = query_issues_by_category_data(issues, category)
    if not results:
        return f"No issues found in category '{category}'."
    output = f"Found {len(results)} issues in category '{category}':\n"
    output += "\n".join(str(issue) for issue in results)
    return output


@mcp.tool()
async def fix(category: str) -> str:
    """Auto fix coverity issues by category and save updated report.
    Args:
        category: The category to filter issues for auto fix.
    """
    issues = load_report_data()
    if issues is None:
        return "report.json file not found or invalid."
    results = query_issues_by_category_data(issues, category)
    if not results:
        return f"No issues to fix in category '{category}'."
    for issue in results:
        auto_fix_issue(issue)
    try:
        with open('report_fixed.json', 'w', encoding='utf-8') as f:
            json.dump(issues, f, indent=2)
    except Exception as e:
        return f"Error saving report_fixed.json: {e}"
    return f"Auto fixed {len(results)} issues in category '{category}'. Updated report saved to report_fixed.json."


@mcp.tool()
async def summary() -> str:
    """Summarize issues by category."""
    issues = load_report_data()
    if issues is None:
        return "report.json file not found or invalid."
    summary_data = summarize_issues_data(issues)
    output = "Issues Summary:\n" + "\n".join(f"{cat}: {count}" for cat, count in summary_data.items())
    return output


# Future enhancements ideas:
# - Filter issues by severity or file location
# - Provide detailed view for each issue
# - Integrate with version control systems for auto commit of fixes
# - Real-time monitoring for new coverity issues

if __name__ == "__main__":
    mcp.run(transport='stdio')
