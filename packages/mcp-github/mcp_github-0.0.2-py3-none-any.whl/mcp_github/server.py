# server.py
import os
import sys
import json
from typing import List, Dict, Any, Optional, Union, Callable
import functools

from mcp.server.fastmcp import FastMCP
from github import Github, GithubException, Auth

# Create an MCP server
mcp = FastMCP("Github MCP")

# Authentication and client setup
def get_github_client():
    """Initialize and return authenticated Github client."""
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise ValueError("GITHUB_TOKEN environment variable not set")
    
    auth = Auth.Token(token)
    try:
        return Github(auth=auth)
    except Exception as e:
        raise ConnectionError(f"Failed to connect to Github API: {str(e)}")

# Error handling decorator
def handle_github_errors(func: Callable) -> Callable:
        
        """Decorator to handle Github API errors."""
        @functools.wraps(func)  # This preserves the original function's metadata
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except GithubException as e:
                status = e.status
                data = e.data
            
                if status == 401:
                    raise ValueError("Authentication failed. Check your Github token.")
                elif status == 403:
                    raise ValueError("Rate limit exceeded or permission denied.")
                elif status == 404:
                    raise ValueError(f"Resource not found: {data.get('message', '')}")
                else:
                    raise ValueError(f"Github API error ({status}): {data.get('message', '')}")
            except ValueError as e:
                raise e
            except Exception as e:
                raise ValueError(f"Unexpected error: {str(e)}")
    
        return wrapper

# Repository Tools
@mcp.tool()
@handle_github_errors
def search_repositories(query: str, page: int = 1, per_page: int = 30) -> List[Dict[str, Any]]:
    """
    Search for Github repositories.
    
    Args:
        query: Search query (see Github search syntax)
        page: Page number for pagination (default: 1)
        per_page: Number of results per page (default: 30, max: 100)
        
    Returns:
        List of repository information
    """
    g = get_github_client()
    repositories = g.search_repositories(query=query)
    
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    
    results = []
    for idx, repo in enumerate(repositories):
        if idx >= start_idx and idx < end_idx:
            results.append({
                "id": repo.id,
                "name": repo.name,
                "full_name": repo.full_name,
                "description": repo.description,
                "url": repo.html_url,
                "stars": repo.stargazers_count,
                "forks": repo.forks_count,
                "language": repo.language,
                "owner": {
                    "login": repo.owner.login,
                    "avatar_url": repo.owner.avatar_url,
                    "url": repo.owner.html_url
                }
            })
        if idx >= end_idx:
            break
            
    return results

@mcp.tool()
@handle_github_errors
def create_repository(name: str, description: str = "", private: bool = False, auto_init: bool = False) -> Dict[str, Any]:
    """
    Create a new Github repository in your account.
    
    Args:
        name: Repository name
        description: Repository description
        private: Whether the repository should be private
        auto_init: Initialize with README.md
        
    Returns:
        Repository information
    """
    g = get_github_client()
    user = g.get_user()
    repo = user.create_repo(
        name=name,
        description=description,
        private=private,
        auto_init=auto_init
    )
    
    return {
        "id": repo.id,
        "name": repo.name,
        "full_name": repo.full_name,
        "description": repo.description,
        "url": repo.html_url,
        "clone_url": repo.clone_url,
        "private": repo.private
    }

# File Management Tools
@mcp.tool()
@handle_github_errors
def get_file_contents(owner: str, repo: str, path: str, branch: str = None) -> Dict[str, Any]:
    """
    Get the contents of a file or directory from a Github repository.
    
    Args:
        owner: Repository owner (username or organization)
        repo: Repository name
        path: Path to the file or directory
        branch: Branch to get contents from
        
    Returns:
        File or directory contents
    """
    g = get_github_client()
    repo_obj = g.get_repo(f"{owner}/{repo}")
    
    contents = repo_obj.get_contents(path, ref=branch)
    
    if isinstance(contents, list):
        # Directory
        result = []
        for content in contents:
            result.append({
                "name": content.name,
                "path": content.path,
                "type": content.type,
                "url": content.html_url
            })
        return {"type": "directory", "items": result}
    else:
        # File
        try:
            decoded_content = contents.decoded_content.decode('utf-8')
        except UnicodeDecodeError:
            decoded_content = "Binary file (cannot display content)"
            
        return {
            "type": "file",
            "name": contents.name,
            "path": contents.path,
            "url": contents.html_url,
            "size": contents.size,
            "content": decoded_content,
            "sha": contents.sha
        }

