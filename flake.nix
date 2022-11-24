{
  description =
    ''
    Fuzzy-filtering menu-based interactive curses interface for python,
    plus utilities
    '';
  inputs = {
    nixpkgs.url = github:NixOS/nixpkgs/nixos-22.05;
    flake-utils.url = github:numtide/flake-utils;
    mach-nix.url = "mach-nix/3.4.0";
  };
  outputs = { self, nixpkgs, flake-utils, mach-nix }:
    let
      system = "x86_64-linux";
      pkgs = pkgs.${system}.default;
      machNix = mach-nix.lib."${system}";
      tuzue = machNix.buildPythonApplication {
        pname = "tuzue";
        version = "0.1.2";
        src = self;
      };
    in rec {
      packages.${system}.default = tuzue;

      apps = {
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
    };
}
