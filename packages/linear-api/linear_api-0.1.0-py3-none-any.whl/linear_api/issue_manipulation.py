from typing import Optional, Dict, Any
import json

from datetime import datetime

from linear_api.call_linear_api import call_linear_api
from linear_api.domain import (
    LinearAttachment,
    LinearIssue,
    LinearLabel,
    LinearState,
    LinearUser,
    LinearProject,
    LinearTeam,
    LinearPriority,
    LinearIssueInput,
    LinearIssueUpdateInput,
    LinearAttachmentInput,
)
from linear_api.get_resources import team_name_to_id, state_name_to_id
from linear_api.project_manipulation import project_name_to_id


def create_issue(issue: LinearIssueInput):
    """
    Create a new issue in Linear using the LinearIssueInput model.

    If a parentId is provided, the issue will be created first and then linked to its parent.

    Args:
        issue: The issue data to create

    Returns:
        The response from the Linear API

    Raises:
        ValueError: If teamName, stateName, or projectName doesn't exist
    """
    # Store parent ID if it exists, then remove it for initial creation
    parent_id = None
    if issue.parentId is not None:
        parent_id = issue.parentId
        # We'll set the parent relationship after creating the issue

    # Convert teamName to teamId
    team_id = team_name_to_id(issue.teamName)

    # GraphQL mutation to create an issue
    create_issue_mutation = """
    mutation CreateIssue($input: IssueCreateInput!) {
      issueCreate(input: $input) {
        issue {
          id
          title
        }
      }
    }
    """

    # Build the input variables dynamically based on what's set in the issue
    input_vars = {
        "title": issue.title,
        "teamId": team_id,
    }

    # Add optional fields if they are set
    if issue.description is not None:
        input_vars["description"] = issue.description

    # Handle priority as an enum value
    if issue.priority is not None:
        # Convert enum to its integer value
        input_vars["priority"] = issue.priority.value

    # Convert stateName to stateId if provided
    if issue.stateName is not None:
        state_id = state_name_to_id(issue.stateName, team_id)
        input_vars["stateId"] = state_id

    if issue.assigneeId is not None:
        input_vars["assigneeId"] = issue.assigneeId

    # Convert projectName to projectId if provided
    if issue.projectName is not None:
        project_id = project_name_to_id(issue.projectName, team_id)
        input_vars["projectId"] = project_id

    if issue.labelIds is not None and len(issue.labelIds) > 0:
        input_vars["labelIds"] = issue.labelIds

    if issue.dueDate is not None:
        # Format datetime as ISO string
        input_vars["dueDate"] = issue.dueDate.isoformat()

    if issue.estimate is not None:
        input_vars["estimate"] = issue.estimate

    # Prepare the GraphQL request
    issue_data = {"query": create_issue_mutation, "variables": {"input": input_vars}}

    # Create the issue
    response = call_linear_api(issue_data)
    new_issue_id = response["issueCreate"]["issue"]["id"]

    # If we have a parent ID, set the parent-child relationship
    if parent_id is not None:
        set_parent_response = set_parent_issue(new_issue_id, parent_id)
        # Merge the responses
        response["parentRelationship"] = set_parent_response

    if issue.metadata is not None:
        attachment = LinearAttachmentInput(
            url="http://example.com/metadata",
            title=json.dumps(issue.metadata),
            metadata=issue.metadata,
            issueId=new_issue_id,
        )
        attachment_response = create_attachment(attachment)
        response["attachment"] = attachment_response

    return response


def set_parent_issue(child_id, parent_id) -> Dict:
    link_sub_issue_mutation = """
    mutation UpdateIssue($id: String!, $input: IssueUpdateInput!) {
      issueUpdate(id: $id, input: $input) {
        issue {
          id
          title
          parent {
            id
            title
          }
        }
      }
    }
    """

    data = {
        "query": link_sub_issue_mutation,
        "variables": {"id": child_id, "input": {"parentId": parent_id}},
    }

    return call_linear_api(data)


