%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global pname tempestconf

%if 0%{?fedora} >= 24
# Since python3-tempest is not available.
# so disabling python3.
%global with_python3 0
%endif

Name:           python-%{pname}
Version:        1.0.0
Release:        1%{?dist}
Summary:        OpenStack Tempest Config generator

License:        ASL 2.0
URL:            https://github.com/redhat-openstack/python-%{pname}
Source0:        https://github.com/redhat-openstack/python-%{pname}/archive/%{upstream_version}.tar.gz

BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-pbr >= 1.8
BuildRequires:  python2-setuptools
BuildRequires:  git

# test dependencies

BuildRequires:  python-subunit
BuildRequires:  python-oslotest
BuildRequires:  python-testrepository
BuildRequires:  python-testscenarios
BuildRequires:  python-testtools
BuildRequires:  python-tempest

%description
python-tempestconf will automatically generates the tempest
configuration based on your cloud.

%package -n     python2-%{pname}
Summary:        OpenStack Tempest Config generator
%{?python_provide:%python_provide python2-%{pname}}

Requires:       python-pbr >= 1.8
Requires:       python-tempest >= 14.0.0
Requires:       python2-setuptools
Requires:       python-requests

%description -n python2-%{pname}
python-tempestconf will automatically generates the tempest
configuration based on your cloud.

%package -n python2-%{pname}-tests
Summary:    python-tempestconf tests
Requires:   python2-%{pname} = %{version}-%{release}

Requires:   python-subunit
Requires:   python-oslotest
Requires:   python-testrepository
Requires:   python-testscenarios
Requires:   python-testtools

%description -n python2-%{pname}-tests
python-tempestconf will automatically generates the tempest
configuration based on your cloud.

It contains the test suite.

%if 0%{?with_python3}
%package -n     python3-%{pname}
Summary:        OpenStack Tempest Config generator
%{?python_provide:%python_provide python3-%{pname}}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr >= 1.8
BuildRequires:  python3-setuptools

Requires:       python3-pbr >= 1.8
Requires:       python3-tempest >= 14.0.0
Requires:       python3-setuptools
Requires:       python3-requests

%description -n python3-%{pname}
python-tempestconf will automatically generates the tempest
configuration based on your cloud.

%package -n python3-%{pname}-tests
Summary:    python-tempestconf tests
Requires:   python3-%{pname} = %{version}-%{release}

BuildRequires:  python3-subunit
BuildRequires:  python3-oslotest
BuildRequires:  python3-testrepository
BuildRequires:  python3-testscenarios
BuildRequires:  python3-testtools
BuildRequires:  python3-tempest

Requires:   python3-subunit
Requires:   python3-oslotest
Requires:   python3-testrepository
Requires:   python3-testscenarios
Requires:   python3-testtools

%description -n python3-%{pname}-tests
python-tempestconf will automatically generates the tempest
configuration based on your cloud.

It contains the test suite.
%endif

%package -n python-%{pname}-doc
Summary:        python-tempestconf documentation

BuildRequires:  python-sphinx
BuildRequires:  python-oslo-sphinx

%description -n python-%{pname}-doc
python-tempestconf will automatically generates the tempest
configuration based on your cloud.

Documentation for python-tempestconf

%prep
%autosetup -n python-tempestconf-%{upstream_version} -S git

%build
%py2_build

%if 0%{?with_python3}
%py3_build
%endif

# generate html docs
%{__python2} setup.py build_sphinx
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

%install
%if 0%{?with_python3}
%py3_install
cp %{buildroot}/%{_bindir}/discover-tempest-config %{buildroot}/%{_bindir}/discover-tempest-config-3
ln -sf %{_bindir}/discover-tempest-config-3 %{buildroot}/%{_bindir}/discover-tempest-config-%{python3_version}
%endif

%py2_install
cp %{buildroot}/%{_bindir}/discover-tempest-config %{buildroot}/%{_bindir}/discover-tempest-config-2
ln -sf %{_bindir}/discover-tempest-config-2 %{buildroot}/%{_bindir}/discover-tempest-config-%{python2_version}

# move config files at proper place
mkdir -p %{buildroot}/etc/tempest
mv %{buildroot}/usr/etc/tempest/* %{buildroot}/etc/tempest

%check
%{__python2} setup.py testr

%if 0%{?with_python3}
rm -rf .testrepository
%{__python3} setup.py testr
%endif

%files -n python2-%{pname}
%license LICENSE
%doc README.rst
%{_bindir}/discover-tempest-config
%{_bindir}/discover-tempest-config-2
%{_bindir}/discover-tempest-config-%{python2_version}
%{python2_sitelib}/config_tempest
%exclude %{python2_sitelib}/config_tempest/tests
%{python2_sitelib}/python_tempestconf-*.egg-info
%config(noreplace) %{_sysconfdir}/tempest/*.conf

%files -n python2-%{pname}-tests
%license LICENSE
%{python2_sitelib}/config_tempest/tests

%if 0%{?with_python3}
%files -n python3-%{pname}
%license LICENSE
%doc README.rst
%{_bindir}/discover-tempest-config-3
%{_bindir}/discover-tempest-config-%{python3_version}
%{python3_sitelib}/config_tempest
%exclude %{python3_sitelib}/config_tempest/tests
%{python3_sitelib}/python_tempestconf-*.egg-info
%config(noreplace) %{_sysconfdir}/tempest/*.conf

%files -n python3-%{pname}-tests
%license LICENSE
%{python3_sitelib}/config_tempest/tests
%endif

%files -n python-%{pname}-doc
%license LICENSE
%doc doc/build/html

%changelog
* Fri Feb 10 2017 Alfredo Moralejo <amoralej@redhat.com> 1.0.0-1
- Update to 1.0.0

# REMOVEME: error caused by commit https://github.com/redhat-openstack/python-tempestconf.git/commit/6220c362903469c4847eae3377d93b26939e7cab
