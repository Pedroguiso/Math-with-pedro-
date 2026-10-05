python() {
  if [ "$1" = "-m" ] && [ "$2" = "zipfile" ] && [ "$3" = "-e" ]; then
    command python "$@"
    status=$?
    if [ $status -eq 0 ]; then
      root="site/math-with-pedro-deploy-v17"
      command python patch_v19.py
      command python patch_v20.py
      asset="$root/static/ucf-logo.png"
      if command -v curl >/dev/null 2>&1 && curl -L --fail --silent --show-error --retry 2 "https://www.ucf.edu/brand/wp-content/blogs.dir/13/files/2016/07/UCF-tab-NoBleed_vert-KG-7406.png" -o "$asset"; then
        sed -i 's#https://www.ucf.edu/brand/wp-content/blogs.dir/13/files/2016/07/UCF-tab-NoBleed_vert-KG-7406.png#/static/ucf-logo.png#g' "$root/index.html" "$root/pt/index.html"
      else
        sed -i 's/alt="UCF logo" loading="lazy"\/>/alt="UCF logo" referrerpolicy="no-referrer" loading="eager"\/>/g' "$root/index.html" 2>/dev/null || true
        sed -i 's/alt="Logo da UCF" loading="lazy"\/>/alt="Logo da UCF" referrerpolicy="no-referrer" loading="eager"\/>/g' "$root/pt/index.html" 2>/dev/null || true
      fi
    fi
    return $status
  fi
  command python "$@"
}
