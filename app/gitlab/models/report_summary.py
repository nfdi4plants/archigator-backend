from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel


class Total(BaseModel):
    time: int
    count: int
    success: int
    failed: int
    skipped: int
    error: int
    suite_error: Any


class TestSuite(BaseModel):
    name: str
    total_time: int
    total_count: int
    success_count: int
    failed_count: int
    skipped_count: int
    error_count: int
    build_ids: List[int]
    suite_error: Any


class TestSummary(BaseModel):
    total: Optional[Total] = None
    test_suites: Optional[List[TestSuite]] = None