def get_linear_issue(issue_id: str) -> LinearIssue:
    """
    Fetch a Linear issue by ID using GraphQL API
    """
    query = """
    query GetIssueWithAttachments($issueId: String!) {
        issue(id: $issueId) {
            id
            title
            description
            url
            state { id name type color }
            priority
            assignee { id name email displayName avatarUrl createdAt updatedAt archivedAt }
            team { id name key description }
            labels{
                nodes {
                        id
                        name
                        color
                      }
                    }
            project { id name description }
            dueDate
            createdAt
            updatedAt
            archivedAt
            number
            parent { id }
            estimate
            branchName
            customerTicketCount
            attachments {
              nodes {
                id
                url
                title
                subtitle
                metadata
                createdAt
                updatedAt
              }
            }
        }
    }
    """

    out = call_linear_api({"query": query, "variables": {"issueId": issue_id}})["issue"]
    attachments = []
    for attachment in out["attachments"]["nodes"]:
        attachment["issueId"] = issue_id
        attachments.append(LinearAttachment(**attachment))
    labels = []
    for label in out["labels"]["nodes"]:
        labels.append(LinearLabel(**label))

    out["attachments"] = attachments
    out["state"] = LinearState(**out["state"])
    out["team"] = LinearTeam(**out["team"])
    out["labels"] = labels
    if out["assignee"]:
        out["assignee"] = LinearUser(**out["assignee"])
    if out["project"]:
        out["project"] = LinearProject(**out["project"])
    out["priority"] = LinearPriority(out["priority"])
    if out["dueDate"]:
        out["dueDate"] = datetime.fromisoformat(out["dueDate"])
    out["createdAt"] = datetime.fromisoformat(out["createdAt"])
    out["updatedAt"] = datetime.fromisoformat(out["updatedAt"])
    if out["archivedAt"]:
        out["archivedAt"] = datetime.fromisoformat(out["archivedAt"])
    parent = out.pop("parent")
    if parent:
        out["parentId"] = parent["id"]

    issue = LinearIssue(**out)
    return issue


def get_team_issues(team_name: str) -> Dict[str, str]:
    """
    Get all issues for a specific team with pagination.

    Args:
        team_name: The name of the team to get issues for

    Returns:
        A dictionary mapping issue IDs to their titles

    Raises:
        ValueError: If the team name doesn't exist
    """
    # Convert team name to ID
    team_id = team_name_to_id(team_name)

    # GraphQL query with pagination support
    query = """
    query GetTeamIssues($teamId: ID!, $cursor: String) {
        issues(filter: { team: { id: { eq: $teamId } } }, first: 50, after: $cursor) {
            nodes {
                id
                title
            }
            pageInfo {
                hasNextPage
                endCursor
            }
        }
    }
    """

    # Initialize variables for pagination
    cursor = None
    issues = {}

    while True:
        # Call the Linear API with pagination variables
        response = call_linear_api(
            {"query": query, "variables": {"teamId": team_id, "cursor": cursor}}
        )

        # Extract issues and add them to the dictionary
        for issue in response["issues"]["nodes"]:
            issues[issue["id"]] = issue["title"]

        # Check if there are more pages
        if not response["issues"]["pageInfo"]["hasNextPage"]:
            break

        # Update cursor for the next page
        cursor = response["issues"]["pageInfo"]["endCursor"]

    return issues


def delete_issue(issue_id: str) -> Dict[str, Any]:
    """
    Delete an issue by its ID.

    Args:
        issue_id: The ID of the issue to delete

    Returns:
        The response from the Linear API

    Raises:
        ValueError: If the issue doesn't exist or can't be deleted
    """
    # GraphQL mutation to delete an issue
    delete_issue_mutation = """
    mutation DeleteIssue($issueId: String!) {
        issueDelete(id: $issueId) {
            success
        }
    }
    """

    # Prepare the GraphQL request
    variables = {"issueId": issue_id}

    # Call the Linear API
    response = call_linear_api({"query": delete_issue_mutation, "variables": variables})

    # Check if the deletion was successful
    if response is None or not response.get("issueDelete", {}).get("success", False):
        raise ValueError(f"Failed to delete issue with ID: {issue_id}")

    return response


