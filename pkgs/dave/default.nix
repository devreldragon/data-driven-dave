{inputs, python3, newrelic, writeScriptBin,gnused}:
let
  env = python3.withPackages (ps: with ps; [newrelic pygame]);
in
writeScriptBin "dave" ''
  TMP_DIR="$(mktemp -d)"
  pushd "$TMP_DIR"
  trap "rm -fr $TMP_DIR" EXIT
  cp --no-preserve=mode -r ${inputs.self}/* .
  export NEW_RELIC_LICENSE_KEY="''${1:-$NEW_RELIC_LICENSE_KEY}"
  export NEW_RELIC_ACCOUNT="''${1:-$NEW_RELIC_ACCOUNT}"
  chmod +w newrelic.ini game_stats.json
  ${gnused}/bin/sed -i newrelic.ini "s#INSERT_YOUR_LICENSE_KEY_HERE#"$NEW_RELIC_LICENSE_KEY#"
  ${gnused}/bin/sed -i game_stats.json. "s#YOUR_ACCOUNT#"$NEW_RELIC_ACCOUNT#"
  ${env}/bin/python ${inputs.self}/main_fun.py
  popd
''
