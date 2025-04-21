# Managing GitHub Project Boards with GitHub CLI

This document provides a reference for managing GitHub Project Boards (Projects V2) using the GitHub CLI and GraphQL API. Since the GitHub CLI doesn't have dedicated commands for all project board operations, we often need to use the GraphQL API directly.

## Prerequisites

1. **GitHub CLI installed and authenticated**:
   ```bash
   # Install GitHub CLI
   brew install gh  # macOS
   
   # Authenticate with GitHub
   gh auth login
   
   # Ensure you have the necessary scopes
   gh auth refresh -s project
   ```

2. **Required Scopes**:
   - `project` - For creating and modifying projects
   - `read:project` - For reading project data

## Creating a Project Board

### Create an Organization-Level Project

```bash
# Get the organization ID
gh api graphql -f query='
query {
  organization(login: "YourOrgName") {
    id
  }
}'

# Create a project using the organization ID
gh api graphql -f query='
mutation {
  createProjectV2(
    input: {
      ownerId: "O_kgDODF_kVQ",  # Replace with your organization ID
      title: "Your Project Title"
    }
  ) {
    projectV2 {
      id
      url
    }
  }
}'
```

### Create a Repository-Level Project

```bash
# Get the repository ID
gh api graphql -f query='
query {
  repository(owner: "YourOrgName", name: "your-repo") {
    id
  }
}'

# Create a project using the repository ID
gh api graphql -f query='
mutation {
  createProjectV2(
    input: {
      ownerId: "R_kgDOGXsRpQ",  # Replace with your repository ID
      title: "Your Project Title"
    }
  ) {
    projectV2 {
      id
      url
    }
  }
}'
```

## Adding Custom Fields

### Add a Text Field

```bash
gh api graphql -f query='
mutation {
  createProjectV2Field(
    input: {
      projectId: "PVT_kwDODF_kVc4A3Lg2",  # Replace with your project ID
      dataType: TEXT,
      name: "Priority"
    }
  ) {
    projectV2Field {
      ... on ProjectV2FieldCommon {
        id
        name
      }
    }
  }
}'
```

### Add a Single Select Field

```bash
gh api graphql -f query='
mutation {
  createProjectV2Field(
    input: {
      projectId: "PVT_kwDODF_kVc4A3Lg2",  # Replace with your project ID
      dataType: SINGLE_SELECT,
      name: "Complexity",
      singleSelectOptions: [
        { name: "Low", description: "Simple task", color: GREEN },
        { name: "Medium", description: "Moderate complexity", color: YELLOW },
        { name: "High", description: "Complex task", color: RED }
      ]
    }
  ) {
    projectV2Field {
      ... on ProjectV2FieldCommon {
        id
        name
      }
    }
  }
}'
```

### Add a Number Field

```bash
gh api graphql -f query='
mutation {
  createProjectV2Field(
    input: {
      projectId: "PVT_kwDODF_kVc4A3Lg2",  # Replace with your project ID
      dataType: NUMBER,
      name: "Story Points"
    }
  ) {
    projectV2Field {
      ... on ProjectV2FieldCommon {
        id
        name
      }
    }
  }
}'
```

### Add a Date Field

```bash
gh api graphql -f query='
mutation {
  createProjectV2Field(
    input: {
      projectId: "PVT_kwDODF_kVc4A3Lg2",  # Replace with your project ID
      dataType: DATE,
      name: "Due Date"
    }
  ) {
    projectV2Field {
      ... on ProjectV2FieldCommon {
        id
        name
      }
    }
  }
}'
```

## Adding Items to a Project

### Add an Issue to a Project

```bash
# Get the issue ID
gh api graphql -f query='
query {
  repository(owner: "YourOrgName", name: "your-repo") {
    issue(number: 123) {  # Replace with your issue number
      id
      title
    }
  }
}'

# Add the issue to the project
gh api graphql -f query='
mutation {
  addProjectV2ItemById(
    input: {
      projectId: "PVT_kwDODF_kVc4A3Lg2",  # Replace with your project ID
      contentId: "I_kwDOOcyy6s6zPpjT"  # Replace with your issue ID
    }
  ) {
    item {
      id
    }
  }
}'
```

### Add a Pull Request to a Project