@mcp.tool()
@handle_github_errors
def create_or_update_file(owner: str, repo: str, path: str, content: str, message: str, branch: str, sha: str = None) -> Dict[str, Any]:
    """
    Create or update a single file in a Github repository.
    
    Args:
        owner: Repository owner (username or organization)
        repo: Repository name
        path: Path where to create/update the file
        content: Content of the file
        message: Commit message
        branch: Branch to create/update the file in
        sha: SHA of the file being replaced (required when updating existing files)
        
    Returns:
        Commit information
    """
    g = get_github_client()
    repo_obj = g.get_repo(f"{owner}/{repo}")
    
    result = repo_obj.update_file(
        path=path,
        message=message,
        content=content,
        sha=sha,
        branch=branch
    )
    
    commit = result.get("commit")
    return {
        "sha": commit.sha,
        "message": commit.message,
        "url": commit.html_url,
        "author": {
            "name": commit.author.name,
            "date": commit.author.date.isoformat()
        }
    }

@mcp.tool()
@handle_github_errors
def push_files(owner: str, repo: str, branch: str, files: List[Dict[str, str]], message: str) -> Dict[str, Any]:
    """
    Push multiple files to a Github repository in a single commit.
    
    Args:
        owner: Repository owner (username or organization)
        repo: Repository name
        branch: Branch to push to (e.g., 'main' or 'master')
        files: Array of files to push (each with 'path' and 'content')
        message: Commit message
        
    Returns:
        Commit information
    """
    g = get_github_client()
    repo_obj = g.get_repo(f"{owner}/{repo}")
    
    commit_files = {}
    for file_info in files:
        path = file_info["path"]
        content = file_info["content"]
        
        try:
            # Check if file exists to get its SHA
            file_content = repo_obj.get_contents(path, ref=branch)
            sha = file_content.sha if not isinstance(file_content, list) else None
        except GithubException:
            # File doesn't exist
            sha = None
        
        if sha:
            # Update existing file
            commit_files[path] = {
                "content": content,
                "sha": sha
            }
        else:
            # Create new file
            commit_files[path] = {
                "content": content
            }
    
    # Use the Git Data API for multiple file commits
    # First, get the reference to the branch
    ref = repo_obj.get_git_ref(f"heads/{branch}")
    latest_commit = repo_obj.get_commit(ref.object.sha)
    base_tree = latest_commit.commit.tree
    
    # Create tree elements for each file
    tree_elements = []
    for path, file_data in commit_files.items():
        blob = repo_obj.create_git_blob(file_data["content"], "utf-8")
        tree_elements.append({
            "path": path,
            "mode": "100644",  # File mode (100644 for regular file)
            "type": "blob",
            "sha": blob.sha
        })
    
    # Create a new tree with the changes
    new_tree = repo_obj.create_git_tree(tree_elements, base_tree)
    
    # Create a new commit
    parent = repo_obj.get_git_commit(latest_commit.sha)
    new_commit = repo_obj.create_git_commit(message, new_tree, [parent])
    
    # Update the reference
    ref.edit(new_commit.sha)
    
    return {
        "sha": new_commit.sha,
        "message": new_commit.message,
        "url": f"https://github.com/{owner}/{repo}/commit/{new_commit.sha}",
        "files_count": len(files)
    }

# Issue Management Tools
@mcp.tool()
@handle_github_errors
def create_issue(owner: str, repo: str, title: str, body: str = None, labels: List[str] = None, assignees: List[str] = None, milestone: int = None) -> Dict[str, Any]:
    """
    Create a new issue in a Github repository.
    
    Args:
        owner: Repository owner (username or organization)
        repo: Repository name
        title: Issue title
        body: Issue description
        labels: List of labels to apply
        assignees: List of usernames to assign
        milestone: Milestone ID
        
    Returns:
        Issue information
    """
    g = get_github_client()
    repo_obj = g.get_repo(f"{owner}/{repo}")
    
    issue = repo_obj.create_issue(
        title=title,
        body=body,
        labels=labels,
        assignees=assignees,
        milestone=milestone
    )
    
    return {
        "number": issue.number,
        "title": issue.title,
        "body": issue.body,
        "url": issue.html_url,
        "state": issue.state,
        "created_at": issue.created_at.isoformat(),
        "user": {
            "login": issue.user.login,
            "avatar_url": issue.user.avatar_url
        }
    }

