import asyncio
from fastapi import FastAPI, Depends
from pyppeteer import launch, browser
from readability import Document
from playwright.async_api import async_playwright

app = FastAPI()


async def get_page_html(url: str, wait_time: int) -> dict:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        # Wait for either the 'domcontentloaded' event or the specified timeout
        done, pending = await asyncio.wait(
            [
                page.goto(url, wait_until="domcontentloaded"),
                asyncio.sleep(wait_time)
            ],
            return_when=asyncio.FIRST_COMPLETED
        )

        # Cancel any pending tasks
        for task in pending:
            task.cancel()

        html = await page.content()

        await page.close()
        await context.close()
        await browser.close()

    return html


async def extract_main_content(html: str) -> dict:
    document = Document(html)
    title = document.title()
    return {
        "title": title,
        "content": html,
    }


@app.get("/scrape/")
async def scrape(url: str, wait_time: int = 5):
    try:
        html = await get_page_html(url, wait_time)
        extracted_data = await extract_main_content(html)
        return {
            "title": extracted_data["title"],
            "content": extracted_data["content"],
        }
    except Exception as e:
        return {"error": str(e)}
