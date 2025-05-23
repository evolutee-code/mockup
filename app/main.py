import asyncio
import random
import time
import traceback

from services.gmail_service import GmailService
from helper import generate_totp
from services.browser_profile_service import PlaywrightProfileManager
from services.gpm_service import GpmService
import pyotp


class Mockup:
    def __init__(self):
        self.browser = None
        self.context = None
        self.page = None
        self.profile = None
        self.gmail_url = "https://accounts.google.com/ServiceLogin?continue=https://mail.google.com/mail/"
        self.email = 'cuongnguyen20072002@gmail.com'
        self.email_pw = 'forjyus3775'
        self.two_fa_secret = 'j67g 7kvt ai7z fcex 4c3h ku5e hdpk imez'
        self.gpm_service = GpmService()
        self.browser_service = PlaywrightProfileManager()
        self.gmail_service = None

    async def getProfileBrowser(self):
        profile = await self.gpm_service.getProfile('123e4567-e89b-12d3-a456-426614174000')
        self.profile = profile['data']
        # profile_path = await self.browser_service.create_profile(f'customized_profile_{int(time.time())}', True, 'chromium')
        # print(profile_path)

    async def loadBrowser(self):
        try:
            self.context = await self.browser_service.launch_browser_with_profile(
                profile_name=self.profile['name'],
                browser_type=self.profile['browser_type']
            )
            self.page = await self.context.new_page()
            return None
        except Exception as e:
            traceback.print_exc()
            return None

    async def setBrowser(self):
        self.gmail_service = GmailService(
            browser=self.browser,
            context=self.context,
            page=self.page,
            email=self.email,
            email_pw=self.email_pw,
            two_fa_secret=self.two_fa_secret)

    async def checkLoginGmail(self) -> bool:
        await self.setBrowser()
        return await self.gmail_service.checkLoginGmail()

    async def loginGmail(self):
        await self.setBrowser()
        return await self.gmail_service.loginGmail()

    async def loginOpenAI(self):
        await self.page.goto(
            'https://auth.openai.com/log-in',
            # 'https://chatgpt.com',
            wait_until="networkidle"
        )

        email_button = await self.page.wait_for_selector('button[value="google"]')
        await asyncio.sleep(random.uniform(4, 8))
        await email_button.click()
        await self.page.wait_for_load_state("networkidle")

    async def sendPromtImage(self):
        print('sendPromt')

    async def getImageFromOpenAI(self):
        print('getImageFromOpenAI')

    async def sendImageToSystem(self):
        print('sendImageToSystem')

    async def closeBrowser(self):
        await self.browser.close()
        await self.browser_service.close_profile(self.profile['name'])


async def main():
    mockup = Mockup()
    await mockup.getProfileBrowser()
    await mockup.loadBrowser()
    is_logged_in = await mockup.checkLoginGmail()
    if not is_logged_in:
        await mockup.loginGmail()
    await mockup.loginOpenAI()
    # await mockup.sendPromtImage()
    # await mockup.getImageFromOpenAI()
    # await mockup.sendImageToSystem()
    #

    await asyncio.sleep(20)
    await mockup.closeBrowser()


if __name__ == '__main__':
    asyncio.run(main())
