#
# Conditional build:
%bcond_without	apidocs		# API documentation
#
Summary:	Transducers for C++
Summary(pl.UTF-8):	Przetworniki dla C++
Name:		zug
Version:	0.1.1
Release:	1
License:	Boost v1.0
Group:		Libraries
#Source0Download: https://github.com/arximboldi/zug/tags
Source0:	https://github.com/arximboldi/zug/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	42d556f4ed260bb7c9361dfbe4030442
%define	theme_gitref	b5adfa2a6def8aa55d95dedc4e1bfde214a5e36c
Source1:	https://github.com/arximboldi/sinusoidal-sphinx-theme/archive/%{theme_gitref}/sinusoidal-sphinx-theme-%{theme_gitref}.tar.gz
# Source1-md5:	8873555af1d9f75d42a440fb1c60bd07
URL:		https://github.com/arximboldi/immer
BuildRequires:	cmake >= 3.8
BuildRequires:	libstdc++-devel >= 6:5
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.605
%{?with_apidocs:BuildRequires:	sphinx-pdg-3 >= 1.3}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# header-only library, but cmake files location is arch-dependent
%define		_enable_debug_packages	0

%description
Zug is a C++ library providing transducers. Transducers are composable
sequential transformations independent of the source. They are
extremely lightweight, and can be used to express algorithms over
pull-based sequences (iterators, files) but also push based sequences
(signals, events, asynchronous streams) in a generic way.

%description -l pl.UTF-8
Zug to biblioteka C++ zapewniająca przetworniki. Są to dające się
składać przekształcenia sekwencyjne niezależne od źródła. Są bardzo
lekkie i mogą być używane do generycznego wyrażania algorytmów na
sekwencjach pobieranych (iteratorach, plikach), ale także sekwencjach
dostarczanych (sygnałach, zdarzeniach, strumieniach asynchronicznych).

%package devel
Summary:	Transducers for C++
Summary(pl.UTF-8):	Przetworniki dla C++
Group:		Development/Libraries
Requires:	libstdc++-devel >= 6:5

%description devel
Zug is a C++ library providing transducers. Transducers are composable
sequential transformations independent of the source. They are
extremely lightweight, and can be used to express algorithms over
pull-based sequences (iterators, files) but also push based sequences
(signals, events, asynchronous streams) in a generic way.

%description devel -l pl.UTF-8
Zug to biblioteka C++ zapewniająca przetworniki. Są to dające się
składać przekształcenia sekwencyjne niezależne od źródła. Są bardzo
lekkie i mogą być używane do generycznego wyrażania algorytmów na
sekwencjach pobieranych (iteratorach, plikach), ale także sekwencjach
dostarczanych (sygnałach, zdarzeniach, strumieniach asynchronicznych).

%package apidocs
Summary:	API documentation for Zug library
Summary(pl.UTF-8):	Dokumentacja API biblioteki Zug
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for Zug library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki Zug.

%prep
%setup -q

tar xf %{SOURCE1} -C tools/sinusoidal-sphinx-theme --strip-components=1

%build
install -d build
cd build
%cmake .. \
	-Dzug_BUILD_EXAMPLES=OFF \
	-Dzug_BUILD_TESTS=OFF

%{__make}
cd ..

%if %{with apidocs}
%{__make} -C doc html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files devel
%defattr(644,root,root,755)
%doc LICENSE README.rst
%{_includedir}/zug
%{_libdir}/cmake/Zug

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/_build/html/{_images,_static,*.html,*.js}
%endif
