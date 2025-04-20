from __future__ import annotations
from abc import ABC, abstractmethod

from typing import List, Optional
from automacao_blaze_cassino import AutomacaoBlazeChrome
from .utils.utils_chrome import UtilityFunctions

import time

class IRoleta(ABC):
    """
    Roleta generica como se fosse um contrato em que todas as roletas
    vão compartilhar de seus metodos propios.
    """
    
    def __init__(self, nome_usuario: str, senha: str, nome: str, url_roleta: str):
        super().__init__()
        
        self.usuario = nome_usuario
        self.senha = senha
        self.url_roleta = url_roleta

        self._blaze = AutomacaoBlazeChrome(nome_usuario, senha, url_roleta)

        self.roleta = nome
        

        # Configurações iniciais
        self._rodada_refresh = 15
        self._resultados_catalogados: Optional[List[dict]] = []
        self.indice_ficha = 0 # número do índice da ficha levando em consideração que é do 0 até a quantidade de fichas, ex: 0 = R$: 2,50 e os demais respectivamente à sua sequência.
        self.numeros = None
        self.fichas = None
        self.rodada = 0
        self._status = 0
        self._gale = 1

        # Atributos fichas
        self.um_real = None
        self.dois_e_cinquenta = None
        self.cinco_reais = None
        self.vinte_e_cinco_reais = None
        self.cento_e_vinte_e_cinco_reais = None
        self.quinhentos_reais = None

        # Atributos Colunas e Duzias
        self.colunas = None
        self.duzias = None
        self.btn_coluna1 = None
        self.btn_coluna2 = None
        self.btn_coluna3 = None
        self.btn_duzia1 = None
        self.btn_duzia2 = None
        self.btn_duzia3 = None
    
    @abstractmethod
    def get_saldo(self) -> float: pass
    
    @abstractmethod
    def fechar_aviso_saldo_baixo(self) -> None:  pass
    
    @abstractmethod
    def mudar_frame(self) -> None:  pass
    
    @abstractmethod
    def login(self) -> None:  pass
    
    @abstractmethod
    def recent_numbers(self) -> List[int]:  pass
    
    @abstractmethod
    def catalogar_resultados(self, resultado: int) -> None:  pass
    
    @abstractmethod
    def encontrar_elementos_essenciais(self) -> None:  pass
    
    @abstractmethod
    def apostar(self, numeros: Optional[List[int]], duzias: Optional[List[int]], colunas: Optional[List[int]], aposta: Optional[int], nome: Optional[str]):  pass

    @abstractmethod
    def aguardar_fichas(self) -> None:  pass

    @abstractmethod
    def refresh(self, rodada, important) -> None:  pass


