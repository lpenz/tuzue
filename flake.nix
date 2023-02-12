{
  description =
    ''
    Fuzzy-filtering menu-based interactive curses interface for python,
    plus utilities
    '';
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-22.05";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages."${system}";
        tuzue = pkgs.python3Packages.buildPythonApplication {
          pname = "tuzue";
          version = "0.1.3";
          src = self;
        };
      in
      rec {
        packages.default = tuzue;
        apps.default = {
          tuzue-chdir = {
            type = "app";
            program = "${tuzue}/bin/tuzue-chdir";
          };
          tuzue-json = {
            type = "app";
            program = "${tuzue}/bin/tuzue-json";
          };
          tuzue-manmenu = {
            type = "app";
            program = "${tuzue}/bin/tuzue-manmenu";
          };
        };
      }
    );
}
