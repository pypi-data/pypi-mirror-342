# treefmt.nix
{ ... }:
{
  projectRootFile = "treefmt.nix";
  settings.global.excludes = [
    "*.toml"
    "Jenkinsfile"
    "*.txt"
    ".gitattributes"
    "CLAUDE.md"
    ".parrot.md"
    "*.ambr"
    ".python-version"
  ];

  programs.deadnix.enable = true;
  programs.mdsh.enable = true;
  programs.nixfmt.enable = true;
  programs.shellcheck.enable = true;
  programs.shfmt.enable = true;
  programs.yamlfmt.enable = true;
  programs.just.enable = true;

  programs.ruff-format.enable = true;
  programs.ruff-check.enable = true;

}
