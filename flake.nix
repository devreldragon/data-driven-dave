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
    {inherit (inputs.nixpkgs.legacyPackages) x86_64-linux;};
  in {
    packages = proc {
      dave = import ./pkgs/dave;
      newrelic = import ./pkgs/newrelic;
    };
  };
}
