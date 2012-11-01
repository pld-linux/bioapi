# TODO:
# - change code to do not require *.so libs and dlopen by SONAME
#
# Conditional build:
%bcond_without	qt	# don't build qtpwbsp module
#
Summary:	Framework for biometric-based authentication
Summary(pl.UTF-8):	Szkielet do uwierzytelniania opartego o biometrykę
Name:		bioapi
Version:	1.2.4
Release:	0.1
License:	BSD
Group:		Applications/Networking
#Source0Download: http://code.google.com/p/bioapi-linux/downloads/list
Source0:	http://bioapi-linux.googlecode.com/files/%{name}_%{version}.tar.gz
# Source0-md5:	98c20bd7bb2d87f24980c87b6e1c3fb6
Patch0:		%{name}-build.patch
Patch1:		%{name}-no-delete.patch
URL:		http://code.google.com/p/bioapi-linux/
BuildRequires:	autoconf >= 2.67
BuildRequires:	automake >= 1.6
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2
%{?with_qt:BuildRequires:	qt-devel}
%{?with_qt:BuildRequires:	xorg-lib-libXt-devel}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# circular symbol dependencies between libmds_util and libbioapi_mds300
%define		skip_post_check_so	libmds_util.so.*

# to get /var/lib/bioapi instead of /var/bioapi
%define		_localstatedir	/var/lib

%description
BioAPI reference implementation for Unix-based platforms. The
Unix-based reference implementation was developed by the Convergent
Information Division (CISD), Information Technology Laboratory (ITL)
of the National Institute of Standards and Technology (NIST). The
Unix-based reference implementation is based directly on the BioAPI
Consortium's Windows reference implementation and the Common Data
Security Architecture (CDSA) reference implementation. The Unix-based
reference implementation includes the Sample application and the
MdsEdit utility from code provided by the International Biometric
Group (IBG).

%description -l pl.UTF-8
Wzorcowa implementacja BioAPI dla platform uniksowych. Została
stworzona przez Convergent Information Division (CISD), Information
Technology Laboratory (ITL) z National Institute of Standards and
Technology (NIST). Jest oparta bezpośrednio na wzorcowej implementacji
BioAPI Consortium dla Windows oraz wzorcowej implementacji Common Data
Security Architecture (CDSA). Uniksowa implementacja zawiera aplikację
przykładową i narzędzie MdsEdit z kodu dostarczonego przez
International Biometric Group (IBG).

%package devel
Summary:	Header files for BioAPI
Summary(pl.UTF-8):	Pliki nagłówkowe BioAPI
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel

%description devel
Header files for BioAPI.

%description devel -l pl.UTF-8
Pliki nagłówkowe BioAPI.

%package static
Summary:	Static BioAPI libraries
Summary(pl.UTF-8):	Statyczne biblioteki BioAPI
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static BioAPI libraries.

%description static -l pl.UTF-8
Statyczne biblioteki BioAPI.

%package qt
Summary:	Sample BioAPI Qt application
Summary(pl.UTF-8):	Przykładowa aplikacja BioAPI w Qt
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}

%description qt
Sample BioAPI QT application.

%description qt -l pl.UTF-8
Przykładowa aplikacja BioAPI w Qt.

%prep
%setup -q -n %{name}-linux
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
%if %{with qt}
	--with-Qt-bin-dir=/usr/bin \
	--with-Qt-include-dir=/usr/include/qt \
	--with-Qt-lib-dir=%{_libdir} \
	--with-Qt-lib=qt-mt \
%else
	--without-Qt-dir \
%endif
	--includedir=%{_includedir}/%{name}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_includedir}/%{name},/var/lib/bioapi}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cp -p imports/cdsa/v2_0/inc/cssmtype.h \
        $RPM_BUILD_ROOT%{_includedir}/%{name}

mv $RPM_BUILD_ROOT%{_bindir}/Sample $RPM_BUILD_ROOT%{_bindir}/BioAPI-Sample
mv $RPM_BUILD_ROOT%{_bindir}/mds_install $RPM_BUILD_ROOT%{_bindir}/BioAPI-mds_install
mv $RPM_BUILD_ROOT%{_bindir}/mod_install $RPM_BUILD_ROOT%{_bindir}/BioAPI-mod_install

%if %{with qt}
mv $RPM_BUILD_ROOT%{_bindir}/MdsEdit $RPM_BUILD_ROOT%{_bindir}/BioAPI-MdsEdit
mv $RPM_BUILD_ROOT%{_bindir}/QSample $RPM_BUILD_ROOT%{_bindir}/BioAPI-QSample
%endif

# modules to dlopen
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib{bioapi_dummy100,pwbsp,qtpwbsp}.{la,a}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%{_bindir}/BioAPI-mds_install -s %{_libdir}
%{_bindir}/BioAPI-mod_install -fi %{_libdir}/libbioapi100.so
%{_bindir}/BioAPI-mod_install -fi %{_libdir}/libbioapi_dummy100.so
%{_bindir}/BioAPI-mod_install -fi %{_libdir}/libpwbsp.so

%postun -p /sbin/ldconfig

%post qt
/sbin/ldconfig
%{_bindir}/BioAPI-mod_install -fi %{_libdir}/libqtpwbsp.so

%postun qt -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc *.htm Disclaimer
%attr(755,root,root) %{_bindir}/BioAPI-Sample
%attr(755,root,root) %{_bindir}/BioAPI-*_*
%attr(755,root,root) %{_bindir}/BioAPITest
%attr(755,root,root) %{_libdir}/libbioapi100.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libbioapi100.so.0
%attr(755,root,root) %{_libdir}/libbioapi_dummy100.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libbioapi_dummy100.so.0
%attr(755,root,root) %{_libdir}/libbioapi_mds300.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libbioapi_mds300.so.0
%attr(755,root,root) %{_libdir}/libmds_util.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmds_util.so.0
%attr(755,root,root) %{_libdir}/libpwbsp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpwbsp.so.0
# libraries are dlopened too
%attr(755,root,root) %{_libdir}/libbioapi100.so
%attr(755,root,root) %{_libdir}/libbioapi_dummy100.so
%attr(755,root,root) %{_libdir}/libbioapi_mds300.so
%attr(755,root,root) %{_libdir}/libmds_util.so
%attr(755,root,root) %{_libdir}/libpwbsp.so
%dir /var/lib/bioapi

%files devel
%defattr(644,root,root,755)
# *.so needed in main package (maybe except libmds_util.so?)
%{_libdir}/libbioapi100.la
%{_libdir}/libbioapi_mds300.la
%{_libdir}/libmds_util.la
%{_includedir}/%{name}

%files static
%defattr(644,root,root,755)
%{_libdir}/libbioapi100.a
%{_libdir}/libbioapi_mds300.a
%{_libdir}/libmds_util.a

%if %{with qt}
%files qt
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/BioAPI-MdsEdit
%attr(755,root,root) %{_bindir}/BioAPI-QSample
%attr(755,root,root) %{_libdir}/libqtpwbsp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libqtpwbsp.so.0
%attr(755,root,root) %{_libdir}/libqtpwbsp.so
%endif
