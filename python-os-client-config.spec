%global sname os-client-config

%if 0%{?fedora}
%global with_python3 1
%endif

Name:           python-%{sname}
Version:        1.2.0
Release:        2%{?dist}
Summary:        OpenStack Client Configuation Library
License:        ASL 2.0
URL:            https://github.com/openstack/%{sname}
Source0:        https://pypi.python.org/packages/source/o/%{sname}/%{sname}-%{version}.tar.gz

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-pbr
BuildRequires:  python-fixtures

BuildArch:      noarch

Requires:       python-setuptools
Requires:       python-fixtures
Requires:       python-appdirs

%description
The os-client-config is a library for collecting client configuration for
using an OpenStack cloud in a consistent and comprehensive manner. It
will find cloud config for as few as 1 cloud and as many as you want to
put in a config file. It will read environment variables and config files,
and it also contains some vendor specific default values so that you don't
have to know extra info to use OpenStack

* If you have a config file, you will get the clouds listed in it
* If you have environment variables, you will get a cloud named `envvars`
* If you have neither, you will get a cloud named `defaults` with base defaults

%package doc
Summary:    Documentation for OpenStack os-client-config library
BuildRequires: python-sphinx
BuildRequires: python-oslo-sphinx

%description doc
Documentation for the os-client-config library.

%if 0%{?with_python3}
%package -n python3-%{sname}
Summary:        OpenStack Client Configuation Library
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr
BuildArch:      noarch

Requires:       python3-setuptools
Requires:       python3-fixtures
Requires:       python3-appdirs

%description -n python3-%{sname}
The os-client-config is a library for collecting client configuration for
using an OpenStack cloud in a consistent and comprehensive manner. It
will find cloud config for as few as 1 cloud and as many as you want to
put in a config file. It will read environment variables and config files,
and it also contains some vendor specific default values so that you don't
have to know extra info to use OpenStack

* If you have a config file, you will get the clouds listed in it
* If you have environment variables, you will get a cloud named `envvars`
* If you have neither, you will get a cloud named `defaults` with base defaults

%package -n    python3-%{sname}-doc
Summary:       Documentation for OpenStack os-client-config library
BuildRequires: python3-sphinx
BuildRequires: python3-oslo-sphinx 

%description -n python3-%{sname}-doc
Documentation for the os-client-config library.
%endif

%prep
%setup -qc
mv %{sname}-%{version} python2

pushd python2
rm -rf *.egg-info

# Let RPM handle the dependencies
rm -f test-requirements.txt requirements.txt

cp -p LICENSE ChangeLog CONTRIBUTING.rst PKG-INFO README.rst ../
popd

%if 0%{?with_python3}
cp -a python2 python3
%endif

%build
pushd python2
%py2_build
popd
%if 0%{?with_python3}
pushd python3
%py3_build
popd
%endif

%install
pushd python2
%py2_install
export PYTHONPATH="$( pwd ):$PYTHONPATH"
pushd doc
sphinx-build -b html -d build/doctrees   source build/html
# Fix hidden-file-or-dir warnings
rm -fr build/html/.buildinfo

# Fix this rpmlint warning
sed -i "s|\r||g" build/html/_static/jquery.js
popd
popd

%if 0%{?with_python3}
pushd python3
%py3_install
export PYTHONPATH="$( pwd ):$PYTHONPATH"
pushd doc
sphinx-build-3 -b html -d build/doctrees   source build/html

# Fix hidden-file-or-dir warnings
rm -fr build/html/.buildinfo

# Fix this rpmlint warning
sed -i "s|\r||g" build/html/_static/jquery.js
popd
popd
%endif

%check
pushd python2
%{__python2} setup.py test
popd

%if 0%{?with_python3}
pushd python3
%{__python3} setup.py test
popd
%endif

%files
%doc ChangeLog CONTRIBUTING.rst PKG-INFO README.rst
%license LICENSE
%{python2_sitelib}/os_client_config
%{python2_sitelib}/*.egg-info

%files doc
%doc python2/doc/build/html

%if 0%{?with_python3}
%files -n python3-%{sname}
%doc ChangeLog CONTRIBUTING.rst PKG-INFO README.rst
%license LICENSE
%{python3_sitelib}/os_client_config
%{python3_sitelib}/*.egg-info

%files -n python3-%{sname}-doc
%doc python3/doc/build/html
%endif

%changelog
* Sat Aug 01 2015 Parag Nemade <pnemade AT redhat DOT com> - 1.2.0-2
- enable python3 version
- Add missing Requires: python3-appdirs
- enable tests

* Mon Jul 27 2015 Parag Nemade <pnemade AT redhat DOT com> - 1.2.0-1
- Initial packaging