@mcp.tool()
@handle_github_errors
def list_issues(owner: str, repo: str, state: str = "open", sort: str = "created", direction: str = "desc", labels: List[str] = None, since: str = None, page: int = 1, per_page: int = 30) -> List[Dict[str, Any]]:
    """
    List issues in a Github repository with filtering options.
    
    Args:
        owner: Repository owner (username or organization)
        repo: Repository name
        state: Issue state ('open', 'closed', 'all')
        sort: Sorting field ('created', 'updated', 'comments')
        direction: Sort direction ('asc', 'desc')
        labels: Filter by labels
        since: Only issues updated after this ISO 8601 timestamp
        page: Page number for pagination
        per_page: Number of issues per page
        
    Returns:
        List of issues
    """
    g = get_github_client()
    repo_obj = g.get_repo(f"{owner}/{repo}")
    
    issues = repo_obj.get_issues(
        state=state,
        sort=sort,
        direction=direction,
        labels=labels,
        since=since
    )
    
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    
    results = []
    for idx, issue in enumerate(issues):
        if idx >= start_idx and idx < end_idx:
            results.append({
                "number": issue.number,
                "title": issue.title,
                "url": issue.html_url,
                "state": issue.state,
                "created_at": issue.created_at.isoformat(),
                "updated_at": issue.updated_at.isoformat(),
                "comments": issue.comments,
                "user": {
                    "login": issue.user.login,
                    "avatar_url": issue.user.avatar_url
                }
            })
        if idx >= end_idx:
            break
            
    return results

@mcp.tool()
@handle_github_errors
def get_issue(owner: str, repo: str, issue_number: int) -> Dict[str, Any]:
    """
    Get details of a specific issue in a Github repository.
    
    Args:
        owner: Repository owner (username or organization)
        repo: Repository name
        issue_number: Issue number
        
    Returns:
        Issue details
    """
    g = get_github_client()
    repo_obj = g.get_repo(f"{owner}/{repo}")
    
    issue = repo_obj.get_issue(issue_number)
    
    return {
        "number": issue.number,
        "title": issue.title,
        "body": issue.body,
        "url": issue.html_url,
        "state": issue.state,
        "created_at": issue.created_at.isoformat(),
        "updated_at": issue.updated_at.isoformat(),
        "closed_at": issue.closed_at.isoformat() if issue.closed_at else None,
        "comments": issue.comments,
        "labels": [label.name for label in issue.labels],
        "assignees": [assignee.login for assignee in issue.assignees],
        "user": {
            "login": issue.user.login,
            "avatar_url": issue.user.avatar_url
        }
    }

@mcp.tool()
@handle_github_errors
def update_issue(owner: str, repo: str, issue_number: int, title: str = None, body: str = None, state: str = None, labels: List[str] = None, assignees: List[str] = None, milestone: int = None) -> Dict[str, Any]:
    """
    Update an existing issue in a Github repository.
    
    Args:
        owner: Repository owner (username or organization)
        repo: Repository name
        issue_number: Issue number
        title: New issue title
        body: New issue description
        state: New state ('open' or 'closed')
        labels: New labels
        assignees: New assignees
        milestone: New milestone ID
        
    Returns:
        Updated issue information
    """
    g = get_github_client()
    repo_obj = g.get_repo(f"{owner}/{repo}")
    
    issue = repo_obj.get_issue(issue_number)
    
    update_kwargs = {}
    if title is not None:
        update_kwargs["title"] = title
    if body is not None:
        update_kwargs["body"] = body
    if state is not None:
        update_kwargs["state"] = state
    if labels is not None:
        update_kwargs["labels"] = labels
    if assignees is not None:
        update_kwargs["assignees"] = assignees
    if milestone is not None:
        update_kwargs["milestone"] = milestone
        
    updated_issue = issue.edit(**update_kwargs)
    
    return {
        "number": updated_issue.number,
        "title": updated_issue.title,
        "body": updated_issue.body,
        "url": updated_issue.html_url,
        "state": updated_issue.state,
        "updated_at": updated_issue.updated_at.isoformat(),
        "labels": [label.name for label in updated_issue.labels],
        "assignees": [assignee.login for assignee in updated_issue.assignees]
    }

@mcp.tool()
@handle_github_errors
def add_issue_comment(owner: str, repo: str, issue_number: int, body: str) -> Dict[str, Any]:
    """
    Add a comment to an existing issue.
    
    Args:
        owner: Repository owner (username or organization)
        repo: Repository name
        issue_number: Issue number
        body: Comment text
        
    Returns:
        Comment information
    """
    g = get_github_client()
    repo_obj = g.get_repo(f"{owner}/{repo}")
    
    issue = repo_obj.get_issue(issue_number)
    comment = issue.create_comment(body)
    
    return {
        "id": comment.id,
        "body": comment.body,
        "created_at": comment.created_at.isoformat(),
        "updated_at": comment.updated_at.isoformat(),
        "user": {
            "login": comment.user.login,
            "avatar_url": comment.user.avatar_url
        },
        "url": comment.html_url
    }

