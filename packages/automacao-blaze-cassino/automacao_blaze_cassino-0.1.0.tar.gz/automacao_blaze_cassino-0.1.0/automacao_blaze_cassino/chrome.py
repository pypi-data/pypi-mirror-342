from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
from typing import Optional
import logging


class AutomacaoBlazeChrome:
    """
    Classe responsável por automatizar interações com o site Stake.bet, incluindo login e navegação até a roleta.

    Esta classe utiliza o Selenium para controlar um navegador Chrome, permitindo a automação de tarefas como aceitar cookies,
    realizar login e navegar até uma página específica de roleta.

    Atributos:
        profile_dir (str): Diretório onde o perfil do Chrome será armazenado. Padrão é "selenium_profile_chrome".
        driver (Optional[WebDriver]): Instância do WebDriver do Selenium para controlar o navegador.
        btn_coockes (Optional[WebElement]): Elemento do botão de aceitação de cookies.
        btn_entrar (Optional[WebElement]): Elemento do botão de login.
        _CSS (str): Constante para o seletor CSS.

    Métodos:
        __init__(self, nome_de_usuario: str, senha: str, roleta: str, profile_dir: str = "selenium_profile_chrome"):
            Inicializa a automação, configurando o perfil do Chrome, iniciando o navegador e realizando as interações iniciais.

        encontrar_elementos_iniciais(self):
            Localiza os elementos iniciais da página, como o botão de cookies e o botão de login.

        configure_chrome_profile(self, profile_dir: str) -> ChromeOptions:
            Configura o perfil do Chrome para salvar cookies e histórico no diretório especificado.

        login(self, usuario: str, senha: str, url_roleta: str) -> None:
            Realiza o login no site Stake.bet com as credenciais fornecidas e navega até a URL da roleta especificada.
    """

    def __init__(self, nome_de_usuario: str, senha: str, roleta: str, profile_dir: str = "selenium_profile_chrome"):
        """
        Inicializa a automação, configurando o perfil do Chrome, iniciando o navegador e realizando as interações iniciais.

        Args:
            nome_de_usuario (str): Nome de usuário para login no site Stake.bet.
            senha (str): Senha para login no site Stake.bet.
            roleta (str): URL da roleta para onde o navegador será direcionado após o login.
            profile_dir (str): Diretório onde o perfil do Chrome será armazenado. Padrão é "selenium_profile_chrome".
        """
        # Configuração do logging
        logging.basicConfig(
            filename="automacao_Blaze.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            encoding="utf-8"
        )
        self.logger = logging.getLogger("AutomacaoBlaze")

        self.profile_dir = profile_dir
        self.driver: Optional[WebDriver] = None
        
        self._CSS = "css selector"
        
        # elementos do DOM
        self.btn_coockes: Optional[WebElement] = None
        self.btn_entrar: Optional[WebElement] = None
        
        chrome_options = self.configure_chrome_profile(self.profile_dir)

        # Baixa e instala o chromedriver automaticamente
        driver_path = ChromeDriverManager().install()

        # Inicializa o driver do Chrome
        service = Service(executable_path=driver_path)
        
        self.driver = Chrome(service=service, options=chrome_options)
        
        # Remove a detecção de automação
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        # Abre uma página
        self.driver.get("https://blaze.bet.br/pt/?modal=auth")

        time.sleep(10)

        # Iniciar as interações.
        self.encontrar_elementos_iniciais()
        # Tenta clicar no botão de cookies do site.
        try:
            self.btn_coockes.click()
            self.logger.info("Cookies aceitos com sucesso.")
        except Exception as e:
            self.logger.warning("Cookies já aceitos ou elemento não encontrado.")
        # Executa o login recebendo os parâmetros passados para a classe 'nome_de_usuario', 'senha'.
        self.login(nome_de_usuario, senha, roleta)

    def encontrar_elementos_iniciais(self):
        """
        Localiza os elementos iniciais da página, como o botão de cookies e o botão de login.
        Este método utiliza seletores CSS para encontrar os elementos na página e atribuí-los aos atributos da classe.
        """
        # Bateria de seletores css baseados em classes e ids
        btn_coockes = "div.policy-regulation-button-container button"
        entrar = "div.input-footer button"

        try:
            self.btn_coockes = self.driver.find_element(self._CSS, btn_coockes)
            self.logger.info("Elemento de cookies encontrado com sucesso.")
        except Exception as e:
            self.logger.error("Erro ao encontrar o elemento de cookies.")
        try:
            self.btn_entrar = self.driver.find_element(self._CSS, entrar)
            self.logger.info("Elemento de login encontrado com sucesso.")
        except Exception as e:
            self.logger.error("Erro ao encontrar o elemento de login.")

    def configure_chrome_profile(self, profile_dir):
        """
        Configura o perfil do Chrome para salvar cookies e histórico no diretório especificado.
        Args:
            profile_dir (str): Diretório onde o perfil do Chrome será armazenado.
        Returns:
            ChromeOptions: Opções configuradas para o perfil do Chrome.
        """
        # Obtém o diretório atual
        diretorio_atual = os.getcwd()
        # Define o diretório do perfil do Chrome para salvar cookies e histórico
        profile_path = os.path.expanduser(f"{diretorio_atual}/{profile_dir}")
        if not os.path.exists(profile_path):
            os.makedirs(profile_path)
            self.logger.info(f"Diretório do perfil criado: {profile_path}")

        chrome_options = ChromeOptions()
        chrome_options.add_argument("--start-maximized") # vai abrir em tela cheia...
        chrome_options.add_argument(f"--user-data-dir={profile_path}")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        return chrome_options

    def login(self, usuario: str, senha: str, url_roleta: str) -> None:
        """
        Realiza o login no site Stake.bet com as credenciais fornecidas e navega até a URL da roleta especificada.

        Args:
            usuario (str): Nome de usuário para login.
            senha (str): Senha para login.
            url_roleta (str): URL da roleta para onde o navegador será direcionado após o login.
        """
        try:
            self.driver.find_elements("css selector", "button.age-verification-button")[0].click()
            time.sleep(3)
        except Exception:
            self.logger.warning("Aviso inexistente ou não encontrado.")
        try:
            # Seletores css baseados em classes e ids
            username = "username"
            password = "password"
            
            self.driver.find_element("name", username).send_keys(usuario)
            time.sleep(0.8)
            self.driver.find_element("name", password).send_keys(senha)
            time.sleep(0.8)
            self.btn_entrar.click()
            self.logger.info("Login realizado com sucesso.")
            time.sleep(5)
        except Exception as e:
            self.logger.warning("Erro ao realizar login. Possivelmente já logado.")
        try:
            self.driver.get(url_roleta)
            self.logger.info(f"Navegando até {url_roleta}")
        except Exception as error:
            self.logger.warning(f"{error}")
        time.sleep(10)