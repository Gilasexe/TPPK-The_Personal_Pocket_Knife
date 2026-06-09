# 🔪 TPPK - The Personal Pocket Knife

![Versão Atual](https://img.shields.io/badge/Vers%C3%A3o-1.0.0-blue?style=flat-square)
![Plataforma Windows](https://img.shields.io/badge/OS-Windows-0078D6?style=flat-square&logo=windows)
![Plataforma Linux](https://img.shields.io/badge/OS-Arch_Linux-1793D1?style=flat-square&logo=arch-linux)
![Python](https://img.shields.io/badge/Python-3.x-F5D04C?style=flat-square&logo=python)

O **TPPK** (The Personal Pocket Knife) é um canivete suíço digital com interface gráfica moderna desenvolvida em Python (CustomTkinter). Ele centraliza atalhos de sistema operacional, ferramentas de manutenção e um almanaque pessoal para estudos e desenvolvimento.

Originalmente projetado para otimizar fluxos no Arch Linux, o TPPK possui versões adaptadas para gerenciar instâncias do Windows de maneira rápida e indolor.

## ✨ Funcionalidades

### 🪟 Ferramentas do Sistema
- **Controle de Energia Dinâmico:** Alterne com um clique entre os planos de Alto Desempenho, Equilibrado e Economia de Bateria. *(No Linux: Integração com EnvyControl para GPUs Híbridas).*
- **Faxina do Sistema:** Limpeza em um clique de arquivos temporários (`%TEMP%`) e limpeza de cache DNS (Flush DNS) para resolver pequenos bugs de rede. *(No Linux: Limpeza de pacotes órfãos do Pacman).*

### 📚 Almanaque do Desenvolvedor (Cadernos)
- Leitor interno de anotações dinâmico.
- Organize seus estudos criando pastas (ex: `Python`, `Calculo`, `Banco_de_Dados`).
- O sistema automaticamente renderiza arquivos `.txt`, utilizando a primeira linha como título e o resto como o corpo da matéria.

### ⚙️ Sistema Integrado de Updates
- Verificação assíncrona da API do GitHub para alertar sobre novas versões sem congelar a interface.

## 🚀 Como instalar e executar

### Pré-requisitos (Para rodar pelo código fonte)
Certifique-se de ter o Python 3 instalado e instale os pacotes necessários:
```bash
pip install customtkinter requests