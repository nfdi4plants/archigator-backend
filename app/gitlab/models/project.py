from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel


class Namespace(BaseModel):
    id: int
    name: Optional[str] = None
    path: Optional[str] = None
    kind: Optional[str] = None
    full_path: Optional[str] = None
    parent_id: Any
    avatar_url: Optional[str] = None
    web_url: Optional[str] = None


class _Links(BaseModel):
    self: str
    issues: str
    merge_requests: str
    repo_branches: str
    labels: str
    events: str
    members: str
    cluster_agents: str


class Owner(BaseModel):
    id: int
    username: str
    name: str
    state: str
    avatar_url: str
    web_url: str


class ContainerExpirationPolicy(BaseModel):
    cadence: str
    enabled: bool
    keep_n: int
    older_than: str
    name_regex: str
    name_regex_keep: Any
    next_run_at: str


class Permissions(BaseModel):
    project_access: Any
    group_access: Any


class Project(BaseModel):
    id: Optional[int] = None
    description: Optional[Any] = None
    name: Optional[str] = None
    name_with_namespace: Optional[str] = None
    path: Optional[str] = None
    path_with_namespace: Optional[str] = None
    created_at: Optional[str] = None
    default_branch: Optional[str] = None
    tag_list: Optional[List] = None
    topics: Optional[List] = None
    ssh_url_to_repo: Optional[str] = None
    http_url_to_repo: Optional[str] = None
    web_url: Optional[str] = None
    readme_url: Optional[str] = None
    avatar_url: Optional[Any] = None
    forks_count: Optional[int] = None
    star_count: Optional[int] = None
    last_activity_at: Optional[str] = None
    namespace: Optional[Namespace] = None
    container_registry_image_prefix: Optional[str] = None
    _links: Optional[_Links] = None
    packages_enabled: Optional[bool] = None
    empty_repo: Optional[bool] = None
    archived: Optional[bool] = None
    visibility: Optional[str] = None
    owner: Optional[Owner] = None
    resolve_outdated_diff_discussions: Optional[bool] = None
    container_expiration_policy: Optional[ContainerExpirationPolicy] = None
    issues_enabled: Optional[bool] = None
    merge_requests_enabled: Optional[bool] = None
    wiki_enabled: Optional[bool] = None
    jobs_enabled: Optional[bool] = None
    snippets_enabled: Optional[bool] = None
    container_registry_enabled: Optional[bool] = None
    service_desk_enabled: Optional[bool] = None
    service_desk_address: Optional[Any] = None
    can_create_merge_request_in: Optional[bool] = None
    issues_access_level: Optional[str] = None
    repository_access_level: Optional[str] = None
    merge_requests_access_level: Optional[str] = None
    forking_access_level: Optional[str] = None
    wiki_access_level: Optional[str] = None
    builds_access_level: Optional[str] = None
    snippets_access_level: Optional[str] = None
    pages_access_level: Optional[str] = None
    operations_access_level: Optional[str] = None
    analytics_access_level: Optional[str] = None
    container_registry_access_level: Optional[str] = None
    security_and_compliance_access_level: Optional[str] = None
    releases_access_level: Optional[str] = None
    emails_disabled: Optional[bool] = None
    shared_runners_enabled: Optional[bool] = None
    lfs_enabled: Optional[bool] = None
    creator_id: Optional[int] = None
    import_url: Optional[Any] = None
    import_type: Optional[Any] = None
    import_status: Optional[str] = None
    import_error: Optional[Any] = None
    open_issues_count: Optional[int] = None
    runners_token: Optional[str] = None
    ci_default_git_depth: Optional[int] = None
    ci_forward_deployment_enabled: Optional[bool] = None
    ci_job_token_scope_enabled: Optional[bool] = None
    ci_separated_caches: Optional[bool] = None
    ci_opt_in_jwt: Optional[bool] = None
    ci_allow_fork_pipelines_to_run_in_parent_project: Optional[bool] = None
    public_jobs: Optional[bool] = None
    build_git_strategy: Optional[str] = None
    build_timeout: Optional[int] = None
    auto_cancel_pending_pipelines: Optional[str] = None
    ci_config_path: Optional[Any] = None
    shared_with_groups: Optional[List] = None
    only_allow_merge_if_pipeline_succeeds: Optional[bool] = None
    allow_merge_on_skipped_pipeline: Optional[Any] = None
    restrict_user_defined_variables: Optional[bool] = None
    request_access_enabled: Optional[bool] = None
    only_allow_merge_if_all_discussions_are_resolved: Optional[bool] = None
    remove_source_branch_after_merge: Optional[bool] = None
    printing_merge_request_link_enabled: Optional[bool] = None
    merge_method: Optional[str] = None
    squash_option: Optional[str] = None
    enforce_auth_checks_on_uploads: Optional[bool] = None
    suggestion_commit_message: Optional[Any] = None
    merge_commit_template: Optional[Any] = None
    squash_commit_template: Optional[Any] = None
    auto_devops_enabled: Optional[bool] = None
    auto_devops_deploy_strategy: Optional[str] = None
    autoclose_referenced_issues: Optional[bool] = None
    repository_storage: Optional[str] = None
    keep_latest_artifact: Optional[bool] = None
    runner_token_expiration_interval: Optional[Any] = None
    requirements_enabled: Optional[bool] = None
    requirements_access_level: Optional[str] = None
    security_and_compliance_enabled: Optional[bool] = None
    compliance_frameworks: Optional[List] = None
    permissions: Optional[Permissions] = None


class ProjectList(BaseModel):
    projects: List[Project]