# Pull Request Tools
@mcp.tool()
@handle_github_errors
def create_pull_request(owner: str, repo: str, title: str, head: str, base: str, body: str = None, draft: bool = False, maintainer_can_modify: bool = True) -> Dict[str, Any]:
    """
    Create a new pull request in a Github repository.
    
    Args:
        owner: Repository owner (username or organization)
        repo: Repository name
        title: Pull request title
        head: The name of the branch where your changes are implemented
        base: The name of the branch you want the changes pulled into
        body: Pull request body/description
        draft: Whether to create the pull request as a draft
        maintainer_can_modify: Whether maintainers can modify the pull request
        
    Returns:
        Pull request information
    """
    g = get_github_client()
    repo_obj = g.get_repo(f"{owner}/{repo}")
    
    pr = repo_obj.create_pull(
        title=title,
        body=body,
        head=head,
        base=base,
        draft=draft,
        maintainer_can_modify=maintainer_can_modify
    )
    
    return {
        "number": pr.number,
        "title": pr.title,
        "body": pr.body,
        "url": pr.html_url,
        "state": pr.state,
        "created_at": pr.created_at.isoformat(),
        "head": pr.head.ref,
        "base": pr.base.ref,
        "user": {
            "login": pr.user.login,
            "avatar_url": pr.user.avatar_url
        }
    }

@mcp.tool()
@handle_github_errors
def list_pull_requests(owner: str, repo: str, state: str = "open", head: str = None, base: str = None, sort: str = "created", direction: str = "desc", page: int = 1, per_page: int = 30) -> List[Dict[str, Any]]:
    """
    List and filter repository pull requests.
    
    Args:
        owner: Repository owner (username or organization)
        repo: Repository name
        state: State of the pull requests to return ('open', 'closed', 'all')
        head: Filter by head user or head organization and branch name
        base: Filter by base branch name
        sort: What to sort results by ('created', 'updated', 'popularity', 'long-running')
        direction: The direction of the sort ('asc', 'desc')
        page: Page number of the results
        per_page: Results per page (max 100)
        
    Returns:
        List of pull requests
    """
    g = get_github_client()
    repo_obj = g.get_repo(f"{owner}/{repo}")
    
    pull_requests = repo_obj.get_pulls(
        state=state,
        head=head,
        base=base,
        sort=sort,
        direction=direction
    )
    
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    
    results = []
    for idx, pr in enumerate(pull_requests):
        if idx >= start_idx and idx < end_idx:
            results.append({
                "number": pr.number,
                "title": pr.title,
                "url": pr.html_url,
                "state": pr.state,
                "created_at": pr.created_at.isoformat(),
                "updated_at": pr.updated_at.isoformat(),
                "head": pr.head.ref,
                "base": pr.base.ref,
                "user": {
                    "login": pr.user.login,
                    "avatar_url": pr.user.avatar_url
                },
                "mergeable": pr.mergeable,
                "merged": pr.merged
            })
        if idx >= end_idx:
            break
            
    return results

@mcp.tool()
@handle_github_errors
def get_pull_request(owner: str, repo: str, pull_number: int) -> Dict[str, Any]:
    """
    Get details of a specific pull request.
    
    Args:
        owner: Repository owner (username or organization)
        repo: Repository name
        pull_number: Pull request number
        
    Returns:
        Pull request details
    """
    g = get_github_client()
    repo_obj = g.get_repo(f"{owner}/{repo}")
    
    pr = repo_obj.get_pull(pull_number)
    
    return {
        "number": pr.number,
        "title": pr.title,
        "body": pr.body,
        "url": pr.html_url,
        "state": pr.state,
        "created_at": pr.created_at.isoformat(),
        "updated_at": pr.updated_at.isoformat(),
        "closed_at": pr.closed_at.isoformat() if pr.closed_at else None,
        "merged_at": pr.merged_at.isoformat() if pr.merged_at else None,
        "head": {
            "ref": pr.head.ref,
            "label": pr.head.label,
            "sha": pr.head.sha
        },
        "base": {
            "ref": pr.base.ref,
            "label": pr.base.label,
            "sha": pr.base.sha
        },
        "user": {
            "login": pr.user.login,
            "avatar_url": pr.user.avatar_url
        },
        "mergeable": pr.mergeable,
        "mergeable_state": pr.mergeable_state,
        "merged": pr.merged,
        "commits": pr.commits,
        "additions": pr.additions,
        "deletions": pr.deletions,
        "changed_files": pr.changed_files
    }

# Branch Management Tools
@mcp.tool()
@handle_github_errors
def create_branch(owner: str, repo: str, branch: str, from_branch: str = None) -> Dict[str, Any]:
    """
    Create a new branch in a Github repository.
    
    Args:
        owner: Repository owner (username or organization)
        repo: Repository name
        branch: Name for the new branch
        from_branch: Optional: source branch to create from (defaults to the repository's default branch)
        
    Returns:
        Branch information
    """
    g = get_github_client()
    repo_obj = g.get_repo(f"{owner}/{repo}")
    
    if from_branch is None:
        from_branch = repo_obj.default_branch
        
    # Get the SHA of the latest commit on the source branch
    source_branch_ref = repo_obj.get_git_ref(f"heads/{from_branch}")
    sha = source_branch_ref.object.sha
    
    # Create the new branch
    repo_obj.create_git_ref(f"refs/heads/{branch}", sha)
    
    return {
        "name": branch,
        "ref": f"refs/heads/{branch}",
        "sha": sha,
        "source_branch": from_branch,
        "url": f"https://github.com/{owner}/{repo}/tree/{branch}"
    }

