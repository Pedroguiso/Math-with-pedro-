from pathlib import Path
import re

root = Path('site/math-with-pedro-deploy-v17')
app = root/'app.py'
s = app.read_text(encoding='utf-8')

# imports
s = s.replace('from urllib.parse import parse_qs, quote, unquote, urlencode\n', 'from urllib import request as urllib_request\nfrom urllib.parse import parse_qs, quote, unquote, urlencode\n')

# env vars
needle = 'PUBLIC_PHONE = os.environ.get("PUBLIC_PHONE", "407-580-2652")\n'
insert = needle + 'PUBLIC_SITE_URL = os.environ.get("PUBLIC_SITE_URL", "https://mathwithpedro.com").rstrip("/")\nGOOGLE_MEET_URL = os.environ.get("GOOGLE_MEET_URL", "").strip()\nPUBLIC_WHATSAPP = os.environ.get("PUBLIC_WHATSAPP", "").strip()\nBREVO_API_KEY = os.environ.get("BREVO_API_KEY", "").strip()\nBREVO_SENDER_EMAIL = os.environ.get("BREVO_SENDER_EMAIL", PUBLIC_CONTACT_EMAIL or os.environ.get("SMTP_USER", "")).strip()\nBREVO_SENDER_NAME = os.environ.get("BREVO_SENDER_NAME", "Pedro | Math with Pedro").strip()\n'
if needle in s and 'BREVO_API_KEY' not in s:
    s = s.replace(needle, insert)

# production warning
old_warn = '    if not os.environ.get("SMTP_HOST") or not (os.environ.get("SMTP_FROM") or os.environ.get("SMTP_USER")):\n        log.warning("SMTP is not configured; bookings will still be stored, but confirmation/notification emails will not be sent.")\n'
new_warn = '    if not BREVO_API_KEY and (not os.environ.get("SMTP_HOST") or not (os.environ.get("SMTP_FROM") or os.environ.get("SMTP_USER"))):\n        log.warning("Email delivery is not configured; bookings will still be stored, but confirmation/notification emails will not be sent.")\n'
s = s.replace(old_warn, new_warn)

