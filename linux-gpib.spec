#
# Conditional build:
%bcond_without	kernel		# kernel modules
%bcond_without	drivers_isa	# ISA kernel drivers [ix86 only]
%bcond_without	drivers_usb	# USB kernel drivers
%bcond_without	userspace	# userspace packages
%bcond_without	verbose		# verbose modules build (V=1)

%bcond_without	doc		# documentation build
%bcond_with	hotplug		# legacy hotplug support
%bcond_without	static_libs	# static library
%bcond_without	guile		# guile binding
%bcond_without	perl		# Perl binding
%bcond_with	php		# PHP binding
%bcond_without	python		# Python (any) binding
%bcond_without	python2		# Python 2.x binding
%bcond_without	tcl		# Tcl binding

# The goal here is to have main, userspace, package built once with
# simple release number, and only rebuild kernel packages with kernel
# version as part of release number, without the need to bump release
# with every kernel change.
%if 0%{?_pld_builder:1} && %{with kernel} && %{with userspace}
%{error:kernel and userspace cannot be built at the same time on PLD builders}
exit 1
%endif

%ifnarch %{ix86}
%undefine	with_drivers_isa
%endif
%if %{without python}
%undefine	with_python2
%endif

%define		php_name	php%{?php_suffix}

%define		rel	2
%define		pname	linux-gpib
Summary:	GPIB (IEEE 488) Linux support
Summary(pl.UTF-8):	Obsługa GPIB (IEEE 488) dla Linuksa
Name:		%{pname}%{?_pld_builder:%{?with_kernel:-kernel}}%{_alt_kernel}
Version:	4.3.3
Release:	%{rel}%{?_pld_builder:%{?with_kernel:@%{_kernel_ver_str}}}
License:	GPL v2+
Group:		Applications/System
Source0:	http://downloads.sourceforge.net/linux-gpib/%{pname}-%{version}.tar.gz
# Source0-md5:	1243aa44f788cf23f9b40ded54c14685
Patch2:		%{pname}-python.patch
Patch3:		%{pname}-perl.patch
Patch4:		%{pname}-firmwaredir.patch
Patch5:		%{pname}-guile2.patch
Patch6:		%{pname}-php7.patch
Patch8:		kernel-5.2.patch
Patch9:		kernel-5.10.patch
URL:		http://linux-gpib.sourceforge.net/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	rpmbuild(macros) >= 1.745
%if %{with kernel}
BuildRequires:	kernel-module-build >= 3:2.6.8
%endif
%if %{with userspace}
BuildRequires:	bison
%{?with_doc:BuildRequires:	docbook-utils}
BuildRequires:	flex
%{?with_guile:BuildRequires:	guile-devel >= 1.4}
%{?with_perl:BuildRequires:	perl-devel}
%{?with_php:BuildRequires:	%{php_name}-devel >= 3:5}
%{?with_python:BuildRequires:	python-devel >= 2}
BuildRequires:	readline-devel
%{?with_tcl:BuildRequires:	tcl-devel}
%endif
Requires:	%{pname}-libs = %{version}-%{release}
# for agilent_82357a and ni_usb_gpib
Suggests:	fxload
# for agilent_82357a, agilent/hp_82341, agilent/hp_82350a, ni_usb_gpib
Suggests:	linux-gpib-firmware
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Linux GPIB package provides support for GPIB (IEEE 488) hardware.

%description -l pl.UTF-8
Pakiet Linux GPIB służy do obsługi sprzętu GPIB (IEEE 488).

%package hotplug
Summary:	Linux GPIB support for legacy USB hotplug
Summary(pl.UTF-8):	Obsługa Linux GPIB dla starego systemu hotplug USB
Group:		Applications/System
Requires:	%{pname} = %{version}-%{release}
Requires:	hotplug

%description hotplug
Linux GPIB support for legacy USB hotplug.

%description hotplug -l pl.UTF-8
Obsługa Linux GPIB dla starego systemu hotplug USB.

%package libs
Summary:	Shared GPIB library
Summary(pl.UTF-8):	Biblioteka współdzielona GPIB
Group:		Libraries

%description libs
Shared GPIB library.

%description libs -l pl.UTF-8
Biblioteka współdzielona GPIB.

%package devel
Summary:	Header file for GPIB library
Summary(pl.UTF-8):	Plik nagłówkowy biblioteki GPIB
Group:		Development/Libraries
Requires:	%{pname}-libs = %{version}-%{release}

%description devel
Header file for GPIB library.

%description devel -l pl.UTF-8
Plik nagłówkowy biblioteki GPIB.