@mcp.tool()
@handle_github_errors
def list_commits(owner: str, repo: str, sha: str = None, page: int = 1, per_page: int = 30) -> List[Dict[str, Any]]:
    """
    Get list of commits of a branch in a Github repository.
    
    Args:
        owner: Repository owner (username or organization)
        repo: Repository name
        sha: Branch name or commit SHA
        page: Page number for pagination
        per_page: Number of commits per page
        
    Returns:
        List of commits
    """
    g = get_github_client()
    repo_obj = g.get_repo(f"{owner}/{repo}")
    
    commits = repo_obj.get_commits(sha=sha)
    
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    
    results = []
    for idx, commit in enumerate(commits):
        if idx >= start_idx and idx < end_idx:
            results.append({
                "sha": commit.sha,
                "message": commit.commit.message,
                "url": commit.html_url,
                "date": commit.commit.author.date.isoformat(),
                "author": {
                    "name": commit.commit.author.name,
                    "email": commit.commit.author.email
                },
                "committer": {
                    "name": commit.commit.committer.name,
                    "email": commit.commit.committer.email
                }
            })
        if idx >= end_idx:
            break
            
    return results

# Search Tools
@mcp.tool()
@handle_github_errors
def search_code(q: str, page: int = 1, per_page: int = 30, order: str = "desc") -> List[Dict[str, Any]]:
    """
    Search for code across Github repositories.
    
    Args:
        q: Search query string
        page: Page number (minimum: 1)
        per_page: Results per page (minimum: 1, maximum: 100)
        order: Sort order ('asc' or 'desc')
        
    Returns:
        List of matching code items
    """
    g = get_github_client()
    
    code_results = g.search_code(
        query=q,
        sort="indexed",
        order=order
    )
    
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    
    results = []
    for idx, item in enumerate(code_results):
        if idx >= start_idx and idx < end_idx:
            try:
                content = item.decoded_content.decode('utf-8')
                truncated_content = content[:1000] + "..." if len(content) > 1000 else content
            except UnicodeDecodeError:
                truncated_content = "Binary file (cannot display content)"
                
            results.append({
                "name": item.name,
                "path": item.path,
                "repository": item.repository.full_name,
                "url": item.html_url,
                "content": truncated_content
            })
        if idx >= end_idx:
            break
            
    return results

@mcp.tool()
@handle_github_errors
def search_issues(q: str, sort: str = None, order: str = "desc", page: int = 1, per_page: int = 30) -> List[Dict[str, Any]]:
    """
    Search for issues and pull requests across Github repositories.
    
    Args:
        q: Search query string
        sort: Sorting field (comments, reactions, created, updated)
        order: Sort direction ('asc', 'desc')
        page: Page number (minimum: 1)
        per_page: Results per page (minimum: 1, maximum: 100)
        
    Returns:
        List of matching issues
    """
    g = get_github_client()
    
    issue_results = g.search_issues(
        query=q,
        sort=sort,
        order=order
    )
    
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    
    results = []
    for idx, item in enumerate(issue_results):
        if idx >= start_idx and idx < end_idx:
            results.append({
                "number": item.number,
                "title": item.title,
                "repository": item.repository.full_name,
                "url": item.html_url,
                "state": item.state,
                "is_pull_request": item.pull_request is not None,
                "created_at": item.created_at.isoformat(),
                "updated_at": item.updated_at.isoformat(),
                "user": {
                    "login": item.user.login,
                    "avatar_url": item.user.avatar_url
                }
            })
        if idx >= end_idx:
            break
            
    return results

@mcp.tool()
@handle_github_errors
def search_users(q: str, sort: str = None, order: str = "desc", page: int = 1, per_page: int = 30) -> List[Dict[str, Any]]:
    """
    Search for users on Github.
    
    Args:
        q: Search query string
        sort: Sorting field (followers, repositories, joined)
        order: Sort direction ('asc', 'desc')
        page: Page number (minimum: 1)
        per_page: Results per page (minimum: 1, maximum: 100)
        
    Returns:
        List of matching users
    """
    g = get_github_client()
    
    user_results = g.search_users(
        query=q,
        sort=sort,
        order=order
    )
    
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    
    results = []
    for idx, user in enumerate(user_results):
        if idx >= start_idx and idx < end_idx:
            results.append({
                "login": user.login,
                "name": user.name,
                "avatar_url": user.avatar_url,
                "url": user.html_url,
                "type": user.type,
                "company": user.company,
                "location": user.location,
                "email": user.email,
                "bio": user.bio,
                "public_repos": user.public_repos,
                "followers": user.followers
            })
        if idx >= end_idx:
            break
            
    return results

