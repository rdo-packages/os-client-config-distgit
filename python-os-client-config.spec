# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %{expand:%{python%{pyver}_sitelib}}
%global pyver_install %{expand:%{py%{pyver}_install}}
%global pyver_build %{expand:%{py%{pyver}_build}}
# End of macros for py2/py3 compatibility

%{!?_licensedir:%global license %%doc}
%global pypi_name os-client-config
%global with_doc 1

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
Version:        1.33.0
Release:        2%{?dist}
Summary:        OpenStack Client Configuration Library
License:        ASL 2.0
URL:            https://github.com/openstack/%{pypi_name}
Source0:        https://pypi.io/packages/source/o/%{pypi_name}/%{pypi_name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  git

%description
%{common_desc}


%package -n python%{pyver}-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python%{pyver}-%{pypi_name}}

BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  python%{pyver}-pbr
# Testing requirements
BuildRequires:  python%{pyver}-fixtures
BuildRequires:  python%{pyver}-stestr
BuildRequires:  python%{pyver}-glanceclient >= 0.18.0
BuildRequires:  python%{pyver}-openstacksdk
BuildRequires:  python%{pyver}-oslotest >= 1.10.0
BuildRequires:  python%{pyver}-jsonschema >= 2.6.0

Requires:       python%{pyver}-openstacksdk >= 0.13.0


%description -n python%{pyver}-%{pypi_name}
%{common_desc}


%if 0%{?with_doc}
%package  -n python-%{pypi_name}-doc
Summary:        Documentation for OpenStack os-client-config library

BuildRequires:  python%{pyver}-sphinx
BuildRequires:  python%{pyver}-openstackdocstheme
BuildRequires:  python%{pyver}-reno

%description -n python-%{pypi_name}-doc
Documentation for the os-client-config library.
%endif

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git

# Let RPM handle the dependencies
rm -f test-requirements.txt requirements.txt

%build
%{pyver_build}

%if 0%{?with_doc}
# generate html doc
sphinx-build-%{pyver} -b html doc/source/ doc/build/html
rm -rf doc/build/html/.{doctrees,buildinfo} doc/build/html/objects.inv
%endif

%install
%{pyver_install}

%check
# NOTE(jpena): we are disabling Python2 unit tests when building the Python 3 package.
# The reason is that unit tests require glanceclient, and glanceclient is python3-only
# when building with Python 3. We could revert that, but it is a rabbit hole we do not
# want to enter
export OS_TEST_PATH='./os_client_config/tests'
export PATH=$PATH:$RPM_BUILD_ROOT/usr/bin
export PYTHONPATH=$PWD

#rm -rf .stestr
#PYTHON=python%{pyver} stestr-%{pyver} --test-path $OS_TEST_PATH run

%files -n python%{pyver}-%{pypi_name}
%doc ChangeLog CONTRIBUTING.rst PKG-INFO README.rst
%license LICENSE
%{pyver_sitelib}/os_client_config
%{pyver_sitelib}/*.egg-info

%if 0%{?with_doc}
%files -n python-%{pypi_name}-doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
* Wed Oct 02 2019 Joel Capitao <jcapitao@redhat.com> 1.33.0-2
- Removed python2 subpackages in no el7 distros

* Thu Sep 19 2019 RDO <dev@lists.rdoproject.org> 1.33.0-1
- Update to 1.33.0

