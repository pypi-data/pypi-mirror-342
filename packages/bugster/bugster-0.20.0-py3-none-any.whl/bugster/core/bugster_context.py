from playwright.sync_api import BrowserContext
from bugster.core.base_page import BugsterPage


class BugsterContext:
    """
    A custom browser context abstraction that:
    - Wraps Playwright's BrowserContext with extra functionality
    - Creates BugsterPage instances instead of regular Page objects
    - Provides consistent configuration across all pages
    """

    def __init__(self, context: BrowserContext):
        self._context = context
        self.screenshot = False  # Default screenshot setting for all pages
        self._pages = []  # Track pages created by this context
        self.pages = []

    def new_page(self) -> BugsterPage:
        """
        Create a new BugsterPage with the current context settings.
        """
        page = self._context.new_page()
        bugster_page = BugsterPage(page, context=self)
        bugster_page.screenshot = True

        if self.pages:
            bugster_page.screenshot_index = self.pages[-1].screenshot_index

        self._pages.append(bugster_page)  # Track the page
        return bugster_page

    def set_screenshot_mode(self, enabled: bool = True):
        """
        Enable or disable screenshots for this context and all its pages.
        """
        self.screenshot = enabled
        # Update all existing pages
        for page in self._pages:
            page.screenshot = enabled

    def close(self):
        """
        Close the browser context.
        """
        self._context.close()

    def __getattr__(self, item):
        # Fallback to underlying context attributes if not defined here
        return getattr(self._context, item)

    def goto(self, url: str, **kwargs) -> BugsterPage:
        """
        Create a new page and navigate to the specified URL.
        
        Args:
            url: The URL to navigate to
            **kwargs: Additional arguments for page.goto()
            
        Returns:
            A BugsterPage instance
        """
        page = self.new_page()

        if kwargs:
            page.goto(url, **kwargs)
        else:
            page.goto(url, wait_until='domcontentloaded', timeout=30000)

        return page 
        
    def expect_page(self, **kwargs):
        """
        Creates a waiting context that waits for a new page to be created.
        
        Args:
            **kwargs: Additional arguments for context.expect_page()
            
        Returns:
            A context manager that returns a wrapped page_info with BugsterPage
        """
        original_page_info = self._context.expect_page(**kwargs)
        
        # Store the current page that's initiating this expect_page call
        # We'll use this to get the screenshot index
        initiating_page = None
        if self._pages and len(self._pages) > 0:
            # Assume the last page in the list is the current one
            initiating_page = self._pages[-1]
        
        class WrappedPageInfo:
            def __init__(self, original, bugster_context, source_page):
                self._original = original
                self._bugster_context = bugster_context
                self._source_page = source_page
                self.value = None
            
            def __enter__(self):
                self._page_info = self._original.__enter__()
                return self
            
            def __exit__(self, exc_type, exc_val, exc_tb):
                result = self._original.__exit__(exc_type, exc_val, exc_tb)
                
                # Get the page from the original page_info
                if hasattr(self._page_info, 'value') and self._page_info.value is not None:
                    page = self._page_info.value
                    bugster_page = BugsterPage(page, context=self._bugster_context)
                    
                    # Set screenshot properties based on the source page
                    bugster_page.screenshot = True
                    
                    # Get the next screenshot index from the source page
                    if self._source_page and hasattr(self._source_page, 'screenshot_index'):
                        next_index = self._source_page.screenshot_index + 1
                        print(f"Using source page's screenshot_index: {self._source_page.screenshot_index} + 1 = {next_index}")
                    else:
                        # Fallback if no source page or it has no screenshot_index
                        next_index = 0
                        for p in self._bugster_context._pages:
                            if hasattr(p, 'screenshot_index'):
                                next_index = max(next_index, p.screenshot_index + 1)
                        print(f"Calculated next_index from all pages: {next_index}")
                    
                    bugster_page.screenshot_index = next_index
                    print(f"Setting new page screenshot_index to: {next_index}")
                    
                    self._bugster_context._pages.append(bugster_page)  # Track the page
                    self.value = bugster_page
                    
                    # Verify the screenshot index was set correctly
                    print(f"Verification - new page has screenshot_index: {self.value.screenshot_index}")
                return result
        
        return WrappedPageInfo(original_page_info, self, initiating_page)         

