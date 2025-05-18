import os
import shutil
import asyncio
from typing import Dict, List, Optional, Literal
from playwright.async_api import async_playwright, Browser, BrowserContext, Page

BrowserType = Literal["chromium", "firefox", "webkit"]


class PlaywrightProfileManager:
    """Manage multiple persistent browser profiles for Playwright"""

    def __init__(self, base_dir: str = "playwright_profiles"):
        """
        Initialize the profile manager

        Args:
            base_dir: Base directory for storing profiles
        """
        self.base_dir = os.path.abspath(base_dir)
        self.active_contexts: Dict[str, BrowserContext] = {}
        os.makedirs(self.base_dir, exist_ok=True)

    async def create_profile(self, profile_name: str, overwrite: bool = False, browser_type: str = "chromium") -> str:
        """
        Create a new empty profile directory
    
        Args:
            profile_name: Name of the profile to create
            overwrite: Whether to overwrite if the profile already exists
            browser_type: Type of browser profile to create ("chromium" or "firefox")

        Returns:
            Path to the created profile directory

        Raises:
            FileExistsError: If profile exists and overwrite is False
            ValueError: If invalid browser type specified
        """
        if browser_type not in ["chromium", "firefox"]:
            raise ValueError("Browser type must be either 'chromium' or 'firefox'")

        profile_path = await self.get_profile_path(f"{browser_type}_{profile_name}")

        # Check if profile already exists
        if os.path.exists(profile_path):
            if overwrite:
                # Delete existing profile if overwrite is True
                shutil.rmtree(profile_path)
            else:
                # Raise error if overwrite is False
                raise FileExistsError(f"Profile '{profile_name}' already exists")

        # Create profile directory
        os.makedirs(profile_path, exist_ok=True)

        # Create browser-specific subdirectories
        if browser_type == "chromium":
            os.makedirs(os.path.join(profile_path, "Default"), exist_ok=True)
        elif browser_type == "firefox":
            os.makedirs(os.path.join(profile_path, "cache"), exist_ok=True)
            os.makedirs(os.path.join(profile_path, "extensions"), exist_ok=True)

        print(f"Created {browser_type} profile '{profile_name}' at: {profile_path}")
        return profile_path

    async def get_profile_path(self, profile_name: str) -> str:
        """
        Get the path for a specific profile

        Args:
            profile_name: Name of the profile

        Returns:
            Absolute path to the profile directory
        """
        return os.path.join(self.base_dir, profile_name)

    async def profile_exists(self, profile_name: str) -> bool:
        """
        Check if a profile exists

        Args:
            profile_name: Name of the profile

        Returns:
            True if profile exists, False otherwise
        """
        return os.path.exists(await self.get_profile_path(profile_name))

    async def list_profiles(self) -> List[str]:
        """
        List all available profiles

        Returns:
            List of profile names
        """
        if not os.path.exists(self.base_dir):
            return []

        return [
            item for item in os.listdir(self.base_dir)
            if os.path.isdir(os.path.join(self.base_dir, item))
        ]

    async def delete_profile(self, profile_name: str) -> bool:
        """
        Delete a profile

        Args:
            profile_name: Name of the profile to delete

        Returns:
            True if profile was deleted, False otherwise
        """
        profile_path = await self.get_profile_path(profile_name)

        if not os.path.exists(profile_path):
            return False

        # Check if profile is currently in use
        if profile_name in self.active_contexts:
            raise RuntimeError(f"Cannot delete profile '{profile_name}' while it is in use")

        try:
            shutil.rmtree(profile_path)
            return True
        except Exception as e:
            print(f"Error deleting profile '{profile_name}': {e}")
            return False

    async def launch_browser_with_profile(
            self,
            profile_name: str,
            browser_type: BrowserType = "chromium",
            headless: bool = False,
            **kwargs
    ) -> BrowserContext:
        """
        Launch a browser with a specific profile

        Args:
            profile_name: Name of the profile to use
            browser_type: Type of browser to launch (chromium, firefox, webkit)
            headless: Whether to run in headless mode
            **kwargs: Additional arguments to pass to launch_persistent_context

        Returns:
            Browser context with the specified profile
        """
        profile_path = await self.get_profile_path(profile_name)
        os.makedirs(profile_path, exist_ok=True)

        # Set up default options
        options = {
            "user_data_dir": profile_path,
            "headless": headless,
            "accept_downloads": True,
        }
        # Update with any additional options
        options.update(kwargs)

        # Get playwright instance
        playwright = await async_playwright().start()

        # Get the browser instance based on type
        if browser_type == "chromium":
            browser_instance = playwright.chromium
        elif browser_type == "firefox":
            browser_instance = playwright.firefox
        elif browser_type == "webkit":
            browser_instance = playwright.webkit
        else:
            raise ValueError(f"Invalid browser type: {browser_type}")

        # Launch the browser with persistent context
        context = await browser_instance.launch_persistent_context(**options)

        # Store the active context
        self.active_contexts[profile_name] = context

        return context

    async def close_profile(self, profile_name: str) -> bool:
        """
        Close a browser profile if it's active

        Args:
            profile_name: Name of the profile to close

        Returns:
            True if profile was closed, False if not found
        """
        if profile_name not in self.active_contexts:
            return False

        context = self.active_contexts[profile_name]
        await context.close()
        del self.active_contexts[profile_name]
        return True

    async def close_all_profiles(self) -> None:
        """Close all active browser profiles"""
        for profile_name in list(self.active_contexts.keys()):
            await self.close_profile(profile_name)
