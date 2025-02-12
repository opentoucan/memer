{ pkgs ? import <nixpkgs> { } }:
(pkgs.buildFHSEnv {
    name = "FHS";
    targetPkgs = pkgs: (with pkgs; [
      gcc
      glibc
      zlib
      go-task
      pre-commit
    ]);
    runScript = "fish";
    shellHook = ''
        direnv allow
    '';
}).env