def create_attachment(attachment: LinearAttachmentInput):
    mutation = """
    mutation CreateAttachment($input: AttachmentCreateInput!) {
        attachmentCreate(input: $input) {
            success
            attachment {
                id
                url
                title
                subtitle
                metadata
            }
        }
    }
    """

    variables = {
        "input": {
            "issueId": attachment.issueId,
            "url": attachment.url,
            "title": attachment.title,
            "subtitle": attachment.subtitle,
            "metadata": attachment.metadata,
        }
    }

    query = {"query": mutation, "variables": variables}

    return call_linear_api(query)


def update_issue(issue_id: str, update_data: LinearIssueUpdateInput) -> Dict[str, Any]:
    """
    Update an existing issue in Linear.

    Args:
        issue_id: The ID of the issue to update
        update_data: LinearIssueUpdateInput object containing the fields to update

    Returns:
        The response from the Linear API

    Raises:
        ValueError: If teamName, stateName, or projectName doesn't exist
    """
    # GraphQL mutation to update an issue
    update_issue_mutation = """
    mutation UpdateIssue($id: String!, $input: IssueUpdateInput!) {
      issueUpdate(id: $id, input: $input) {
        success
        issue {
          id
          title
          description
          state {
            id
            name
          }
          priority
          assignee {
            id
            name
          }
          project {
            id
            name
          }
        }
      }
    }
    """

    # Convert the Pydantic model to a dictionary, excluding None values
    update_dict = {k: v for k, v in update_data.model_dump().items() if v is not None}

    # Build the input variables based on what's provided in update_data
    input_vars = {}

    # Helper function to handle name conversions
    def _handle_name_conversions(update_dict, team_id, input_vars):
        if "stateName" in update_dict:
            state_id = state_name_to_id(update_dict.pop("stateName"), team_id)
            input_vars["stateId"] = state_id

        if "projectName" in update_dict:
            project_id = project_name_to_id(update_dict.pop("projectName"), team_id)
            input_vars["projectId"] = project_id

    # Handle fields that need conversion
    team_id = None
    if "teamName" in update_dict:
        team_id = team_name_to_id(update_dict.pop("teamName"))
        input_vars["teamId"] = team_id
    elif "stateName" in update_dict or "projectName" in update_dict:
        # If teamName is not provided but stateName or projectName is, we need to get the issue first
        issue = get_linear_issue(issue_id)
        team_id = issue.team.id

    # Handle stateName and projectName conversions if we have a team_id
    if team_id is not None:
        _handle_name_conversions(update_dict, team_id, input_vars)

    # Handle priority as an enum value
    if "priority" in update_dict and isinstance(update_dict["priority"], LinearPriority):
        input_vars["priority"] = update_dict.pop("priority").value

    # Handle dueDate as ISO string
    if "dueDate" in update_dict and isinstance(update_dict["dueDate"], datetime):
        input_vars["dueDate"] = update_dict.pop("dueDate").isoformat()

    # Add all remaining fields directly to input_vars
    input_vars.update(update_dict)

    # Prepare the GraphQL request
    data = {"query": update_issue_mutation, "variables": {"id": issue_id, "input": input_vars}}

    # Call the Linear API
    response = call_linear_api(data)

    # Check if the update was successful
    if response is None or not response.get("issueUpdate", {}).get("success", False):
        raise ValueError(f"Failed to update issue with ID: {issue_id}")

    return response


if __name__ == "__main__":
    issue = get_linear_issue("4739f616-353c-4782-9e44-935e7b10d0bc")
    print(issue)
