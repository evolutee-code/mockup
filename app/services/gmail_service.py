import asyncio
import random
import traceback

from helper import generate_totp


class GmailService:
    def __init__(self, browser, context, page, email, email_pw, two_fa_secret):
        self.browser = browser
        self.context = context
        self.page = page
        self.gmail_url = "https://accounts.google.com/ServiceLogin?continue=https://mail.google.com/mail/"
        self.email = email
        self.email_pw = email_pw
        self.two_fa_secret = two_fa_secret

    async def checkLoginGmail(self) -> bool:
        await self.page.goto(self.gmail_url)

        if await self.page.query_selector("#gb"):
            print("Already logged in")
            return True

        return False

    async def loginGmail(self):
        try:
            await self.page.goto(
                self.gmail_url,
                wait_until="networkidle"
            )

            email_input = await self.page.wait_for_selector("#identifierId")
            await email_input.type(self.email)

            next_button = await self.page.wait_for_selector("#identifierNext")

            await asyncio.sleep(random.uniform(1, 3))

            await next_button.click()

            password_input = await self.page.wait_for_selector("input[name='Passwd']")

            await password_input.fill(self.email_pw)

            await asyncio.sleep(random.uniform(1, 3))

            await self.page.keyboard.press("Enter")

            code_input = await self.page.wait_for_selector("input[type='text']")

            otp = await self.get2FA()

            if not otp:
                return False

            await code_input.fill(otp)

            await self.page.keyboard.press("Enter")

            return True
        except Exception as e:
            traceback.print_exc()
            return False

    async def get2FA(self):
        try:
            code = generate_totp(self.two_fa_secret)
            return code['code']
        except Exception as e:
            traceback.print_exc()
            return None
