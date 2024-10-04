{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
  nativeBuildInputs = with pkgs; [ 
    pkgs.python312
    pkgs.python312Packages.requests
    pkgs.python312Packages.beautifulsoup4
  ];
}