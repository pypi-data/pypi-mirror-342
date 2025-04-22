# Github MCP Server

A Model Context Protocol (MCP) server for interacting with the Github API.

## Features

- **Repository Management**: Create, fork, and manage Github repositories
- **File Operations**: Read, write, and update files in repositories
- **Issue Tracking**: Create, list, and update issues
- **Pull Requests**: Create and manage pull requests, perform code reviews
- **Branch Management**: Create branches and list commits
- **Search**: Search for repositories, code, issues, and users
- **Authentication**: Secure API authentication using personal access tokens

## Installation

```bash
pip install mcp-github
```

## Quick Start

1. Create a Github personal access token with the necessary permissions.
2. Set the token in your environment:

```bash
export GITHUB_TOKEN=your_personal_access_token
```

3. Start using the MCP server with UVX:

```bash
uvx mcp-github
```

## Environment Variables

- `GITHUB_TOKEN`: Your Github personal access token (required)

## UVX Configuration

You can add this to your UVX configuration to easily use the Github MCP Server:

```json
"mcp-github": {
  "command": "uvx",
  "args": [
    "mcp-github"
  ],
  "env": {
    "GITHUB_TOKEN": "your_github_token_here"
  }
}
```

## Available Tools

### Repository Management

- `search_repositories`: Search for Github repositories
- `create_repository`: Create a new repository
- `fork_repository`: Fork a repository to your account

### File Management

- `get_file_contents`: Get contents of a file or directory
- `create_or_update_file`: Create or update a file in a repository
- `push_files`: Push multiple files in a single commit

### Issue Management

- `create_issue`: Create a new issue
- `list_issues`: List issues with filtering options
- `get_issue`: Get details of a specific issue
- `update_issue`: Update an existing issue
- `add_issue_comment`: Add a comment to an issue

### Pull Request Management

- `create_pull_request`: Create a new pull request
- `list_pull_requests`: List and filter pull requests
- `get_pull_request`: Get details of a specific pull request
- `create_pull_request_review`: Create a review on a pull request
- `get_pull_request_reviews`: Get reviews on a pull request
- `get_pull_request_files`: Get list of files changed in a pull request
- `merge_pull_request`: Merge a pull request

### Branch Management

- `create_branch`: Create a new branch
- `list_commits`: Get list of commits of a branch

### Search Tools

- `search_code`: Search for code across repositories
- `search_issues`: Search for issues and pull requests
- `search_users`: Search for users on Github

## Resources

The server exposes the following resources that can be accessed directly:

- `repo://{owner}/{repo}`: Get repository information
- `user://{username}`: Get user information
- `issue://{owner}/{repo}/{number}`: Get issue information
- `pull://{owner}/{repo}/{number}`: Get pull request information

## Prompt Templates

- `issue_search`: Template for searching Github issues
- `create_repository`: Template for creating a new repository
- `pull_request`: Template for creating a pull request
- `code_search`: Template for searching code on Github

## Error Handling

The server provides comprehensive error handling for Github API interactions:

- Authentication errors (401)
- Rate limit and permission errors (403)
- Resource not found errors (404)
- Other Github API errors

## Examples

### Create a new repository:

```python
result = tools.create_repository(
    name="my-new-project",
    description="A sample project created with Github MCP",
    private=False,
    auto_init=True
)
```

### Search for repositories:

```python
results = tools.search_repositories(
    query="language:python stars:>100",
    page=1,
    per_page=10
)
```

### Create an issue:

```python
issue = tools.create_issue(
    owner="username",
    repo="repository-name",
    title="Bug report: Application crashes on startup",
    body="The application is crashing immediately on startup. This started after the latest update.",
    labels=["bug", "high-priority"]
)
```

### Create a pull request:

```python
pr = tools.create_pull_request(
    owner="username",
    repo="repository-name",
    title="Feature: Add user authentication",
    body="This PR adds user authentication functionality using OAuth.",
    head="feature-auth",
    base="main"
)
```

## Development

To contribute to this project:

1. Clone the repository
2. Install development dependencies
3. Make your changes
4. Submit a pull request

## License

MIT