class AmericanRoulette(IRoleta):
    
    def __str__(self) -> str:
        return "American Roulette"
    
    def __init__(self, nome_usuario: str, senha: str, url_roleta: str) -> None:
        super().__init__(nome_usuario, senha, self.__str__(), url_roleta)
        
        print(f"Abrindo {self.__str__()}...")
        
        time.sleep(10)
        self.fechar_loc()
        time.sleep(1)
        self.mudar_frame()
        time.sleep(1)
        self.fechar_regras()
        time.sleep(1)
        self.encontrar_elementos_essenciais()
        
    # Especial da american fechar regras.
    def fechar_regras(self) -> None:
        """
        Fecha o aviso das regras do jogo se aparecer...
        """
        try:
            self._stake.driver.find_element(self._stake._CSS, "a.close--ed249").click()
        except Exception as error:
            self._stake.logger.warning(f"Error: {error}")

    def fechar_loc(self) -> None:
        """
        Fecha o aviso de erro de localização se aparecer...
        """
        try:
            self._stake.driver.find_element(self._stake._CSS, "span.StyledModalClose-sc-mv2bgq").click()
        except Exception as error:
            self._stake.logger.warning(f"Error: {error}")

    def fechar_aviso_saldo_baixo(self):
        """
        Fecha o aviso de saldo baixo, se estiver presente.
        """
        try:
            self._stake.driver.find_elements(self._stake._CSS, "div.restrictedMinWidth--1bcf0")[0].click()
        except Exception as error:
            print(error)

    def mudar_frame(self):
        """
        Troca para os iframes necessários para interagir com a roleta.
        """
        try:
            # Navega pelos iframes necessários
            frame = self._stake.driver.find_element(self._stake._CSS, "iframe.game")
            self._stake.driver.switch_to.frame(frame)
            time.sleep(1)
            frame1 = self._stake.driver.find_element(self._stake._CSS, "div.games-container iframe")
            self._stake.driver.switch_to.frame(frame1)
            time.sleep(1)
            print("Troca para iframe realizada com sucesso!")
        except Exception as error:
            print(error)

    def encontrar_elementos_essenciais(self):
        """
        Localiza os elementos principais no DOM para interação na roleta.
        """
        
        numeros_colunas_duzias = self._stake.driver.find_elements(self._stake._CSS, "g.dddStandard-wrapper rect")
        self.numeros = numeros_colunas_duzias[0: 35]
        numeros0 = self._stake.driver.find_elements(self._stake._CSS, "g.dddStandard-wrapper polygon.green_shape")
        self.numeros.insert(0, numeros0[0])
        self.numeros.append(numeros0[-1])
        self.fichas = self._stake.driver.find_elements(self._stake._CSS, "div.chipItem--7d58b")

        # Lista de fichas
        self.um_real = self.fichas[0]
        self.dois_e_cinquenta = self.fichas[1]
        self.cinco_reais = self.fichas[2]
        self.vinte_e_cinco_reais = self.fichas[3]
        self.cento_e_vinte_e_cinco_reais = self.fichas[4]
        self.quinhentos_reais = self.fichas[5]

        # Lista de botoes de Colunas e Duzias
        self.colunas = [
            numeros_colunas_duzias[38],
            numeros_colunas_duzias[37],
            numeros_colunas_duzias[36],
        ]
        self.duzias = [
            numeros_colunas_duzias[39],
            numeros_colunas_duzias[40],
            numeros_colunas_duzias[41],
        ]
        self.btn_coluna1 = numeros_colunas_duzias[38]
        self.btn_coluna2 = numeros_colunas_duzias[37]
        self.btn_coluna3 = numeros_colunas_duzias[36]
        self.btn_duzia1 = numeros_colunas_duzias[39]
        self.btn_duzia2 = numeros_colunas_duzias[40]
        self.btn_duzia3 = numeros_colunas_duzias[41]
        
        self.btn2x = self._stake.driver.find_element(self._stake._CSS, "div.doubleRepeatButtonWrapper--54937 button")
        self.btn_desfazer = self._stake.driver.find_element(self._stake._CSS, "div.undoButtonWrapper--5a8a0 button")

    def get_saldo(self):
        return UtilityFunctions.converter_para_float(self._stake.driver.find_element(self._stake._CSS, "span.amount--f8dd5").text)

    def login(self):
        self._stake.login(self.usuario, self.senha, self.url_roleta)

    def recent_numbers(self):
        string_number = self._stake.driver.find_element(self._stake._CSS, "div.recentNumbers--141d3").text
        recent = UtilityFunctions.parse_numbers_from_string(string_number)
        return recent
    
    def catalogar_resultados(self, resultado):
        """
        Adiciona o resultado atual ao catálogo de resultados.

        Args:
            resultado (int): Número do resultado a ser catalogado.
        """
        relogio = UtilityFunctions.get_current_time()
        self.rodada += 1
        self._resultados_catalogados.append(
            {
                "numero": resultado,
                "criado_em": relogio,
                "rodada": self.rodada
            }
        )

    def aguardar_fichas(self):
        
        # Aguarda até que as fichas fiquem visíveis para a aposta
        while not self.fichas[0].is_displayed():
            continue
        
        return

    def apostar(self, numeros: Optional[List[int]], duzias: Optional[List[int]], colunas: Optional[List[int]], aposta: int):
        
        if numeros:
            
            self.um_real.click()
            time.sleep(0.1)
            for num in numeros[1:]:
                self.numeros[num].click()
                time.sleep(0.1)
            
            self.um_real.click()
            self.numeros[0].click()
            time.sleep(0.1)
            self.numeros[36].click()
            return
        
        elif duzias:
            print(f"Apostar em {duzias}")
            return
        
        elif colunas:
            try:
                if aposta == 0:
                    self.um_real.click()
                    time.sleep(0.5)
                    self.numeros[0].click()
                    time.sleep(0.5)
                    self.numeros[36].click()
                    time.sleep(0.5)
                    self.dois_e_cinquenta.click()
                    time.sleep(0.5)
                    self.colunas[colunas[0]].click()
                    time.sleep(0.5)
                    self.colunas[colunas[1]].click()
                    time.sleep(19)
                    return
            except Exception as error:
                self._stake.logger.warning(f"erro! ao tentar apostar: {error}")
                return
            try:
                if aposta == 1:

                    self.dois_e_cinquenta.click()
                    time.sleep(0.5)

                    self.numeros[0].click()
                    time.sleep(0.5)
                    self.numeros[36].click()
                    time.sleep(0.5)

                    self.cinco_reais.click()
                    time.sleep(0.5)
                    self.colunas[colunas[0]].click()
                    time.sleep(0.5)
                    self.colunas[colunas[1]].click()
                    time.sleep(19)
                    return
            except Exception as error:
                self._stake.logger.warning(f"erro! ao tentar apostar: {error}")
                return
            try:
                if aposta == 2:

                    self.um_real.click()
                    time.sleep(0.5)    
                    self.numeros[0].click()
                    time.sleep(0.5)
                    self.numeros[36].click()
                    time.sleep(0.5)
                    self.vinte_e_cinco_reais.click()
                    time.sleep(0.5)
                    self.colunas[colunas[0]].click()
                    time.sleep(0.5)
                    self.colunas[colunas[1]].click()
                    time.sleep(19)
                    return
            except Exception as error:
                self._stake.logger.warning(f"erro! ao tentar apostar: {error}")
                return

    def refresh(self, rodada, important):
        """
        Atualiza a página da roleta após um número específico de rodadas.

        Args:
            rodada (int): Número atual da rodada.
        """
        if important:
            self._stake.driver.refresh()
            time.sleep(10)
            self.mudar_frame()
            self.encontrar_elementos_essenciais()
            self.fechar_loc()
            self.fechar_regras()
            self._rodada_refresh = rodada + 15
            return            
        
        if rodada >= self._rodada_refresh:
            self._stake.driver.refresh()
            time.sleep(10)
            self.mudar_frame()
            self.encontrar_elementos_essenciais()
            self.fechar_loc()
            self.fechar_regras()
            self._rodada_refresh = rodada + 15
            return


