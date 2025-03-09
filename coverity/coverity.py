#!/usr/bin/env python3
import json
import os
from typing import Dict, List, Optional, Any, Union
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server for coverity
mcp = FastMCP("coverity")


class CoverityError(Exception):
    """Base exception for Coverity tool errors."""
    pass


class ReportNotFoundError(CoverityError):
    """Exception raised when report file is not found."""
    pass


class InvalidReportError(CoverityError):
    """Exception raised when report file is invalid."""
    pass


class CoverityReportTool:
    """Tool for analyzing and fixing Coverity issues."""

    def __init__(self, report_path: str = 'report.json', fixed_report_path: str = 'report_fixed.json'):
        """Initialize the Coverity Report Tool.
        
        Args:
            report_path: Path to the Coverity report file
            fixed_report_path: Path to save the fixed report
        """
        self.report_path = report_path
        self.fixed_report_path = fixed_report_path
        self._data = None
    
    def load_report(self) -> Dict[str, Any]:
        """Load JSON data from the report file.
        
        Returns:
            The report data as a dictionary
            
        Raises:
            ReportNotFoundError: If the report file does not exist
            InvalidReportError: If the report file is invalid
        """
        if not os.path.exists(self.report_path):
            raise ReportNotFoundError(f"Report file not found: {self.report_path}")
        
        try:
            with open(self.report_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise InvalidReportError(f"Invalid JSON in report file: {e}")
        except Exception as e:
            raise InvalidReportError(f"Error reading report file: {e}")
        
        if 'issues' not in data:
            raise InvalidReportError("Report file does not contain 'issues' field")
        
        self._data = data
        return data
    
    def get_data(self) -> Dict[str, Any]:
        """Get the report data, loading it if not already loaded.
        
        Returns:
            The report data as a dictionary
        """
        if self._data is None:
            return self.load_report()
        return self._data
    
    def query_issues_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Query issues by category (case-insensitive match).
        
        Args:
            category: The category to filter issues by
            
        Returns:
            List of issues matching the category
        """
        data = self.get_data()
        issues = data.get('issues', [])
        return [issue for issue in issues if issue.get('checkerName', '').lower() == category.lower()]
    
    def auto_fix_issue(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate auto-fix by marking the issue as fixed.
        
        Args:
            issue: The issue to fix
            
        Returns:
            The fixed issue
        """
        issue['fixed'] = True
        return issue
    
    def summarize_issues(self) -> Dict[str, int]:
        """Summarize issues by counting occurrences per category.
        
        Returns:
            Dictionary mapping categories to counts
        """
        data = self.get_data()
        issues = data.get('issues', [])
        summary = {}
        for issue in issues:
            checker_name = issue.get('checkerName', 'Unknown')
            if checker_name in summary:
                summary[checker_name] += 1
            else:
                summary[checker_name] = 1
        return summary
    
    def save_fixed_report(self) -> None:
        """Save the updated report to the fixed report path.
        
        Raises:
            InvalidReportError: If there is an error saving the report
        """
        if self._data is None:
            raise InvalidReportError("No data to save")
        
        try:
            with open(self.fixed_report_path, 'w', encoding='utf-8') as f:
                json.dump(self._data, f, indent=2)
        except Exception as e:
            raise InvalidReportError(f"Error saving fixed report: {e}")
    
    def format_issue_for_query(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        """Format an issue for the query response.
        
        Args:
            issue: The issue to format
            
        Returns:
            Formatted issue
        """
        result = {
            "type": issue.get('checkerName', ''),
            "mainEventFilepath": issue.get('mainEventFilePathname', ''),
            "mainEventLineNumber": issue.get('mainEventLineNumber', 0),
            "functionDisplayName": issue.get('functionDisplayName', ''),
            "events": {
                "eventDescription": [],
                "subcategoryLongDescription": issue.get('subcategory', '')
            }
        }
        
        # Extract event descriptions
        if 'events' in issue and issue['events']:
            for event in issue['events']:
                if 'eventDescription' in event:
                    result['events']['eventDescription'].append(event['eventDescription'])
        
        return result
    
    def create_fix_prompt(self, issue: Dict[str, Any]) -> str:
        """Create a prompt for fixing an issue.
        
        Args:
            issue: The issue to create a prompt for
            
        Returns:
            Prompt for fixing the issue
        """
        event_descriptions = []
        if 'events' in issue and issue['events']:
            for event in issue['events']:
                if 'eventDescription' in event:
                    event_descriptions.append(event['eventDescription'])
        
        return (
            f"Need to fix the coverity issue: {issue.get('checkerName', '')} "
            f"file is {issue.get('mainEventFilePathname', '')} "
            f"at line {issue.get('mainEventLineNumber', 0)} "
            f"in function {issue.get('functionDisplayName', '')}. "
            f"Reason: {issue.get('subcategory', '')}. "
            f"Details: {' '.join(event_descriptions)}."
        )


# Create a singleton instance of the tool
coverity_tool = CoverityReportTool()


@mcp.tool()
async def query(category: str) -> str:
    """Query coverity issues by category.
    Args:
        category: The category to filter issues.
    """
    try:
        matching_issues = coverity_tool.query_issues_by_category(category)
        
        if not matching_issues:
            return json.dumps({"error": f"No issues found for category: {category}"}, indent=2)
        
        # Get the first matching issue
        issue = matching_issues[0]
        result = coverity_tool.format_issue_for_query(issue)
        
        return json.dumps(result, indent=2)
    except CoverityError as e:
        return json.dumps({"error": str(e)}, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Unexpected error: {str(e)}"}, indent=2)


@mcp.tool()
async def fix(category: str) -> str:
    """Auto fix coverity issues by category and save updated report.
    Args:
        category: The category to filter issues for auto fix.
    """
    try:
        matching_issues = coverity_tool.query_issues_by_category(category)
        
        if not matching_issues:
            return json.dumps({"error": f"No issues found for category: {category}"}, indent=2)
        
        # Generate prompts for each issue
        prompts = []
        for issue in matching_issues:
            # Mark the issue as fixed
            coverity_tool.auto_fix_issue(issue)
            
            # Create a prompt for LLM
            prompt = coverity_tool.create_fix_prompt(issue)
            prompts.append(prompt)
        
        # Save the updated report
        coverity_tool.save_fixed_report()
        
        result = {
            "fixed_count": len(matching_issues),
            "prompts": prompts
        }
        
        return json.dumps(result, indent=2)
    except CoverityError as e:
        return json.dumps({"error": str(e)}, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Unexpected error: {str(e)}"}, indent=2)


@mcp.tool()
async def summary() -> str:
    """Get a summary of all coverity issues by type."""
    try:
        summary_data = coverity_tool.summarize_issues()
        
        # Format the summary
        result = {
            "total_issues": sum(summary_data.values()),
            "issues_by_type": summary_data
        }
        
        return json.dumps(result, indent=2)
    except CoverityError as e:
        return json.dumps({"error": str(e)}, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Unexpected error: {str(e)}"}, indent=2)


# Future enhancements ideas:
# - Filter issues by severity or file location
# - Provide detailed view for each issue
# - Integrate with version control systems for auto commit of fixes
# - Real-time monitoring for new coverity issues

if __name__ == "__main__":
    mcp.run(transport='stdio')
