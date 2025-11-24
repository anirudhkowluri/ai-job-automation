from job_agent.utils.browser import BrowserManager
import time

def test_browser_launch():
    print("Testing browser launch...")
    manager = BrowserManager(headless=True)
    try:
        page = manager.start()
        page.goto("https://www.google.com")
        title = page.title()
        print(f"Page title: {title}")
        assert "Google" in title
        print("Browser launch test passed!")
    except Exception as e:
        print(f"Browser launch test failed: {str(e).encode('utf-8', errors='ignore').decode('utf-8')}")
    finally:
        manager.stop()

if __name__ == "__main__":
    test_browser_launch()
