echo "[build_env] loaded"

python() {
  if [ "${MWP_PYTHON_WRAPPER_ACTIVE:-0}" = "1" ]; then
    command python "$@"
    return $?
  fi

  if [ "$1" = "-m" ] && [ "$2" = "zipfile" ] && [ "$3" = "-e" ]; then
    echo "[build_env] intercepting ZIP extraction"
    export MWP_PYTHON_WRAPPER_ACTIVE=1
    command python "$@"
    status=$?
    unset MWP_PYTHON_WRAPPER_ACTIVE
    if [ $status -ne 0 ]; then
      return $status
    fi

    root="site/math-with-pedro-deploy-v17"
    echo "[build_env] applying V19/V20 site patches"
    command python patch_v19.py || return $?
    command python patch_v20.py || return $?

    echo "[build_env] validating patched contact section"
    command python - <<'PY'
from pathlib import Path

root = Path("site/math-with-pedro-deploy-v17")
pt = (root / "pt/index.html").read_text(encoding="utf-8")
en = (root / "index.html").read_text(encoding="utf-8")
css = (root / "static/site.css").read_text(encoding="utf-8")

checks = {
    "pt_contact_sections": pt.count('class="section contact-section contact-section-pt" id="contact"'),
    "en_contact_sections": en.count('class="section contact-section" id="contact"'),
    "pt_whatsapp_cards": pt.count('class="contact-method contact-whatsapp-card"'),
    "en_whatsapp_cards": en.count('class="contact-method contact-whatsapp-card"'),
    "wa_png_refs_pt": pt.count("/static/whatsapp-green.png"),
    "pt_whatsapp_floats": pt.count('class="whatsapp-float"'),
    "v20_css_markers": css.count("V20: prominent WhatsApp + balanced contact layout"),
}
print("[build_env] validation:", checks)

assert checks["pt_contact_sections"] == 1, checks
assert checks["en_contact_sections"] == 1, checks
assert checks["pt_whatsapp_cards"] >= 1, checks
assert checks["en_whatsapp_cards"] >= 1, checks
assert checks["wa_png_refs_pt"] == 4, checks
assert checks["pt_whatsapp_floats"] == 1, checks
assert checks["v20_css_markers"] == 1, checks
PY
    validation_status=$?
    if [ $validation_status -ne 0 ]; then
      echo "[build_env] validation FAILED"
      return $validation_status
    fi
    echo "[build_env] validation PASSED"

    asset="$root/static/ucf-logo.png"
    if command -v curl >/dev/null 2>&1 && curl -L --fail --silent --show-error --retry 2 "https://www.ucf.edu/brand/wp-content/blogs.dir/13/files/2016/07/UCF-tab-NoBleed_vert-KG-7406.png" -o "$asset"; then
      sed -i 's#https://www.ucf.edu/brand/wp-content/blogs.dir/13/files/2016/07/UCF-tab-NoBleed_vert-KG-7406.png#/static/ucf-logo.png#g' "$root/index.html" "$root/pt/index.html"
    else
      sed -i 's/alt="UCF logo" loading="lazy"\/>/alt="UCF logo" referrerpolicy="no-referrer" loading="eager"\/>/g' "$root/index.html" 2>/dev/null || true
      sed -i 's/alt="Logo da UCF" loading="lazy"\/>/alt="Logo da UCF" referrerpolicy="no-referrer" loading="eager"\/>/g' "$root/pt/index.html" 2>/dev/null || true
    fi
    return 0
  fi
  command python "$@"
}
