"""Build first, then verify manual progress in Chromium (requires Playwright)."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[1]
CHAPTER = "chapters/01-why-metadata.html"
KEY = "metadata-book:v1:manual-completion:01-why-metadata"
MARK = '[data-lesson-link="01-why-metadata"] .lesson-done'


class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


server = ThreadingHTTPServer(("127.0.0.1", 0), partial(Quiet, directory=str(ROOT / "_site")))
Thread(target=server.serve_forever, daemon=True).start()
base = f"http://127.0.0.1:{server.server_port}/"
try:
    with sync_playwright() as p:
        system = Path("/usr/bin/chromium")
        browser = p.chromium.launch(**({"executable_path": str(system)} if system.exists() else {}))
        errors = []
        for width, theme in [(1280, "light"), (390, "light"), (390, "dark")]:
            context = browser.new_context(viewport={"width": width, "height": 950}, color_scheme=theme)
            page = context.new_page()
            page.on("pageerror", lambda e: errors.append(str(e)))
            page.goto(base + CHAPTER)
            check = page.get_by_role("checkbox", name="Mark lesson as done")
            expect(check).not_to_be_checked()
            check.focus()
            check.press("Space")
            expect(check).to_be_checked()
            assert page.evaluate("key => localStorage.getItem(key)", KEY) == "true"
            assert page.locator(MARK).evaluate_all("marks => marks.every(m => !m.hidden)")
            page.reload()
            expect(check).to_be_checked()
            # A different lesson has its own mark. Next does not mark it automatically.
            page.locator(".pagination-next").click()
            expect(check).not_to_be_checked()
            check.check()
            other_key = "metadata-book:v1:manual-completion:02-reading-a-database"
            other = context.new_page()
            other.goto(base + CHAPTER)
            other.get_by_role("checkbox").uncheck()
            expect(page.locator(MARK).first).to_be_hidden()
            assert page.evaluate("key => localStorage.getItem(key)", other_key) == "true"
            other.get_by_role("checkbox").check()
            expect(page.locator(MARK).first).to_have_js_property("hidden", False)
            # Contents on the introduction, sidebar and phone all reflect stored marks.
            page.goto(base + "index.html")
            expect(page.locator(".prose " + MARK)).to_be_visible()
            if width == 390:
                page.locator(".mobile-contents > summary").click()
                expect(page.locator(".mobile-contents " + MARK)).to_be_visible()
            else:
                expect(page.locator(".book-sidebar " + MARK)).to_be_visible()
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth + 1")
            other.evaluate("localStorage.clear()")
            expect(page.locator(".prose " + MARK)).to_be_hidden()
            page.goto(base + "summary.html")
            expect(page.get_by_role("checkbox")).to_have_count(0)
            page.goto(base + CHAPTER)
            check.check()
            check.scroll_into_view_if_needed()
            dest = ROOT / "out" / "completion-review"
            dest.mkdir(parents=True, exist_ok=True)
            page.screenshot(path=str(dest / f"{width}-{theme}.png"))
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth + 1")
            print(f"{width}px {theme}: keyboard, reload, next, per-lesson isolation, cross-tab/clear and contents passed")
            context.close()
        # Denied reads/writes must not break reading or pretend the change was saved.
        context = browser.new_context()
        context.add_init_script("""Object.defineProperty(window, 'localStorage', {
            get() { throw new DOMException('Blocked', 'SecurityError'); }
        });""")
        page = context.new_page()
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(base + CHAPTER)
        page.get_by_role("checkbox").check()
        expect(page.get_by_role("checkbox")).to_be_checked()
        expect(page.get_by_role("status")).to_have_text("Progress could not be saved in this browser.")
        page.get_by_role("checkbox").uncheck()
        expect(page.locator(MARK).first).to_be_hidden()
        context.close()
        context = browser.new_context(java_script_enabled=False)
        page = context.new_page()
        page.goto(base + CHAPTER)
        expect(page.locator(".lesson-completion")).to_be_hidden()
        expect(page.locator(".pagination-next")).to_be_visible()
        context.close()
        browser.close()
        assert not errors, errors
        print("Blocked storage and no-JavaScript reading passed; no page errors.")
finally:
    server.shutdown()
