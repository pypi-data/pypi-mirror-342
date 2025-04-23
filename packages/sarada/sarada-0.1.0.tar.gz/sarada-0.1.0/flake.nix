{
  description = "Application packaged using poetry2nix";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs";

  inputs.treefmt-nix.url = "github:numtide/treefmt-nix";

  inputs.pyproject-nix.url = "github:pyproject-nix/pyproject.nix";
  inputs.pyproject-nix.inputs.nixpkgs.follows = "nixpkgs";
  inputs.uv2nix = {
    url = "github:pyproject-nix/uv2nix";
    inputs.pyproject-nix.follows = "pyproject-nix";
    inputs.nixpkgs.follows = "nixpkgs";
  };

  inputs.pyproject-build-systems = {
    url = "github:pyproject-nix/build-system-pkgs";
    inputs.pyproject-nix.follows = "pyproject-nix";
    inputs.uv2nix.follows = "uv2nix";
    inputs.nixpkgs.follows = "nixpkgs";
  };

  outputs =
    {
      self,
      nixpkgs,
      treefmt-nix,
      uv2nix,
      pyproject-nix,
      pyproject-build-systems,
    }:
    let
      # inherit (nixpkgs) lib;
      # pkgs = nixpkgs.legacyPackages.${system};
      supportedSystems = [ "x86_64-linux" ];
      pkgsFor =
        system:
        nixpkgs.legacyPackages.${system}.extend (
          # blank but overlays can go here
          nixpkgs.lib.composeManyExtensions ([ ])
        );
      eachSystem = f: nixpkgs.lib.genAttrs supportedSystems (system: f (pkgsFor system));

      treefmtEval = eachSystem (pkgs: treefmt-nix.lib.evalModule pkgs ./treefmt.nix);
      workspace = uv2nix.lib.workspace.loadWorkspace { workspaceRoot = ./.; };
      overlay = workspace.mkPyprojectOverlay { sourcePreference = "wheel"; };

      pythonSet = (
        pkgs:
        let
          python = pkgs.python312;
          pyprojectOverrides = final: prev: {
            jaconv = prev.jaconv.overrideAttrs (old: {

              nativeBuildInputs =
                old.nativeBuildInputs or [ ]
                ++ (final.resolveBuildSystem {
                  setuptools-scm = [ ];
                  setuptools = [ ];
                });
            });

            pyswisseph = prev.pyswisseph.overrideAttrs (old: {
              nativeBuildInputs =
                old.nativeBuildInputs or [ ] ++ (final.resolveBuildSystem { setuptools = [ ]; });
            });

            pymeeus = prev.pymeeus.overrideAttrs (old: {
              nativeBuildInputs =
                old.nativeBuildInputs or [ ] ++ (final.resolveBuildSystem { setuptools = [ ]; });
            });

            wget = prev.wget.overrideAttrs (old: {
              nativeBuildInputs =
                old.nativeBuildInputs or [ ] ++ (final.resolveBuildSystem { setuptools = [ ]; });
            });

            yurl = prev.yurl.overrideAttrs (old: {
              nativeBuildInputs =
                old.nativeBuildInputs or [ ] ++ (final.resolveBuildSystem { setuptools = [ ]; });
            });

          };

        in
        (pkgs.callPackage pyproject-nix.build.packages { inherit python; }).overrideScope (
          nixpkgs.lib.composeManyExtensions [
            pyproject-build-systems.overlays.default
            overlay
            pyprojectOverrides
          ]
        )
      );

    in
    {
      # formatter = forAllSystems (system: nixpkgs.legacyPackages.${system}.nixpkgs-fmt);
      formatter = eachSystem (pkgs: treefmtEval.${pkgs.system}.config.build.wrapper);

      # for `nix flake check`
      checks = eachSystem (pkgs: {
        formatting = treefmtEval.${pkgs.system}.config.build.check self;
      });

      packages = eachSystem (pkgs: {

        default = (pythonSet pkgs).mkVirtualEnv "sarada-env" workspace.deps.default;

      });
      devShells = eachSystem (
        pkgs:
        let

          inherit (pkgs) lib;
          thisPythonSet = pythonSet pkgs;
          editableOverlay = workspace.mkEditablePyprojectOverlay { root = "$REPO_ROOT"; };
          # Override previous set with our overrideable overlay.
          editablePythonSet = thisPythonSet.overrideScope (
            lib.composeManyExtensions [
              editableOverlay

              # Apply fixups for building an editable package of your workspace packages
              (final: prev: {
                # Change some stuff here for your new project!
                sarada = prev.sarada.overrideAttrs (old: {
                  # It's a good idea to filter the sources going into an editable build
                  # so the editable package doesn't have to be rebuilt on every change.
                  # I stole this from pyproject-nix but still don't know what this does
                  src = lib.fileset.toSource {
                    root = old.src;
                    fileset = lib.fileset.unions [
                      (old.src + "/pyproject.toml")
                      (old.src + "/README.md")
                      (old.src + "/src/sarada/__init__.py")
                    ];
                  };

                  # Hatchling (our build system) has a dependency on the `editables` package when building editables.
                  #
                  # In normal Python flows this dependency is dynamically handled, and doesn't need to be explicitly declared.
                  # This behaviour is documented in PEP-660.
                  #
                  # With Nix the dependency needs to be explicitly declared.
                  nativeBuildInputs =
                    old.nativeBuildInputs
                    ++ final.resolveBuildSystem {
                      editables = [ ];
                      setuptools = [ ];
                    };
                });

              })
            ]
          );
          virtualenv = editablePythonSet.mkVirtualEnv "sarada-dev-env" workspace.deps.all;

        in
        {
          default = pkgs.mkShell {
            # inputsFrom = [ self.packages.${system}.myappApp ];
            packages = [
              virtualenv
              pkgs.uv
              pkgs.pyright
              pkgs.just
              pkgs.nodejs
            ];
            env = {
              DO_NIX_CUSTOM = "1";
              # Force uv to use Python interpreter from venv
              UV_PYTHON = "${virtualenv}/bin/python";

              # Prevent uv from downloading managed Python's
              UV_PYTHON_DOWNLOADS = "never";
            };
            shellHook = ''
              # Undo dependency propagation by nixpkgs.
              unset PYTHONPATH

              # Get repository root using git. This is expanded at runtime by the editable `.pth` machinery.
              export REPO_ROOT=$(git rev-parse --show-toplevel)
            '';
          };
        }
      );
    };

}
