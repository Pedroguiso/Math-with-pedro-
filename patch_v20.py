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

# Header WhatsApp.
old = '<a class="login-link" href="login.html">Área do Aluno</a><a class="button button-small button-contact-top" href="#contact">Contato</a><a class="button button-small" href="apply.html">Agendar Aula Grátis</a>'
new = f'<a class="login-link" href="login.html">Área do Aluno</a><a class="wa-top-button" href="{PT_WA}" target="_blank" rel="noopener" aria-label="Falar com Pedro no WhatsApp">{WA_ICON}<span>WhatsApp</span></a><a class="button button-small" href="apply.html">Agendar Aula Grátis</a>'
x = x.replace(old, new)

# Mobile-menu WhatsApp.
old = f'<a href="{PT_WA}" target="_blank" rel="noopener">WhatsApp</a>'
new = f'<a class="mobile-wa-button" href="{PT_WA}" target="_blank" rel="noopener">{WA_ICON}<span>WhatsApp</span></a>'
x = x.replace(old, new)

# Floating action.
old = f'<a class="whatsapp-float" href="{PT_WA}" target="_blank" rel="noopener" aria-label="Falar com Pedro no WhatsApp">WhatsApp</a>'
new = f'<a class="whatsapp-float" href="{PT_WA}" target="_blank" rel="noopener" aria-label="Falar com Pedro no WhatsApp" title="WhatsApp">{WA_ICON}<span class="sr-only">WhatsApp</span></a>'
x = x.replace(old, new)

# Rebuild the contact section from scratch so old/duplicate markup cannot survive.
x = re.sub(r'\s*<section class="section contact-section(?: contact-section-pt)?" id="contact">.*?</section>', '', x, flags=re.I|re.S)
pt_contact = f'''<section class="section contact-section contact-section-pt" id="contact"><div class="shell contact-card"><div class="contact-copy"><div class="kicker">CONTATO</div><h2>Quer falar comigo antes de agendar?</h2><p>Pode me chamar diretamente para tirar dúvidas sobre SAT Math, a aula experimental gratuita ou o plano de 4 semanas.</p></div><div class="contact-actions"><a class="contact-method contact-whatsapp-card" href="{PT_WA}" target="_blank" rel="noopener"><span class="contact-icon">{WA_ICON}</span><span class="contact-text"><small>WHATSAPP</small><strong>Falar com Pedro</strong></span></a><a class="contact-method" href="mailto:mathwithpedro@gmail.com"><span class="contact-text"><small>E-MAIL</small><strong>mathwithpedro@gmail.com</strong></span></a><a class="contact-method" href="tel:+14075802652"><span class="contact-text"><small>TELEFONE / SMS</small><strong>(407) 580-2652</strong></span></a></div></div></section>'''
x = x.replace('<section class="final-cta final-cta-v5"', pt_contact + '\n<section class="final-cta final-cta-v5"', 1)
p.write_text(x, encoding='utf-8')

# English: same clean, responsive contact layout.
p = root/'index.html'
x = p.read_text(encoding='utf-8')
x = re.sub(r'\s*<section class="section contact-section(?: contact-section-pt)?" id="contact">.*?</section>', '', x, flags=re.I|re.S)
en_contact = f'''<section class="section contact-section" id="contact"><div class="shell contact-card"><div class="contact-copy"><div class="kicker">CONTACT</div><h2>Questions before booking?</h2><p>Reach out directly. I’m happy to answer questions about SAT Math, the free first session, or whether the 4-week plan is a good fit.</p></div><div class="contact-actions"><a class="contact-method contact-whatsapp-card" href="{EN_WA}" target="_blank" rel="noopener"><span class="contact-icon">{WA_ICON}</span><span class="contact-text"><small>WHATSAPP</small><strong>Message Pedro</strong></span></a><a class="contact-method" href="mailto:mathwithpedro@gmail.com"><span class="contact-text"><small>EMAIL</small><strong>mathwithpedro@gmail.com</strong></span></a><a class="contact-method" href="tel:+14075802652"><span class="contact-text"><small>PHONE / TEXT</small><strong>(407) 580-2652</strong></span></a></div></div></section>'''
x = x.replace('<section class="final-cta final-cta-v5"', en_contact + '\n<section class="final-cta final-cta-v5"', 1)
p.write_text(x, encoding='utf-8')

