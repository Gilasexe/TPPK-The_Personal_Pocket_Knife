# 🔪 TPPK - The Personal Pocket Knife

Bem-vindo ao **TPPK**, o verdadeiro "Canivete Suíço" para estudantes e usuários de Linux. Desenvolvido em Python com `CustomTkinter`, este aplicativo foi desenhado para centralizar ferramentas de sistema do EndeavourOS/Arch Linux e organizar cadernos de estudo de forma dinâmica.

---

## ✨ Funcionalidades

* **🛠️ Ferramentas Linux Integradas:**
    * **Controle de GPU (EnvyControl):** Alterna facilmente entre os modos NVIDIA (foco em performance/jogos), Integrada (economia de bateria) e Híbrido, lidando nativamente com a autenticação de administrador (`pkexec`).
    * **Faxina de Sistema:** Limpa o cache antigo do Pacman com um clique, liberando espaço no SSD sem precisar decorar comandos no terminal.
* **📚 Leitor de Almanaque Dinâmico:**
    * Um leitor de textos embutido que gera páginas e categorias automaticamente.
    * Basta soltar arquivos `.txt` dentro da pasta `cadernos/` e o aplicativo constrói a interface de leitura sozinho.
* **⚙️ Atualização via Nuvem (OTA):**
    * Verifica automaticamente a API de Releases do GitHub em segundo plano.
    * Avisa quando há uma nova versão disponível, mostrando o Changelog diretamente na interface.

---

## 🚀 Como instalar e rodar (Ambiente de Desenvolvimento)

### Pré-requisitos
* **Sistema Operacional:** Arch Linux / EndeavourOS (para as ferramentas de sistema funcionarem corretamente).
* **Python:** 3.10 ou superior.
* **Pacotes do Sistema:** `envycontrol`, `pacman-contrib` (para o `paccache`).

## 📥 Instalação Fácil (Para Usuários)

Não quer mexer com código ou terminal? Siga os passos abaixo:

1. Acesse a página de [Releases](../../releases/latest) aqui do GitHub.
2. Baixe o arquivo `.zip` da versão mais recente.
3. Garanta que seu sistema possui as dependências nativas: `yay -S envycontrol pacman-contrib`.
4. Extraia o ZIP e dê um duplo clique no arquivo `TPPK` para abrir. Pronto!

---

## 💻 Instalação para Desenvolvedores (Build a partir do código)

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/Gilasexe/TPPK-The_Personal_Pocket_Knife.git](https://github.com/Gilasexe/TPPK-The_Personal_Pocket_Knife.git)
   cd TPPK-The_Personal_Pocket_Knife
   
2. **Crie e ative o ambiente Virtual (Recomendado)**
   1-python -m venv .venv (o .venv pode ser nomeado como qualquer coisa)
   2-source .venv/bin/activate
   
3. **Baixe as dependencias do código**
   ```bash
   pip freeze > requirements.txt

4. **Execute o aplicativo**
   ```bash
   python main.py