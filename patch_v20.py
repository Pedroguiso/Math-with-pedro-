from pathlib import Path

root = Path('site/math-with-pedro-deploy-v17')
PT_WA = 'https://wa.me/14075802652?text=Oi%20Pedro%21%20Tenho%20interesse%20nas%20aulas%20de%20SAT%20Math%20e%20gostaria%20de%20tirar%20uma%20d%C3%BAvida.'
EN_WA = 'https://wa.me/14075802652?text=Hi%20Pedro%21%20I%20have%20a%20question%20about%20SAT%20Math%20tutoring.'
WA_ICON = '''<svg class="wa-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M6.62 10.79a15.46 15.46 0 0 0 6.59 6.59l2.2-2.2a1 1 0 0 1 1.02-.24c1.12.37 2.33.57 3.57.57a1 1 0 0 1 1 1V20a1 1 0 0 1-1 1C10.61 21 3 13.39 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>'''

# Portuguese: make WhatsApp a primary header contact action.
p = root/'pt/index.html'
x = p.read_text(encoding='utf-8')
old = '<a class="login-link" href="login.html">Área do Aluno</a><a class="button button-small button-contact-top" href="#contact">Contato</a><a class="button button-small" href="apply.html">Agendar Aula Grátis</a>'
new = f'<a class="login-link" href="login.html">Área do Aluno</a><a class="wa-top-button" href="{PT_WA}" target="_blank" rel="noopener" aria-label="Falar com Pedro no WhatsApp">{WA_ICON}<span>WhatsApp</span></a><a class="button button-small" href="apply.html">Agendar Aula Grátis</a>'
x = x.replace(old, new)

# Upgrade the Portuguese mobile menu WhatsApp item to a real green button.
old = f'<a href="{PT_WA}" target="_blank" rel="noopener">WhatsApp</a>'
new = f'<a class="mobile-wa-button" href="{PT_WA}" target="_blank" rel="noopener">{WA_ICON}<span>WhatsApp</span></a>'
x = x.replace(old, new)

# Floating action becomes icon-first rather than a text pill.
old = f'<a class="whatsapp-float" href="{PT_WA}" target="_blank" rel="noopener" aria-label="Falar com Pedro no WhatsApp">WhatsApp</a>'
new = f'<a class="whatsapp-float" href="{PT_WA}" target="_blank" rel="noopener" aria-label="Falar com Pedro no WhatsApp" title="WhatsApp">{WA_ICON}<span class="sr-only">WhatsApp</span></a>'
x = x.replace(old, new)

# Make WhatsApp contact tile consistent with the other contact tiles.
old = f'<a class="button contact-whatsapp" href="{PT_WA}" target="_blank" rel="noopener">Falar com Pedro no WhatsApp</a>'
new = f'<a class="contact-method contact-whatsapp-card" href="{PT_WA}" target="_blank" rel="noopener"><span class="contact-icon">{WA_ICON}</span><small>WHATSAPP</small><strong>Falar com Pedro</strong></a>'
x = x.replace(old, new)
p.write_text(x, encoding='utf-8')

# English contact section gets the same balanced contact tiles.
p = root/'index.html'
x = p.read_text(encoding='utf-8')
old = f'<a class="button contact-whatsapp" href="{EN_WA}" target="_blank" rel="noopener">WhatsApp Pedro</a>'
new = f'<a class="contact-method contact-whatsapp-card" href="{EN_WA}" target="_blank" rel="noopener"><span class="contact-icon">{WA_ICON}</span><small>WHATSAPP</small><strong>Message Pedro</strong></a>'
x = x.replace(old, new)
p.write_text(x, encoding='utf-8')

# Visual cleanup for contact section and WhatsApp controls.
css = root/'static/site.css'
c = css.read_text(encoding='utf-8')
append = r'''

/* V20: prominent WhatsApp + balanced contact layout */
.sr-only{position:absolute!important;width:1px!important;height:1px!important;padding:0!important;margin:-1px!important;overflow:hidden!important;clip:rect(0,0,0,0)!important;white-space:nowrap!important;border:0!important}
.wa-icon{width:20px;height:20px;display:block;fill:currentColor;flex:0 0 auto}
.wa-top-button{display:inline-flex;align-items:center;gap:8px;background:#1f9d55;color:#fff;text-decoration:none;font-weight:800;border-radius:999px;padding:10px 15px;box-shadow:0 8px 20px rgba(31,157,85,.22);transition:transform .18s ease,box-shadow .18s ease}
.wa-top-button:hover{transform:translateY(-1px);box-shadow:0 11px 25px rgba(31,157,85,.28)}
.mobile-wa-button{display:flex!important;align-items:center!important;justify-content:center!important;gap:9px!important;background:#1f9d55!important;color:#fff!important;border-radius:12px!important;padding:12px 14px!important;font-weight:800!important;margin:4px 0!important}
.contact-card{grid-template-columns:1fr!important;gap:26px!important;align-items:stretch!important;padding:34px!important}
.contact-card>div:first-child{max-width:760px}
.contact-card h2{max-width:760px}
.contact-actions{display:grid!important;grid-template-columns:repeat(3,minmax(0,1fr))!important;gap:14px!important;align-items:stretch!important}
.contact-method{min-width:0;min-height:98px;justify-content:center;padding:16px 17px!important;border-radius:16px!important;box-sizing:border-box}
.contact-method strong{font-size:.98rem!important;line-height:1.28!important;overflow-wrap:anywhere!important;word-break:break-word}
.contact-method small{margin-top:2px}
.contact-whatsapp-card{background:#f2fbf6!important;border-color:#bfe7cf!important;color:#176b3a!important;position:relative}
.contact-whatsapp-card .contact-icon{position:absolute;right:14px;top:14px;display:grid;place-items:center;width:34px;height:34px;border-radius:50%;background:#1f9d55;color:#fff}
.whatsapp-float{display:grid!important;place-items:center!important;width:56px!important;height:56px!important;padding:0!important;border-radius:50%!important;background:#1f9d55!important;color:#fff!important;box-shadow:0 12px 30px rgba(0,0,0,.24)!important}
.whatsapp-float .wa-icon{width:25px;height:25px}
@media(max-width:1080px){
  .wa-top-button span{display:none}
  .wa-top-button{width:42px;height:42px;padding:0;justify-content:center}
}
@media(max-width:900px){
  .contact-card{padding:26px!important}
  .contact-actions{grid-template-columns:1fr!important}
  .contact-method{min-height:78px}
  .wa-top-button{display:none!important}
}
@media(max-width:640px){
  .contact-card{padding:20px!important;gap:22px!important}
  .contact-actions{gap:10px!important}
  .contact-method{min-height:72px;padding:14px 15px!important}
  .contact-method strong{font-size:.95rem!important}
  .whatsapp-float{right:16px!important;bottom:84px!important;width:54px!important;height:54px!important}
}
'''
if 'V20: prominent WhatsApp' not in c:
    c += append
css.write_text(c, encoding='utf-8')