# Visual cleanup for contact section and WhatsApp controls.
css = root/'static/site.css'
c = css.read_text(encoding='utf-8')
append = r'''

/* V20: prominent WhatsApp + balanced contact layout */
.sr-only{position:absolute!important;width:1px!important;height:1px!important;padding:0!important;margin:-1px!important;overflow:hidden!important;clip:rect(0,0,0,0)!important;white-space:nowrap!important;border:0!important}

/* WhatsApp image must never inherit a global responsive-image width. */
img.wa-icon,.wa-icon{
  display:block!important;
  width:22px!important;
  height:22px!important;
  min-width:22px!important;
  min-height:22px!important;
  max-width:22px!important;
  max-height:22px!important;
  object-fit:contain!important;
  flex:0 0 22px!important;
}

.wa-top-button{display:inline-flex!important;align-items:center!important;justify-content:center!important;gap:8px!important;background:#fff!important;color:#142d4e!important;text-decoration:none!important;font-weight:800!important;border:1px solid #dce4ef!important;border-radius:999px!important;padding:9px 13px!important;box-sizing:border-box!important}
.mobile-wa-button{display:flex!important;align-items:center!important;justify-content:center!important;gap:8px!important;background:#fff!important;color:#142d4e!important;border:1px solid #bfe7cf!important;border-radius:12px!important;padding:12px 14px!important;font-weight:800!important}

.contact-section{background:#f5f8fc!important}
.contact-card{
  display:grid!important;
  grid-template-columns:minmax(0,1fr)!important;
  gap:24px!important;
  align-items:start!important;
  background:#fff!important;
  border:1px solid rgba(20,45,78,.10)!important;
  border-radius:22px!important;
  padding:32px!important;
  box-shadow:0 18px 50px rgba(20,45,78,.08)!important;
  box-sizing:border-box!important;
}
.contact-copy{max-width:760px!important}
.contact-card h2{margin:.35rem 0 .75rem!important;font-size:clamp(1.8rem,3vw,2.6rem)!important;line-height:1.08!important}
.contact-card p{max-width:760px!important;margin:0!important;color:#526174!important}

.contact-actions{
  display:grid!important;
  grid-template-columns:repeat(3,minmax(0,1fr))!important;
  gap:12px!important;
  width:100%!important;
  align-items:stretch!important;
}
.contact-method{
  display:flex!important;
  flex-direction:row!important;
  align-items:center!important;
  justify-content:flex-start!important;
  gap:11px!important;
  min-width:0!important;
  min-height:78px!important;
  padding:14px 15px!important;
  border:1px solid #dce4ef!important;
  border-radius:14px!important;
  background:#fbfcfe!important;
  color:#142d4e!important;
  text-decoration:none!important;
  box-sizing:border-box!important;
  overflow:hidden!important;
}
.contact-text{display:flex!important;flex-direction:column!important;gap:2px!important;min-width:0!important}
.contact-method small{display:block!important;font-size:.70rem!important;line-height:1.1!important;letter-spacing:.08em!important;color:#758398!important;font-weight:800!important}
.contact-method strong{display:block!important;font-size:.94rem!important;line-height:1.25!important;overflow-wrap:anywhere!important;word-break:break-word!important}
.contact-icon{display:grid!important;place-items:center!important;width:28px!important;height:28px!important;min-width:28px!important;max-width:28px!important;flex:0 0 28px!important}
.contact-whatsapp-card{background:#f2fbf6!important;border-color:#bfe7cf!important;color:#176b3a!important}
.contact-whatsapp-card img.wa-icon{width:24px!important;height:24px!important;min-width:24px!important;min-height:24px!important;max-width:24px!important;max-height:24px!important}

.whatsapp-float{display:grid!important;place-items:center!important;width:52px!important;height:52px!important;min-width:52px!important;min-height:52px!important;padding:0!important;border-radius:50%!important;background:#fff!important;border:1px solid #bfe7cf!important;box-shadow:0 10px 28px rgba(0,0,0,.18)!important}
.whatsapp-float img.wa-icon{width:27px!important;height:27px!important;min-width:27px!important;min-height:27px!important;max-width:27px!important;max-height:27px!important}

@media(max-width:1080px){
  .wa-top-button span{display:none!important}
  .wa-top-button{width:42px!important;height:42px!important;padding:0!important}
}
@media(max-width:820px){
  .wa-top-button{display:none!important}
  .contact-card{padding:24px!important;border-radius:18px!important}
  .contact-actions{grid-template-columns:1fr!important;gap:10px!important}
  .contact-method{min-height:68px!important;padding:13px 14px!important}
}
@media(max-width:520px){
  .contact-section{padding-top:34px!important;padding-bottom:34px!important}
  .contact-card{padding:18px!important;gap:20px!important}
  .contact-card h2{font-size:1.75rem!important}
  .contact-card p{font-size:.97rem!important}
  .contact-method{min-height:64px!important}
  .contact-method strong{font-size:.92rem!important}
  .whatsapp-float{right:14px!important;bottom:84px!important;width:50px!important;height:50px!important;min-width:50px!important;min-height:50px!important}
}
'''
if 'V20: prominent WhatsApp' not in c:
    c += append
css.write_text(c, encoding='utf-8')


# Force browsers to fetch the current stylesheet after this layout fix.
V20_CACHE_BUSTER = "20261005-2204"
for rel in ("index.html", "pt/index.html"):
    page = root / rel
    html = page.read_text(encoding="utf-8")
    html = re.sub(
        r'href="([^"]*site\.css)(?:\?[^"]*)?"',
        lambda m: f'href="{m.group(1)}?v={V20_CACHE_BUSTER}"',
        html,
    )
    page.write_text(html, encoding="utf-8")
