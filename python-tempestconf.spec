%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global pname tempestconf

%global with_doc 1

%global common_desc \
python-tempestconf will automatically generates the tempest \
configuration based on your cloud.

Name:           python-%{pname}
Version:        3.2.0
Release:        1%{?dist}
Summary:        OpenStack Tempest Config generator

License:        ASL 2.0
URL:            http://git.openstack.org/cgit/openstack/python-%{pname}
Source0:        http://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-pbr >= 3.1.1
BuildRequires:  python3-setuptools
BuildRequires:  git
BuildRequires:  python3-tenacity

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

Requires:      python3-PyYAML

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
* Mon May 03 2021 RDO <dev@lists.rdoproject.org> 3.2.0-1
- Update to 3.2.0

* Thu May 07 2020 RDO <dev@lists.rdoproject.org> 2.5.0-1
- Update to 2.5.0

