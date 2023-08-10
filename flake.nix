{
  inputs = {
    nixpkgs.url = "nixpkgs";
  };
  outputs = inputs: let
    proc = set:
    builtins.mapAttrs (
      system: pkgs:
      let
        callPackage = pkgs.lib.callPackageWith (pkgs // newpkgs // {inherit inputs;});
        newpkgs  = builtins.mapAttrs (name: func:
          if func == {} then pkgs.${name} else
          callPackage func {}) set;
      in newpkgs
    )
    {inherit (inputs.nixpkgs.legacyPackages) x86_64-linux x86_64-darwin aarch64-linux aarch64-darwin;};
  in {
    packages = proc rec {
      default = dave;
      dave = import ./pkgs/dave;
      newrelic = import ./pkgs/newrelic;
    };
  };
}
