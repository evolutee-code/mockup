from typing import TypedDict, Optional, Any, Coroutine
import aiohttp
import os


class ProfileResponse(TypedDict):
    success: bool
    data: dict
    message: str


class GpmService:
    def __init__(self, base_url: str = "http://127.0.0.1:19995"):
        self.base_url = base_url
        self.api_version = "v3"

    async def getProfile(self, profile_id: str) -> dict[str, bool | dict[str, str] | str] | None | Any:
        """
        Fetch profile data from GPM API
        Args:
            profile_id: UUID of the profile to fetch
        Returns:
            Profile data if successful, None otherwise
        """
        if True:
        # if os.getenv('APP_ENV') == 'localhost':
            return {
                "success": True,
                "data": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "name": "customized_profile",
                    "raw_proxy": "",
                    "browser_type": "chromium",
                    "browser_version": "120.0.6099.28",
                    "group_id": "987fcdeb-51a2-3e4b-9876-543210fedcba",
                    "profile_path": "/var/www/Evalutee/mockup/playwright_profiles/customized_profile",
                    # "browser_type": "firefox",
                    # "browser_version": "119.0",
                    # "group_id": "987fcdeb-51a2-3e4b-9876-543210fedcba",
                    # "profile_path": "/var/www/Evalutee/mockup/playwright_profiles/firefox_customized_profile",
                    "note": "Selenium test profile",
                    "created_at": "2024-10-20T10:30:00Z"
                },
                "message": "OK"
            }

        # url = f"{self.base_url}/api/{self.api_version}/profiles/{profile_id}"
        #
        # async with aiohttp.ClientSession() as session:
        #     async with session.get(url) as response:
        #         if response.status == 200:
        #             return await response.json()
        #         return None
