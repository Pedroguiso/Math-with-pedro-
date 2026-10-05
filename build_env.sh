python() {
  if [ "$1" = "-m" ] && [ "$2" = "zipfile" ] && [ "$3" = "-e" ]; then
    command python "$@"
    status=$?
    if [ $status -eq 0 ]; then
      sed -i 's/alt="UCF logo" loading="lazy"\/>/alt="UCF logo" referrerpolicy="no-referrer" loading="eager"\/>/g' site/math-with-pedro-deploy-v17/index.html 2>/dev/null || true
      sed -i 's/alt="Logo da UCF" loading="lazy"\/>/alt="Logo da UCF" referrerpolicy="no-referrer" loading="eager"\/>/g' site/math-with-pedro-deploy-v17/pt/index.html 2>/dev/null || true
    fi
    return $status
  fi
  command python "$@"
}