# Fork and Pull Request Review Tools
@mcp.tool()
@handle_github_errors
def fork_repository(owner: str, repo: str, organization: str = None) -> Dict[str, Any]:
    """
    Fork a Github repository to your account or specified organization.
    
    Args:
        owner: Repository owner (username or organization)
        repo: Repository name
        organization: Optional: organization to fork to (defaults to your personal account)
        
    Returns:
        Fork information
    """
    g = get_github_client()
    repo_obj = g.get_repo(f"{owner}/{repo}")
    
    fork = repo_obj.create_fork(organization=organization)
    
    return {
        "id": fork.id,
        "name": fork.name,
        "full_name": fork.full_name,
        "description": fork.description,
        "url": fork.html_url,
        "clone_url": fork.clone_url,
        "owner": {
            "login": fork.owner.login,
            "avatar_url": fork.owner.avatar_url
        },
        "parent": {
            "full_name": fork.parent.full_name,
            "url": fork.parent.html_url
        }
    }

@mcp.tool()
@handle_github_errors
def create_pull_request_review(owner: str, repo: str, pull_number: int, body: str, event: str, comments: List[Dict[str, Any]] = None, commit_id: str = None) -> Dict[str, Any]:
    """
    Create a review on a pull request.
    
    Args:
        owner: Repository owner (username or organization)
        repo: Repository name
        pull_number: Pull request number
        body: The body text of the review
        event: The review action to perform ('APPROVE', 'REQUEST_CHANGES', 'COMMENT')
        comments: Comments to post as part of the review (specify either position or line, not both)
        commit_id: The SHA of the commit that needs a review
        
    Returns:
        Review information
    """
    g = get_github_client()
    repo_obj = g.get_repo(f"{owner}/{repo}")
    pr = repo_obj.get_pull(pull_number)
    
    review_kwargs = {
        "body": body,
        "event": event
    }
    
    if commit_id:
        review_kwargs["commit_id"] = commit_id
        
    if comments:
        review_comments = []
        for comment in comments:
            comment_data = {
                "path": comment["path"],
                "body": comment["body"]
            }
            
            if "position" in comment:
                comment_data["position"] = comment["position"]
            elif "line" in comment:
                comment_data["line"] = comment["line"]
                
            review_comments.append(comment_data)
            
        review_kwargs["comments"] = review_comments
    
    review = pr.create_review(**review_kwargs)
    
    return {
        "id": review.id,
        "body": review.body,
        "state": review.state,
        "submitted_at": review.submitted_at.isoformat() if review.submitted_at else None,
        "user": {
            "login": review.user.login,
            "avatar_url": review.user.avatar_url
        },
        "commit_id": review.commit_id
    }

@mcp.tool()
@handle_github_errors
def get_pull_request_reviews(owner: str, repo: str, pull_number: int) -> List[Dict[str, Any]]:
    """
    Get the reviews on a pull request.
    
    Args:
        owner: Repository owner (username or organization)
        repo: Repository name
        pull_number: Pull request number
        
    Returns:
        List of reviews
    """
    g = get_github_client()
    repo_obj = g.get_repo(f"{owner}/{repo}")
    pr = repo_obj.get_pull(pull_number)
    
    reviews = pr.get_reviews()
    
    results = []
    for review in reviews:
        results.append({
            "id": review.id,
            "body": review.body,
            "state": review.state,
            "submitted_at": review.submitted_at.isoformat() if review.submitted_at else None,
            "user": {
                "login": review.user.login,
                "avatar_url": review.user.avatar_url
            },
            "commit_id": review.commit_id
        })
            
    return results

@mcp.tool()
@handle_github_errors
def get_pull_request_files(owner: str, repo: str, pull_number: int) -> List[Dict[str, Any]]:
    """
    Get the list of files changed in a pull request.
    
    Args:
        owner: Repository owner (username or organization)
        repo: Repository name
        pull_number: Pull request number
        
    Returns:
        List of changed files
    """
    g = get_github_client()
    repo_obj = g.get_repo(f"{owner}/{repo}")
    pr = repo_obj.get_pull(pull_number)
    
    files = pr.get_files()
    
    results = []
    for file in files:
        results.append({
            "filename": file.filename,
            "status": file.status,
            "additions": file.additions,
            "deletions": file.deletions,
            "changes": file.changes,
            "url": file.raw_url,
            "patch": file.patch
        })
            
    return results

