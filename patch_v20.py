from pathlib import Path
import re
import base64

root = Path('site/math-with-pedro-deploy-v17')
PT_WA = 'https://wa.me/14075802652?text=Oi%20Pedro%21%20Tenho%20interesse%20nas%20aulas%20de%20SAT%20Math%20e%20gostaria%20de%20tirar%20uma%20d%C3%BAvida.'
EN_WA = 'https://wa.me/14075802652?text=Hi%20Pedro%21%20I%20have%20a%20question%20about%20SAT%20Math%20tutoring.'
WA_PNG_B64 = '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'
(root/'static/whatsapp-green.png').write_bytes(base64.b64decode(WA_PNG_B64))
WA_ICON = '''<img class="wa-icon" src="/static/whatsapp-green.png" alt="" aria-hidden="true">'''

# Portuguese: make WhatsApp a primary header contact action.
p = root/'pt/index.html'
x = p.read_text(encoding='utf-8')
# Remove internal offer-positioning copy that should not be customer-facing.
x = re.sub(r'<h2[^>]*>\s*Um plano principal\. Uma opção avulsa\.\s*</h2>', '', x, flags=re.I)
x = re.sub(r'<p[^>]*>\s*O Plano SAT Math de 4 semanas é a principal oferta\. A aula avulsa continua disponível para quem precisa de ajuda pontual\.\s*</p>', '', x, flags=re.I)
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
.wa-icon{width:20px!important;height:20px!important;min-width:20px!important;min-height:20px!important;max-width:20px!important;max-height:20px!important;display:block!important;object-fit:contain!important;flex:0 0 20px!important}
.contact-whatsapp-card svg.wa-icon{width:20px!important;height:20px!important;max-width:20px!important;max-height:20px!important}
.wa-top-button{display:inline-flex;align-items:center;gap:8px;background:#fff;color:#142d4e;text-decoration:none;font-weight:800;border:1px solid #dce4ef;border-radius:999px;padding:9px 13px;box-shadow:none;transition:transform .18s ease,border-color .18s ease}
.wa-top-button:hover{transform:translateY(-1px);border-color:#20c66a}
.mobile-wa-button{display:flex!important;align-items:center!important;justify-content:center!important;gap:9px!important;background:#fff!important;color:#142d4e!important;border:1px solid #bfe7cf!important;border-radius:12px!important;padding:12px 14px!important;font-weight:800!important;margin:4px 0!important}
.contact-card{grid-template-columns:1fr!important;gap:26px!important;align-items:stretch!important;padding:34px!important}
.contact-card>div:first-child{max-width:760px}
.contact-card h2{max-width:760px}
.contact-actions{display:grid!important;grid-template-columns:repeat(3,minmax(0,1fr))!important;gap:14px!important;align-items:stretch!important}
.contact-method{min-width:0;min-height:98px;justify-content:center;padding:16px 17px!important;border-radius:16px!important;box-sizing:border-box}
.contact-method strong{font-size:.98rem!important;line-height:1.28!important;overflow-wrap:anywhere!important;word-break:break-word}
.contact-method small{margin-top:2px}
.contact-whatsapp-card{background:#f2fbf6!important;border-color:#bfe7cf!important;color:#176b3a!important;position:relative}
.contact-whatsapp-card .contact-icon{position:absolute;right:14px;top:14px;display:grid;place-items:center;width:30px;height:30px;background:transparent;color:inherit}
.contact-whatsapp-card .contact-icon .wa-icon{width:26px!important;height:26px!important;min-width:26px!important;min-height:26px!important;max-width:26px!important;max-height:26px!important}
.whatsapp-float{display:grid!important;place-items:center!important;width:56px!important;height:56px!important;padding:0!important;border-radius:50%!important;background:#fff!important;border:1px solid #bfe7cf!important;color:#142d4e!important;box-shadow:0 12px 30px rgba(0,0,0,.18)!important}
.whatsapp-float .wa-icon{width:30px!important;height:30px!important;min-width:30px!important;min-height:30px!important;max-width:30px!important;max-height:30px!important}
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
