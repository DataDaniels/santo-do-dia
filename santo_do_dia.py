import requests
import json
from datetime import datetime
import os
import google.generativeai as genai
from zoneinfo import ZoneInfo
import urllib.parse

# ========== CONFIGURAÇÕES ==========

# Gemini API Key (será lida de secrets do GitHub)
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

# Timezone do Brasil
BRASIL_TZ = ZoneInfo("America/Sao_Paulo")

# Unsplash (sem necessidade de API key para basic usage)
UNSPLASH_API = "https://source.unsplash.com/800x600/"

# ========== FUNÇÕES ==========

def buscar_santo_do_dia():
    """Busca santo do dia via API"""
    hoje = datetime.now(BRASIL_TZ)
    
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
    except Exception as e:
        print(f"⚠️ API falhou: {e}")
    
    # Fallback
    return {
        'nome': f'Santo do dia {hoje.strftime("%d/%m")}',
        'data': hoje.strftime('%Y-%m-%d'),
        'fonte': 'Base local'
    }

def buscar_imagem_santo(nome_santo):
    """Busca imagem do santo via Unsplash"""
    try:
        # Termos de busca: santo católico + nome
        query = f"catholic saint {nome_santo}"
        # Usa source.unsplash.com (sem API key necessária)
        url = f"https://source.unsplash.com/800x600/?{urllib.parse.quote(query)}"
        print(f"🖼️ Buscando imagem: {query}")
        return url
    except Exception as e:
        print(f"⚠️ Erro ao buscar imagem: {e}")
        return None

