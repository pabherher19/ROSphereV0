from flask import Flask, Response, request
import os

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    # Mensaje informativo para Vercel
    return """
    <html>
    <head>
        <title>ROSphere Monitor</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 40px;
                line-height: 1.6;
                color: #333;
                background-color: #f5f5f5;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background-color: white;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 {
                color: #2c3e50;
            }
            .info {
                background-color: #e3f2fd;
                padding: 15px;
                border-radius: 5px;
                margin: 20px 0;
            }
            .cta {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                text-decoration: none;
                border-radius: 5px;
                display: inline-block;
                margin-top: 20px;
            }
            code {
                background-color: #f8f9fa;
                padding: 2px 5px;
                border-radius: 3px;
                font-family: monospace;
            }
            .features {
                background-color: #f0f8ff;
                padding: 15px;
                border-radius: 5px;
                margin: 20px 0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🫁 ROSphere Monitor</h1>
            
            <div class="features">
                <h2>Características principales:</h2>
                <ul>
                    <li>Monitoreo de parámetros hemodinámicos en tiempo real</li>
                    <li>Selección entre 20 pacientes diferentes</li>
                    <li>Carga de datos desde archivos Excel para cada paciente</li>
                    <li>Simulación de tendencias en parámetros médicos</li>
                    <li>Predicción de riesgo mediante algoritmo de Machine Learning</li>
                </ul>
            </div>
            
            <div class="info">
                <p><strong>Nota importante:</strong> Esta aplicación Streamlit no puede ejecutarse directamente en Vercel.</p>
                <p>Vercel es una plataforma para aplicaciones sin servidor (serverless), mientras que Streamlit necesita ejecutarse como un servidor activo.</p>
            </div>
            
            <h2>Opciones para desplegar esta aplicación:</h2>
            <ol>
                <li><strong>Streamlit Cloud:</strong> La opción más sencilla para desplegar aplicaciones Streamlit.</li>
                <li><strong>Render:</strong> Plataforma que soporta bien aplicaciones Streamlit.</li>
                <li><strong>Railway:</strong> Ofrece una experiencia similar a Vercel pero con soporte para apps con servidor.</li>
                <li><strong>Heroku:</strong> Una plataforma clásica para este tipo de aplicaciones.</li>
            </ol>
            
            <h2>Para desarrollo local:</h2>
            <p>Ejecuta <code>streamlit run app.py</code> en tu entorno local.</p>
            
            <a href="https://github.com/pabherher19/ROSphereV0" class="cta">Ver en GitHub</a>
        </div>
    </body>
    </html>
    """

# Para pruebas locales
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))