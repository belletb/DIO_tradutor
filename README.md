# 🌍 Tradutor de Voz em Tempo Real (PT → EN)

Tradutor de voz em tempo real que grava áudio em português, transcreve, traduz para inglês e reproduz a tradução em áudio.

## Características

- Gravação de áudio via microfone
- Transcrição usando Whisper 
- Tradução PT → EN
- Síntese de voz (Text-to-Speech)

## Instalação Rápida

### 1. Clonar/baixar o projeto

```bash
cd tradutor-voz
```

### 2. Criar ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Instalar dependências

```bash
pip install -r requirements_improved.txt
```

### 4. Executar:

```bash
python tradutor_voz.py
```

## Personalização

### Alterar duração da gravação

Edite a constante no arquivo Python:

```python
DEFAULT_RECORDING_DURATION = 10  # 10 segundos
```

### Alterar idiomas

```python
SOURCE_LANGUAGE = "pt"  # português
TARGET_LANGUAGE = "es"  # espanhol
```

### Alterar modelo Whisper

```python
WHISPER_MODEL_SIZE = "medium"  # opções: tiny, base, small, medium, large
```

**Trade-offs dos modelos:**
- `tiny`: Rápido, menos preciso
- `small`: Balanceado (padrão)
- `medium`: Mais preciso, mais lento
- `large`: Muito preciso, muito lento

## 🔧 Solução de Problemas

### Erro: "Nenhum dispositivo de áudio encontrado"

**Linux:**
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
```

**Mac:**
```bash
brew install portaudio
```

**Windows:**
- Instale o PyAudio manualmente
- Ou use o arquivo wheel apropriado

### Erro: Modelo Whisper não carrega

**Possíveis causas:**
- Pouca memória RAM (Whisper precisa de ~2GB)
- Falta de espaço em disco
- Conexão de internet (primeira vez baixa o modelo)

**Solução:**
```python
WHISPER_MODEL_SIZE = "tiny"  # Use modelo menor
```

### Áudio não reproduz

Verifique:
1. Volume do sistema
2. Dispositivos de saída de áudio conectados
3. Permissões do pygame/SDL

## 🛠️ Requisitos do Sistema

- **Python**: 3.10 ou superior
- **RAM**: Mínimo 4GB (8GB recomendado)
- **Espaço**: ~2GB para modelos Whisper
- **SO**: Linux, macOS, Windows
- **Microfone**: Qualquer dispositivo de entrada de áudio
- **Alto-falantes**: Qualquer dispositivo de saída de áudio

## Extensões Futuras

Ideias para melhorar o projeto:

1. **Suporte a mais idiomas**
   - Adicionar detecção automática de idioma
   - Tradução para múltiplos idiomas alvo

2. **Interface gráfica (GUI)**
   - Usando Tkinter ou PyQt
   - Visualização de forma de onda

3. **Gravação contínua**
   - Detecção de voz automática (VAD)
   - Gravação apenas quando falar

4. **Histórico de traduções**
   - Salvar traduções em arquivo
   - Exportar para diferentes formatos

5. **Melhoria de áudio**
   - Redução de ruído
   - Normalização de volume

## 📝 Estrutura do Projeto

```
tradutor-voz/
├── tradutor_voz.py             
├── requirements.txt             
├── .gitignore                   
└── README.md                   
```

## 🤝 Contribuindo

Sugestões e melhorias são bem-vindas! Sinta-se livre para:
- Reportar bugs
- Sugerir novos recursos
- Enviar pull requests
- Compartilhar casos de uso

## 📄 Licença

Este projeto é de código aberto e está disponível para uso educacional e pessoal.

**Feito com ❤️ para aprender processamento de linguagem natural e síntese de voz**