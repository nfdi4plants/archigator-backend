from __future__ import annotations

from typing import Any, List, Optional, Union

from pydantic import BaseModel


class SystemOutputItem(BaseModel):
    message: str


class TestCase(BaseModel):
    status: str
    name: str
    classname: Any
    file: Any
    execution_time: float
    # system_output: Optional[SystemOutputItem]
    system_output: Optional[Union[str, dict]] = None
    stack_trace: Any
    recent_failures: Any


class TestSuite(BaseModel):
    name: str
    total_time: float
    total_count: int
    success_count: int
    failed_count: int
    skipped_count: int
    error_count: int
    suite_error: Any
    test_cases: List[TestCase]


class TestReport(BaseModel):
    total_time: Optional[float] = None
    total_count: Optional[int] = None
    success_count: Optional[int] = None
    failed_count: Optional[int] = None
    skipped_count: Optional[int] = None
    error_count: Optional[int] = None
    test_suites: Optional[List[TestSuite]] = None