# replace email functions block
start = s.index('def smtp_configured() -> bool:\n')
end = s.index('\ndef lead_owner_email(', start)
new_email_block = r'''def smtp_configured() -> bool:
    return bool(os.environ.get("SMTP_HOST") and (os.environ.get("SMTP_FROM") or os.environ.get("SMTP_USER")))


def brevo_configured() -> bool:
    return bool(BREVO_API_KEY and BREVO_SENDER_EMAIL)


def email_configured() -> bool:
    return brevo_configured() or smtp_configured()


def whatsapp_number() -> str:
    digits = re.sub(r"\D", "", PUBLIC_WHATSAPP or PUBLIC_PHONE)
    if len(digits) == 10:
        digits = "1" + digits
    return digits


def whatsapp_link(language: str = "en") -> str:
    message = (
        "Oi Pedro! Tenho interesse nas aulas de SAT Math e gostaria de tirar uma dúvida."
        if language == "pt"
        else "Hi Pedro! I have a question about SAT Math tutoring."
    )
    return f"https://wa.me/{whatsapp_number()}?text={quote(message)}"


def add_to_calendar_url(lead: sqlite3.Row | dict) -> str:
    try:
        start = datetime.fromisoformat(str(lead["preferred_session"]))
        if start.tzinfo is None:
            start = start.replace(tzinfo=timezone.utc)
        start = start.astimezone(timezone.utc)
        service = lead["service_option"] or "accelerator"
    except Exception:
        return ""
    end = start + timedelta(minutes=SERVICE_DURATION_MINUTES.get(service, 50))
    dates = start.strftime("%Y%m%dT%H%M%SZ") + "/" + end.strftime("%Y%m%dT%H%M%SZ")
    details = "1-on-1 SAT Math session with Pedro."
    if GOOGLE_MEET_URL:
        details += f" Join Google Meet: {GOOGLE_MEET_URL}"
    params = {
        "action": "TEMPLATE",
        "text": "SAT Math with Pedro",
        "dates": dates,
        "details": details,
        "location": GOOGLE_MEET_URL or "Online",
    }
    return "https://calendar.google.com/calendar/render?" + urlencode(params)


def send_email(to_address: str, subject: str, text: str, *, reply_to: str | None = None, html_body: str | None = None) -> None:
    if not email_configured() or not to_address:
        raise RuntimeError("Email delivery is not configured")

    if brevo_configured():
        payload = {
            "sender": {"name": BREVO_SENDER_NAME, "email": BREVO_SENDER_EMAIL},
            "to": [{"email": to_address}],
            "subject": subject,
            "textContent": text,
        }
        if html_body:
            payload["htmlContent"] = html_body
        if reply_to:
            payload["replyTo"] = {"email": reply_to}
        req = urllib_request.Request(
            "https://api.brevo.com/v3/smtp/email",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "accept": "application/json",
                "content-type": "application/json",
                "api-key": BREVO_API_KEY,
            },
            method="POST",
        )
        with urllib_request.urlopen(req, timeout=12) as resp:
            if resp.status >= 300:
                raise RuntimeError(f"Brevo returned HTTP {resp.status}")
        return

    host = os.environ["SMTP_HOST"]
    port = int(os.environ.get("SMTP_PORT", "587"))
    username = os.environ.get("SMTP_USER", "")
    password = os.environ.get("SMTP_PASSWORD", "")
    sender = os.environ.get("SMTP_FROM") or username
    use_ssl = os.environ.get("SMTP_USE_SSL", "0").lower() in {"1", "true", "yes"} or port == 465
    use_starttls = os.environ.get("SMTP_STARTTLS", "1").lower() in {"1", "true", "yes"}

    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = to_address
    msg["Subject"] = subject
    if reply_to:
        msg["Reply-To"] = reply_to
    msg.set_content(text)
    if html_body:
        msg.add_alternative(html_body, subtype="html")

    smtp_cls = smtplib.SMTP_SSL if use_ssl else smtplib.SMTP
    with smtp_cls(host, port, timeout=10) as smtp:
        if not use_ssl and use_starttls:
            smtp.starttls()
        if username:
            smtp.login(username, password)
        smtp.send_message(msg)
'''
s = s[:start] + new_email_block + s[end:]