%package static
Summary:	Static GPIB library
Summary(pl.UTF-8):	Biblioteka statyczna GPIB
Group:		Development/Libraries
Requires:	%{pname}-devel = %{version}-%{release}

%description static
Static GPIB library.

%description static -l pl.UTF-8
Biblioteka statyczna GPIB.

%package -n guile-gpib
Summary:	Guile bindings for GPIB library
Summary(pl.UTF-8):	Wiązania Guile do biblioteki GPIB
Group:		Development/Languages/Perl
Requires:	%{pname}-libs = %{version}-%{release}
Requires:	guile-libs

%description -n guile-gpib
Guile bindings for GPIB library.

%description -n guile-gpib -l pl.UTF-8
Wiązania Guile do biblioteki GPIB.

%package -n perl-gpib
Summary:	Perl bindings for GPIB library
Summary(pl.UTF-8):	Wiązania Perla do biblioteki GPIB
Group:		Development/Languages/Perl
Requires:	%{pname}-libs = %{version}-%{release}

%description -n perl-gpib
Perl bindings for GPIB library.

%description -n perl-gpib -l pl.UTF-8
Wiązania Perla do biblioteki GPIB.

%package -n %{php_name}-gpib
Summary:	PHP bindings for GPIB library
Summary(pl.UTF-8):	Wiązania PHP do biblioteki GPIB
Group:		Development/Languages/PHP
Provides:	php(gpib) = %{version}
Requires:	%{pname}-libs = %{version}-%{release}
%{?requires_php_extension}

%description -n %{php_name}-gpib
PHP bindings for GPIB library.

%description -n %{php_name}-gpib -l pl.UTF-8
Wiązania PHP do biblioteki GPIB.

%package -n python-gpib
Summary:	Python 2 bindings for GPIB library
Summary(pl.UTF-8):	Wiązania Pythona 2 do biblioteki GPIB
Group:		Libraries/Python
Requires:	%{pname}-libs = %{version}-%{release}
Requires:	python-libs

%description -n python-gpib
Python 2 bindings for GPIB library.

%description -n python-gpib -l pl.UTF-8
Wiązania Pythona 2 do biblioteki GPIB.

%package -n python3-gpib
Summary:	Python 3 bindings for GPIB library
Summary(pl.UTF-8):	Wiązania Pythona 3 do biblioteki GPIB
Group:		Libraries/Python
Requires:	%{pname}-libs = %{version}-%{release}
Requires:	python3-libs

%description -n python3-gpib
Python 3 bindings for GPIB library.

%description -n python3-gpib -l pl.UTF-8
Wiązania Pythona 3 do biblioteki GPIB.

%package -n tcl-gpib
Summary:	Tcl bindings for GPIB library
Summary(pl.UTF-8):	Wiązania Tcl-a do biblioteki GPIB
Group:		Libraries
Requires:	%{pname}-libs = %{version}-%{release}
Requires:	tcl

%description -n tcl-gpib
Tcl bindings for GPIB library.

%description -n tcl-gpib -l pl.UTF-8
Wiązania Tcl-a do biblioteki GPIB.

%package doc
Summary:	Linux-GPIB tools and library documentation
Summary(pl.UTF-8):	Dokumentacja narzędzi i biblioteki Linux-GPIB
License:	GFDL v1.2+ or GPL v2+
Group:		Documentation

%description doc
Linux-GPIB tools and library documentation.

%description doc -l pl.UTF-8
Dokumentacja narzędzi i biblioteki Linux-GPIB.

%define kernel_pkg()\
%package -n kernel%{_alt_kernel}-gpib\
Summary:	Linux GPIB drivers\
Summary(pl.UTF-8):	Sterowniki GPIB dla Linuksa\
Release:	%{rel}@%{_kernel_ver_str}\
Group:		Base/Kernel\
Requires(post,postun):	/sbin/depmod\
%requires_releq_kernel\
Requires(postun):	%releq_kernel\
\
%description -n kernel%{_alt_kernel}-gpib\
This package contains Linux drivers for GPIB (IEEE 488) hardware.\
\
%description -n kernel%{_alt_kernel}-gpib -l pl.UTF-8\
Ten pakiet zawiera sterowniki dla Linuksa do urządzeń GPIB (IEEE 488).\
\
%if %{with kernel}\
%files -n kernel%{_alt_kernel}-gpib\
%defattr(644,root,root,755)\
/lib/modules/%{_kernel_ver}/kernel/gpib\
%endif\
\
%post -n kernel%{_alt_kernel}-gpib\
%depmod %{_kernel_ver}\
\
%postun -n kernel%{_alt_kernel}-gpib\
%depmod %{_kernel_ver}\
%{nil}

