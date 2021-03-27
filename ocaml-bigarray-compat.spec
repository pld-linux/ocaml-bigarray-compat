#
# Conditional build:
%bcond_without	ocaml_opt	# skip building native optimized binaries (bytecode is always built)

# not yet available on x32 (ocaml 4.02.1), update when upstream will support it
%ifnarch %{ix86} %{x8664} %{arm} aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

%define		_enable_debug_packages	0

%define		module	bigarray-compat
Summary:	Compatibility library to use Stdlib.Bigarray when possible
Name:		ocaml-%{module}
Version:	1.0.0
Release:	1
License:	ISC
Source0:	https://github.com/mirage/bigarray-compat/archive/v%{version}/%{module}-%{version}.tar.gz
# Source0-md5:	1cc7c25382a8900bada34aadfd66632e
URL:		https://github.com/mirage/bigarray-compat
BuildRequires:	ocaml >= 4.03.0
BuildRequires:	ocaml-dune >= 1.0
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Bigarray-compat is an OCaml library that exposes `Stdlib.Bigarray`
when possible (OCaml >= 4.07) but can fallback to `Bigarray`. The
compability bigarray module is exposed under `Bigarray_compat`.

%package        devel
Summary:	Development files for %{name}
Requires:	%{name} = %{version}-%{release}
%requires_eq ocaml

%description    devel
This package contains libraries and signature files for developing
applications that use %{name}.

%prep
%setup -q -n %{module}-%{version}

%build
dune build %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
dune install --destdir=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%dir %{_libdir}/ocaml/bigarray-compat
%{_libdir}/ocaml/bigarray-compat/META
%{_libdir}/ocaml/bigarray-compat/*.cma
%{_libdir}/ocaml/bigarray-compat/*.cmi
%if %{with ocaml_opt}
%attr(755,root,root) %{_libdir}/ocaml/bigarray-compat/*.cmxs
%endif

%files devel
%defattr(644,root,root,755)
%{_libdir}/ocaml/bigarray-compat/dune-package
%{_libdir}/ocaml/bigarray-compat/opam
%if %{with ocaml_opt}
%{_libdir}/ocaml/bigarray-compat/*.a
%{_libdir}/ocaml/bigarray-compat/*.cmx
%{_libdir}/ocaml/bigarray-compat/*.cmxa
%endif
%{_libdir}/ocaml/bigarray-compat/*.cmt