def gerar_svg_fallback():
    """Gera SVG decorativo GRANDE e impactante"""
    return '''
    <svg viewBox="0 0 800 600" xmlns="http://www.w3.org/2000/svg" class="saint-icon" preserveAspectRatio="xMidYMid meet">
        <defs>
            <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
                <stop offset="50%" style="stop-color:#764ba2;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#f093fb;stop-opacity:1" />
            </linearGradient>
            
            <radialGradient id="glow1" cx="50%" cy="50%">
                <stop offset="0%" style="stop-color:#ffffff;stop-opacity:0.8" />
                <stop offset="50%" style="stop-color:#f093fb;stop-opacity:0.4" />
                <stop offset="100%" style="stop-color:#667eea;stop-opacity:0" />
            </radialGradient>
            
            <filter id="blur">
                <feGaussianBlur in="SourceGraphic" stdDeviation="8" />
            </filter>
            
            <filter id="glow">
                <feGaussianBlur stdDeviation="10" result="coloredBlur"/>
                <feMerge>
                    <feMergeNode in="coloredBlur"/>
                    <feMergeNode in="coloredBlur"/>
                    <feMergeNode in="SourceGraphic"/>
                </feMerge>
            </filter>
        </defs>
        
        <!-- Fundo com gradiente radial -->
        <circle cx="400" cy="300" r="350" fill="url(#glow1)" opacity="0.3">
            <animate attributeName="r" values="350;380;350" dur="4s" repeatCount="indefinite"/>
        </circle>
        
        <!-- Círculos de fundo animados -->
        <circle cx="400" cy="300" r="280" fill="none" stroke="url(#grad1)" stroke-width="2" opacity="0.2">
            <animate attributeName="r" values="280;300;280" dur="3s" repeatCount="indefinite"/>
        </circle>
        <circle cx="400" cy="300" r="220" fill="none" stroke="url(#grad1)" stroke-width="3" opacity="0.3">
            <animate attributeName="r" values="220;240;220" dur="3.5s" repeatCount="indefinite"/>
        </circle>
        <circle cx="400" cy="300" r="160" fill="none" stroke="url(#grad1)" stroke-width="4" opacity="0.4">
            <animate attributeName="r" values="160;180;160" dur="4s" repeatCount="indefinite"/>
        </circle>
        
        <!-- Raios de luz (mais visíveis) -->
        <g opacity="0.6">
            <path d="M 400 100 L 400 50" stroke="url(#grad1)" stroke-width="8" stroke-linecap="round">
                <animate attributeName="opacity" values="0.6;1;0.6" dur="2s" repeatCount="indefinite"/>
            </path>
            <path d="M 500 150 L 540 110" stroke="url(#grad1)" stroke-width="8" stroke-linecap="round">
                <animate attributeName="opacity" values="0.6;1;0.6" dur="2.2s" repeatCount="indefinite"/>
            </path>
            <path d="M 300 150 L 260 110" stroke="url(#grad1)" stroke-width="8" stroke-linecap="round">
                <animate attributeName="opacity" values="0.6;1;0.6" dur="2.4s" repeatCount="indefinite"/>
            </path>
            <path d="M 580 280 L 630 270" stroke="url(#grad1)" stroke-width="8" stroke-linecap="round">
                <animate attributeName="opacity" values="0.6;1;0.6" dur="2.6s" repeatCount="indefinite"/>
            </path>
            <path d="M 220 280 L 170 270" stroke="url(#grad1)" stroke-width="8" stroke-linecap="round">
                <animate attributeName="opacity" values="0.6;1;0.6" dur="2.8s" repeatCount="indefinite"/>
            </path>
        </g>
        
        <!-- Cruz central GRANDE com brilho forte -->
        <g filter="url(#glow)">
            <!-- Sombra da cruz -->
            <rect x="385" y="160" width="30" height="280" fill="#000000" opacity="0.1" rx="15"/>
            <rect x="280" y="265" width="240" height="30" fill="#000000" opacity="0.1" rx="15"/>
            
            <!-- Cruz principal -->
            <rect x="380" y="155" width="40" height="290" fill="url(#grad1)" rx="20">
                <animate attributeName="opacity" values="1;0.9;1" dur="2s" repeatCount="indefinite"/>
            </rect>
            <rect x="275" y="260" width="250" height="40" fill="url(#grad1)" rx="20">
                <animate attributeName="opacity" values="1;0.9;1" dur="2s" repeatCount="indefinite"/>
            </rect>
        </g>
        
        <!-- Auréola grande -->
        <circle cx="400" cy="200" r="120" fill="none" stroke="url(#grad1)" stroke-width="12" opacity="0.7" filter="url(#glow)">
            <animate attributeName="r" values="120;125;120" dur="3s" repeatCount="indefinite"/>
            <animate attributeName="opacity" values="0.7;0.9;0.7" dur="3s" repeatCount="indefinite"/>
        </circle>
        
        <!-- Estrelas decorativas -->
        <g fill="url(#grad1)" opacity="0.8">
            <circle cx="300" cy="120" r="6">
                <animate attributeName="opacity" values="0.8;1;0.8" dur="1.5s" repeatCount="indefinite"/>
            </circle>
            <circle cx="500" cy="130" r="8">
                <animate attributeName="opacity" values="0.8;1;0.8" dur="1.8s" repeatCount="indefinite"/>
            </circle>
            <circle cx="250" cy="250" r="5">
                <animate attributeName="opacity" values="0.8;1;0.8" dur="2.1s" repeatCount="indefinite"/>
            </circle>
            <circle cx="550" cy="240" r="7">
                <animate attributeName="opacity" values="0.8;1;0.8" dur="2.4s" repeatCount="indefinite"/>
            </circle>
        </g>
    </svg>
    '''