@mcp.tool()
@handle_github_errors
def merge_pull_request(owner: str, repo: str, pull_number: int, commit_title: str = None, commit_message: str = None, merge_method: str = "merge") -> Dict[str, Any]:
    """
    Merge a pull request.
    
    Args:
        owner: Repository owner (username or organization)
        repo: Repository name
        pull_number: Pull request number
        commit_title: Title for the automatic commit message
        commit_message: Extra detail to append to automatic commit message
        merge_method: Merge method to use ('merge', 'squash', 'rebase')
        
    Returns:
        Merge result information
    """
    g = get_github_client()
    repo_obj = g.get_repo(f"{owner}/{repo}")
    pr = repo_obj.get_pull(pull_number)
    
    merge_result = pr.merge(
        commit_title=commit_title,
        commit_message=commit_message,
        merge_method=merge_method
    )
    
    return {
        "merged": merge_result.merged,
        "message": merge_result.message,
        "sha": merge_result.sha
    }

# Prompts for Github workflows
@mcp.prompt("issue_search")
def issue_search_prompt(query: str = None, repo: str = None, state: str = "open"):
    """
    A prompt template for searching Github issues.
    
    Args:
        query: Search query for issues
        repo: Repository to search in (format: 'owner/repo')
        state: Issue state ('open', 'closed', 'all')
    """
    # Construct the search query
    search_query = []
    
    if repo:
        search_query.append(f"repo:{repo}")
    
    if query:
        search_query.append(query)
    
    if state in ["open", "closed"]:
        search_query.append(f"is:{state}")
    
    full_query = " ".join(search_query)
    
    return {
        "messages": [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": f"Please search for Github issues with the following query: {full_query}\n\nAnalyze the results and provide a summary of the key issues found."
                }
            }
        ]
    }

@mcp.prompt("create_repository")
def create_repository_prompt(name: str = None, description: str = None, private: bool = False):
    """
    A prompt template for creating a new Github repository.
    
    Args:
        name: Name for the new repository
        description: Repository description
        private: Whether the repository should be private
    """
    visibility = "private" if private else "public"
    
    name_text = f" named '{name}'" if name else ""
    description_text = f" with description: '{description}'" if description else ""
    
    return {
        "messages": [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": f"Please create a new {visibility} Github repository{name_text}{description_text}. After creating it, let me know what files I should add to get started."
                }
            }
        ]
    }

@mcp.prompt("pull_request")
def pull_request_prompt(title: str = None, description: str = None, repo: str = None, base: str = "main", head: str = None):
    """
    A prompt template for creating a pull request.
    
    Args:
        title: Title for the pull request
        description: Pull request description
        repo: Repository where to create the PR (format: 'owner/repo')
        base: The branch to merge into
        head: The branch with changes
    """
    title_text = f" with title '{title}'" if title else ""
    description_text = f"\n\nDescription: {description}" if description else ""
    repo_text = f" in the repository {repo}" if repo else ""
    branch_text = f" from branch '{head}' into '{base}'" if head else f" into branch '{base}'"
    
    return {
        "messages": [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": f"Please create a pull request{title_text}{repo_text}{branch_text}.{description_text}"
                }
            }
        ]
    }

@mcp.prompt("code_search")
def code_search_prompt(query: str = None, language: str = None):
    """
    A prompt template for searching code on Github.
    
    Args:
        query: Search terms
        language: Programming language to filter by
    """
    # Construct the search query
    search_query = []
    
    if query:
        search_query.append(query)
    
    if language:
        search_query.append(f"language:{language}")
    
    full_query = " ".join(search_query)
    
    return {
        "messages": [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": f"Please search for code on Github with the query: {full_query}\n\nAnalyze the results and show me examples of how this is typically implemented."
                }
            }
        ]
    }

@mcp.resource("repo://{owner}/{repo}")
def get_repo_info(owner: str, repo: str) -> Dict[str, Any]:
    """Get information about a specific Github repository."""
    g = get_github_client()
    try:
        repo_obj = g.get_repo(f"{owner}/{repo}")
        return {
            "id": repo_obj.id,
            "name": repo_obj.name,
            "full_name": repo_obj.full_name,
            "description": repo_obj.description,
            "url": repo_obj.html_url,
            "homepage": repo_obj.homepage,
            "language": repo_obj.language,
            "visibility": repo_obj.visibility,
            "default_branch": repo_obj.default_branch,
            "created_at": repo_obj.created_at.isoformat(),
            "updated_at": repo_obj.updated_at.isoformat(),
            "pushed_at": repo_obj.pushed_at.isoformat(),
            "size": repo_obj.size,
            "stars": repo_obj.stargazers_count,
            "watchers": repo_obj.watchers_count,
            "forks": repo_obj.forks_count,
            "open_issues": repo_obj.open_issues_count,
            "license": repo_obj.license.name if repo_obj.license else None,
            "topics": repo_obj.topics,
            "has_wiki": repo_obj.has_wiki,
            "has_pages": repo_obj.has_pages,
            "has_projects": repo_obj.has_projects,
            "has_issues": repo_obj.has_issues,
            "owner": {
                "login": repo_obj.owner.login,
                "type": repo_obj.owner.type,
                "avatar_url": repo_obj.owner.avatar_url,
                "url": repo_obj.owner.html_url
            }
        }
    except Exception as e:
        raise ValueError(f"Error retrieving repository information: {str(e)}")

