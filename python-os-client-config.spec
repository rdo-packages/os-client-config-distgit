%{!?_licensedir:%global license %%doc}
%global pypi_name os-client-config

%if 0%{?fedora} >= 24
%global with_python3 1
%endif

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global common_desc \
The os-client-config is a library for collecting client configuration for \
using an OpenStack cloud in a consistent and comprehensive manner. It \
will find cloud config for as few as 1 cloud and as many as you want to \
put in a config file. It will read environment variables and config files, \
and it also contains some vendor specific default values so that you don't \
have to know extra info to use OpenStack \
 \
* If you have a config file, you will get the clouds listed in it \
* If you have environment variables, you will get a cloud named `envvars` \
* If you have neither, you will get a cloud named `defaults` with base defaults

Name:           python-%{pypi_name}
Version:        XXX
Release:        XXX
Summary:        OpenStack Client Configuration Library
License:        ASL 2.0
URL:            https://github.com/openstack/%{pypi_name}
Source0:        https://pypi.io/packages/source/o/%{pypi_name}/%{pypi_name}-%{version}.tar.gz

BuildArch:      noarch

%description
%{common_desc}

%package -n python2-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{pypi_name}}
Obsoletes: python-%{pypi_name} < 1.7.3
# compat for previous Delorean Trunk package
Provides:       os-client-config

BuildRequires:  git
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-pbr

# Testing requirements
BuildRequires:  python-fixtures
BuildRequires:  python-glanceclient >= 0.18.0
BuildRequires:  python-jsonschema >= 2.0.0
BuildRequires:  python-keystoneclient >= 1.1.0
BuildRequires:  python-oslotest >= 1.10.0

# Requirements
BuildRequires:  python-appdirs >= 1.3.0
BuildRequires:  python-keystoneauth1 >= 3.1.0
BuildRequires:  python-requestsexceptions >= 1.2.0
BuildRequires:  PyYAML >= 3.10

Requires:       python-appdirs >= 1.3.0
Requires:       python-keystoneauth1 >= 3.1.0
Requires:       python-requestsexceptions >= 1.2.0
Requires:       PyYAML >= 3.10

%description -n python2-%{pypi_name}
%{common_desc}

%package  -n python2-%{pypi_name}-doc
Summary:        Documentation for OpenStack os-client-config library
%{?python_provide:%python_provide python2-%{pypi_name}-doc}

BuildRequires:  python-sphinx
BuildRequires:  python-openstackdocstheme
BuildRequires:  python-reno

%description -n python2-%{pypi_name}-doc
Documentation for the os-client-config library.


%if 0%{?with_python3}
%package -n python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr

# Testing requirements
BuildRequires:  python3-fixtures
BuildRequires:  python3-jsonschema >= 2.0.0
BuildRequires:  python3-keystoneclient >= 2.1.0
BuildRequires:  python3-oslotest >= 1.10.0

# Requirements
BuildRequires:  python3-appdirs >= 1.3.0
BuildRequires:  python3-keystoneauth1 >= 3.1.0
BuildRequires:  python3-requestsexceptions >= 1.2.0
BuildRequires:  python3-PyYAML >= 3.10

Requires:       python3-appdirs >= 1.3.0
Requires:       python3-keystoneauth1 >= 3.1.0
Requires:       python3-requestsexceptions >= 1.2.0
Requires:       python3-PyYAML >= 3.10

%description -n python3-%{pypi_name}
%{common_desc}

%package -n    python3-%{pypi_name}-doc
Summary:       Documentation for OpenStack os-client-config library
%{?python_provide:%python_provide python3-%{pypi_name}-doc}
Obsoletes: python-%{pypi_name}-doc < 1.7.3

BuildRequires: python3-sphinx
BuildRequires: python3-oslo-sphinx
BuildRequires: openstack-macros

%description -n python3-%{pypi_name}-doc
Documentation for the os-client-config library.
%endif

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git

# Let RPM handle the dependencies
%py_req_cleanup

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

%install
%py2_install

# generate html doc
%{__python2} setup.py build_sphinx -b html
rm -rf doc/build/html/.{doctrees,buildinfo} doc/build/html/objects.inv

%if 0%{?with_python3}
%py3_install
%endif

%check
%{__python2} setup.py testr
# cleanup testrepository
rm -rf .testrepository
%if 0%{?with_python3}
%{__python3} setup.py testr
%endif

%files -n python2-%{pypi_name}
%doc ChangeLog CONTRIBUTING.rst PKG-INFO README.rst
%license LICENSE
%{python2_sitelib}/os_client_config
%{python2_sitelib}/*.egg-info

%files -n python2-%{pypi_name}-doc
%license LICENSE
%doc doc/build/html

%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%doc ChangeLog CONTRIBUTING.rst PKG-INFO README.rst
%license LICENSE
%{python3_sitelib}/os_client_config
%{python3_sitelib}/*.egg-info

%files -n python3-%{pypi_name}-doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
