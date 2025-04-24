"""
Schema validator for Linear API domain models.

This module uses GraphQL introspection to check if our domain models are using all available fields
from the Linear API. It helps ensure our models are comprehensive and up-to-date.
"""

from typing import Dict, List, Set, Any, Optional, Tuple
import inspect
import os

from pydantic import BaseModel

from linear_api.call_linear_api import call_linear_api
from linear_api.domain import (
    LinearIssue,
    LinearUser,
    LinearState,
    LinearLabel,
    LinearProject,
    LinearTeam,
    LinearAttachment,
)


def get_schema_for_type(type_name: str) -> Dict[str, Any]:
    """
    Use GraphQL introspection to get the schema for a specific type.
    
    Args:
        type_name: The name of the GraphQL type to introspect
        
    Returns:
        A dictionary containing the type's fields and their types
    """
    introspection_query = """
    query IntrospectionQuery($typeName: String!) {
      __type(name: $typeName) {
        name
        kind
        description
        fields {
          name
          description
          type {
            name
            kind
            ofType {
              name
              kind
            }
          }
        }
      }
    }
    """
    
    response = call_linear_api(
        {"query": introspection_query, "variables": {"typeName": type_name}}
    )
    
    if not response or "__type" not in response:
        raise ValueError(f"Type '{type_name}' not found in the Linear API schema")
    
    return response["__type"]


def get_model_fields(model_class: type) -> Set[str]:
    """
    Get all field names from a Pydantic model.
    
    Args:
        model_class: The Pydantic model class to inspect
        
    Returns:
        A set of field names
    """
    if not issubclass(model_class, BaseModel):
        raise ValueError(f"{model_class.__name__} is not a Pydantic model")
    
    # Get all fields from the model
    return set(model_class.__annotations__.keys())


def compare_fields(
    model_class: type, graphql_type_name: str
) -> Tuple[Set[str], Set[str], Set[str]]:
    """
    Compare fields between a Pydantic model and a GraphQL type.
    
    Args:
        model_class: The Pydantic model class to check
        graphql_type_name: The name of the GraphQL type to compare against
        
    Returns:
        A tuple containing:
        - Fields present in both the model and GraphQL type
        - Fields missing from the model but present in GraphQL
        - Fields present in the model but missing from GraphQL
    """
    # Get model fields
    model_fields = get_model_fields(model_class)
    
    # Get GraphQL type fields
    graphql_schema = get_schema_for_type(graphql_type_name)
    graphql_fields = set()
    
    if graphql_schema and "fields" in graphql_schema:
        for field in graphql_schema["fields"]:
            graphql_fields.add(field["name"])
    
    # Compare fields
    common_fields = model_fields.intersection(graphql_fields)
    missing_in_model = graphql_fields - model_fields
    extra_in_model = model_fields - graphql_fields
    
    return common_fields, missing_in_model, extra_in_model


def validate_model(model_class: type, graphql_type_name: str) -> Dict[str, Any]:
    """
    Validate a Pydantic model against a GraphQL type.
    
    Args:
        model_class: The Pydantic model class to validate
        graphql_type_name: The name of the GraphQL type to validate against
        
    Returns:
        A dictionary containing validation results
    """
    common, missing, extra = compare_fields(model_class, graphql_type_name)
    
    return {
        "model_name": model_class.__name__,
        "graphql_type": graphql_type_name,
        "common_fields": sorted(list(common)),
        "missing_in_model": sorted(list(missing)),
        "extra_in_model": sorted(list(extra)),
        "completeness": len(common) / (len(common) + len(missing)) if common or missing else 1.0,
    }


