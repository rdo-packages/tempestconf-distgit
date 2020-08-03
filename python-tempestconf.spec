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
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global pname tempestconf

%global with_doc 1

%global common_desc \
python-tempestconf will automatically generates the tempest \
configuration based on your cloud.

Name:           python-%{pname}
Version:        2.4.0
Release:        1%{?dist}
Summary:        OpenStack Tempest Config generator

License:        ASL 2.0
URL:            http://git.openstack.org/cgit/openstack/python-%{pname}
Source0:        http://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz

BuildArch:      noarch

BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-pbr >= 3.1.1
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  git

# test dependencies

BuildRequires:  python%{pyver}-subunit
BuildRequires:  python%{pyver}-oslotest
BuildRequires:  python%{pyver}-stestr
BuildRequires:  python%{pyver}-testscenarios
BuildRequires:  python%{pyver}-testtools
BuildRequires:  python%{pyver}-tempest
BuildRequires:  python%{pyver}-openstacksdk >= 0.11.3

%description
%{common_desc}

%package -n     python%{pyver}-%{pname}
Summary:        OpenStack Tempest Config generator
%{?python_provide:%python_provide python%{pyver}-%{pname}}
%if %{pyver} == 3
Obsoletes: python2-%{pname} < %{version}-%{release}
%endif

Requires:       python%{pyver}-pbr >= 3.1.1
Requires:       python%{pyver}-tempest >= 1:18.0.0
Requires:       python%{pyver}-setuptools
Requires:       python%{pyver}-requests
Requires:       python%{pyver}-openstacksdk >= 0.11.3
Requires:       python%{pyver}-castellan
Requires:       python%{pyver}-cryptography
Requires:       python%{pyver}-six
Requires:       python%{pyver}-oslo-config >= 2:3.23.0

# Handle python2 exception
%if %{pyver} == 2
Requires:      PyYAML
Requires:      python2-mock
%else
Requires:      python%{pyver}-PyYAML
%endif

%description -n python%{pyver}-%{pname}
%{common_desc}

%package -n python%{pyver}-%{pname}-tests
Summary:    python%{pyver}-tempestconf tests
Requires:   python%{pyver}-%{pname} = %{version}-%{release}

Requires:   python%{pyver}-subunit
Requires:   python%{pyver}-oslotest
Requires:   python%{pyver}-testrepository
Requires:   python%{pyver}-testscenarios
Requires:   python%{pyver}-testtools

%description -n python%{pyver}-%{pname}-tests
%{common_desc}

It contains the test suite.

%if 0%{?with_doc}
%package -n python-%{pname}-doc
Summary:        python-tempestconf documentation

BuildRequires:  python%{pyver}-sphinx
BuildRequires:  python%{pyver}-openstackdocstheme
BuildRequires:  python%{pyver}-sphinx-argparse >= 0.2.2

%description -n python-%{pname}-doc
%{common_desc}

Documentation for python-tempestconf
%endif

%prep
%autosetup -n python-tempestconf-%{upstream_version} -S git

%build
%{pyver_build}

%if 0%{?with_doc}
# generate html docs
export PYTHONPATH=.
sphinx-build-%{pyver} -W -b html doc/source doc/build/html
# remove the sphinx-build-%{pyver} leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{pyver_install}

# Create a versioned binary for backwards compatibility until everything is pure py3
ln -s discover-tempest-config %{buildroot}%{_bindir}/discover-tempest-config-%{pyver}

# The only file from this location is going to be removed soon
rm -rf %{buildroot}/usr/etc/tempest/*

%check
export OS_TEST_PATH='./config_tempest/tests'
export PATH=$PATH:$RPM_BUILD_ROOT/usr/bin
export PYTHONPATH=$PWD
export PYTHON=%{pyver_bin}
stestr-%{pyver} --test-path $OS_TEST_PATH run

%files -n python%{pyver}-%{pname}
%license LICENSE
%doc README.rst
%{_bindir}/discover-tempest-config
%{_bindir}/discover-tempest-config-%{pyver}
%{pyver_sitelib}/config_tempest
%exclude %{pyver_sitelib}/config_tempest/tests
%{pyver_sitelib}/python_tempestconf-*.egg-info

%files -n python%{pyver}-%{pname}-tests
%license LICENSE
%{pyver_sitelib}/config_tempest/tests

%if 0%{?with_doc}
%files -n python-%{pname}-doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
* Tue Dec 17 2019 RDO <dev@lists.rdoproject.org> 2.4.0-1
- Update to 2.4.0

* Thu Oct 03 2019 RDO <dev@lists.rdoproject.org> 2.3.0-1
- Update to 2.3.0