# Replace parent_confirmation_email function completely
start = s.index('def parent_confirmation_email(')
end = s.index('\ndef rate_limit_ok(', start)
new_parent = r'''def parent_confirmation_email(lead: sqlite3.Row | dict) -> tuple[str, str, str]:
    def g(key):
        try:
            return lead[key]
        except Exception:
            return ""

    lang = "pt" if g("language") == "pt" else "en"
    session_label = business_datetime_label(g("preferred_session"), lang)
    meet_url = GOOGLE_MEET_URL
    calendar_url = add_to_calendar_url(lead)
    wa_url = whatsapp_link(lang)
    phone = display_phone(PUBLIC_PHONE)

    if g("service_option") == "single":
        if lang == "pt":
            subject = "Sua aula de Matemática do SAT está agendada"
            intro = f"Sua aula particular de 60 minutos de Matemática do SAT para {g('student_name')} está agendada."
            close = "O valor da aula avulsa é US$ 70."
        else:
            subject = "Your SAT Math session is booked"
            intro = f"Your private 60-minute SAT Math session for {g('student_name')} is booked."
            close = "The single-session rate is $70."
    else:
        if lang == "pt":
            subject = "Sua aula experimental gratuita de SAT Math está agendada"
            intro = f"Sua aula experimental gratuita de 50 minutos para {g('student_name')} está agendada."
            close = "Não há pagamento para esta primeira aula. Se decidir continuar depois, o Plano SAT Math de 4 semanas custa US$ 200 por quatro aulas de 60 minutos."
        else:
            subject = "Your free SAT Math Accelerator session is booked"
            intro = f"Your free 50-minute first session of the 4-Week SAT Math Accelerator for {g('student_name')} is booked."
            close = "There is no payment for this first session. If you decide to continue afterward, the 4-Week Accelerator is $200 for four paid 60-minute sessions."

    meet_text_pt = f"Google Meet: {meet_url}" if meet_url else "O link do Google Meet será enviado antes da aula."
    meet_text_en = f"Google Meet: {meet_url}" if meet_url else "The Google Meet link will be sent before the session."

    if lang == "pt":
        text = f"""Olá {g('parent_name')},

{intro}

Horário agendado: {session_label}
{meet_text_pt}

{close}

FAQ rápido
• O que acontece na primeira aula? Vamos identificar as prioridades que mais custam pontos e trabalhar questões direcionadas.
• O que o aluno deve ter em mãos? Computador, calculadora, papel para rascunho e, se tiver, resultados recentes do Bluebook.
• Há algum compromisso depois da aula? Não. A aula experimental é gratuita e sem compromisso.
• Precisa mudar o horário? Responda este e-mail ou fale comigo diretamente pelo WhatsApp / telefone {phone}.

WhatsApp: {wa_url}
{('Adicionar ao Google Calendar: ' + calendar_url) if calendar_url else ''}

— Pedro
Math with Pedro
"""
        html_body = f"""<!doctype html><html><body style="font-family:Arial,sans-serif;line-height:1.55;color:#162033;background:#f5f7fb;padding:24px"><div style="max-width:640px;margin:auto;background:#fff;border-radius:18px;padding:28px"><p>Olá <strong>{html.escape(str(g('parent_name')))}</strong>,</p><p>{html.escape(intro)}</p><div style="background:#f3f6fb;border-radius:14px;padding:16px;margin:20px 0"><strong>Horário:</strong> {html.escape(session_label)}<br><strong>Formato:</strong> Online pelo Google Meet</div>{f'<p><a href="{html.escape(meet_url)}" style="display:inline-block;background:#163b67;color:#fff;text-decoration:none;padding:13px 18px;border-radius:10px;font-weight:700">Entrar no Google Meet</a></p>' if meet_url else ''}{f'<p><a href="{html.escape(calendar_url)}" style="display:inline-block;border:1px solid #cbd5e1;color:#163b67;text-decoration:none;padding:11px 16px;border-radius:10px;font-weight:700">Adicionar ao Google Calendar</a></p>' if calendar_url else ''}<p>{html.escape(close)}</p><h3 style="margin-top:28px">FAQ rápido</h3><p><strong>O que acontece na primeira aula?</strong><br>Vamos identificar as prioridades que mais custam pontos e trabalhar questões direcionadas.</p><p><strong>O que o aluno deve ter em mãos?</strong><br>Computador, calculadora, papel para rascunho e, se tiver, resultados recentes do Bluebook.</p><p><strong>Há algum compromisso depois da aula?</strong><br>Não. A aula experimental é gratuita e sem compromisso.</p><p><strong>Precisa mudar o horário ou tem alguma dúvida?</strong><br>Responda este e-mail ou fale comigo diretamente.</p><p><a href="{html.escape(wa_url)}" style="display:inline-block;background:#1f9d55;color:#fff;text-decoration:none;padding:13px 18px;border-radius:10px;font-weight:700">Falar com Pedro no WhatsApp</a></p><p style="font-size:14px;color:#5b6575">Telefone: {html.escape(phone)} · E-mail: {html.escape(PUBLIC_CONTACT_EMAIL or BREVO_SENDER_EMAIL)}</p><p>— Pedro<br><strong>Math with Pedro</strong></p></div></body></html>"""
    else:
        text = f"""Hi {g('parent_name')},

{intro}

Booked time: {session_label}
{meet_text_en}

{close}

Quick FAQ
• What happens in the first session? We identify the SAT Math priorities costing the most points and work through targeted problems.
• What should the student have ready? A computer, calculator, scratch paper, and any recent Bluebook results if available.
• Is there any commitment afterward? No. The first session is free and there is no obligation to continue.
• Need to change the time? Reply to this email or contact me directly at {phone}.

WhatsApp: {wa_url}
{('Add to Google Calendar: ' + calendar_url) if calendar_url else ''}

— Pedro
Math with Pedro
"""
        html_body = f"""<!doctype html><html><body style="font-family:Arial,sans-serif;line-height:1.55;color:#162033;background:#f5f7fb;padding:24px"><div style="max-width:640px;margin:auto;background:#fff;border-radius:18px;padding:28px"><p>Hi <strong>{html.escape(str(g('parent_name')))}</strong>,</p><p>{html.escape(intro)}</p><div style="background:#f3f6fb;border-radius:14px;padding:16px;margin:20px 0"><strong>Booked time:</strong> {html.escape(session_label)}<br><strong>Format:</strong> Online via Google Meet</div>{f'<p><a href="{html.escape(meet_url)}" style="display:inline-block;background:#163b67;color:#fff;text-decoration:none;padding:13px 18px;border-radius:10px;font-weight:700">Join Google Meet</a></p>' if meet_url else ''}{f'<p><a href="{html.escape(calendar_url)}" style="display:inline-block;border:1px solid #cbd5e1;color:#163b67;text-decoration:none;padding:11px 16px;border-radius:10px;font-weight:700">Add to Google Calendar</a></p>' if calendar_url else ''}<p>{html.escape(close)}</p><h3 style="margin-top:28px">Quick FAQ</h3><p><strong>What happens in the first session?</strong><br>We identify the SAT Math priorities costing the most points and work through targeted problems.</p><p><strong>What should the student have ready?</strong><br>A computer, calculator, scratch paper, and any recent Bluebook results if available.</p><p><strong>Is there any commitment afterward?</strong><br>No. The first session is free and there is no obligation to continue.</p><p><strong>Need to change the time or have a question?</strong><br>Reply to this email or contact me directly.</p><p><a href="{html.escape(wa_url)}" style="display:inline-block;background:#1f9d55;color:#fff;text-decoration:none;padding:13px 18px;border-radius:10px;font-weight:700">WhatsApp Pedro</a></p><p style="font-size:14px;color:#5b6575">Phone: {html.escape(phone)} · Email: {html.escape(PUBLIC_CONTACT_EMAIL or BREVO_SENDER_EMAIL)}</p><p>— Pedro<br><strong>Math with Pedro</strong></p></div></body></html>"""

    return subject, text, html_body
'''
s = s[:start] + new_parent + s[end:]

