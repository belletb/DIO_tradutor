# Tradutor de Voz em Tempo Real

Este projeto implementa um tradutor de voz em tempo real que:
1. Grava áudio em português usando o microfone.
2. Transcreve o áudio para texto com o modelo Whisper.
3. Traduz o texto para inglês usando o modelo GPT da OpenAI.
4. Converte a tradução em áudio com gTTS e reproduz com pygame.

## Requisitos

- Python 3.10 ou superior
- Ambiente virtual recomendado

## Instalação

Crie e ative um ambiente virtual:

```bash
python3 -m venv venv
source venv/bin/activate
```

Instale as dependências:
```bash
pip install -r requirements.txt
```

configure sua chave da OpenAI:
```bash
export OPENAI_API_KEY="sua_chave_aqui"
```

Execute o script:
```bash
python tradutor_voz.py
```
