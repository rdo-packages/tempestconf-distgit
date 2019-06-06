%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global pname tempestconf

%if 0%{?fedora} >= 24
# Since python3-tempest is not available.
# so disabling python3.
%global with_python3 0
%endif

%global common_desc \
python-tempestconf will automatically generates the tempest \
configuration based on your cloud.

Name:           python-%{pname}
Version:        2.2.0
Release:        4%{?dist}
Summary:        OpenStack Tempest Config generator

License:        ASL 2.0
URL:            http://git.openstack.org/cgit/openstack/python-%{pname}
Source0:        https://github.com/openstack/python-%{pname}/archive/%{upstream_version}.tar.gz

Patch0001:      0001-Fix-checking-of-roles.patch
Patch0002:      0001-Clear-the-difference-between-service-type-and-name.patch
Patch0003:      0002-Fix-checking-for-volume-backup.patch
Patch0004:      0001-Remove-heat_stack_owner-role-assigning-to-user.patch
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python2-pbr >= 1.8
BuildRequires:  python2-setuptools
BuildRequires:  git

# test dependencies

BuildRequires:  python2-subunit
BuildRequires:  python2-oslotest
BuildRequires:  python2-stestr
BuildRequires:  python2-testscenarios
BuildRequires:  python2-testtools
BuildRequires:  python2-tempest
BuildRequires:  python2-os-client-config

%description
%{common_desc}

%package -n     python2-%{pname}
Summary:        OpenStack Tempest Config generator
%{?python_provide:%python_provide python2-%{pname}}

Requires:       python2-pbr >= 1.8
Requires:       python2-tempest >= 14.0.0
Requires:       python2-setuptools
Requires:       python2-requests
Requires:       python2-os-client-config
Requires:       python2-castellan
Requires:       python2-cryptography
%if 0%{?fedora} > 0
Requires:      python2-pyyaml
%else
Requires:      PyYAML
%endif

%description -n python2-%{pname}
%{common_desc}

%package -n python2-%{pname}-tests
Summary:    python-tempestconf tests
Requires:   python2-%{pname} = %{version}-%{release}

Requires:   python2-subunit
Requires:   python2-oslotest
Requires:   python2-testrepository
Requires:   python2-testscenarios
Requires:   python2-testtools

%description -n python2-%{pname}-tests
%{common_desc}

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
Requires:       python3-os-client-config
Requires:       python-castellan
Requires:       python3-cryptography
Requires:       python3-PyYAML

%description -n python3-%{pname}
%{common_desc}

%package -n python3-%{pname}-tests
Summary:    python-tempestconf tests
Requires:   python3-%{pname} = %{version}-%{release}

BuildRequires:  python3-subunit
BuildRequires:  python3-oslotest
BuildRequires:  python3-stestr
BuildRequires:  python3-testscenarios
BuildRequires:  python3-testtools
BuildRequires:  python3-tempest
BuildRequires:  python3-os-client-config

Requires:   python3-subunit
Requires:   python3-oslotest
Requires:   python3-testrepository
Requires:   python3-testscenarios
Requires:   python3-testtools

%description -n python3-%{pname}-tests
%{common_desc}

It contains the test suite.
%endif

%package -n python-%{pname}-doc
Summary:        python-tempestconf documentation

BuildRequires:  python2-sphinx
# FIXME(chkumar246): Keeping oslo-sphinx dependency in order
# to make cbs build passing
BuildRequires:  python2-oslo-sphinx
BuildRequires:  python2-openstackdocstheme
BuildRequires:  python2-sphinx-argparse >= 0.2.2

%description -n python-%{pname}-doc
%{common_desc}

Documentation for python-tempestconf

%prep
%autosetup -n python-tempestconf-%{upstream_version} -S git

%build
%py2_build

%if 0%{?with_python3}
%py3_build
%endif

# generate html docs
export PYTHONPATH=.
sphinx-build -W -b html doc/source doc/build/html
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

# The only file from this location is going to be removed soon
rm -rf %{buildroot}/usr/etc/tempest/*

%check
export OS_TEST_PATH='./config_tempest/tests'
export PATH=$PATH:$RPM_BUILD_ROOT/usr/bin
export PYTHONPATH=$PWD
stestr --test-path $OS_TEST_PATH run
%if 0%{?with_python3}
rm -rf .stestr
stestr-3 --test-path $OS_TEST_PATH run
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

%files -n python3-%{pname}-tests
%license LICENSE
%{python3_sitelib}/config_tempest/tests
%endif

%files -n python-%{pname}-doc
%license LICENSE
%doc doc/build/html

%changelog
* Thu Jun 06 2019 Chandan Kumar <chkumar@redhat.com> 2.2.0-4
- Added patch for removing heat_stack_owner role
- https://review.opendev.org/660913

* Wed Jun 05 2019 Chandan Kumar <chkumar@redhat.com> 2.2.0-3
- Added patch for fixing volume backup service
- https://review.opendev.org/#/c/663061/
- https://review.opendev.org/#/c/662835/

* Thu May 23 2019 Chandan Kumar <chkumar@redhat.com> 2.2.0-2
- Added patch for fixing the member role

* Tue May 07 2019 RDO <dev@lists.rdoproject.org> 2.2.0-1
- Update to 2.2.0

* Wed Aug 22 2018 RDO <dev@lists.rdoproject.org> 2.0.0-1
- Update to 2.0.0

* Wed Aug 22 2018 Chandan Kumar <chkumar@redhat.com> 1.1.4-2
- Fixed the doc dependencies for tempestconf-2.0.0
- Removes default-overrides.conf as it is not needed

* Mon Feb 19 2018 Chandan Kumar <chkumar@redhat.com> 1.1.4-1
- Update to 1.1.4
