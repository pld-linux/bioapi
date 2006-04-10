# TODO:
# - change code to do not require *.so libs and use *.so.X.X.X
# - create qt-devel (if necessary), kill -qt R: in -devel
#
# Conditional build:
%bcond_without	qt
#
Summary:	Framework for biometric-based authentication
Summary(pl):	Szkielet do uwierzytelniania opartego o biometrykê
Name:		bioapi
Version:	1.2.2
Release:	0.2
License:	BSD
Group:		Applications/Networking
Source0:	http://www.qrivy.net/~michael/blua/bioapi/%{name}-%{version}.tar.bz2
# Source0-md5:	924f723895c339552e501999945b7920
Patch0:		%{name}-c++.patch
URL:		http://www.qrivy.net/~michael/blua/
%{?with_qt:BuildRequires:	qt-devel}
BuildRequires:	xorg-lib-libX11-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%description -l pl
Wzorcowa implementacja BioAPI dla platform uniksowych. Zosta³a
stworzona przez Convergent Information Division (CISD), Information
Technology Laboratory (ITL) z National Institute of Standards and
Technology (NIST). Jest oparta bezpo¶rednio na wzorcowej implementacji
BioAPI Consortium dla Windows oraz wzorcowej implementacji Common Data
Security Architecture (CDSA). Uniksowa implementacja zawiera aplikacjê
przyk³adow± i narzêdzie MdsEdit z kodu dostarczonego przez
International Biometric Group (IBG).

%package devel
Summary:	Header files for BioAPI
Summary(pl):	Pliki nag³ówkowe BioAPI
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
%{?with_qt:Requires:	%{name}-qt = %{epoch}:%{version}-%{release}}

%description devel
Header files for BioAPI.

%description devel -l pl
Pliki nag³ówkowe BioAPI.

%package static
Summary:	Static BioAPI libraries
Summary(pl):	Statyczne biblioteki BioAPI
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static BioAPI libraries.

%description static -l pl
Statyczne biblioteki BioAPI.

%package qt
Summary:	Sample BioAPI Qt application
Summary(pl):	Przyk³adowa aplikacja BioAPI w Qt
Group:		X11/Applications

%description qt
Sample BioAPI QT application.

%description qt -l pl
Przyk³adowa aplikacja BioAPI w Qt.

%prep
%setup -q
%patch0 -p1

%build
%configure \
%if %{with qt}
	--with-Qt-lib-dir=%{_libdir} \
%else
	--with-Qt-dir=no \
%endif
	--includedir=%{_includedir}/%{name}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_includedir}/%{name}

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
%{?with_qt:%exclude %{_libdir}/libqtpwbsp.so*}
%attr(755,root,root) %{_libdir}/lib*.so*

%files devel
%defattr(644,root,root,755)
%{_includedir}/%{name}
%{_libdir}/lib*.la
# *.so needed in main package
#%{?with_qt:%exclude %{_libdir}/libqtpwbsp.so.*}
#%attr(755,root,root) %{_libdir}/lib*.so

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a

%if %{with qt}
%files qt
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/BioAPI-MdsEdit
%attr(755,root,root) %{_bindir}/BioAPI-QSample
%attr(755,root,root) %{_libdir}/libqtpwbsp.so*
%endif