%define build_kernel_pkg()\
%{__make} VERBOSE=1 LINUX_SRCDIR=%{_kernelsrcdir}\
cd drivers/gpib\
%if %{_kernel_version_code} < %{_kernel_version_magic 5 10 0}\
%if %{with drivers_usb}\
%install_kernel_modules -D installed -m lpvo_usb_gpib/lpvo_usb_gpib -d kernel/gpib\
%endif\
%endif\
%ifarch %{ix86}\
%install_kernel_modules -D installed -m agilent_82350b/agilent_82350b,cb7210/cb7210,cec/cec_gpib,hp_82335/hp82335,ines/ines_gpib,nec7210/nec7210,sys/gpib_common,tms9914/tms9914,tnt4882/tnt4882%{?with_drivers_isa:,pc2/pc2_gpib}%{?with_drivers_usb:,agilent_82357a/agilent_82357a,ni_usb/ni_usb_gpib} -d kernel/gpib\
%else\
%install_kernel_modules -D installed -m agilent_82350b/agilent_82350b,cb7210/cb7210,cec/cec_gpib,hp_82335/hp82335,hp_82341/hp_82341,ines/ines_gpib,nec7210/nec7210,sys/gpib_common,tms9914/tms9914,tnt4882/tnt4882%{?with_drivers_isa:,pc2/pc2_gpib}%{?with_drivers_usb:,agilent_82357a/agilent_82357a,ni_usb/ni_usb_gpib} -d kernel/gpib\
%endif\
cd ../..\
%{nil}

%define install_kernel_pkg()\
%{nil}

%{?with_kernel:%{expand:%create_kernel_packages}}

%prep
%setup -q -n %{pname}-%{version}
%if %{with userspace}
tar xzf linux-gpib-user-%{version}.tar.gz
cd linux-gpib-user-%{version}
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
#%patch6 -p1
cd ..
%endif

%if %{with kernel}
tar xzf linux-gpib-kernel-%{version}.tar.gz
cd linux-gpib-kernel-%{version}
%ifarch %{ix86}
%patch8 -p1
%endif
%patch9 -p1
%endif

%build
%if %{with userspace}
cd linux-gpib-user-%{version}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%if %{with guile}
CPPFLAGS="%{rpmcppflags} -I/usr/include/guile/2.2"
%endif
%configure \
	--with-udev-libdir=/lib/udev \
	%{!?with_doc:--disable-documentation} \
	%{!?with_guile:--disable-guile-binding} \
	%{!?with_perl:--disable-perl-binding} \
	%{!?with_php:--disable-php-binding} \
	%{!?with_python:--disable-python-binding} \
	%{?with_static_libs:--enable-static} \
	%{!?with_tcl:--disable-tcl-binding}

%{__make}

%if %{with python2}
cd language/python
%py_build
cd ../..
%endif
cd ..
%endif

%if %{with kernel}
cd linux-gpib-kernel-%{version}
%{expand:%build_kernel_packages}
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}

