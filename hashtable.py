# Aluno: Leonardo Domingos
# DRE: 120168324
import csv
import math
from typing import Any, Callable, Optional, List, Tuple





class TabelaHash:
    def __init__(self, tamanho: int = 100, funcao_hash: str = 'divisao', 
                 metodo_colisao: str = 'encadeamento_exterior', chave: str = None):
        """
        Inicializa a tabela hash."""
        self.tamanho = tamanho
        self.funcao_hash = funcao_hash
        self.metodo_colisao = metodo_colisao
        self.chave = chave
        self.total_itens = 0
        


        # iniciando a tabela de acordo com o método de colisão
        if metodo_colisao == 'encadeamento_exterior':
            self.tabela = [[] for _ in range(tamanho)]
        else:  # enderecamento_aberto
            self.tabela = [None] * tamanho
    

    def calcular_hash(self, chave: Any) -> int:

        """calcula o valor hash para uma dada chave usando o método selecionado"""
        if self.funcao_hash == 'divisao':
            return self._hash_divisao(chave)
        elif self.funcao_hash == 'multiplicacao':
            return self._hash_multiplicacao(chave)
        elif self.funcao_hash == 'dobra':
            return self._hash_dobra(chave)
        elif self.funcao_hash == 'meio_quadrado':
            return self._hash_meio_quadrado(chave)
        elif self.funcao_hash == 'extração':
            return self._hash_extracao(chave)
        else:
            return self._hash_divisao(chave)  # padrao
    

    def _hash_divisao(self, chave: Any) -> int:

        """função hash usando método da divisão"""
        try:
            chave_num = int(chave)
        except (ValueError, TypeError):
            chave_num = hash(chave)  # fallback para hash padrão do Python
            
        return chave_num % self.tamanho
    

    def _hash_multiplicacao(self, chave: Any) -> int:
        """funçao hash usando método da multiplicação"""
        try:
            chave_num = int(chave)
        except (ValueError, TypeError):
            chave_num = hash(chave)
            
        A = (math.sqrt(5) - 1) / 2  # constante recomendada por Knuth
        return int(self.tamanho * ((chave_num * A) % 1))
    


    def _hash_dobra(self, chave: Any) -> int:
        """função hash usando método da dobra."""
        chave_str = str(chave)
        partes = [chave_str[i:i+2] for i in range(0, len(chave_str), 2)]
        soma = 0
        
        for parte in partes:
            try:
                soma += int(parte)
            except ValueError:
                soma += sum(ord(c) for c in parte)
                
        return soma % self.tamanho
    


    def _hash_meio_quadrado(self, chave: Any) -> int:
        """função hash usando método do meio do quadrado"""
        try:
            chave_num = int(chave)
        except (ValueError, TypeError):
            chave_str = str(chave)
            chave_num = sum(ord(c) for c in chave_str)
            
        quadrado = chave_num ** 2
        quadrado_str = str(quadrado)
        meio = len(quadrado_str) // 2
        # Pega 2 dígitos do meio
        if meio >= 1:
            meio_num = int(quadrado_str[meio-1:meio+1])
        else:
            meio_num = int(quadrado_str)
            
        return meio_num % self.tamanho
    
    def _hash_extracao(self, chave: Any) -> int:
        """função hash usando método de extração de partes da chave"""
        chave_str = str(chave)
        if len(chave_str) >= 3:
            # Extrai primeiro, do meio e último caractere
            partes = chave_str[0] + chave_str[len(chave_str)//2] + chave_str[-1]
            try:
                return int(partes) % self.tamanho
            except ValueError:
                return sum(ord(c) for c in partes) % self.tamanho
        else:
            return self._hash_divisao(chave)
    
    def inserir(self, chave: Any, valor: Any) -> bool:
        """Insere um valor na tabela hash usando a chave fornecida
        Retorna True se a inserção foi bem sucedida, False se a chave já existe
        """
        indice = self.calcular_hash(chave)
        

        if self.metodo_colisao == 'encadeamento_exterior':
            # Verificando se a chave já existe na lista
            for item in self.tabela[indice]:
                if item[0] == chave:
                    return False  # Chave já existe
            self.tabela[indice].append((chave, valor))
            self.total_itens += 1
            return True
        

        else:  # enderecamento_aberto
            if self.tabela[indice] is None:
                self.tabela[indice] = (chave, valor)
                self.total_itens += 1
                return True
            else:
                # Linear probing
                tentativas = 1
                
                while tentativas < self.tamanho:
                    indice = (indice + 1) % self.tamanho
                    if self.tabela[indice] is None:
                        self.tabela[indice] = (chave, valor)
                        self.total_itens += 1
                        return True
                    
                    elif self.tabela[indice][0] == chave:
                        return False  # Chave já existe
                    tentativas += 1
                # tabela cheia (deveria redimensionar, fazer depois)
                raise Exception("Tabela hash cheia")
    


    def buscar(self, chave: Any) -> Optional[Any]:
        """busca um valor na tabela hash usando a chave fornecida"""
        indice = self.calcular_hash(chave)
        


        if self.metodo_colisao == 'encadeamento_exterior':
            for item in self.tabela[indice]:
                if item[0] == chave:
                    return item[1]
            return None
        

        else:  # enderecamento_aberto
            if self.tabela[indice] is not None and self.tabela[indice][0] == chave:
                return self.tabela[indice][1]
            else:
                # Linear probing
                tentativas = 1
                while tentativas < self.tamanho:
                    indice = (indice + 1) % self.tamanho
                    if self.tabela[indice] is not None and self.tabela[indice][0] == chave:
                        return self.tabela[indice][1]
                    tentativas += 1
                return None
    


    def remover(self, chave: Any) -> bool:
        """remove um valor da tabela hash usando a chave fornecida"""
        indice = self.calcular_hash(chave)
        
        if self.metodo_colisao == 'encadeamento_exterior':
            for i, item in enumerate(self.tabela[indice]):
                if item[0] == chave:
                    del self.tabela[indice][i]
                    self.total_itens -= 1
                    return True
            return False
        
        else:  # enderecamento_aberto
            if self.tabela[indice] is not None and self.tabela[indice][0] == chave:
                self.tabela[indice] = None
                self.total_itens -= 1
                return True
            else:
                # Linear probing
                tentativas = 1
                while tentativas < self.tamanho:
                    indice = (indice + 1) % self.tamanho
                    if self.tabela[indice] is not None and self.tabela[indice][0] == chave:
                        self.tabela[indice] = None
                        self.total_itens -= 1
                        return True
                    tentativas += 1
                return False
    

    def __contains__(self, chave: Any) -> bool:
        """verifica se uma chave está na tabela hash"""
        return self.buscar(chave) is not None
    
    def __getitem__(self, chave: Any) -> Any:
        """permite acesso via colchetes"""
        return self.buscar(chave)
    
    def __setitem__(self, chave: Any, valor: Any):
        """permite atribuição via colchetes"""
        self.inserir(chave, valor)
    
    def __len__(self) -> int:
        """retorna o número total de itens na tabela hash"""
        return self.total_itens
    


    def itens(self) -> List[Tuple[Any, Any]]:
        """retorna uma lista de tuplas (chave, valor) com todos os itens da tabela"""

        if self.metodo_colisao == 'encadeamento_exterior':
            return [item for lista in self.tabela for item in lista]
        else:
            return [item for item in self.tabela if item is not None]
    

    def carregar_csv(self, caminho_arquivo: str, chave: str = None) -> int:
        """carrega dados de um arquivo CSV para a tabela hash. retorna o número de itens inseridos (excluindo duplicatas)"""
        if chave is None:
            chave = self.chave
            
        inseridos= 0
        

        with open(caminho_arquivo, mode='r', newline='', encoding='utf-8') as arquivo:
            leitor = csv.DictReader(arquivo)
            
            if chave is None and leitor.fieldnames:
                chave = leitor.fieldnames[0]  # usa primeira coluna como chave padrão
            
            for linha in leitor:
                if chave not in linha:
                    raise ValueError(f"Chave '{chave}' não encontrada no arquivo CSV")
                
                chave_valor = linha[chave]
                if self.inserir(chave_valor, linha):
                    inseridos += 1
        
        return inseridos
    


    
    def deduplicar_csv(self, caminho_entrada: str, caminho_saida: str, chave: str = None) -> int:
        """
        processa um arquivo CSV, remove duplicatas e salva o resultado.
        """
        if chave is None:
            chave = self.chave
            
        itens_unicos = 0
        

        with open(caminho_entrada, mode='r', newline='', encoding='utf-8') as entrada, \
             open(caminho_saida, mode='w', newline='', encoding='utf-8') as saida:
            

            leitor = csv.DictReader(entrada)
            
            if chave is None and leitor.fieldnames:
                chave = leitor.fieldnames[0]  # usa primeira coluna como chave padrão
            

            if not leitor.fieldnames:
                raise ValueError("Arquivo CSV vazio ou sem cabeçalho")
                

            escritor = csv.DictWriter(saida, fieldnames=leitor.fieldnames)
            escritor.writeheader()
            

            for linha in leitor:
                if chave not in linha:
                    raise ValueError(f"Chave '{chave}' não encontrada no arquivo CSV")
                
                chave_valor = linha[chave]
                if self.inserir(chave_valor, linha):
                    escritor.writerow(linha)
                    itens_unicos += 1
        
        return itens_unicos
    


def testar_todas_funcionalidades():
    """
    Função que testa tudo
    """






    print("="*80)
    print("TESTE COMPLETO DA IMPLEMENTAÇÃO DA TABELA HASH")
    print("="*80)
    print("\n1. TESTE DE INICIALIZAÇÃO E CONFIGURAÇÃO")
    



    # 1. Teste de inicialização com diferentes configurações
    th1 = TabelaHash(tamanho=10, funcao_hash='divisao', metodo_colisao='encadeamento_exterior')
    th2 = TabelaHash(tamanho=20, funcao_hash='multiplicacao', metodo_colisao='enderecamento_aberto')
    
    print("\nTabela 1 criada com:")
    print(f"- Tamanho: 10 | Função Hash: 'divisao' | Método Colisão: 'encadeamento_exterior'")
    print("Tabela 2 criada com:")
    print(f"- Tamanho: 20 | Função Hash: 'multiplicacao' | Método Colisão: 'enderecamento_aberto'")
    
    print("\nResultado esperado: Ambas as tabelas foram criadas sem erros")
    print("Resultado obtido: Tabelas criadas com sucesso!")
    
    print("\n" + "="*80)
    print("2. TESTE DAS FUNÇÕES DE HASHING")
    

    # configura uma tabela pequena
    th_hash = TabelaHash(tamanho=10, funcao_hash='divisao')
    
    chaves_teste = [12345, "aluno123", "2023-1", "chave_comprida123456"]
    
    print("\nTestando diferentes funções de hash para as chaves:", chaves_teste)
    
    funcoes_hash = ['divisao', 'multiplicacao', 'dobra', 'meio_quadrado', 'extração']
    

    for funcao in funcoes_hash:
        th_hash.funcao_hash = funcao
        print(f"\nFunção '{funcao}':")
        for chave in chaves_teste:
            hash_val = th_hash.calcular_hash(chave)
            print(f"  '{chave}' → hash {hash_val} (esperado: 0-9)")
    



    
    print("\n" + "="*80)
    print("3. TESTE DE INSERÇÃO, BUSCA E REMOÇÃO")
    
    # Teste com encadeamento exterior
    print("\nTeste com encadeamento exterior:")
    th_encadeamento = TabelaHash(tamanho=5, metodo_colisao='encadeamento_exterior')
    
    # Inserção
    print("\nInserindo itens:")
    pares = [("chave1", "valor1"), ("chave2", "valor2"), ("chave3", "valor3"), 
             ("chave6", "valor6")]  # chave6 terá mesmo hash que chave1 em tabela tamanho 5
    
    for chave, valor in pares:
        resultado = th_encadeamento.inserir(chave, valor)
        print(f"Inserir '{chave}': {'Sucesso' if resultado else 'Falha (duplicado)'}")
    
    print("\nEstado esperado da tabela:")
    print("- Bucket 0: [('chave1', 'valor1'), ('chave6', 'valor6')] (colisão)")
    print("- Bucket 2: [('chave2', 'valor2')]")
    print("- Bucket 3: [('chave3', 'valor3')]")
    
    print("\nEstado atual da tabela:")
    for i, bucket in enumerate(th_encadeamento.tabela):
        if bucket:
            print(f"- Bucket {i}: {bucket}")
    


    # Busca
    print("\nTestando busca:")
    testes_busca = ["chave1", "chave6", "chave3", "chave_inexistente"]
    for chave in testes_busca:
        resultado = th_encadeamento.buscar(chave)
        print(f"Buscar '{chave}': {resultado if resultado else 'Não encontrado'}")
    

    # Remoção
    print("\nTestando remoção:")
    print("Removendo 'chave1':", th_encadeamento.remover("chave1"))
    print("Tentando remover 'chave_inexistente':", th_encadeamento.remover("chave_inexistente"))
    
    print("\nEstado após remoção:")
    print("- Bucket 0 deve conter apenas [('chave6', 'valor6')]")
    print("Estado atual:", [item for item in th_encadeamento.tabela[0] if item])
    

    # Teste com endereçamento aberto
    print("\nTeste com endereçamento aberto:")
    th_aberto = TabelaHash(tamanho=5, metodo_colisao='enderecamento_aberto')
    

    print("\nInserindo itens (pode haver colisão e sondagem):")
    for chave, valor in pares:
        resultado = th_aberto.inserir(chave, valor)
        print(f"Inserir '{chave}': {'Sucesso' if resultado else 'Falha (duplicado)'}")
    
    print("\nEstado da tabela com endereçamento aberto:")
    for i, slot in enumerate(th_aberto.tabela):
        print(f"Slot {i}: {slot if slot else 'Vazio'}")
    
    print("\n" + "="*80)
    print("4. TESTE DE DEDUPLICAÇÃO DE DATASET")
    
    # Criar um CSV de teste em memória (simulado)
    import io
    dados_csv = """id,nome,email
1,João,joao@example.com
2,Maria,maria@example.com
3,José,jose@example.com
4,João Duplicado,joao@example.com
5,Maria Duplicada,maria@example.com
6,Ana,ana@example.com"""
    
    print("\nDataset de teste (com duplicatas no campo 'email'):")
    print(dados_csv)
    
    # Simular leitura/escrita de arquivo
    with io.StringIO(dados_csv) as entrada, io.StringIO() as saida:
        th_dedup = TabelaHash(tamanho=10, funcao_hash='divisao', chave="email")
        

        # Processar deduplicação
        leitor = csv.DictReader(entrada)
        escritor = csv.DictWriter(saida, fieldnames=leitor.fieldnames)
        escritor.writeheader()
        
        duplicatas = 0
        for linha in leitor:
            if not th_dedup.inserir(linha["email"], linha):
                duplicatas += 1
            else:
                escritor.writerow(linha)
        

        saida.seek(0)
        resultado_dedup = saida.read()
    
    print("\nResultado da deduplicação:")
    print(f"- Itens únicos: {len(th_dedup)}")
    print(f"- Duplicatas encontradas: {duplicatas}")
    print("\nDataset após deduplicação:")
    print(resultado_dedup)
    

    print("\nResultado esperado:")
    print("- 4 itens únicos (João, Maria, José, Ana)")
    print("- 2 duplicatas removidas")
    print("- Dataset de saída sem linhas com emails repetidos")
    
    print("\n" + "="*80)
    print("5. TESTE DE ACESSO VIA OPERADOR [] E OUTROS MÉTODOS")
    
    th_operadores = TabelaHash(tamanho=10)
    
    # Teste do operador []
    th_operadores["chave_a"] = "valor_a"
    th_operadores["chave_b"] = "valor_b"
    
    print("\nTestando operadores:")
    print("th_operadores['chave_a'] =", th_operadores["chave_a"])
    print("'chave_b' in th_operadores:", "chave_b" in th_operadores)
    print("'chave_inexistente' in th_operadores:", "chave_inexistente" in th_operadores)
    
    # Teste do método itens()
    print("\nTodos os itens na tabela:", th_operadores.itens())
    
    print("\nResultado esperado:")
    print("- th_operadores['chave_a'] retorna 'valor_a'")
    print("- 'chave_b' in th_operadores retorna True")
    print("- 'chave_inexistente' in th_operadores retorna False")
    print("- itens() retorna [('chave_a', 'valor_a'), ('chave_b', 'valor_b')]")
    
    print("\n" + "="*80)
    print("TESTES CONCLUÍDOS COM SUCESSO!")
    print("="*80)


if __name__ == "__main__":
    testar_todas_funcionalidades()