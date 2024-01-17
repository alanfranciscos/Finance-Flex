<img src="https://img.shields.io/badge/python-v3.11-green"/>

# FinanceFlex

Bem-vindo ao FinanceFlex - Sua solução flexível para gerenciamento financeiro pessoal.

## Visão Geral

O FinanceFlex é um aplicativo de planejamento financeiro desenvolvido para proporcionar uma experiência intuitiva e eficaz no controle das suas finanças. Com recursos poderosos e uma interface amigável, o FinanceFlex ajuda você a tomar decisões financeiras informadas e atingir suas metas.

## Funcionalidades Principais

- **Cadastro e Personalização:**
  - Crie uma conta personalizada e adapte as configurações de acordo com suas preferências.

- **Gerenciamento de Despesas e Receitas:**
  - Registre e categorize transações facilmente.

- **Orçamento Mensal:**
  - Defina metas mensais e monitore seu progresso em tempo real.

- **Alertas e lembretes:**
  - Uma forma de lembrar de todas as suas responsabilidades.

- **Relatórios Detalhados e Análises:**
  - Acesse relatórios financeiros e gráficos para insights valiosos.

- **Metas Financeiras Personalizadas:**
  - Estabeleça e acompanhe suas metas financeiras a longo prazo.

## Instalação

- Clone o repositório: `git clone https://github.com/seu-usuario/FinanceFlex.git`

## Backend

- Preencha o arquivo env de acordo com o exemplo
- Instale o [python v3.11](https://www.python.org/downloads/release/python-3110/)
- Crie uma virtual env

```bash
cd backend
python3.11 -m venv venv
```

- Instale as dependências

```bash
pip install -r requirements.txt
```

- Inicie o backend: ``

```bash
uvicorn app.main:app --reload
```

- [Acesse o swagger no seu navegador para verificar a documentacao da api](http://localhost:8000/docs)

---

**Desenvolvido por Alan Francisco Silva | © 2023 FinanceFlex. Todos os direitos reservados.**