# notify function uses email_configured + html body
s = s.replace('    if smtp_configured():\n', '    if email_configured():\n', 1)
s = s.replace('            subject, text = parent_confirmation_email(lead)\n            send_email(lead["email"], subject, text)\n', '            subject, text, html_body = parent_confirmation_email(lead)\n            send_email(lead["email"], subject, text, html_body=html_body)\n')

# Admin test config check supports Brevo
s = s.replace('        if not LEAD_NOTIFY_TO or not smtp_configured():\n            return respond(start_response, environ, "SMTP or LEAD_NOTIFY_TO is not configured.", "503 Service Unavailable", "text/plain; charset=utf-8", sensitive=True)\n', '        if not LEAD_NOTIFY_TO or not email_configured():\n            return respond(start_response, environ, "Email delivery or LEAD_NOTIFY_TO is not configured.", "503 Service Unavailable", "text/plain; charset=utf-8", sensitive=True)\n')

app.write_text(s, encoding='utf-8')

# HTML patches
EN_WA = 'https://wa.me/14075802652?text=Hi%20Pedro%21%20I%20have%20a%20question%20about%20SAT%20Math%20tutoring.'
PT_WA = 'https://wa.me/14075802652?text=Oi%20Pedro%21%20Tenho%20interesse%20nas%20aulas%20de%20SAT%20Math%20e%20gostaria%20de%20tirar%20uma%20d%C3%BAvida.'
MEET = 'https://meet.google.com/gkw-ssjw-waw'

