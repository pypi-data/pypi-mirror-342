"""
Enhanced Playwright scraper with anti-detection features.
"""
from typing import Dict, Any, Optional

from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page

from .scraper import PlaywrightScraper

class PhantomPlaywrightScraper(PlaywrightScraper):
    """Playwright scraper with enhanced anti-detection capabilities."""

    def __init__(self, headless: bool = True, navigation_timeout: int = PlaywrightScraper.DEFAULT_NAVIGATION_TIMEOUT):
        """Initialize the phantom scraper.
        
        Args:
            headless: Whether to run the browser in headless mode.
            navigation_timeout: Maximum time in milliseconds to wait for navigation.
        """
        super().__init__(headless=headless, navigation_timeout=navigation_timeout)
        self._stealth_script = self._get_stealth_script()
        
    def _get_browser_launch_options(self) -> Dict[str, Any]:
        """Get browser launch options with anti-detection features.
        
        Returns:
            Dictionary of browser launch options.
        """
        options = super()._get_browser_launch_options()
        options["args"].extend([
            '--disable-blink-features=AutomationControlled',
            '--disable-dev-shm-usage',  # Overcome limited resource problems
            '--disable-accelerated-2d-canvas',  # Reduce detection surface
            '--no-first-run',
            '--no-default-browser-check',
            '--use-gl=angle',  # Use ANGLE instead of SwiftShader
            '--use-angle=default',  # Default ANGLE backend
            '--window-size=1280,720',  # Match test expectations
            '--start-maximized'
        ])
        return options
        
    def _get_context_options(self) -> Dict[str, Any]:
        """Get browser context options with anti-detection features.
        
        Returns:
            Dictionary of context options.
        """
        options = super()._get_context_options()
        options.update({
            "user_agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/121.0.0.0 Safari/537.36"
            ),
            "viewport": {
                "width": 1280,
                "height": 720
            },
            "screen": {
                "width": 1280,
                "height": 720
            },
            "java_script_enabled": True,
            "bypass_csp": True,  # Bypass Content Security Policy
            "ignore_https_errors": True,
            "has_touch": False,
            "is_mobile": False,
            "locale": "en-US",
            "timezone_id": "America/New_York"
        })
        return options

    def open(self) -> 'PhantomPlaywrightScraper':
        """Initialize and open the browser with anti-detection measures.
        
        Returns:
            Self for method chaining.
            
        Raises:
            RuntimeError: If browser is already open.
        """
        super().open()
        
        # Add stealth script
        self._page.add_init_script(self._stealth_script)
        
        return self
        
    def _get_stealth_script(self) -> str:
        """Get the JavaScript code for anti-detection.
        
        Returns:
            JavaScript code as string.
        """
        return """
        // Pass the Webdriver test by setting it to false
        Object.defineProperty(navigator, 'webdriver', {
            get: () => false,
            configurable: true,
            enumerable: true
        });

        // Pass Chrome test
        window.chrome = {
          runtime: {},
          webstore: {},
          app: {
            InstallState: 'hehe',
            RunningState: 'ready',
            isInstalled: false,
            getDetails: function() {},
            getIsInstalled: function() {},
            runningState: function() {}
          }
        };

        // Pass Plugins Length Test
        Object.defineProperty(navigator, 'plugins', {
          get: () => [1, 2, 3, 4, 5].map(() => ({
            name: 'Chrome PDF Plugin',
            filename: 'internal-pdf-viewer',
            description: 'Portable Document Format',
            length: 1
          }))
        });

        // Pass Languages Test
        Object.defineProperty(navigator, 'languages', {
          get: () => ['en-US', 'en'],
        });

        // WebGL vendor spoofing
        (() => {
            // Store original functions
            const getParameterProto = WebGLRenderingContext.prototype.getParameter;
            const getExtensionProto = WebGLRenderingContext.prototype.getExtension;
            
            // Constants for WebGL debug info
            const UNMASKED_VENDOR_WEBGL = 0x9245;
            const UNMASKED_RENDERER_WEBGL = 0x9246;
            
            // Create a fake debug info extension
            const fakeDebugInfo = {
                UNMASKED_VENDOR_WEBGL,
                UNMASKED_RENDERER_WEBGL
            };
            
            // Override getExtension
            WebGLRenderingContext.prototype.getExtension = function(name) {
                if (name === 'WEBGL_debug_renderer_info') {
                    return fakeDebugInfo;
                }
                return getExtensionProto.apply(this, [name]);
            };
            
            // Override getParameter
            WebGLRenderingContext.prototype.getParameter = function(parameter) {
                // UNMASKED_VENDOR_WEBGL
                if (parameter === UNMASKED_VENDOR_WEBGL) {
                    return 'Intel Inc.';
                }
                // UNMASKED_RENDERER_WEBGL
                if (parameter === UNMASKED_RENDERER_WEBGL) {
                    return 'Intel Iris OpenGL Engine';
                }
                return getParameterProto.apply(this, [parameter]);
            };

            // Do the same for WebGL2 if it exists
            if (typeof WebGL2RenderingContext !== 'undefined') {
                const getParameterProto2 = WebGL2RenderingContext.prototype.getParameter;
                const getExtensionProto2 = WebGL2RenderingContext.prototype.getExtension;
                
                WebGL2RenderingContext.prototype.getExtension = function(name) {
                    if (name === 'WEBGL_debug_renderer_info') {
                        return fakeDebugInfo;
                    }
                    return getExtensionProto2.apply(this, [name]);
                };
                
                WebGL2RenderingContext.prototype.getParameter = function(parameter) {
                    if (parameter === UNMASKED_VENDOR_WEBGL) {
                        return 'Intel Inc.';
                    }
                    if (parameter === UNMASKED_RENDERER_WEBGL) {
                        return 'Intel Iris OpenGL Engine';
                    }
                    return getParameterProto2.apply(this, [parameter]);
                };
            }
        })();

        // Notification API
        window.Notification = {
          permission: 'default'
        };

        // Platform
        Object.defineProperty(navigator, 'platform', {
          get: () => 'Win32'
        });

        // Hardware Concurrency
        Object.defineProperty(navigator, 'hardwareConcurrency', {
          get: () => 8
        });

        // Device Memory
        Object.defineProperty(navigator, 'deviceMemory', {
          get: () => 8
        });
        """ 