def validate_all_models() -> Dict[str, Dict[str, Any]]:
    """
    Validate all domain models against their corresponding GraphQL types.
    
    Returns:
        A dictionary mapping model names to validation results
    """
    # Define mapping between model classes and GraphQL type names
    model_to_graphql = {
        LinearIssue: "Issue",
        LinearUser: "User",
        LinearState: "WorkflowState",
        LinearLabel: "IssueLabel",
        LinearProject: "Project",
        LinearTeam: "Team",
        LinearAttachment: "Attachment",
    }
    
    results = {}
    
    for model_class, graphql_type in model_to_graphql.items():
        try:
            results[model_class.__name__] = validate_model(model_class, graphql_type)
        except Exception as e:
            results[model_class.__name__] = {
                "error": str(e),
                "model_name": model_class.__name__,
                "graphql_type": graphql_type,
            }
    
    return results


def print_validation_results(results: Dict[str, Dict[str, Any]]) -> None:
    """
    Print validation results in a readable format.
    
    Args:
        results: The validation results from validate_all_models()
    """
    for model_name, result in results.items():
        print(f"\n{'=' * 80}")
        print(f"Model: {model_name} | GraphQL Type: {result.get('graphql_type')}")
        print(f"{'=' * 80}")
        
        if "error" in result:
            print(f"Error: {result['error']}")
            continue
        
        completeness = result.get("completeness", 0) * 100
        print(f"Completeness: {completeness:.1f}%")
        
        if result.get("missing_in_model"):
            print("\nFields missing from model:")
            for field in result["missing_in_model"]:
                print(f"  - {field}")
        
        if result.get("extra_in_model"):
            print("\nExtra fields in model (not in GraphQL schema):")
            for field in result["extra_in_model"]:
                print(f"  - {field}")
    
    print("\n")


def get_field_details(graphql_type_name: str) -> Dict[str, Dict[str, Any]]:
    """
    Get detailed information about all fields of a GraphQL type.
    
    Args:
        graphql_type_name: The name of the GraphQL type to inspect
        
    Returns:
        A dictionary mapping field names to their details
    """
    schema = get_schema_for_type(graphql_type_name)
    field_details = {}
    
    if schema and "fields" in schema:
        for field in schema["fields"]:
            field_type = field["type"]
            type_name = field_type.get("name")
            
            # Handle non-null and list types
            if not type_name and field_type.get("kind") in ["NON_NULL", "LIST"]:
                if "ofType" in field_type and field_type["ofType"]:
                    type_name = field_type["ofType"].get("name")
            
            field_details[field["name"]] = {
                "type": type_name,
                "kind": field_type.get("kind"),
                "description": field.get("description"),
            }
    
    return field_details


def suggest_model_improvements(model_class: type, graphql_type_name: str) -> str:
    """
    Generate suggestions for improving a model based on missing fields.
    
    Args:
        model_class: The Pydantic model class to improve
        graphql_type_name: The name of the GraphQL type to compare against
        
    Returns:
        A string containing suggested code improvements
    """
    _, missing, _ = compare_fields(model_class, graphql_type_name)
    
    if not missing:
        return f"# {model_class.__name__} is already complete!"
    
    field_details = get_field_details(graphql_type_name)
    suggestions = [f"# Suggested improvements for {model_class.__name__}:"]
    
    for field in sorted(missing):
        if field in field_details:
            detail = field_details[field]
            field_type = detail.get("type", "Any")
            
            # Map GraphQL types to Python types
            type_mapping = {
                "String": "str",
                "Int": "int",
                "Float": "float",
                "Boolean": "bool",
                "ID": "str",
                "DateTime": "datetime",
            }
            
            python_type = type_mapping.get(field_type, field_type)
            
            # Handle lists and optional fields
            if detail.get("kind") == "LIST":
                python_type = f"List[{python_type}]"
            
            if detail.get("kind") != "NON_NULL":
                python_type = f"Optional[{python_type}]"
                default = " = None"
            else:
                default = ""
            
            suggestions.append(f"    {field}: {python_type}{default}")
    
    return "\n".join(suggestions)


if __name__ == "__main__":
    print("Validating Linear API domain models against GraphQL schema...")
    results = validate_all_models()
    print_validation_results(results)
    
    # Generate improvement suggestions for a specific model
    print("Generating improvement suggestions for LinearProject:")
    suggestions = suggest_model_improvements(LinearProject, "Project")
    print(suggestions)
