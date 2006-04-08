# TODO:
# - fix qt build on gcc 4.1
# - change code to do not require *.so libs and use *.so.X.X.X
%bcond_with qt
#
Summary:	Framework for biometric-based authentication
Name:		bioapi
Version:	1.2.2
Release:	0.1
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

%package devel
Summary:	Header files and development documentation for BioAPI
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
%{?with_qt:Requires:	%{name}-qt = %{epoch}:%{version}-%{release}}

%description devel
Header files and development documentation for BioAPI.

%package static
Summary:	Static BioAPI libraries
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static BioAPI libraries.

%package qt
Summary:	Sample BioAPI QT application
Group:		Applications

%description qt
Sample BioAPI QT application.

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
%attr(755,root,root) %{_bindir}/*
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
%attr(755,root,root) %{_bindir}/*qt*
%attr(755,root,root) %{_libdir}/libqtpwbsp.so*
%endif
