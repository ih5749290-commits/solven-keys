from flask import Flask, render_template_string
import sqlite3
import time
from datetime import datetime

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Solven Keys - Premium</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Roboto:wght@300;400;700&display=swap');
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body { 
            background-color: #050505; 
            color: #ffffff; 
            font-family: 'Roboto', sans-serif; 
            overflow-x: hidden;
        }

        /* Фон с частицами */
        #particles-js {
            position: fixed;
            width: 100%;
            height: 100%;
            top: 0;
            left: 0;
            z-index: -1;
            background: radial-gradient(circle at 50% 50%, #1a0000 0%, #000000 100%);
        }

        .container { 
            max-width: 900px; 
            margin: 0 auto; 
            padding: 40px 20px; 
            position: relative;
            z-index: 1;
        }

        h1 { 
            font-family: 'Orbitron', sans-serif;
            font-size: 3.5rem;
            color: #fff; 
            text-align: center; 
            text-transform: uppercase; 
            letter-spacing: 5px;
            text-shadow: 0 0 10px #ff0033, 0 0 20px #ff0033, 0 0 40px #ff0033;
            margin-bottom: 5px;
            animation: flicker 3s infinite alternate;
        }

        .subtitle {
            text-align: center;
            color: #ff0033;
            font-family: 'Orbitron', sans-serif;
            letter-spacing: 3px;
            margin-bottom: 40px;
            font-size: 1.2rem;
            text-shadow: 0 0 5px #ff0033;
        }

        @keyframes flicker {
            0%, 18%, 22%, 25%, 53%, 57%, 100% { text-shadow: 0 0 10px #ff0033, 0 0 20px #ff0033, 0 0 40px #ff0033, 0 0 80px #ff0033; }
            20%, 24%, 55% { text-shadow: none; }
        }

        .card { 
            background: rgba(15, 15, 15, 0.85); 
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 0, 51, 0.3); 
            border-radius: 15px; 
            padding: 30px; 
            margin-bottom: 30px; 
            box-shadow: 0 10px 30px rgba(0,0,0,0.8), inset 0 0 20px rgba(255, 0, 51, 0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(255,0,0,0.2), inset 0 0 30px rgba(255, 0, 51, 0.2);
            border-color: rgba(255, 0, 51, 0.8);
        }

        .card h2 { 
            font-family: 'Orbitron', sans-serif;
            color: #ff0033; 
            margin-bottom: 20px; 
            font-size: 1.8rem;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        table { width: 100%; border-collapse: separate; border-spacing: 0 10px; }
        th { 
            color: #aaa; 
            font-weight: 400; 
            text-transform: uppercase; 
            font-size: 0.85rem; 
            letter-spacing: 1px;
            padding: 10px 15px;
            text-align: left;
        }
        td { 
            padding: 15px; 
            background: rgba(255, 255, 255, 0.03);
            border-top: 1px solid rgba(255, 255, 255, 0.05);
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }
        td:first-child { border-left: 1px solid rgba(255, 255, 255, 0.05); border-radius: 10px 0 0 10px; }
        td:last-child { border-right: 1px solid rgba(255, 255, 255, 0.05); border-radius: 0 10px 10px 0; }
        tr:hover td { background: rgba(255, 0, 51, 0.1); }

        .rank-1 { color: #ffd700; font-weight: bold; font-size: 1.2rem; text-shadow: 0 0 10px #ffd700; }
        .rank-2 { color: #c0c0c0; font-weight: bold; font-size: 1.1rem; text-shadow: 0 0 10px #c0c0c0; }
        .rank-3 { color: #cd7f32; font-weight: bold; font-size: 1.1rem; text-shadow: 0 0 10px #cd7f32; }
        
        .key-active { 
            color: #00ff00; 
            font-weight: bold;
            text-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.6; }
            100% { opacity: 1; }
        }

        code {
            background: #000;
            padding: 4px 8px;
            border-radius: 5px;
            color: #ff0033;
            border: 1px solid #333;
        }

    </style>
</head>
<body>
    <!-- Анимированный фон -->
    <div id="particles-js"></div>

    <div class="container">
        <h1>Solven Keys</h1>
        <div class="subtitle">Premium Access</div>
        
        <div class="card">
            <h2>🏆 Топ покупателей</h2>
            <table>
                <tr><th>#</th><th>Игрок</th><th>Pubg ID</th><th>Ключей</th></tr>
                {% for user in top_users %}
                <tr>
                    <td class="rank-{{ loop.index }}">{{ loop.index }}</td>
                    <td>{{ user[1] or 'Аноним' }}</td>
                    <td><code>{{ user[2] or 'Не привязан' }}</code></td>
                    <td style="font-weight: bold; color: #fff;">{{ user[3] }}</td>
                </tr>
                {% endfor %}
            </table>
        </div>

        <div class="card">
            <h2>🕒 Активные тарифы</h2>
            <table>
                <tr><th>Владелец</th><th>Ключ</th><th>Осталось</th></tr>
                {% for key in active_keys %}
                <tr>
                    <td>{{ key[1] or 'Аноним' }}</td>
                    <td><code>{{ key[0] }}</code></td>
                    <td class="key-active">{{ key[2] }}</td>
                </tr>
                {% endfor %}
            </table>
        </div>
    </div>

    <!-- Скрипт для частиц -->
    <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
    <script>
        particlesJS("particles-js", {
            "particles": {
                "number": { "value": 80, "density": { "enable": true, "value_area": 800 } },
                "color": { "value": "#ff0033" },
                "shape": { "type": "circle" },
                "opacity": { "value": 0.5, "random": true, "anim": { "enable": true, "speed": 1, "opacity_min": 0.1, "sync": false } },
                "size": { "value": 3, "random": true, "anim": { "enable": true, "speed": 2, "size_min": 0.1, "sync": false } },
                "line_linked": { "enable": true, "distance": 150, "color": "#ff0033", "opacity": 0.4, "width": 1 },
                "move": { "enable": true, "speed": 3, "direction": "none", "random": true, "straight": false, "out_mode": "out", "bounce": false }
            },
            "interactivity": {
                "detect_on": "canvas",
                "events": {
                    "onhover": { "enable": true, "mode": "grab" },
                    "onclick": { "enable": true, "mode": "push" }
                },
                "modes": {
                    "grab": { "distance": 140, "line_linked": { "opacity": 1 } },
                    "push": { "particles_nb": 4 }
                }
            },
            "retina_detect": true
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    conn = sqlite3.connect('solven.db')
    c = conn.cursor()
    
    c.execute("SELECT user_id, username, pubg_id, total_keys FROM users ORDER BY total_keys DESC LIMIT 10")
    top_users = c.fetchall()
    
    c.execute("SELECT k.key, u.username, k.expires_at FROM keys k JOIN users u ON k.user_id = u.user_id WHERE k.expires_at > ?", (time.time(),))
    raw_keys = c.fetchall()
    conn.close()

    active_keys = []
    for key, username, expires_at in raw_keys:
        dt = datetime.fromtimestamp(expires_at) - datetime.now()
        hours, remainder = divmod(dt.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        active_keys.append((key, username, f"{hours} ч {minutes} мин"))

    return render_template_string(HTML_TEMPLATE, top_users=top_users, active_keys=active_keys)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
