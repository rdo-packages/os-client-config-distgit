%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x01527a34f0d0080f8a5db8d6eb6c5df21b4b6363
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
Version:        XXX
Release:        XXX
Summary:        OpenStack Client Configuration Library
License:        ASL 2.0
URL:            https://github.com/openstack/%{pypi_name}
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:      noarch
BuildRequires:  git-core

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif

%description
%{common_desc}


%package -n python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr
# Testing requirements
BuildRequires:  python3-fixtures
BuildRequires:  python3-stestr
BuildRequires:  python3-glanceclient >= 0.18.0
BuildRequires:  python3-openstacksdk
BuildRequires:  python3-oslotest >= 1.10.0
BuildRequires:  python3-jsonschema >= 2.6.0

Requires:       python3-openstacksdk >= 0.13.0


%description -n python3-%{pypi_name}
%{common_desc}


%if 0%{?with_doc}
%package  -n python-%{pypi_name}-doc
Summary:        Documentation for OpenStack os-client-config library

BuildRequires:  python3-sphinx
BuildRequires:  python3-openstackdocstheme
BuildRequires:  python3-reno

%description -n python-%{pypi_name}-doc
Documentation for the os-client-config library.
%endif

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{pypi_name}-%{upstream_version} -S git

# Let RPM handle the dependencies
rm -f test-requirements.txt requirements.txt

%build
%{py3_build}

%if 0%{?with_doc}
# generate html doc
sphinx-build-3 -b html doc/source/ doc/build/html
rm -rf doc/build/html/.{doctrees,buildinfo} doc/build/html/objects.inv
%endif

%install
%{py3_install}

%check
# NOTE(jpena): we are disabling Python2 unit tests when building the Python 3 package.
# The reason is that unit tests require glanceclient, and glanceclient is python3-only
# when building with Python 3. We could revert that, but it is a rabbit hole we do not
# want to enter
export OS_TEST_PATH='./os_client_config/tests'
export PATH=$PATH:$RPM_BUILD_ROOT/usr/bin
export PYTHONPATH=$PWD

#rm -rf .stestr
#PYTHON=python3 stestr-3 --test-path $OS_TEST_PATH run

%files -n python3-%{pypi_name}
%doc ChangeLog CONTRIBUTING.rst PKG-INFO README.rst
%license LICENSE
%{python3_sitelib}/os_client_config
%{python3_sitelib}/*.egg-info

%if 0%{?with_doc}
%files -n python-%{pypi_name}-doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
