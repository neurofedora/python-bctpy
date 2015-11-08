%global modname bctpy
%global commit a266f25a60bbb283d8ada13d5a6f68088019a930
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           python-%{modname}
Version:        0.4.1
Release:        0.1git%{shortcommit}%{?dist}
Summary:        Brain connectivity toolbox

License:        GPLv3+
URL:            https://github.com/aestrivex/bctpy
Source0:        https://github.com/aestrivex/bctpy/archive/%{commit}/%{modname}-%{shortcommit}.tar.gz

BuildArch:      noarch

%description
BCT is a matlab toolbox with many graph theoretical measures off of which bctpy
is based.  I did not write BCT (apart from small bugfixes I have submitted)
and a quality of life improvements that I have taken liberties to add.
With few exceptions, bctpy is a direct translation of matlab code to python.

bctpy should be considered beta software, with BCT being the gold standard by
comparison. I did my best to test all functionality in bctpy, but much of it is
arcane math that flies over the head of this humble programmer. There *are*
bugs lurking in bctpy, the question is not whether but how many. If you locate
bugs, please submit them to %{url}.

%package -n python2-%{modname}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{modname}}
BuildRequires:  python2-devel
BuildRequires:  python2-nose
Requires:       numpy scipy
# more efficient breadth first search
Recommends:     python-networkx

%description -n python2-%{modname}
%{summary}.

Python 2 version.

%package -n python3-%{modname}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{modname}}
BuildRequires:  python3-devel
BuildRequires:  python3-nose
Requires:       python3-numpy python3-scipy
# more efficient breadth first search
Recommends:     python3-networkx

%description -n python3-%{modname}
%{summary}.

Python 3 version.

%prep
%autosetup -n %{modname}-%{commit}

rm -rf %{py3dir}
mkdir -p %{py3dir}
cp -a . %{py3dir}
2to3 --nobackups --write %{py3dir}/{bct,test,setup.py}

%build
%py2_build
pushd %{py3dir}
  %py3_build
popd

%install
%py2_install
pushd %{py3dir}
  %py3_install
popd

%check
# very_long_tests.test_link_communities takes too much time (more than 15 mins) and doesnt work:
# https://github.com/aestrivex/bctpy/issues/29
nosetests-%{python2_version} -v --exclude="very_long_tests.test_link_communities"
pushd %{py3dir}
  # disable some of tests due to python3 not fully supported:
  # https://github.com/aestrivex/bctpy/issues/28
  nosetests-%{python3_version} -v --exclude="core_tests.test_threshold_proportional|very_long_tests.test_link_communities"
popd

%files -n python2-%{modname}
%license LICENSE
%doc README CHANGELOG
%{python2_sitelib}/%{modname}*

%files -n python3-%{modname}
%license LICENSE
%doc README CHANGELOG
%{python3_sitelib}/%{modname}*

%changelog
* Sun Nov 08 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.4.1-0.1gita266f25
- Initial package