def gerar_conteudo_ia(santo_nome):
    """Gera conteúdo com Gemini"""
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f'''Você é um especialista em hagiografia católica.

SANTO: {santo_nome}

Crie um JSON com:

1. "biografia": Biografia completa em 4-5 parágrafos sobre:
   - Origem e contexto histórico
   - Vida e principais feitos
   - Virtudes marcantes
   - Como alcançou santidade
   - Legado para a Igreja

2. "frase": Citação marcante do santo (ou sobre ele)

3. "virtudes": Array com 4-6 virtudes principais

4. "reflexao": Reflexão em 3 parágrafos conectando o santo com desafios modernos:
   - Como o jeito de ser do santo é relevante hoje
   - Problemas atuais que ele/ela ajuda a enfrentar
   - Aplicação prática no dia a dia

NÃO use a palavra "Reflexão" no texto.
Tom acolhedor e inspirador.

RETORNE APENAS O JSON VÁLIDO (sem markdown, sem explicações):

{{
  "biografia": "texto aqui...",
  "frase": "citação aqui...",
  "virtudes": ["virtude1", "virtude2", "virtude3"],
  "reflexao": "texto aqui..."
}}'''
    
    try:
        print("🤖 Chamando Gemini API...")
        response = model.generate_content(prompt)
        texto = response.text.strip()
        
        print(f"📝 Resposta recebida ({len(texto)} chars)")
        
        # Remove markdown code blocks
        if texto.startswith('```'):
            linhas = texto.split('\n')
            linhas = linhas[1:]
            if linhas and linhas[-1].strip() == '```':
                linhas = linhas[:-1]
            texto = '\n'.join(linhas)
        
        conteudo = json.loads(texto)
        print("✅ Conteúdo parseado com sucesso!")
        
        # Valida campos obrigatórios
        if not conteudo.get('biografia'):
            raise ValueError("Campo 'biografia' vazio")
        if not conteudo.get('reflexao'):
            raise ValueError("Campo 'reflexao' vazio")
            
        return conteudo
        
    except Exception as e:
        print(f"❌ Erro na IA: {e}")
        raise

