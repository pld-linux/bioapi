# TODO:
# - change code to do not require *.so libs and use *.so.X.X.X
#
# Conditional build:
%bcond_without	qt	# don't build qtpwbsp module
#
Summary:	Framework for biometric-based authentication
Summary(pl.UTF-8):	Szkielet do uwierzytelniania opartego o biometrykę
Name:		bioapi
Version:	1.2.3
Release:	0.1
License:	BSD
Group:		Applications/Networking
Source0:	http://bioapi-linux.googlecode.com/files/%{name}_%{version}.tar.gz
# Source0-md5:	9bcfb8505a9e4379aa5012300afd3f8c
Patch0:		%{name}-c++.patch
URL:		http://code.google.com/p/bioapi-linux/
BuildRequires:	libstdc++-devel
%{?with_qt:BuildRequires:	qt-devel}
BuildRequires:	xorg-lib-libX11-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	libstdc++-devel

%description devel
Header files for BioAPI.

%description devel -l pl.UTF-8
Pliki nagłówkowe BioAPI.

%package static
Summary:	Static BioAPI libraries
Summary(pl.UTF-8):	Statyczne biblioteki BioAPI
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static BioAPI libraries.

%description static -l pl.UTF-8
Statyczne biblioteki BioAPI.

%package qt
Summary:	Sample BioAPI Qt application
Summary(pl.UTF-8):	Przykładowa aplikacja BioAPI w Qt
Group:		X11/Applications

%description qt
Sample BioAPI QT application.

%description qt -l pl.UTF-8
Przykładowa aplikacja BioAPI w Qt.

%prep
%setup -q -n %{name}-linux
#%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
%if %{with qt}
	--with-Qt-lib-dir=%{_libdir} \
%else
	--with-Qt-dir=no \
%endif
	--includedir=%{_includedir}/%{name} 

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_includedir}/%{name},/var/lib/bioapi}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install include/bioapi_util.h include/installdefs.h imports/cdsa/v2_0/inc/cssmtype.h \
        $RPM_BUILD_ROOT%{_includedir}/%{name}

mv $RPM_BUILD_ROOT%{_bindir}/Sample $RPM_BUILD_ROOT%{_bindir}/BioAPI-Sample
mv $RPM_BUILD_ROOT%{_bindir}/mds_install $RPM_BUILD_ROOT%{_bindir}/BioAPI-mds_install
mv $RPM_BUILD_ROOT%{_bindir}/mod_install $RPM_BUILD_ROOT%{_bindir}/BioAPI-mod_install

%if %{with qt}
mv $RPM_BUILD_ROOT%{_bindir}/MdsEdit $RPM_BUILD_ROOT%{_bindir}/BioAPI-MdsEdit
mv $RPM_BUILD_ROOT%{_bindir}/QSample $RPM_BUILD_ROOT%{_bindir}/BioAPI-QSample
%endif

# modules to dlopen
rm -f $RPM_BUILD_ROOT%{_libdir}/lib{bioapi_dummy100,pwbsp,qtpwbsp}.{la,a}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%{_bindir}/BioAPI-mds_install -s %{_libdir}
%{_bindir}/BioAPI-mod_install -fi %{_libdir}/libbioapi100.so
%{_bindir}/BioAPI-mod_install -fi %{_libdir}/libbioapi_dummy100.so

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
%attr(755,root,root) %{_libdir}/libbioapi_dummy100.so.*.*.*
%attr(755,root,root) %{_libdir}/libbioapi_mds300.so.*.*.*
%attr(755,root,root) %{_libdir}/libmds_util.so.*.*.*
%attr(755,root,root) %{_libdir}/libpwbsp.so.*.*.*
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
%attr(755,root,root) %{_libdir}/libqtpwbsp.so
%endif
