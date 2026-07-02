import requests
import json
from datetime import datetime
import os
import google.generativeai as genai

# ========== CONFIGURAÇÕES ==========

# Gemini API Key (será lida de secrets do GitHub)
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

# ========== FUNÇÕES ==========

def buscar_santo_do_dia():
    """Busca santo do dia via API"""
    hoje = datetime.now()
    
    # Tenta API Liturgia Diária
    try:
        url = f"https://liturgia.up.railway.app/{hoje.strftime('%Y-%m-%d')}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            santo_nome = data.get('santo', 'Santo do dia')
            return {
                'nome': santo_nome,
                'data': hoje.strftime('%Y-%m-%d'),
                'fonte': 'API Liturgia Diária'
            }
    except:
        pass
    
    # Fallback
    return {
        'nome': f'Santo do dia {hoje.strftime("%d/%m")}',
        'data': hoje.strftime('%Y-%m-%d'),
        'fonte': 'Base local'
    }

def gerar_conteudo_ia(santo_nome):
    """Gera conteúdo com Gemini"""
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    prompt = f'''Crie conteúdo sobre: {santo_nome}

Retorne APENAS este JSON:

{{
  "biografia": "Biografia completa em 4-5 parágrafos",
  "frase": "Citação marcante",
  "core": "Essência em 1 frase",
  "virtudes": ["virtude1", "virtude2", "virtude3"],
  "reflexao": "3 parágrafos conectando com mundo moderno"
}}'''
    
    try:
        response = model.generate_content(prompt)
        texto = response.text.strip()
        
        # Remove markdown
        if texto.startswith('```'):
            texto = texto.split('\n', 1)[1]
            texto = texto.rsplit('```', 1)[0]
        
        return json.loads(texto)
    except:
        # Fallback
        return {
            "biografia": f"{santo_nome}\n\nBiografia em breve.",
            "frase": "Que a fé guie nossos passos.",
            "core": "Fé e devoção",
            "virtudes": ["Fé", "Esperança", "Caridade"],
            "reflexao": f"Hoje celebramos {santo_nome}."
        }

def gerar_html(santo, conteudo):
    """Gera HTML completo"""
    data_obj = datetime.strptime(santo['data'], "%Y-%m-%d")
    data_br = data_obj.strftime("%d de %B de %Y")
    
    # Traduz mês para português
    meses = {
        'January': 'janeiro', 'February': 'fevereiro', 'March': 'março',
        'April': 'abril', 'May': 'maio', 'June': 'junho',
        'July': 'julho', 'August': 'agosto', 'September': 'setembro',
        'October': 'outubro', 'November': 'novembro', 'December': 'dezembro'
    }
    for en, pt in meses.items():
        data_br = data_br.replace(en, pt)
    
    mensagem = f"{conteudo['biografia']}\n\n\"{conteudo['frase']}\"\n\n{conteudo['reflexao']}"
    mensagem_html = mensagem.replace('\n\n', '</p><p>').replace('\n', '<br>')
    if not mensagem_html.startswith('<p>'):
        mensagem_html = f'<p>{mensagem_html}</p>'
    
    return f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{santo['nome']} - Santo do Dia</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: Georgia, serif;
            min-height: 100vh;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .card {{
            max-width: 600px;
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }}
        h1 {{
            color: #764ba2;
            text-align: center;
            margin-bottom: 10px;
            font-size: 2em;
        }}
        .data {{
            text-align: center;
            color: #666;
            font-style: italic;
            margin-bottom: 30px;
        }}
        .mensagem {{
            line-height: 1.9;
            text-align: justify;
            color: #333;
        }}
        .mensagem p {{ margin-bottom: 20px; }}
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid #eee;
            text-align: center;
            color: #999;
        }}
        @media (max-width: 600px) {{
            body {{ padding: 10px; }}
            .card {{ padding: 25px; }}
            h1 {{ font-size: 1.5em; }}
        }}
    </style>
</head>
<body>
    <div class="card">
        <h1>✨ {santo['nome']} ✨</h1>
        <p class="data">{data_br}</p>
        <div class="mensagem">
            {mensagem_html}
        </div>
        <div class="footer">
            <p>🙏 Que esta mensagem ilumine seu dia!</p>
        </div>
    </div>
</body>
</html>'''

# ========== MAIN ==========

if __name__ == "__main__":
    print("🎯 Gerando Santo do Dia...")
    
    # 1. Buscar santo
    santo = buscar_santo_do_dia()
    print(f"✅ Santo: {santo['nome']}")
    
    # 2. Gerar conteúdo IA
    conteudo = gerar_conteudo_ia(santo['nome'])
    print("✅ Conteúdo gerado")
    
    # 3. Gerar HTML
    html = gerar_html(santo, conteudo)
    
    # 4. Salvar
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("✅ index.html gerado!")
    print(f"🎉 Pronto! Santo: {santo['nome']}")
