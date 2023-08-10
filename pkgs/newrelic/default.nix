{python3Packages, fetchPypi}:
python3Packages.buildPythonPackage rec {
  pname = "newrelic";
  version = "8.9.0";
  src = fetchPypi {
    inherit pname version;
    hash = "sha256-qOjN/VrF+OWKoRkJkh5ltNqK+3Id6ZbNTs1cNy4znDw=";
  };
  propagatedBuildInputs = with python3Packages; [
  ];
  postPatch = ''
  substituteInPlace setup.py \
    --replace 'setup_requires=["setuptools_scm>=3.2,<7"],' "setup_requires=[],"
'';
  doCheck = false;

}
