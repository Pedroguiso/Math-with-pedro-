from pathlib import Path

root = Path('site/math-with-pedro-deploy-v17')
PT_WA = 'https://wa.me/14075802652?text=Oi%20Pedro%21%20Tenho%20interesse%20nas%20aulas%20de%20SAT%20Math%20e%20gostaria%20de%20tirar%20uma%20d%C3%BAvida.'
EN_WA = 'https://wa.me/14075802652?text=Hi%20Pedro%21%20I%20have%20a%20question%20about%20SAT%20Math%20tutoring.'
WA_ICON = '''<svg class="wa-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.198-.347.223-.644.074-.297-.149-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.009-.371-.011-.57-.011-.198 0-.52.074-.792.372-.273.297-1.04 1.016-1.04 2.479s1.065 2.876 1.213 3.074c.149.198 2.095 3.2 5.076 4.487.709.306 1.262.489 1.69.625.71.226 1.357.194 1.87.118.57-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.981.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.897a9.825 9.825 0 0 1 2.893 6.991c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.055 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.14 1.588 5.945L.056 24l6.3-1.65a11.889 11.889 0 0 0 5.694 1.448h.005c6.558 0 11.894-5.335 11.897-11.893a11.821 11.821 0 0 0-3.488-8.413Z"/></svg>'''

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
