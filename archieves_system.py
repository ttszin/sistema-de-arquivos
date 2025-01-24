#coding: UTF-8
import warnings 
"""
O objetivo deste trabalho é implementar um sistema de arquivos baseado em i-nodes. Para isso, considere as seguintes informações:

O seu disco rígido possui uma capacidade de 256MB 
Os blocos para armazenamento de dados possuem 4KB
Que cada i-node tem a seguinte estrutura:
Nome do arquivo/diretório
Criador
Dono
Tamanho
Data de criação
Data de modificação
Permissões de acesso (dono e outros usuários - leitura, escrita, execução)
Apontadores para blocos
Apontador para eventual outro i-node
Lembre que parte do espaço do disco rígido é utilizado para armazenar as informações de gerenciamento, isto é, controle sobre quais blocos/i-nodes estão livres ou ocupados e também os i-nodes em si.

O sistema de arquivo deverá suportar as seguintes operações:

Operações sobre arquivos:

    - Criar arquivo (touch arquivo)
    - Remover arquivo (rm arquivo)
    - Criar um arquivo já adicionando conteúdo (echo "conteúdo legal" > arquivo)
    - Adicionar conteúdo a um arquivo existente ou criá-lo caso não exista (echo "conteudo legal" >> arquivo)
    - Ler arquivo (cat arquivo)
    - Copiar arquivo (cp arquivo1 arquivo2)
    - Renomear/mover arquivo (mv arquivo1 arquivo2)
    - Criar links entre arquivos (ln -s arquivoOriginal link)

Operações sobre diretórios:

    - Criar diretório (mkdir diretorio)
    - Remover diretório (rmdir diretorio) - só funciona se diretório estiver vazio
    - Listar o conteúdo de um diretório (ls diretório)
    - Trocar de diretório (cd diretorio)
        * Não esquecer dos arquivos especiais . e .. 
    - Renomear/mover diretório (mv diretorio1 diretorio2)

    - Criar links entre diretório (ln -s arquivoOriginal link)

Importante! 

O sistema de arquivos deve ser persistente, o que significa que se o processo do sistema de arquivos for encerrado, o conteúdo deve ser mantido e carregado na próxima vez que o processo for iniciado;
Todos os comandos devem funcionar com caminhos absolutos e relativos 
"""


import os
import pickle
import time

# Configurações gerais
disk_file = "disco.img"
disk_size = 256 * 1024 * 1024  # 256 MB
block_size = 4 * 1024  # 4 KB
num_blocks = disk_size // block_size
inode_table_size = 1024  # Número máximo de i-nodes
bitmap_size = num_blocks  # Um bit por bloco
inode_struct_size = 256  # Tamanho de um i-node serializado