@mcp.resource("user://{username}")
def get_user_info(username: str) -> Dict[str, Any]:
    """Get information about a specific Github user."""
    g = get_github_client()
    try:
        user = g.get_user(username)
        return {
            "login": user.login,
            "name": user.name,
            "company": user.company,
            "location": user.location,
            "email": user.email,
            "bio": user.bio,
            "avatar_url": user.avatar_url,
            "url": user.html_url,
            "type": user.type,
            "public_repos": user.public_repos,
            "public_gists": user.public_gists,
            "followers": user.followers,
            "following": user.following,
            "created_at": user.created_at.isoformat(),
            "updated_at": user.updated_at.isoformat()
        }
    except Exception as e:
        raise ValueError(f"Error retrieving user information: {str(e)}")

@mcp.resource("issue://{owner}/{repo}/{number}")
def get_issue_info(owner: str, repo: str, number: str) -> Dict[str, Any]:
    """Get information about a specific Github issue."""
    g = get_github_client()
    try:
        repo_obj = g.get_repo(f"{owner}/{repo}")
        issue = repo_obj.get_issue(int(number))
        
        # Get comments
        comments = []
        for comment in issue.get_comments():
            comments.append({
                "id": comment.id,
                "body": comment.body,
                "created_at": comment.created_at.isoformat(),
                "updated_at": comment.updated_at.isoformat(),
                "user": {
                    "login": comment.user.login,
                    "avatar_url": comment.user.avatar_url
                }
            })
        
        return {
            "number": issue.number,
            "title": issue.title,
            "body": issue.body,
            "url": issue.html_url,
            "state": issue.state,
            "created_at": issue.created_at.isoformat(),
            "updated_at": issue.updated_at.isoformat(),
            "closed_at": issue.closed_at.isoformat() if issue.closed_at else None,
            "labels": [label.name for label in issue.labels],
            "assignees": [assignee.login for assignee in issue.assignees],
            "comments": comments,
            "comment_count": issue.comments,
            "user": {
                "login": issue.user.login,
                "avatar_url": issue.user.avatar_url
            }
        }
    except Exception as e:
        raise ValueError(f"Error retrieving issue information: {str(e)}")

@mcp.resource("pull://{owner}/{repo}/{number}")
def get_pull_info(owner: str, repo: str, number: str) -> Dict[str, Any]:
    """Get information about a specific Github pull request."""
    g = get_github_client()
    try:
        repo_obj = g.get_repo(f"{owner}/{repo}")
        pr = repo_obj.get_pull(int(number))
        
        # Get files changed
        files = []
        for file in pr.get_files():
            files.append({
                "filename": file.filename,
                "status": file.status,
                "additions": file.additions,
                "deletions": file.deletions,
                "changes": file.changes
            })
        
        # Get reviews
        reviews = []
        for review in pr.get_reviews():
            reviews.append({
                "id": review.id,
                "body": review.body,
                "state": review.state,
                "submitted_at": review.submitted_at.isoformat() if review.submitted_at else None,
                "user": {
                    "login": review.user.login,
                    "avatar_url": review.user.avatar_url
                }
            })
        
        return {
            "number": pr.number,
            "title": pr.title,
            "body": pr.body,
            "url": pr.html_url,
            "state": pr.state,
            "created_at": pr.created_at.isoformat(),
            "updated_at": pr.updated_at.isoformat(),
            "closed_at": pr.closed_at.isoformat() if pr.closed_at else None,
            "merged_at": pr.merged_at.isoformat() if pr.merged_at else None,
            "head": {
                "ref": pr.head.ref,
                "label": pr.head.label,
                "sha": pr.head.sha
            },
            "base": {
                "ref": pr.base.ref,
                "label": pr.base.label,
                "sha": pr.base.sha
            },
            "user": {
                "login": pr.user.login,
                "avatar_url": pr.user.avatar_url
            },
            "mergeable": pr.mergeable,
            "merged": pr.merged,
            "commits": pr.commits,
            "additions": pr.additions,
            "deletions": pr.deletions,
            "changed_files": pr.changed_files,
            "files": files,
            "reviews": reviews
        }
    except Exception as e:
        raise ValueError(f"Error retrieving pull request information: {str(e)}")

if __name__ == "__main__":
    print("Starting Github MCP server...", file=sys.stderr)
    mcp.run()