class RoletaBrasileira(IRoleta):
    
    def __str__(self) -> str:
        return "Roleta Brasileira"
    
    def __init__(self, nome_usuario: str, senha: str, url_roleta: str, casa_aposta: str) -> None:
        super().__init__(nome_usuario, senha, self.__str__(), url_roleta, casa_aposta)
        
        print(f"Abrindo {self.__str__()}...")

        self.mudar_frame()
        time.sleep(1)
        self.fechar_regras()
        time.sleep(1)
        self.encontrar_elementos_essenciais()
        
    # Especial da american fechar regras.
    def fechar_regras(self) -> None:
        """#
        Fecha o aviso das regras do jogo se aparecer...
        """
        try:
            self._blaze.driver.find_element(self._blaze._CSS, "div.modal-close-button svg").click()
            self._blaze.logger.info("Regras fechadas com sucesso!")
        except Exception as error:
            self._blaze.logger.warning(f"Error: {error}")

    def fechar_aviso_saldo_baixo(self):
        """
        Fecha o aviso de saldo baixo, se estiver presente.
        """
        try:
            self._blaze.driver.find_elements(self._blaze._CSS, "div.restrictedMinWidth--1bcf0")[0].click()
        except Exception as error:
            print(error)

    def mudar_frame(self):
        """
        Troca para os iframes necessários para interagir com a roleta.
        """
        try:
            # Navega pelos iframes necessários
            frame = self._blaze.driver.find_element(self._blaze._CSS, "#main iframe")
            self._blaze.driver.switch_to.frame(frame)
            time.sleep(1)
            shadow_host = self._blaze.driver.find_element(self._blaze._CSS, "body game-container")
            shadow_root = self._blaze.driver.execute_script("return arguments[0].shadowRoot", shadow_host)
            frame1 = shadow_root.find_element(self._blaze._CSS, "iframe")
            self._blaze.driver.switch_to.frame(frame1)
            time.sleep(1)

            print("Troca para iframe realizada com sucesso!")
        except Exception as error:
            print(error)

    def encontrar_elementos_essenciais(self):
        """
        Localiza os elementos principais no DOM para interação na roleta.
        """
        
        # seletores
        container_numeros = "div.screen-main__table--lMQgQ svg g g.table-cell--Wz6uJ"
        fichas = "div.arrow-slider__scrollable-content svg"
        _2x = "div.action-button_double"
        
        numeros_colunas_duzias = self._blaze.driver.find_elements(self._blaze._CSS, container_numeros)
        self.numeros = numeros_colunas_duzias[13: 49]
        self.numeros.insert(0, numeros_colunas_duzias[0])
        self.fichas = self._blaze.driver.find_elements(self._blaze._CSS, fichas)

        # Lista de fichas
        self.cinquenta_centavos = self.fichas[0]
        self.um_real = self.fichas[1]
        self.dois_e_cinquenta = self.fichas[2]
        self.cinco_reais = self.fichas[3]
        self.vinte_reais = self.fichas[4]
        self.cinquenta_reais = self.fichas[5]
        self.cem_reais = self.fichas[6]
        self.quinhentos_reais = self.fichas[7]
        self.dois_mil_reais = self.fichas[8]
        self.cinco_mil_reais = self.fichas[9]

        # Lista de botoes de Colunas e Duzias
        self.colunas = [
            numeros_colunas_duzias[3],
            numeros_colunas_duzias[2],
            numeros_colunas_duzias[1],
        ]
        self.duzias = [
            numeros_colunas_duzias[4],
            numeros_colunas_duzias[5],
            numeros_colunas_duzias[6],
        ]
        self.btn_coluna1 = numeros_colunas_duzias[3]
        self.btn_coluna2 = numeros_colunas_duzias[2]
        self.btn_coluna3 = numeros_colunas_duzias[1]
        self.btn_duzia1 = numeros_colunas_duzias[4]
        self.btn_duzia2 = numeros_colunas_duzias[5]
        self.btn_duzia3 = numeros_colunas_duzias[6]
        
        self.btn2x = self._blaze.driver.find_element(self._blaze._CSS, _2x)
        self.btn_desfazer = None

    def get_saldo(self):
        return UtilityFunctions.converter_para_float(self._blaze.driver.find_element(self._blaze._CSS, "div.balance__value  div.fit-container__content--l2noR").text)

    def login(self):
        self._blaze.login(self.usuario, self.senha, self.url_roleta)

    def recent_numbers(self):
        """Obtém os números mais recentes do histórico da roleta da Blaze.

        Tenta recuperar os últimos números exibidos na interface da roleta da Blaze fazendo:
        1. Localiza o elemento do histórico usando o seletor CSS.
        2. Extrai o conteúdo de texto.
        3. Faz o parsing dos números a partir da string.

        Retorna:
            list: Uma lista de números recentemente sorteados (como inteiros). Retorna uma lista vazia em caso de erro.

        Levanta:
            Exception: Qualquer exceção ocorrida durante o processo é capturada, registrada como warning
                    e resulta no retorno de uma lista vazia. A exceção original não é propagada.

        Observação:
            A localização do elemento web depende da classe CSS atual da Blaze ('div.roulette-history--fOmuw'),
            que pode mudar e exigir atualização no código.
        """

        try:
            return UtilityFunctions.parse_numbers_from_string(self._blaze.driver.find_element(self._blaze._CSS, "div.roulette-history--fOmuw").text)
        except Exception as error:
            self._blaze.logger.warning(f"Erro ao pegar os números recentes: {error}")
            return []
    
    def catalogar_resultados(self, resultado):
        """
        Adiciona o resultado atual ao catálogo de resultados.

        Args:
            resultado (int): Número do resultado a ser catalogado.
        """
        relogio = UtilityFunctions.get_current_time()
        self.rodada += 1
        self._resultados_catalogados.append(
            {
                "numero": resultado,
                "criado_em": relogio,
                "rodada": self.rodada
            }
        )

    def aguardar_fichas(self):
        
        # Aguarda até que as fichas fiquem visíveis para a aposta
        while not self.fichas[0].is_displayed():
            continue
        
        return

    def apostar(self, numeros: Optional[List[int]], duzias: Optional[List[int]], colunas: Optional[List[int]], aposta: int):
        
        if numeros:
            if aposta == 0:
                self.cinquenta_centavos.click()
                time.sleep(0.1)
                for num in numeros:
                    self.numeros[num].click()
                    time.sleep(0.1)
                
                self.cinquenta_centavos.click()
                self.numeros[0].click()
                time.sleep(0.1)
                return 

            if aposta == 1: 
                self.um_real.click()
                time.sleep(0.1)
                for num in numeros:
                    self.numeros[num].click()
                    time.sleep(0.1)
                
                self.um_real.click()
                self.numeros[0].click()
                time.sleep(0.1)
                return
        
        elif duzias:
            print(f"Apostar em {duzias}")
            return
        
        elif colunas:
            try:
                if aposta == 0:
                
                    self.cinquenta_centavos.click()
                    time.sleep(0.1)
                    self.numeros[0].click()
                    time.sleep(0.1)

                    self.um_real.click()
                    time.sleep(0.1)
                    self.colunas[colunas[0]].click()
                    self.colunas[colunas[0]].click()
                    time.sleep(0.1)
                    self.colunas[colunas[1]].click()
                    self.colunas[colunas[1]].click()
                    time.sleep(0.1)
                    return
            except Exception as error:
                self._blaze.logger.warning(f"erro! ao tentar apostar: {error}")
                return
            try:
                if aposta == 1:

                    self.um_real.click()
                    time.sleep(0.1)
                    self.numeros[0].click()
                    time.sleep(0.1)

                    self.cinco_reais.click()
                    time.sleep(0.1)
                    for _ in range(0, 3):
                        self.colunas[colunas[0]].click()
                        time.sleep(0.1)
                        self.colunas[colunas[1]].click()
                        time.sleep(0.1)
                    return
            except Exception as error:
                self._blaze.logger.warning(f"erro! ao tentar apostar: {error}")
                return
            try:
                if aposta == 2:

                    self.um_real.click()
                    time.sleep(0.1)    
                    self.numeros[0].click()
                    self.numeros[0].click()
                    time.sleep(0.1)

                    self.cinco_reais.click()
                    time.sleep(0.1)
                    self.colunas[colunas[0]].click()
                    self.colunas[colunas[0]].click()
                    self.colunas[colunas[0]].click()
                    time.sleep(0.1)
                    self.colunas[colunas[1]].click()
                    self.colunas[colunas[1]].click()
                    self.colunas[colunas[1]].click()
                    time.sleep(0.1)
                    return
            except Exception as error:
                self._blaze.logger.warning(f"erro! ao tentar apostar: {error}")
                return

    def refresh(self, rodada, important):
        """
        Atualiza a página da roleta após um número específico de rodadas.

        Args:
            rodada (int): Número atual da rodada.
        """         
        
        if rodada >= self._rodada_refresh or important:
            self._blaze.driver.refresh()
            time.sleep(10)
            go_back = False
            tentativa = 0
            while tentativa < 3 and not go_back:
                try:
                    self.mudar_frame()
                    self.encontrar_elementos_essenciais()
                    self.fechar_regras()
                    go_back = True
                except ErrorRefresh as error:
                    tentativa += 1
                    self._blaze.logger.warning(f"Error: {error}")
            self._rodada_refresh = rodada + 15
            return


class ErrorRefresh(Exception):
    def __init__(self):
        super().__init__("erro ao tentar reiniciar a roleta por favor aguarde...",)
        

class ErrorAviator(Exception):
    def __init__(self):
        super().__init__("erro ao tentar reiniciar o aviator por favor aguarde...",)
