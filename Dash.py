from flask import Flask, render_template_string
import pandas as pd
import plotly.express as px

# Simulação de dados reais de pontos do Recife
data = {
    "hora": ["10:00", "10:05", "10:10", "10:15", "10:20"],
    "Joana Bezerra": [10, 12, 15, 18, 20],
    "Derby": [5, 6, 7, 8, 9],
    "Afogados": [2, 3, 4, 5, 7],
    "Casa Forte": [1, 1, 2, 2, 3]
}
df = pd.DataFrame(data)

# Transformar em formato longo para Plotly
df_long = df.melt(id_vars="hora", var_name="Ponto", value_name="Nível de água")

# Criar gráfico interativo
fig = px.line(
    df_long, x="hora", y="Nível de água", color="Ponto",
    title="Monitoramento de Alagamentos - Recife",
    markers=True
)
fig.update_layout(template="plotly_dark", title_x=0.5)

# Converter gráfico para HTML
graph_html = fig.to_html(full_html=False)

# Inicializando o Flask
app = Flask(__name__)

@app.route("/")
def dashboard():
    # Verificação de alerta (nível crítico > 15 cm)
    alertas = []
    ultimo = df.iloc[-1]  # pega última medição
    for ponto, nivel in ultimo.items():
        if ponto != "hora" and nivel > 15:
            alertas.append(f"⚠️ Alerta de alagamento em {ponto} (nível: {nivel} cm)")

    return render_template_string("""
        <html>
        <head>
            <title>Dashboard Recife - Alagamentos</title>
            <style>
                body { font-family: Arial, sans-serif; background: #121212; color: white; text-align: center; }
                h1 { color: #00ccff; }
                .alerta { background: #ff4444; padding: 10px; margin: 10px; border-radius: 8px; }
                .graph { margin: 20px auto; width: 80%; }
            </style>
        </head>
        <body>
            <h1>🌧️ Monitoramento de Alagamentos - Recife</h1>
            {% if alertas %}
                {% for alerta in alertas %}
                    <div class="alerta">{{ alerta }}</div>
                {% endfor %}
            {% else %}
                <p>✅ Nenhum ponto crítico detectado</p>
            {% endif %}
            <div class="graph">
                {{ graph|safe }}
            </div>
        </body>
        </html>
    """, graph=graph_html, alertas=alertas)

if __name__ == "__main__":
    app.run(debug=True)
