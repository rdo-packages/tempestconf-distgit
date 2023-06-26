%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order
%global pname tempestconf

%global with_doc 1

%global common_desc \
python-tempestconf will automatically generates the tempest \
configuration based on your cloud.

Name:           python-%{pname}
Version:        XXX
Release:        XXX
Summary:        OpenStack Tempest Config generator

License:        Apache-2.0
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
BuildRequires:  pyproject-rpm-macros
BuildRequires:  git-core


%description
%{common_desc}

%package -n     python3-%{pname}
Summary:        OpenStack Tempest Config generator
Obsoletes: python2-%{pname} < %{version}-%{release}

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

BuildRequires:  python3-sphinxcontrib-rsvgconverter

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

sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs};do
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
# generate html docs
export PYTHONPATH=.
sed -i '/^ *releasenotes\/index/d' doc/source/index.rst
sphinx-build -W -b html doc/source doc/build/html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%pyproject_install

# The only file from this location is going to be removed soon
rm -rf %{buildroot}/usr/etc/tempest/*

%check
export OS_TEST_PATH='./config_tempest/tests'
%tox -e %{default_toxenv}

%files -n python3-%{pname}
%license LICENSE
%doc README.rst
%{_bindir}/discover-tempest-config
%{python3_sitelib}/config_tempest
%exclude %{python3_sitelib}/config_tempest/tests
%{python3_sitelib}/python_tempestconf-*.dist-info

%files -n python3-%{pname}-tests
%license LICENSE
%{python3_sitelib}/config_tempest/tests

%if 0%{?with_doc}
%files -n python-%{pname}-doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
