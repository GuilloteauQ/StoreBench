{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/23.05";
  };

  outputs = { self, nixpkgs}:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
    in
    {
      apps.${system} = rec{
        default = storebench;
        storebench = {
          type = "app";
          program = "${self.packages.${system}.default}/bin/storebench";
        };
      };
      packages.${system} = rec {
        default = storebench;
        storebench = pkgs.python3Packages.buildPythonPackage {
          name = "storebench";
          version = "0.0.1";
          src = ./.;
          propagatedBuildInputs = with (pkgs.python3Packages); [
            pkgs.gcc
          ];
          doCheck = false;
        };      
      };
      devShells.${system}.default = with pkgs;
        mkShell {
          packages = [ python3 ];
        };
    };
}
