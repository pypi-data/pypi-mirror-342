import difflib
from datetime import datetime, timedelta

class UtilityFunctions:
    """Uma classe que contém funções utilitárias para o sistema."""

    @staticmethod
    def parse_numbers_from_string(number_string: str) -> list:
        """
        Analisa uma sequência de números separados por '\n' em uma lista de inteiros.

        Argumentos:
        number_string (str): A sequência de entrada contendo números separados por '\n'.

        Retorna:
        list: Uma lista de inteiros analisados ​​da sequência.
        """
        try:
            return [int(num) for num in number_string.split('\n') if num.strip().isdigit()]
        except ValueError:
            raise ValueError("A sequência de entrada contém números inválidos.")

    @staticmethod
    def compare_strings(target: str, comparison: str, threshold: float = 0.8) -> bool:
        """
        Compare duas strings e determine se elas são compatíveis com base em um limite de similaridade.

        Argumentos:
        target (str): A string de destino a ser comparada.
        comparison (str): A string a ser comparada com o destino.
        threshold (float): O limite de similaridade (o padrão é 0,8).

        Retorna:
        bool: True se a similaridade estiver acima do limite, False caso contrário.
        """
        similarity = difflib.SequenceMatcher(None, target, comparison).ratio()
        return similarity >= threshold

    @staticmethod
    def reverse_number(input_value) -> int:
        """
        Inverte os dígitos de um número, seja fornecido como um inteiro ou uma string.

        Argumentos:
        input_value (int ou str): O número a ser revertido, fornecido como um inteiro ou string.

        Retorna:
        int: O número revertido como um inteiro.
        """
        try:
            # Converta a entrada em uma string, inverta-a e converta de volta para um inteiro
            reversed_number = int(str(input_value)[::-1])
            return reversed_number
        except (ValueError, TypeError):
            raise ValueError("A entrada deve ser um inteiro ou uma string representando um inteiro.")

    @staticmethod
    def get_current_time():
        """
        Obtem o minuto e o segundo atuais como inteiros.

        Retorna:
        objeto: Um objeto com atributos `minute` e `second`.
        """
        now = datetime.now()
        return type("TimeObject", (object,), {"hour": now.hour, "minute": now.minute, "second": now.second})()

    @staticmethod
    def adicionar_minutos(minutos_adicionais):
        """
        Adiciona um número de minutos ao tempo atual, ajustando a hora se necessário.

        Parâmetros:
            minutos_adicionais (int): O número de minutos a serem adicionados.

        Retorna:
            datetime.time: O novo horário ajustado.
        """
        # Converte o tempo_atual para um objeto datetime para facilitar a manipulação
        datetime_atual = datetime.combine(datetime.today(), datetime.now().time())
        
        # Adiciona os minutos usando timedelta
        novo_datetime = datetime_atual + timedelta(minutes=minutos_adicionais)
        
        # Retorna apenas a parte do tempo ajustada
        return novo_datetime.time()

    @staticmethod
    def converter_para_float(valor_str: str) -> float:
        """
        Converte uma string que representa um valor monetário em real (R$) para um número float.
        Remove caracteres Unicode invisíveis e formata o valor corretamente.

        Args:
            valor_str (str): String contendo o valor monetário, possivelmente com caracteres Unicode invisíveis.

        Returns:
            float: O valor convertido para float.

        Exemplo:
            >>> converter_para_float('\u2066\u2066R$\u2069 31,90\u2069')
            31.9
        """
        # Remove todos os caracteres Unicode invisíveis
        valor_str = ''.join(char for char in valor_str if char.isprintable())
        
        # Remove o símbolo de real (R$) e espaços em branco
        valor_str = valor_str.replace('R$', '').strip()
        
        # Substitui a vírgula por ponto para converter para float
        valor_str = valor_str.replace(',', '.')
        
        # Converte a string para float
        valor_float = float(valor_str)
        
        return valor_float

    @staticmethod
    def calcular_acrescimo(valor, porcentagem) -> float:
        """
        Calcula o valor de um número com um acréscimo percentual.

        Args:
            valor (float): O valor inicial ao qual o acréscimo será aplicado.
            porcentagem (float): A porcentagem de acréscimo a ser aplicada.

        Returns:
            float: O valor inicial com o acréscimo percentual aplicado.
        
        Exemplo:
            >>> calcular_acrescimo(100.0, 20)
            120.0
        """
        # Calcula o valor do acréscimo
        acrescimo = valor * (porcentagem / 100)
        
        # Retorna o valor original mais o acréscimo
        return float(valor + acrescimo)

    @staticmethod
    def string_para_datetime(hora_string):
        """
        Converte uma string no formato "HH:MM:SS" para um objeto datetime.datetime
        (usando a data atual)
        
        Args:
            hora_string (str): String no formato "21:32:20"
        
        Returns:
            datetime.datetime: Objeto datetime com a hora convertida e data atual
        """
        horas, minutos, segundos = map(int, hora_string.split(':'))
        agora = datetime.now()
        return datetime(agora.year, agora.month, agora.day, horas, minutos, segundos)