def gerar_html(santo, conteudo, imagem_url=None):
    """Gera HTML completo e impactante com suporte a Dark Mode"""
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
    
    # Monta mensagem
    mensagem = f"{conteudo['biografia']}\n\n\"{conteudo['frase']}\"\n\n{conteudo['reflexao']}"
    
    # Converte para HTML
    paragrafos = mensagem.split('\n\n')
    mensagem_html = ''
    for p in paragrafos:
        if p.strip():
            # Detecta citação (entre aspas)
            if p.strip().startswith('"') and p.strip().endswith('"'):
                p_html = p.replace('\n', '<br>')
                mensagem_html += f'<blockquote class="quote">{p_html}</blockquote>\n'
            else:
                p_html = p.replace('\n', '<br>')
                mensagem_html += f'<p>{p_html}</p>\n'
    
    # Virtudes
    virtudes_html = ' '.join([f'<span class="badge">{v}</span>' for v in conteudo.get('virtudes', [])])
    
    # Header com imagem ou SVG
    if imagem_url:
        header_content = f'<img src="{imagem_url}" alt="{santo["nome"]}" class="saint-photo" onerror="this.style.display=\'none\'; document.querySelector(\'.svg-fallback\').style.display=\'flex\';">'
        svg_fallback = f'<div class="svg-fallback" style="display:none;">{gerar_svg_fallback()}</div>'
    else:
        header_content = f'<div class="svg-fallback">{gerar_svg_fallback()}</div>'
        svg_fallback = ''
    
    return f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{santo['nome']} - Santo do Dia</title>
    <meta name="description" content="Conheça a história de {santo['nome']} e uma reflexão para seu dia">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        :root {{
            --primary: #764ba2;
            --secondary: #667eea;
            --accent: #f093fb;
            --text-dark: #2d3748;
            --text-light: #4a5568;
            --bg-light: #f7fafc;
            --card-bg: #ffffff;
            --footer-bg: rgba(102,126,234,0.05);
        }}
        
        /* Dark Mode */
        @media (prefers-color-scheme: dark) {{
            :root {{
                --text-dark: #e2e8f0;
                --text-light: #cbd5e0;
                --bg-light: #1a202c;
                --card-bg: #2d3748;
                --footer-bg: rgba(102,126,234,0.15);
            }}
        }}
        
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            min-height: 100vh;
            background: linear-gradient(135deg, var(--secondary) 0%, var(--primary) 100%);
            padding: 0;
            margin: 0;
            animation: gradientShift 15s ease infinite;
            background-size: 200% 200%;
        }}
        
        @keyframes gradientShift {{
            0%, 100% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
        }}
        
        .container {{
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .card {{
            background: var(--card-bg);
            border-radius: 24px;
            overflow: hidden;
            box-shadow: 0 30px 80px rgba(0,0,0,0.3);
            animation: fadeInUp 0.8s ease;
            margin-top: 20px;
        }}
        
        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        .header {{
            position: relative;
            height: 400px;
            background: linear-gradient(180deg, rgba(102,126,234,0.1) 0%, rgba(118,75,162,0.1) 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
        }}
        
        .saint-photo {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.3s ease;
        }}
        
        .saint-photo:hover {{
            transform: scale(1.05);
        }}
        
        .saint-icon {{
            width: 100%;
            height: 100%;
            max-width: 800px;
            max-height: 600px;
        }}
        
        .svg-fallback {{
            display: flex;
            align-items: center;
            justify-content: center;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, rgba(102,126,234,0.05) 0%, rgba(118,75,162,0.05) 100%);
        }}
        
        .content {{
            padding: 50px;
        }}
        
        .title-section {{
            text-align: center;
            margin-bottom: 40px;
            animation: fadeIn 1s ease 0.3s both;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}
        
        h1 {{
            font-family: 'Playfair Display', serif;
            font-size: 3em;
            font-weight: 700;
            background: linear-gradient(135deg, var(--secondary) 0%, var(--primary) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 15px;
            line-height: 1.2;
        }}
        
        .date {{
            font-size: 1.1em;
            color: var(--text-light);
            font-weight: 400;
            letter-spacing: 1px;
            text-transform: uppercase;
        }}
        
        .badges {{
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            justify-content: center;
            margin: 35px 0 45px 0;
            animation: fadeIn 1s ease 0.5s both;
        }}
        
        .badge {{
            display: inline-block;
            padding: 10px 24px;
            background: linear-gradient(135deg, var(--secondary), var(--primary));
            color: white;
            border-radius: 50px;
            font-size: 0.95em;
            font-weight: 500;
            box-shadow: 0 4px 15px rgba(102,126,234,0.3);
            transition: all 0.3s ease;
        }}
        
        .badge:hover {{
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(102,126,234,0.4);
        }}
        
        .text {{
            color: var(--text-dark);
            line-height: 1.9;
            font-size: 1.1em;
            animation: fadeIn 1s ease 0.7s both;
        }}
        
        .text p {{
            margin-bottom: 25px;
            text-align: justify;
        }}
        
        .quote {{
            font-family: 'Playfair Display', serif;
            font-size: 1.35em;
            font-style: italic;
            text-align: center;
            color: var(--primary);
            padding: 35px 40px;
            margin: 40px 0;
            background: linear-gradient(135deg, rgba(102,126,234,0.08) 0%, rgba(118,75,162,0.08) 100%);
            border-radius: 16px;
            border-left: 5px solid var(--primary);
            position: relative;
            box-shadow: 0 4px 20px rgba(118,75,162,0.1);
        }}
        
        @media (prefers-color-scheme: dark) {{
            .quote {{
                background: linear-gradient(135deg, rgba(102,126,234,0.2) 0%, rgba(118,75,162,0.2) 100%);
                color: var(--accent);
            }}
        }}
        
        .quote::before {{
            content: '"';
            font-size: 4em;
            position: absolute;
            top: -10px;
            left: 20px;
            color: var(--accent);
            opacity: 0.3;
            font-family: Georgia, serif;
        }}
        
        .footer {{
            text-align: center;
            padding: 40px 50px;
            background: var(--footer-bg);
            border-top: 1px solid rgba(118,75,162,0.1);
            animation: fadeIn 1s ease 0.9s both;
        }}
        
        .footer p {{
            font-size: 1.15em;
            color: var(--text-light);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }}
        
        .emoji {{
            font-size: 1.5em;
            display: inline-block;
            animation: pulse 2s ease-in-out infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(1.1); }}
        }}
        
        /* Responsivo Mobile */
        @media (max-width: 768px) {{
            .container {{
                padding: 10px;
            }}
            
            .card {{
                border-radius: 16px;
                margin-top: 10px;
            }}
            
            .header {{
                height: 300px;
            }}
            
            .content {{
                padding: 30px 25px;
            }}
            
            h1 {{
                font-size: 2em;
            }}
            
            .date {{
                font-size: 0.95em;
            }}
            
            .badges {{
                gap: 8px;
                margin: 25px 0 35px 0;
            }}
            
            .badge {{
                padding: 8px 18px;
                font-size: 0.85em;
            }}
            
            .text {{
                font-size: 1em;
            }}
            
            .quote {{
                font-size: 1.15em;
                padding: 25px 20px;
                margin: 30px 0;
            }}
            
            .quote::before {{
                font-size: 3em;
                left: 10px;
            }}
            
            .footer {{
                padding: 30px 25px;
            }}
            
            .footer p {{
                font-size: 1em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <div class="header">
                {header_content}
                {svg_fallback}
            </div>
            
            <div class="content">
                <div class="title-section">
                    <h1>{santo['nome']}</h1>
                    <p class="date">{data_br}</p>
                </div>
                
                <div class="badges">
                    {virtudes_html}
                </div>
                
                <div class="text">
                    {mensagem_html}
                </div>
            </div>
            
            <div class="footer">
                <p>
                    <span class="emoji">🙏</span>
                    Que esta mensagem ilumine seu dia!
                    <span class="emoji">✨</span>
                </p>
            </div>
        </div>
    </div>
</body>
</html>'''

# ========== MAIN ==========

if __name__ == "__main__":
    print("=" * 70)
    print("🎯 SANTO DO DIA - GERADOR")
    print("=" * 70)
    print(f"🕐 Horário: Brasil (UTC-3)")
    print("")
    
    try:
        # 1. Buscar santo
        santo = buscar_santo_do_dia()
        print(f"✅ Santo: {santo['nome']}")
        print(f"📅 Data: {santo['data']}")
        print(f"📡 Fonte: {santo['fonte']}")
        print("")
        
        # 2. Buscar imagem
        imagem_url = buscar_imagem_santo(santo['nome'])
        if imagem_url:
            print(f"✅ Imagem: {imagem_url}")
        else:
            print(f"ℹ️ Usando ícone SVG (imagem não encontrada)")
        print("")
        
        # 3. Gerar conteúdo IA
        conteudo = gerar_conteudo_ia(santo['nome'])
        print(f"📊 Biografia: {len(conteudo['biografia'])} chars")
        print(f"📊 Reflexão: {len(conteudo['reflexao'])} chars")
        print(f"📊 Virtudes: {len(conteudo.get('virtudes', []))} itens")
        print("")
        
        # 4. Gerar HTML
        html = gerar_html(santo, conteudo, imagem_url)
        
        # 5. Salvar
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html)
        
        print("=" * 70)
        print("✅ SUCESSO!")
        print("=" * 70)
        print(f"💾 Arquivo: index.html")
        print(f"📏 Tamanho: {len(html)} chars")
        print(f"🎉 Santo: {santo['nome']}")
        print("")
        
    except Exception as e:
        print("")
        print("=" * 70)
        print("❌ ERRO!")
        print("=" * 70)
        print(f"⚠️ {str(e)}")
        print("")
        exit(1)
