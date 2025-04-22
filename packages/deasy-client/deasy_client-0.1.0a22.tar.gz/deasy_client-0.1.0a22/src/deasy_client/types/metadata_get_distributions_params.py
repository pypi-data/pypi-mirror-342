# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = ["MetadataGetDistributionsParams"]


class MetadataGetDistributionsParams(TypedDict, total=False):
    vdb_profile_name: Required[str]

    analysis_level: Literal["file", "chunk", "both"]

    schema_name: Optional[str]

    tag_names: Optional[List[str]]
