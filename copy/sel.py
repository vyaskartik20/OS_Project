# import unittest
# from selenium import webdriver

# class GoogleOrgSearch(unittest.TestCase):

#     def setUp(self):
#         self.driver = webdriver.Chrome(executable_path="/home/vyas20/Downloads/chromedriver_linux64/chromedriver")
#     def test_google_search_page(self):
#         driver = self.driver
#         driver.get("http://www.cdot.in")
#         window_before = driver.window_handles[0]
#         print (window_before)
#         driver.find_element_by_xpath("//a[@href='http://www.cdot.in/home.htm']").click()
#         window_after = driver.window_handles[1]
#         driver.switch_to_window(window_after)
#         print (window_after)
#         driver.find_element_by_link_text("ATM").click()
#         driver.switch_to_window(window_before)

#     def tearDown(self):
#         self.driver.close()

# # if __name__ == "__main__":
# unittest.main()


# from selenium import webdriver
# driver = webdriver.Chrome(executable_path="/home/vyas20/Downloads/chromedriver_linux64/chromedriver")

# # driver.get("https://selenium.dev")
# print(driver.current_url)
# print(driver.title)


# from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# # Start the driver

# driver = webdriver.Chrome(executable_path="/home/vyas20/Downloads/chromedriver_linux64/chromedriver")
# # Open URL
# driver.get("https://seleniumhq.github.io")

# # Setup wait for later
# wait = WebDriverWait(driver, 10)

# # Store the ID of the original window
# original_window = driver.current_window_handle

# # Check we don't have other windows open already
# print(len(driver.window_handles))
# exit()

# # Click the link which opens in a new window
# # driver.find_element(By.LINK_TEXT, "new window").click()

# # Wait for the new window or tab
# # wait.until(EC.number_of_windows_to_be(2))

# # Loop through until we find a new window handle
# for window_handle in driver.window_handles:
#     if window_handle != original_window:
#         driver.switch_to.window(window_handle)
#         break

# # Wait for the new tab to finish loading content
# wait.until(EC.title_is("SeleniumHQ Browser Automation"))


# import uiautomation as auto


# class BrowserWindow:
#     def __init__(self, browser_name, window_index=1):
#         """
#         A Browser Window support UIAutomation.

#         :param browser_name: Browser name, support 'Google Chrome', 'Firefox', 'Edge', 'Opera', etc.
#         :param window_index: Count from back to front, default value 1 represents the most recently created window.
#         """
#         if browser_name == 'Firefox':
#             addr_bar = auto.Control(Depth=1, ClassName='MozillaWindowClass', foundIndex=window_index) \
#                 .ToolBarControl(AutomationId='nav-bar').ComboBoxControl(Depth=1, foundIndex=1) \
#                 .EditControl(Depth=1, foundIndex=1)
#         else:
#             win = auto.Control(Depth=1, ClassName='Chrome_WidgetWin_1', SubName=browser_name, foundIndex=window_index)
#             win_pane = win.PaneControl(Depth=1, Compare=lambda control, _depth: control.Name != '')
#             if browser_name == 'Edge':
#                 addr_pane = win_pane.PaneControl(Depth=1, foundIndex=1).PaneControl(Depth=1, foundIndex=2) \
#                     .PaneControl(Depth=1, foundIndex=1).ToolBarControl(Depth=1, foundIndex=1)
#             elif browser_name == 'Opera':
#                 addr_pane = win_pane.GroupControl(Depth=1, foundIndex=1).PaneControl(Depth=1, foundIndex=1) \
#                     .PaneControl(Depth=1, foundIndex=2).GroupControl(Depth=1, foundIndex=1) \
#                     .GroupControl(Depth=1, foundIndex=1).ToolBarControl(Depth=1, foundIndex=1) \
#                     .EditControl(Depth=1, foundIndex=1)
#             else:
#                 addr_pane = win_pane.PaneControl(Depth=1, foundIndex=2).PaneControl(Depth=1, foundIndex=1) \
#                     .PaneControl(Depth=1, Compare=lambda control, _depth:
#                 control.GetFirstChildControl() and control.GetFirstChildControl().ControlTypeName == 'ButtonControl')
#             addr_bar = addr_pane.GroupControl(Depth=1, foundIndex=1).EditControl(Depth=1)
#         assert addr_bar is not None
#         self.addr_bar = addr_bar

#     @property
#     def current_tab_url(self):
#         """Get current tab url."""
#         return self.addr_bar.GetValuePattern().Value

#     @current_tab_url.setter
#     def current_tab_url(self, value: str):
#         """Set current tab url."""
#         self.addr_bar.GetValuePattern().SetValue(value)


# browser = BrowserWindow('Google Chrome')

# print(browser.current_tab_url)
# browser.current_tab_url = 'www.google.com'
# print(browser.current_tab_url)

# from pywinauto import Application
# app = Application(backend='uia')
# app.connect(title_re=".*Chrome.*")
# element_name="Address and search bar"
# dlg = app.top_window()
# url = dlg.child_window(title=element_name, control_type="Edit").get_value()
# print(url)


# https://www.oreilly.com/library/view/x-window-system/9780937175149/Chapter08.html
# https://www.google.com/search?q=how+to+get+url+of+chrome+tabs+using+python&oq=how+to+get+url+of+chrome+tabs+using+python&aqs=chrome..69i57.12685j0j1&sourceid=chrome&ie=UTF-8
# https://www.quora.com/How-can-we-get-a-current-URL-running-on-Google-Chrome-to-my-Python-code
# https://stackoverflow.com/questions/25614391/internet-history-script-for-google-chrome
# https://www.tutorialfor.com/questions-307690.htm
# https://unix.stackexchange.com/questions/241658/is-there-a-way-to-get-the-url-from-current-tab-in-google-chrome
# https://medium.com/@tarunkhare54321/track-website-browsing-time-using-python-838552fc0ede
# https://www.reddit.com/r/learnprogramming/comments/409jos/python_3_how_to_get_the_url_of_all_open_tabs_in/
# https://chrome.google.com/webstore/detail/copy-all-urls/djdmadneanknadilpjiknlnanaolmbfk/related?hl=en
# https://superuser.com/questions/117754/is-there-a-way-to-copy-urls-from-all-open-tabs-in-a-google-chrome-or-other-brow
# https://stackoverflow.com/questions/52675506/get-chrome-tab-url-in-python
