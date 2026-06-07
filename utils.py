# Utility: build HTML tables safely (avoids f-string join escaping bug in Streamlit)
def tbl(headers, rows, col_widths=None):
    th = "".join(f"<th>{h}</th>" for h in headers)
    body = ""
    for row in rows:
        tds = ""
        for i, cell in enumerate(row):
            style = f' style="width:{col_widths[i]}"' if col_widths and i < len(col_widths) else ""
            tds += f"<td{style}>{cell}</td>"
        body += f"<tr>{tds}</tr>"
    return f'<table class="styled-table"><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table>'

def card(title, body_html, accent_color=None):
    border = f"border-left:3px solid {accent_color};" if accent_color else ""
    return f'<div class="glass-card" style="{border}">{("<div class=card-title>"+title+"</div>") if title else ""}{body_html}</div>'

def badge(text, style="blue"):
    return f'<span class="badge badge-{style}">{text}</span>'

def timeline(steps):
    colors = ["#4f9cf9","#22d3c5","#a78bfa","#fbbf24","#34d399","#f472b6"]
    html = ""
    for i, (title, detail) in enumerate(steps):
        c = colors[i % len(colors)]
        html += f'''<div class="timeline-item">
          <div class="timeline-dot" style="background:{c}22;color:{c};">{i+1}</div>
          <div><strong>{title}</strong> — {detail}</div>
        </div>'''
    return html

def info(text): return f'<div class="info-box">{text}</div>'
def warn(text): return f'<div class="warning-box">{text}</div>'
def ok(text):   return f'<div class="success-box">{text}</div>'
