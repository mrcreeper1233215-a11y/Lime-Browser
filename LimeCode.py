import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QPushButton
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile
from PyQt6.QtCore import QUrl

class LimeBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lime Browser")
        self.resize(1200, 800)

        # Setup Persistent Storage (Saves Login/Cookies)
        storage_path = os.path.join(os.getenv('APPDATA'), 'Lime', 'Profile')
        if not os.path.exists(storage_path):
            os.makedirs(storage_path)
            
        self.profile = QWebEngineProfile("LimeProfile", QWebEngineProfile.defaultProfile())
        self.profile.setPersistentStoragePath(storage_path)

        # Setup Tabs
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        
        # Add "+" button
        self.add_tab_btn = QPushButton("+")
        self.add_tab_btn.clicked.connect(lambda: self.add_new_tab("https://www.google.com"))
        self.tabs.setCornerWidget(self.add_tab_btn)
        
        self.add_new_tab("https://www.google.com")
        self.setCentralWidget(self.tabs)

    def add_new_tab(self, url):
        # Create browser with the persistent profile
        browser = QWebEngineView(self.profile)
        browser.setUrl(QUrl(url))
        
        # Auto-update tab title
        browser.page().titleChanged.connect(lambda title, b=browser: self.tabs.setTabText(self.tabs.indexOf(b), title))
        
        self.tabs.addTab(browser, "Loading...")
        self.tabs.setCurrentIndex(self.tabs.count() - 1)

    def close_tab(self, i):
        # 1. Get the browser widget for this tab
        browser = self.tabs.widget(i)
        
        # 2. Stop the browser and delete it to kill audio/video processes
        if browser:
            browser.page().deleteLater()
            browser.deleteLater()
            
        # 3. Remove the tab from the UI
        self.tabs.removeTab(i)
        
        # 4. If no tabs are left, close the whole application
        if self.tabs.count() == 0:
            self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LimeBrowser()
    window.show()
    sys.exit(app.exec())