%if %{with kernel}
cd linux-gpib-kernel-%{version}
%{expand:%install_kernel_packages}
cp -a drivers/gpib/installed/* $RPM_BUILD_ROOT
cd ..
%endif

%if %{with userspace}
cd linux-gpib-user-%{version}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	HOTPLUG_USB_CONF_DIR=/lib/udev \
	UDEV_RULES_DIR=/lib/udev/rules.d \
	USB_FIRMWARE_DIR=/lib/firmware

%if %{with python2}
cd language/python
%py_install
cd ../..
%endif

%if %{with hotplug}
# use udev paths as base and legacy hotplug as addon (not the opposite)
install -d $RPM_BUILD_ROOT/etc/hotplug/usb
%{__mv} $RPM_BUILD_ROOT/lib/udev/*.usermap $RPM_BUILD_ROOT/etc/hotplug/usb
ln -snf /lib/udev/agilent_82357a $RPM_BUILD_ROOT/etc/hotplug/usb/agilent_82357a
ln -snf /lib/udev/ni_usb_gpib $RPM_BUILD_ROOT/etc/hotplug/usb/ni_usb_gpib
%endif

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libgpib.la

%if %{with guile}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libgpib-guile.la
%if %{with static_libs}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libgpib-guile.a
%endif
%endif

%if %{with perl}
%{__make} -C language/perl pure_install \
	DESTDIR=$RPM_BUILD_ROOT

cp -pr language/perl/examples $RPM_BUILD_ROOT%{_examplesdir}/perl-gpib-%{version}

%{__rm} -f $RPM_BUILD_ROOT%{perl_vendorarch}/auto/LinuxGpib/.packlist
%endif

%if %{with php}
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/gpib.ini
; Enable gpib extension module
extension=gpib_php.so
EOF

%{__rm} $RPM_BUILD_ROOT%{php_extensiondir}/gpib_php.la
%if %{with static_libs}
%{__rm} $RPM_BUILD_ROOT%{php_extensiondir}/gpib_php.a
%endif
%endif

%if %{with python}
%py_postclean
%endif

%if %{with tcl}
cp -pr language/tcl/examples $RPM_BUILD_ROOT%{_examplesdir}/tcl-gpib-%{version}

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libgpib_tcl.la
%if %{with static_libs}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libgpib_tcl.a
%endif
%endif

%if %{with doc}
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/linux-gpib-user/html
%endif
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post	-n guile-gpib -p /sbin/ldconfig
%postun	-n guile-gpib -p /sbin/ldconfig

%post	-n tcl-gpib -p /sbin/ldconfig
%postun	-n tcl-gpib -p /sbin/ldconfig

%post	-n %{php_name}-gpib
%php_webserver_restart

%postun	-n %{php_name}-gpib
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%if %{with userspace}
%files
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/gpib.conf
%attr(755,root,root) %{_bindir}/ibterm
%attr(755,root,root) %{_bindir}/ibtest
%attr(755,root,root) %{_sbindir}/gpib_config
/lib/udev/rules.d/98-gpib-generic.rules
/lib/udev/rules.d/99-agilent_82357a.rules
/lib/udev/rules.d/99-ni_usb_gpib.rules
%attr(755,root,root) /lib/udev/gpib_udev_config
%attr(755,root,root) /lib/udev/gpib_udev_fxloader
%attr(755,root,root) /lib/udev/gpib_udevadm_wrapper

%if %{with hotplug}
%files hotplug
%defattr(644,root,root,755)
%attr(755,root,root) /etc/hotplug/usb/agilent_82357a
%attr(755,root,root) /etc/hotplug/usb/ni_usb_gpib
/etc/hotplug/usb/agilent_82357a.usermap
/etc/hotplug/usb/ni_usb_gpib.usermap
%endif

%files libs
%defattr(644,root,root,755)
%doc linux-gpib-user-%{version}/{AUTHORS,ChangeLog,README,README.HAMEG,README.hp82335,TODO}
%attr(755,root,root) %{_libdir}/libgpib.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgpib.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgpib.so
%{_includedir}/gpib
%{_pkgconfigdir}/libgpib.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libgpib.a
%endif

%if %{with guile}
%files -n guile-gpib
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgpib-guile-%{version}.so
%attr(755,root,root) %{_libdir}/libgpib-guile.so
%endif

%if %{with perl}
%files -n perl-gpib
%defattr(644,root,root,755)
%doc linux-gpib-user-%{version}/language/perl/{Changes,README}
%{perl_vendorarch}/LinuxGpib.pm
%dir %{perl_vendorarch}/auto/LinuxGpib
%attr(755,root,root) %{perl_vendorarch}/auto/LinuxGpib/LinuxGpib.so
%{perl_vendorarch}/auto/LinuxGpib/autosplit.ix
%{_mandir}/man3/LinuxGpib.3pm*
%{_examplesdir}/perl-gpib-%{version}
%endif

%if %{with php}
%files -n %{php_name}-gpib
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/gpib.ini
%attr(755,root,root) %{php_extensiondir}/gpib_php-%{version}.so
%attr(755,root,root) %{php_extensiondir}/gpib_php.so
%endif

%if %{with python2}
%files -n python-gpib
%defattr(644,root,root,755)
%doc linux-gpib-user-%{version}/language/python/README
%attr(755,root,root) %{py_sitedir}/gpib.so
%{py_sitedir}/Gpib.py[co]
%{py_sitedir}/gpib-1.0-py*.egg-info
%endif

%if %{with python}
%files -n python3-gpib
%defattr(644,root,root,755)
%doc linux-gpib-user-%{version}/language/python/README
%attr(755,root,root) %{py3_sitedir}/gpib.cpython-*.so
%{py3_sitedir}/Gpib.py
%{py3_sitedir}/__pycache__/Gpib.cpython-*.py[co]
%{py3_sitedir}/gpib-1.0-py*.egg-info
%endif

%if %{with tcl}
%files -n tcl-gpib
%defattr(644,root,root,755)
%doc linux-gpib-user-%{version}/language/tcl/README
%attr(755,root,root) %{_libdir}/libgpib_tcl-%{version}.so
%attr(755,root,root) %{_libdir}/libgpib_tcl.so
%{_examplesdir}/tcl-gpib-%{version}
%endif

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%doc linux-gpib-user-%{version}/doc/doc_html/*
%endif
%endif