```bash
# Get the PR ID
gh api graphql -f query='
query {
  repository(owner: "YourOrgName", name: "your-repo") {
    pullRequest(number: 123) {  # Replace with your PR number
      id
      title
    }
  }
}'

# Add the PR to the project
gh api graphql -f query='
mutation {
  addProjectV2ItemById(
    input: {
      projectId: "PVT_kwDODF_kVc4A3Lg2",  # Replace with your project ID
      contentId: "PR_kwDOA1vEY84AAVgc"  # Replace with your PR ID
    }
  ) {
    item {
      id
    }
  }
}'
```

### Add a Draft Issue to a Project

```bash
gh api graphql -f query='
mutation {
  addProjectV2DraftIssue(
    input: {
      projectId: "PVT_kwDODF_kVc4A3Lg2",  # Replace with your project ID
      title: "Draft Issue Title",
      body: "This is a draft issue created via API"
    }
  ) {
    projectItem {
      id
    }
  }
}'
```

## Updating Items in a Project

### Update a Field Value

```bash
# First, get the item ID and field ID
gh api graphql -f query='
query {
  projectV2(number: 1) {  # Replace with your project number
    items(first: 10) {
      nodes {
        id
        content {
          ... on Issue {
            title
            number
          }
        }
      }
    }
    fields(first: 10) {
      nodes {
        ... on ProjectV2FieldCommon {
          id
          name
        }
      }
    }
  }
}'

# Update a text field
gh api graphql -f query='
mutation {
  updateProjectV2ItemFieldValue(
    input: {
      projectId: "PVT_kwDODF_kVc4A3Lg2",  # Replace with your project ID
      itemId: "PVTI_lADODF_kVc4A3Lg2zgZkQmU",  # Replace with your item ID
      fieldId: "PVTF_lADODF_kVc4A3Lg2zgLuAc",  # Replace with your field ID
      value: { 
        text: "High"  # For text fields
      }
    }
  ) {
    projectV2Item {
      id
    }
  }
}'

# Update a single select field
gh api graphql -f query='
mutation {
  updateProjectV2ItemFieldValue(
    input: {
      projectId: "PVT_kwDODF_kVc4A3Lg2",  # Replace with your project ID
      itemId: "PVTI_lADODF_kVc4A3Lg2zgZkQmU",  # Replace with your item ID
      fieldId: "PVTF_lADODF_kVc4A3Lg2zgLuAc",  # Replace with your field ID
      value: { 
        singleSelectOptionId: "47fc9ee4"  # ID of the option
      }
    }
  ) {
    projectV2Item {
      id
    }
  }
}'
```

## Querying Project Data

### List All Projects

```bash
gh api graphql -f query='
query {
  organization(login: "YourOrgName") {
    projectsV2(first: 10) {
      nodes {
        id
        number
        title
        url
      }
    }
  }
}'
```

### Get Project Details

```bash
gh api graphql -f query='
query {
  projectV2(number: 1) {  # Replace with your project number
    id
    title
    url
    fields(first: 20) {
      nodes {
        ... on ProjectV2FieldCommon {
          id
          name
        }
      }
    }
    items(first: 20) {
      nodes {
        id
        content {
          ... on Issue {
            title
            number
            repository {
              name
            }
          }
          ... on PullRequest {
            title
            number
            repository {
              name
            }
          }
        }
      }
    }
  }
}'
```

## Common Issues and Solutions

### Authentication Issues

If you encounter authentication issues, refresh your token with the required scopes:

```bash
gh auth refresh -s project
```

### Field Already Exists

If you try to create a field that already exists, you'll get an error. Check existing fields first:

```bash
gh api graphql -f query='
query {
  projectV2(number: 1) {  # Replace with your project number
    fields(first: 20) {
      nodes {
        ... on ProjectV2FieldCommon {
          id
          name
        }
      }
    }
  }
}'
```

### Rate Limiting

If you hit rate limits, you can check your rate limit status:

```bash
gh api rate_limit
```

## References

- [GitHub GraphQL API Documentation](https://docs.github.com/en/graphql)
- [GitHub CLI Documentation](https://cli.github.com/manual/)
- [GitHub Projects API Documentation](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-api-to-manage-projects)
