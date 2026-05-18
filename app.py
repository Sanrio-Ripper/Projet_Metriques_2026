<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Températures Paris — Atelier Métriques</title>
  <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/chartjs-adapter-date-fns/dist/chartjs-adapter-date-fns.bundle.min.js"></script>

  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }

    body {
      min-height: 100vh;
      font-family: 'Space Grotesk', sans-serif;
      background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #1a1a2e);
      background-size: 400% 400%;
      animation: gradientBG 15s ease infinite;
      color: #fff;
      padding: 40px 20px;
    }

    @keyframes gradientBG {
      0% { background-position: 0% 50%; }
      50% { background-position: 100% 50%; }
      100% { background-position: 0% 50%; }
    }

    .container { max-width: 1200px; margin: 0 auto; }

    .header { text-align: center; margin-bottom: 40px; }

    .badge {
      display: inline-block;
      padding: 6px 16px;
      background: rgba(255, 255, 255, 0.1);
      backdrop-filter: blur(10px);
      border: 1px solid rgba(255, 255, 255, 0.2);
      border-radius: 50px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      letter-spacing: 2px;
      margin-bottom: 20px;
    }
    .badge::before {
      content: "●";
      color: #4ade80;
      margin-right: 6px;
      animation: pulse 2s infinite;
    }
    @keyframes pulse {
      0%, 100% { opacity: 1; }
      50% { opacity: 0.4; }
    }

    h1 {
      font-size: clamp(2rem, 5vw, 3.5rem);
      font-weight: 700;
      letter-spacing: -1px;
      line-height: 1.1;
      margin-bottom: 15px;
      background: linear-gradient(135deg, #fff 0%, #a78bfa 50%, #60a5fa 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }

    .subtitle { color: rgba(255, 255, 255, 0.6); font-size: 1rem; }

    .card {
      background: rgba(255, 255, 255, 0.05);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 24px;
      padding: 30px;
      box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    }

    .chart-container { position: relative; height: 500px; }

    #status {
      margin-top: 16px;
      text-align: center;
      font-family: 'JetBrains Mono', monospace;
      font-size: 12px;
      color: rgba(255, 255, 255, 0.5);
      letter-spacing: 1px;
    }

    .back {
      position: fixed;
      top: 20px;
      left: 20px;
      padding: 10px 20px;
      background: rgba(255, 255, 255, 0.05);
      backdrop-filter: blur(10px);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 50px;
      color: #fff;
      text-decoration: none;
      font-family: 'JetBrains Mono', monospace;
      font-size: 12px;
      transition: all 0.3s ease;
      z-index: 10;
    }
    .back:hover {
      background: rgba(255, 255, 255, 0.15);
      transform: translateX(-3px);
    }
  </style>
</head>

<body>
  <a href="/" class="back">← Accueil</a>

  <div class="container">
    <div class="header">
      <div class="badge">RAPPORT / TEMPÉRATURES</div>
      <h1>Températures<br>horaires Paris</h1>
      <p class="subtitle">Prévisions sur 7 jours • Source : open-meteo.com</p>
    </div>

    <div class="card">
      <div class="chart-container">
        <canvas id="chart"></canvas>
      </div>
      <div id="status"></div>
    </div>
  </div>

  <script>
    async function init() {
      try {
        const res = await fetch('/paris');
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const json = await res.json();

        const labels = json.map(p => new Date(p.datetime));
        const data = json.map(p => Number(p.temperature_c));

        new Chart(document.getElementById('chart'), {
          type: 'line',
          data: {
            labels: labels,
            datasets: [{
              label: 'Température (°C)',
              data: data,
              borderColor: '#a78bfa',
              backgroundColor: 'rgba(167, 139, 250, 0.15)',
              borderWidth: 2.5,
              fill: true,
              tension: 0.4,
              pointRadius: 0,
              pointHoverRadius: 6,
              pointHoverBackgroundColor: '#60a5fa',
              pointHoverBorderColor: '#fff',
              pointHoverBorderWidth: 2
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: { mode: 'index', intersect: false },
            plugins: {
              legend: { labels: { color: 'rgba(255,255,255,0.85)', font: { size: 13 } } },
              tooltip: {
                backgroundColor: 'rgba(15, 12, 41, 0.95)',
                borderColor: 'rgba(167, 139, 250, 0.3)',
                borderWidth: 1,
                padding: 12,
                callbacks: { label: ctx => ` ${ctx.parsed.y} °C` }
              }
            },
            scales: {
              x: {
                type: 'time',
                time: { unit: 'day', tooltipFormat: 'dd/MM HH:mm', displayFormats: { day: 'dd/MM' } },
                ticks: { color: 'rgba(255,255,255,0.5)' },
                grid: { color: 'rgba(255,255,255,0.05)' }
              },
              y: {
                ticks: { color: 'rgba(255,255,255,0.5)', callback: v => v + '°' },
                grid: { color: 'rgba(255,255,255,0.05)' }
              }
            }
          }
        });

        document.getElementById('status').textContent = `${json.length} POINTS CHARGÉS DEPUIS /PARIS`;
      } catch (err) {
        document.getElementById('status').textContent = 'ERREUR : ' + err.message;
        console.error(err);
      }
    }

    init();
  </script>
</body>
</html>