class FileSystem:
    def __init__(self):
        self.bitmap = [0] * num_blocks
        self.inode_table = [None] * inode_table_size
        self.cwd = 0  # Current working directory inode index
        self.directory = "$"
        if not os.path.exists(disk_file):
            self.format_disk()
        else:
            try:
                self.load_disk()
            except (pickle.UnpicklingError, UnicodeDecodeError):
                print("Erro ao carregar o disco. Reformatando...")
                self.format_disk()

    def format_disk(self):
        """Inicializa o disco virtual formatando-o."""
        with open(disk_file, "wb") as f:
            f.write(b"\0" * disk_size)
        self.save_disk()

    def save_disk(self):
        """Salva os metadados do sistema de arquivos no disco."""
        with open(disk_file, "r+b") as f:
            f.seek(0)
            pickle.dump((self.bitmap, self.inode_table), f)

    def load_disk(self):
        """Carrega os metadados do sistema de arquivos do disco."""
        with open(disk_file, "rb") as f:
            self.bitmap, self.inode_table = pickle.load(f)
            print

    def allocate_block(self):
        """Encontra um bloco livre e o aloca."""
        for i in range(len(self.bitmap)):
            if self.bitmap[i] == 0:
                self.bitmap[i] = 1
                return i
        raise RuntimeError("No free blocks available.")

    def free_block(self, block_index):
        """Libera um bloco ocupado."""
        self.bitmap[block_index] = 0

    def allocate_inode(self):
        """Encontra um i-node livre e o aloca."""
        for i in range(len(self.inode_table)):
            if self.inode_table[i] is None:
                return i
        raise RuntimeError("No free i-nodes available.")


    def create_directory(self, name):
        #Cria um diretório.
        inode_index = self.allocate_inode()
        self.inode_table[inode_index] = {
            "name": name,
            "owner": os.getlogin(),
            "size": 0,
            "creation_time": time.ctime(),
            "modification_time": time.ctime(),
            "permissions": "rwxr-xr-x",
            "blocks": [],
            "type": "directory",
            "contents": []  # Lista de i-nodes dentro do diretório
        }
        self.save_disk()
        print(f"Diretório '{name}' criado com sucesso.")

    
    
    def change_directory(self, dir_name):
        #Troca o diretório de trabalho para o diretório fornecido. 
        # Primeiro, verificamos se o diretório é especial: "." (diretório atual) ou ".." (diretório pai)
        if dir_name == ".":
            print("Você já está no diretório atual.")
            return

        if dir_name == "..":
            # Ir para o diretório pai (assumimos que o diretório raiz é o primeiro inode)
            if self.cwd == 0:
                print("Você já está no diretório raiz.")
                return
            # A estrutura de diretórios está simplificada, mas aqui é onde iríamos verificar o pai
            self.cwd = 0  # Definir como raiz, ou implementar uma estrutura de árvore mais complexa para navegar.
            print("Diretório de trabalho alterado para o diretório raiz.")
            return

        # Verifique se o diretório existe
        for inode in self.inode_table:
            print(self.inode_table)
            if inode and inode["name"] == dir_name and inode["type"] == "directory":
                # Atualiza o diretório de trabalho
                self.cwd = self.inode_table.index(inode)
                self.directory = 
                print(f"Diretório de trabalho alterado para: {dir_name}")
                return
        
        # Se o diretório não for encontrado
        print(f"Diretório '{dir_name}' não encontrado.")


    """
    def create_file(self, name, content=""):
            #Cria um arquivo com um nome e conteúdo opcional.
            inode_index = self.allocate_inode()
            blocks = []

            # Alocar blocos para o conteúdo
            content_size = len(content.encode("utf-8"))
            while content:
                block_index = self.allocate_block()
                blocks.append(block_index)

                # Escrever o conteúdo no bloco
                with open(disk_file, "r+b") as f:
                    f.seek(block_index * block_size)
                    f.write(content[:block_size].encode("utf-8"))
                content = content[block_size:]

            # Criar i-node
            self.inode_table[inode_index] = {
                "name": name,
                "owner": os.getlogin(),
                "size": content_size,
                "creation_time": time.ctime(),
                "modification_time": time.ctime(),
                "permissions": "rw-r--r--",
                "blocks": blocks,
                "type": "file"
            }
            print(self.inode_table[inode_index])
            self.save_disk()
            print(f"Arquivo '{name}' criado com sucesso.")

    def delete_file(self, name):
        #Remove um arquivo pelo nome.
        for i, inode in enumerate(self.inode_table):
            if inode and inode["name"] == name and inode["type"] == "file":
                # Liberar blocos alocados
                for block in inode["blocks"]:
                    self.free_block(block)
                self.inode_table[i] = None
                self.save_disk()
                print(f"Arquivo '{name}' removido com sucesso.")
                return
        raise FileNotFoundError(f"Arquivo '{name}' não encontrado.")

    def read_file(self, name):
            #Lê o conteúdo de um arquivo pelo nome.
            for inode in self.inode_table:
                if inode and inode["name"] == name and inode.get("type") == "file":
                    content = ""
                    remaining_size = inode["size"]
                    for block in inode["blocks"]:
                        with open(disk_file, "rb") as f:
                            f.seek(block * block_size)
                            block_data = f.read(min(remaining_size, block_size))
                            content += block_data.decode("utf-8")
                            remaining_size -= len(block_data)
                            if remaining_size <= 0:
                                break
                    return content
            raise FileNotFoundError(f"Arquivo '{name}' não encontrado.")

    def copy_file(self, source, destination):
        #Copia um arquivo para um novo arquivo.
        content = self.read_file(source)
        self.create_file(destination, content)
        print(f"Arquivo '{source}' copiado para '{destination}'.")

    def rename_file(self, old_name, new_name):
        #Renomeia ou move um arquivo.
        for inode in self.inode_table:
            if inode and inode["name"] == old_name and inode["type"] == "file":
                inode["name"] = new_name
                self.save_disk()
                print(f"Arquivo '{old_name}' renomeado para '{new_name}'.")
                return
        raise FileNotFoundError(f"Arquivo '{old_name}' não encontrado.")

    def create_symlink(self, target, link_name):
        #Cria um link simbólico para um arquivo.
        inode_index = self.allocate_inode()
        self.inode_table[inode_index] = {
            "name": link_name,
            "owner": os.getlogin(),
            "size": 0,
            "creation_time": time.ctime(),
            "modification_time": time.ctime(),
            "permissions": "rwxrwxrwx",
            "blocks": [],
            "type": "symlink",
            "target": target
        }
        self.save_disk()
        print(f"Link simbólico '{link_name}' criado para '{target}'.")


    def list_directory(self, name):
        #Lista o conteúdo de um diretório.
        for inode in self.inode_table:
            if inode and inode["name"] == name and inode["type"] == "directory":
                print(f"Conteúdo do diretório '{name}':")
                for entry in inode["contents"]:
                    print(f"- {entry}")
                return
        raise FileNotFoundError(f"Diretório '{name}' não encontrado.")

    def remove_directory(self, name):
        #Remove um diretório (apenas se estiver vazio).
        for i, inode in enumerate(self.inode_table):
            if inode and inode["name"] == name and inode["type"] == "directory":
                if len(inode["contents"]) > 0:
                    raise RuntimeError(f"Diretório '{name}' não está vazio.")
                self.inode_table[i] = None
                self.save_disk()
                print(f"Diretório '{name}' removido com sucesso.")
                return
        raise FileNotFoundError(f"Diretório '{name}' não encontrado.")
    """