for rel, lang in [('index.html','en'), ('pt/index.html','pt')]:
    p = root/rel
    x = p.read_text(encoding='utf-8')
    if lang=='en':
        x = x.replace('<a class="login-link" href="/login">Student Login</a><a class="button button-small" href="/apply">Start Free Session</a>', '<a class="login-link" href="/login">Student Login</a><a class="button button-small button-contact-top" href="#contact">Contact</a><a class="button button-small" href="/apply">Start Free Session</a>')
        x = x.replace('<a href="#faq">FAQ</a><a href="/login">Student Login</a>', '<a href="#faq">FAQ</a><a href="#contact">Contact</a><a href="/login">Student Login</a>')
        contact = f'''<section class="section contact-section" id="contact"><div class="shell contact-card"><div><div class="kicker">CONTACT</div><h2>Questions before booking?</h2><p>Reach out directly. I’m happy to answer questions about SAT Math, the free first session, or whether the 4-week plan is a good fit.</p></div><div class="contact-actions"><a class="contact-method" href="mailto:mathwithpedro@gmail.com"><small>EMAIL</small><strong>mathwithpedro@gmail.com</strong></a><a class="contact-method" href="tel:+14075802652"><small>PHONE / TEXT</small><strong>(407) 580-2652</strong></a><a class="button contact-whatsapp" href="{EN_WA}" target="_blank" rel="noopener">WhatsApp Pedro</a></div></div></section>'''
        x = x.replace('<section class="final-cta final-cta-v5"', contact + '\n<section class="final-cta final-cta-v5"')
        x = x.replace('<a href="sms:+14075802652">Text Pedro: (407) 580-2652</a>', '<a href="mailto:mathwithpedro@gmail.com">mathwithpedro@gmail.com</a><a href="tel:+14075802652">Call / text: (407) 580-2652</a><a href="'+EN_WA+'" target="_blank" rel="noopener">WhatsApp Pedro</a>')
    else:
        x = x.replace('<a class="login-link" href="login.html">Área do Aluno</a><a class="button button-small" href="apply.html">Agendar Aula Grátis</a>', '<a class="login-link" href="login.html">Área do Aluno</a><a class="button button-small button-contact-top" href="#contact">Contato</a><a class="button button-small" href="apply.html">Agendar Aula Grátis</a>')
        x = x.replace('<a href="#faq">FAQ</a><a href="login.html">Área do Aluno</a>', '<a href="#faq">FAQ</a><a href="#contact">Contato</a><a href="'+PT_WA+'" target="_blank" rel="noopener">WhatsApp</a><a href="login.html">Área do Aluno</a>')
        contact = f'''<section class="section contact-section contact-section-pt" id="contact"><div class="shell contact-card"><div><div class="kicker">CONTATO</div><h2>Quer falar comigo antes de agendar?</h2><p>Pode me chamar diretamente para tirar dúvidas sobre SAT Math, a aula experimental gratuita ou o plano de 4 semanas.</p></div><div class="contact-actions"><a class="button contact-whatsapp" href="{PT_WA}" target="_blank" rel="noopener">Falar com Pedro no WhatsApp</a><a class="contact-method" href="mailto:mathwithpedro@gmail.com"><small>E-MAIL</small><strong>mathwithpedro@gmail.com</strong></a><a class="contact-method" href="tel:+14075802652"><small>TELEFONE / SMS</small><strong>(407) 580-2652</strong></a></div></div></section>'''
        x = x.replace('<section class="final-cta final-cta-v5"', contact + '\n<section class="final-cta final-cta-v5"')
        x = x.replace('<a href="sms:+14075802652">Fale com Pedro: (407) 580-2652</a>', '<a href="'+PT_WA+'" target="_blank" rel="noopener">WhatsApp Pedro</a><a href="mailto:mathwithpedro@gmail.com">mathwithpedro@gmail.com</a><a href="tel:+14075802652">Telefone / SMS: (407) 580-2652</a>')
        x = x.replace('<footer class="footer">', f'<a class="whatsapp-float" href="{PT_WA}" target="_blank" rel="noopener" aria-label="Falar com Pedro no WhatsApp">WhatsApp</a><footer class="footer">')
    p.write_text(x, encoding='utf-8')

