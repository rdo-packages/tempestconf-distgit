%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global pname tempestconf

%global with_doc 1

%global common_desc \
python-tempestconf will automatically generates the tempest \
configuration based on your cloud.

Name:           python-%{pname}
Version:        XXX
Release:        XXX
Summary:        OpenStack Tempest Config generator

License:        ASL 2.0
URL:            http://git.openstack.org/cgit/openstack/python-%{pname}
Source0:        https://tarballs.opendev.org/openinfra/%{name}/%{name}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.opendev.org/openinfra/%{name}/%{name}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:      noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
BuildRequires:  openstack-macros
%endif

BuildRequires:  python3-devel
BuildRequires:  python3-pbr >= 3.1.1
BuildRequires:  python3-setuptools
BuildRequires:  python3-tenacity
BuildRequires:  git-core

# test dependencies

BuildRequires:  python3-subunit
BuildRequires:  python3-oslotest
BuildRequires:  python3-stestr
BuildRequires:  python3-testscenarios
BuildRequires:  python3-testtools
BuildRequires:  python3-tempest
BuildRequires:  python3-openstacksdk >= 0.11.3

%description
%{common_desc}

%package -n     python3-%{pname}
Summary:        OpenStack Tempest Config generator
%{?python_provide:%python_provide python3-%{pname}}
Obsoletes: python2-%{pname} < %{version}-%{release}

Requires:       python3-pbr >= 3.1.1
Requires:       python3-tempest >= 1:18.0.0
Requires:       python3-requests
Requires:       python3-tenacity
Requires:       python3-openstacksdk >= 0.11.3
Requires:       python3-six
Requires:       python3-oslo-config >= 2:3.23.0

Requires:      python3-yaml >= 3.12

%description -n python3-%{pname}
%{common_desc}

%package -n python3-%{pname}-tests
Summary:    python3-tempestconf tests
Requires:   python3-%{pname} = %{version}-%{release}

Requires:   python3-subunit
Requires:   python3-oslotest
Requires:   python3-testrepository
Requires:   python3-testscenarios
Requires:   python3-testtools

%description -n python3-%{pname}-tests
%{common_desc}

It contains the test suite.

%if 0%{?with_doc}
%package -n python-%{pname}-doc
Summary:        python-tempestconf documentation

BuildRequires:  python3-sphinx
BuildRequires:  python3-openstackdocstheme
BuildRequires:  python3-sphinx-argparse >= 0.2.2
BuildRequires:  python3-sphinxcontrib-rsvgconverter
BuildRequires:  python3-reno

%description -n python-%{pname}-doc
%{common_desc}

Documentation for python-tempestconf
%endif

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n python-tempestconf-%{upstream_version} -S git

%build
%{py3_build}

%if 0%{?with_doc}
# generate html docs
export PYTHONPATH=.
sed -i '/^ *releasenotes\/index/d' doc/source/index.rst
sphinx-build -W -b html doc/source doc/build/html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{py3_install}

# The only file from this location is going to be removed soon
rm -rf %{buildroot}/usr/etc/tempest/*

%check
export OS_TEST_PATH='./config_tempest/tests'
export PATH=$PATH:$RPM_BUILD_ROOT/usr/bin
export PYTHONPATH=$PWD
export PYTHON=%{__python3}
stestr --test-path $OS_TEST_PATH run

%files -n python3-%{pname}
%license LICENSE
%doc README.rst
%{_bindir}/discover-tempest-config
%{python3_sitelib}/config_tempest
%exclude %{python3_sitelib}/config_tempest/tests
%{python3_sitelib}/python_tempestconf-*.egg-info

%files -n python3-%{pname}-tests
%license LICENSE
%{python3_sitelib}/config_tempest/tests

%if 0%{?with_doc}
%files -n python-%{pname}-doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