def main():
    fs = FileSystem()

    while True:
        entrada = input(f"{fs.index}")
   
        argumentos = entrada.split(maxsplit=1)

        if entrada.startswith("mkdir"):
            if len(argumentos)>1: 
                fs.create_directory(argumentos[1])
            else:
                # displaying the warning message  
                warnings.warn('ERRO: Entrada sem argumentos') 

        if entrada.startswith("ls"):
            if len(argumentos)>1: 
                fs.change_directory(argumentos[1])
            else:
                # displaying the warning message  
                warnings.warn('ERRO: Entrada sem argumentos') 

                
        

        


    
    
    

if __name__ == "__main__":
    main()


"""
    def export_file(self, name, output_path):
        content = self.read_file(name)
        with open(output_path, "w") as f:
            f.write(content)
        print(f"Arquivo '{name}' exportado para '{output_path}'.")
        
    def list_files(self):
        print("Arquivos no sistema de arquivos virtual:")
        for inode in self.inode_table:
            if inode:
                print(f"- Nome: {inode['name']}, Tamanho: {inode['size']} bytes, Blocos: {inode['blocks']}")

    # Exemplo que estava bom
    fs = FileSystem(1000)
    fs.create_file("file1.txt", 200)
    fs.create_directory("docs")
    fs.change_directory("docs")
    fs.create_file("file2.txt", 300)
    fs.list_directory()
    fs.change_directory("..")
    fs.disk_usage()            

"""
