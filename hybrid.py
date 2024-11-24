import sys
import json
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

# Liste des mots-clés interdits
blocked_keywords = [
    "porn", "sex", "xxx", "adult", "nude", "hentai", "erotic", "fuck", "tits",
    "ass", "milf", "slut", "cum", "lesbian", "gay", "fetish", "sexy", "vagina",
    "penis", "orgasm", "pornographic", "cam", "webcam", "bukkake", "incest",
    "swingers", "dominatrix", "seduction", "bondage", "shemale", "strip", 
    "brothel", "hooker", "escort", "sexcam", "pornsite", "xvideos", "youjizz",
    "xhamster", "redtube", "adultfriendfinder", "adultwork", "spankwire",
    "tnaflix", "motherless", "altsite", "4tube", "eporner", "hqporner",
    "porn300", "porntrex", "onlyfans", "txxx", "hentaipulse", "hentaimama",
    "porntube", "porn300", "sextube", "xvideos.es", "xvideos.com.br",
    "hqporner.com", "nhentai", "hentaistream", "hentaicomix", "hentaihaven",
    "hentaihaven.org", "youjizz.com", "xtube", "dirty", "sexworld", "rimming",
    "gloryhole", "swing", "kinks", "fetishist", "seduce", "peep", "lust",
    "sensual", "rape", "squeeze", "tickling", "snuff", "hardcore", "adulting",
    "passion", "arousal", "lewd", "depraved", "scandalous", "skanky", "skank",
    "deviant", "racy", "wanton", "immoral", "obscene", "debauchery"
]

class HybridSurfer(QMainWindow):
    def __init__(self):
        super(HybridSurfer, self).__init__()

        self.setWindowTitle("Hybrid Browser")
        self.setGeometry(200, 100, 1280, 900)

        # Historique
        self.history_file = "history.json"
        self.browser_history = []

        # Définir le User-Agent par défaut
        self.default_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Hybrid-browser/1.0"

        # Créer les onglets
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.setCentralWidget(self.tabs)

        # Charger la première page
        self.add_new_tab()

        # Créer la barre d'outils
        navtb = QToolBar("Navigation")
        self.addToolBar(navtb)

        # Boutons de navigation
        back_btn = QAction("Retour", self)
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        navtb.addAction(back_btn)

        forward_btn = QAction("Avancer", self)
        forward_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navtb.addAction(forward_btn)

        reload_btn = QAction("Recharger", self)
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navtb.addAction(reload_btn)

        home_btn = QAction("Accueil", self)
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        add_tab_btn = QAction("Ajouter un onglet", self)
        add_tab_btn.triggered.connect(self.add_new_tab)
        navtb.addAction(add_tab_btn)

        settings_btn = QAction("Paramètres", self)
        settings_btn.triggered.connect(self.show_settings)
        navtb.addAction(settings_btn)

        # Barre d'URL
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.url_bar)

    def add_new_tab(self, url=None):
        """Ajoute un nouvel onglet avec une URL spécifiée ou Google Safe Search par défaut."""
        if not url or isinstance(url, bool):
            url = "https://www.google.com?safe=active"

        browser = QWebEngineView()

        # Définir le User-Agent spécifique
        browser.page().profile().setHttpUserAgent(self.default_user_agent)
        browser.setUrl(QUrl.fromUserInput(url))
        self.tabs.addTab(browser, "Nouvel Onglet")
        self.tabs.setCurrentWidget(browser)

        # Met à jour le titre de l'onglet après le chargement de la page
        def update_tab_title():
            current_index = self.tabs.indexOf(browser)
            title = browser.page().title()
            self.tabs.setTabText(current_index, title)

        browser.loadFinished.connect(update_tab_title)
        browser.urlChanged.connect(self.block_url)

    def block_url(self, q):
        """Vérifie si l'URL contient des mots bloqués et empêche la navigation si nécessaire."""
        url = q.toString().lower()
        if any(keyword in url for keyword in blocked_keywords):
            QMessageBox.warning(self, "Accès refusé", "Ce site est bloqué pour contenu inapproprié.")
            self.tabs.currentWidget().setUrl(QUrl("https://www.google.com?safe=active"))

    def close_current_tab(self, index):
        """Ferme l'onglet actuel."""
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    def navigate_home(self):
        """Navigue vers la page d'accueil."""
        self.tabs.currentWidget().setUrl(QUrl("https://www.google.com?safe=active"))

    def navigate_to_url(self):
        """Navigue vers l'URL entrée dans la barre d'adresse."""
        url = self.url_bar.text()
        if any(keyword in url.lower() for keyword in blocked_keywords):
            QMessageBox.warning(self, "Accès refusé", "Ce site est bloqué pour contenu inapproprié.")
            self.url_bar.setText("")
        else:
            q = QUrl.fromUserInput(url)
            if q.scheme() == "":
                q.setScheme("http")
            self.tabs.currentWidget().setUrl(q)

    def show_settings(self):
        """Affiche la fenêtre des paramètres."""
        QMessageBox.information(self, "Paramètres", "Paramètres non disponibles pour le moment.")

# Exécution de l'application
app = QApplication(sys.argv)
QApplication.setApplicationName("Hybrid Browser")

# Lancer le navigateur
window = HybridSurfer()
window.show()
sys.exit(app.exec_())