# success pages
p = root/'success.html'
x = p.read_text(encoding='utf-8')
x = x.replace('Check your email for the appointment details. Questions? Text Pedro directly at <a href="sms:+14075802652">(407) 580-2652</a>.', f'Your class will take place on Google Meet. The confirmation email also includes the link, a quick FAQ, and an add-to-calendar option. Questions? Text Pedro at <a href="sms:+14075802652">(407) 580-2652</a> or use WhatsApp.')
x = x.replace('<a class="button button-primary" href="/">Back to Home</a>', f'<div class="success-actions"><a class="button button-primary" href="{MEET}" target="_blank" rel="noopener">Open Google Meet</a><a class="button button-outline" href="{EN_WA}" target="_blank" rel="noopener">WhatsApp Pedro</a></div><a class="success-home-link" href="/">Back to Home</a>')
p.write_text(x, encoding='utf-8')

p = root/'pt/success.html'
x = p.read_text(encoding='utf-8')
x = x.replace('Confira seu e-mail para os detalhes. Dúvidas? Fale diretamente com o Pedro pelo número <a href="sms:+14075802652">(407) 580-2652</a>.', 'A aula será pelo Google Meet. O e-mail de confirmação também terá o link, um FAQ rápido e a opção de adicionar ao calendário. Dúvidas? Fale comigo pelo WhatsApp ou pelo número <a href="sms:+14075802652">(407) 580-2652</a>.')
x = x.replace('<a class="button button-primary" href="index.html">Voltar ao Início</a>', f'<div class="success-actions"><a class="button button-primary" href="{MEET}" target="_blank" rel="noopener">Abrir Google Meet</a><a class="button button-outline" href="{PT_WA}" target="_blank" rel="noopener">Falar no WhatsApp</a></div><a class="success-home-link" href="index.html">Voltar ao Início</a>')
p.write_text(x, encoding='utf-8')

# CSS
css = root/'static/site.css'
c = css.read_text(encoding='utf-8')
append = r'''

/* V19: contact + WhatsApp + confirmation actions */
.button-contact-top{background:transparent!important;color:var(--navy,#0b2442)!important;border:1px solid rgba(11,36,66,.22)!important;box-shadow:none!important}
.contact-section{padding-top:54px;padding-bottom:54px;background:#f5f8fc}
.contact-card{display:grid;grid-template-columns:1.15fr .85fr;gap:42px;align-items:center;background:#fff;border:1px solid rgba(20,45,78,.10);border-radius:24px;padding:38px;box-shadow:0 18px 50px rgba(20,45,78,.08)}
.contact-card h2{margin:.25rem 0 .75rem;font-size:clamp(2rem,4vw,3.1rem);line-height:1.02}
.contact-card p{max-width:650px;color:#526174;margin:0}
.contact-actions{display:flex;flex-direction:column;gap:12px}
.contact-method{display:flex;flex-direction:column;gap:3px;padding:13px 15px;border:1px solid #dce4ef;border-radius:14px;text-decoration:none;color:#142d4e;background:#fbfcfe}
.contact-method small{font-size:.72rem;letter-spacing:.09em;color:#758398;font-weight:700}
.contact-method strong{font-size:1rem;overflow-wrap:anywhere}
.contact-whatsapp{background:#1f9d55!important;color:#fff!important;border-color:#1f9d55!important;text-align:center;justify-content:center}
.whatsapp-float{position:fixed;right:18px;bottom:88px;z-index:80;background:#1f9d55;color:#fff;text-decoration:none;font-weight:800;border-radius:999px;padding:12px 17px;box-shadow:0 10px 28px rgba(0,0,0,.2)}
.success-actions{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-top:22px}
.success-home-link{display:inline-block;margin-top:18px;color:#41536c;font-weight:700}
@media(max-width:900px){.contact-card{grid-template-columns:1fr;gap:24px;padding:26px}.button-contact-top{display:none!important}}
@media(max-width:640px){.contact-section{padding:36px 0}.contact-card{border-radius:18px;padding:22px}.contact-card h2{font-size:2rem}.whatsapp-float{right:14px;bottom:84px;padding:11px 15px}.success-actions .button{width:100%}}
'''
if 'V19: contact + WhatsApp' not in c:
    c += append
css.write_text(c, encoding='utf-8')
