from datetime import date
from typing import Optional, Dict

from .consts import API_GET_DIARY, API_GET_VENDORS
from .parser import parse_diary, parse_vendors
from .typings import Vendor, Student
from .httpclient import http_client


async def get_diary(start: date, end: date, vendor: Vendor) -> Optional[Dict[str, Student]]:
    days = f"{start:%Y%m%d}-{end:%Y%m%d}"

    js = await http_client.get(
        url=API_GET_DIARY,
        auth_token=vendor.token,
        student_name=vendor.student_name,
        vendor=vendor.vendor,
        days=days
    )

    return parse_diary(js)


async def get_vendor(v_token: str) -> Optional[Vendor]:
    js = await http_client.get(
        url=API_GET_VENDORS,
        v_token=v_token
    )

    return parse_vendors(js)
