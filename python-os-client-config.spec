%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0xbba3b1e67a7303dd1769d34595bf2e4d09004514
%{!?_licensedir:%global license %%doc}
%global pypi_name os-client-config
%global with_doc 1

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order
# Exclude sphinx from BRs if docs are disabled
%if ! 0%{?with_doc}
%global excluded_brs %{excluded_brs} sphinx openstackdocstheme
%endif

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
Version:        2.1.0
Release:        3%{?dist}
Summary:        OpenStack Client Configuration Library
License:        Apache-2.0
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

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros

%description -n python3-%{pypi_name}
%{common_desc}


%if 0%{?with_doc}
%package  -n python-%{pypi_name}-doc
Summary:        Documentation for OpenStack os-client-config library

%description -n python-%{pypi_name}-doc
Documentation for the os-client-config library.
%endif

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{pypi_name}-%{upstream_version} -S git


sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs}; do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

# Automatic BR generation
%generate_buildrequires
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires -t -e %{default_toxenv}
%endif

%build
%pyproject_wheel

%if 0%{?with_doc}
# generate html doc
%tox -e docs
rm -rf doc/build/html/.{doctrees,buildinfo} doc/build/html/objects.inv
%endif

%install
%pyproject_install

%check
%tox -e %{default_toxenv}

%files -n python3-%{pypi_name}
%doc ChangeLog CONTRIBUTING.rst PKG-INFO README.rst
%license LICENSE
%{python3_sitelib}/os_client_config
%{python3_sitelib}/*.dist-info

%if 0%{?with_doc}
%files -n python-%{pypi_name}-doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
* Fri Mar 15 2024 RDO <dev@lists.rdoproject.org> 2.1.0-3
- Rebuild 2.1.0 in Caracal


