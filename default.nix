#let
#  pkgs = import <nixpkgs> {};
#in pkgs.mkShell {
#  buildInputs = [
#    pkgs.gcc
#    pkgs.glibc
#    pkgs.python3
#    pkgs.python3.pkgs.pytest
#  ];
#  shellHook = ''
#    # Tells pip to put packages into $PIP_PREFIX instead of the usual locations.
#    # See https://pip.pypa.io/en/stable/user_guide/#environment-variables.
#    export PIP_PREFIX=$(pwd)/_build/pip_packages
#    export PYTHONPATH="$PIP_PREFIX/${pkgs.python3.sitePackages}:$PYTHONPATH"
#    export PATH="$PIP_PREFIX/bin:$PATH"
#    unset SOURCE_DATE_EPOCH
#  '';
#}

{ pkgs ? import <nixpkgs> { } }:
(pkgs.buildFHSEnv {
    name = "FHS";
    targetPkgs = pkgs: (with pkgs; [
      gcc
      glibc
      python3.pkgs.pytest
    ]);
    runScript = "fish";
}).env