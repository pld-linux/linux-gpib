# TODO:
# - resolve udev vs hotplug issues (use /lib/udev/rules.d, don't require /etc/hotplug dir with udev)
# - guile 2 support
# - PHP 7 support
#
# Conditional build:
%bcond_without	kernel		# kernel modules
%bcond_without	userspace	# userspace packages
%bcond_without	verbose		# verbose modules build (V=1)

%bcond_without	docs		# documentation build
%bcond_without	static_libs	# static library
%bcond_with	guile		# guile binding
%bcond_without	perl		# Perl binding
%bcond_without	php		# PHP binding
%bcond_without	python		# Python binding
%bcond_without	tcl		# Tcl binding

Summary:	GPIB (IEEE 488) Linux support
Summary(pl.UTF-8):	Obsługa GPIB (IEEE 488) dla Linuksa
Name:		linux-gpib
Version:	4.0.3
%define	rel	0.1
Release:	%{rel}
License:	GPL v2+
Group:		Applications/System
Source0:	http://downloads.sourceforge.net/linux-gpib/%{name}-%{version}.tar.gz
# Source0-md5:	2d97191e538a57ba7350fcc011ee2596
Patch0:		%{name}-include_file.patch
Patch1:		%{name}-destdir.patch
Patch2:		%{name}-python.patch
Patch3:		%{name}-perl.patch
URL:		http://linux-gpib.sourceforge.net/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	rpmbuild(macros) >= 1.614
%if %{with kernel}
BuildRequires:	kernel-module-build >= 3:2.6.8
%endif
%if %{with userspace}
BuildRequires:	bison
%{?with_docs:BuildRequires:	docbook-utils}
BuildRequires:	flex
%{?with_guile:BuildRequires:	guile-devel < 5:2.0}
%{?with_perl:BuildRequires:	perl-devel}
%{?with_php:BuildRequires:	php-devel < 4:7}
%{?with_python:BuildRequires:	python-devel >= 2}
BuildRequires:	readline-devel
%{?with_tcl:BuildRequires:	tcl-devel}
%endif
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Linux GPIB package provides support for GPIB (IEEE 488) hardware.

%description -l pl.UTF-8
Pakiet Linux GPIB służy do obsługi sprzętu GPIB (IEEE 488).

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
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header file for GPIB library.

%description devel -l pl.UTF-8
Plik nagłówkowy biblioteki GPIB.

%package static
Summary:	Static GPIB library
Summary(pl.UTF-8):	Biblioteka statyczna GPIB
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static GPIB library.

%description static -l pl.UTF-8
Biblioteka statyczna GPIB.

%package -n perl-gpib
Summary:	Perl bindings for GPIB library
Summary(pl.UTF-8):	Wiązania Perla do biblioteki GPIB
Group:		Development/Languages/Perl
Requires:	%{name}-libs = %{version}-%{release}

%description -n perl-gpib
Perl bindings for GPIB library.

%description -n perl-gpib -l pl.UTF-8
Wiązania Perla do biblioteki GPIB.

%package -n python-gpib
Summary:	Python bindings for GPIB library
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki GPIB
Group:		Libraries/Python
Requires:	%{name}-libs = %{version}-%{release}
Requires:	python-libs

%description -n python-gpib
Python bindings for GPIB library.

%description -n python-gpib -l pl.UTF-8
Wiązania Pythona do biblioteki GPIB.

%package -n tcl-gpib
Summary:	Tcl bindings for GPIB library
Summary(pl.UTF-8):	Wiązania Tcl-a do biblioteki GPIB
Group:		Libraries
Requires:	%{name}-libs = %{version}-%{release}
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
TOPDIR=$(pwd)\
%build_kernel_modules -C drivers/gpib -m gpib -- EARLYCPPFLAGS="-I$TOPDIR -I$TOPDIR/drivers/gpib/include -I$TOPDIR/include"\
cd drivers/gpib\
%install_kernel_modules -D installed -m agilent_82350b/agilent_82350b,agilent_82357a/agilent_82357a,cb7210/cb7210,cec/cec_gpib,hp_82335/hp82335,hp_82341/hp_82341,ines/ines_gpib,lpvo_usb_gpib/lpvo_usb_gpib,nec7210/nec7210,ni_usb/ni_usb_gpib,pc2/pc2_gpib,sys/gpib_common,tms9914/tms9914,tnt4882/tnt4882 -d kernel/gpib\
%{nil}

%define install_kernel_pkg()\
%{nil}

%{?with_kernel:%{expand:%create_kernel_packages}}

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

# disable modules build by default, just install userspace header
echo 'SUBDIRS = gpib/include' > drivers/Makefile.am

# need to inject -I options before $(LINUXINCLUDE), the simplest way is to override CC
for f in drivers/gpib/*/Makefile ; do
echo 'override CC += $(EARLYCPPFLAGS)' >> $f
done

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
%ifarch %{ix86}
	--enable-isa \
	--enable-pcmcia \
%endif
	%{!?with_docs:--disable-documentation} \
	%{!?with_guile:--disable-guile-binding} \
	%{!?with_perl:--disable-perl-binding} \
	%{!?with_php:--disable-php-binding} \
	%{!?with_python:--disable-python-binding} \
	%{?with_static_libs:--enable-static} \
	%{!?with_tcl:--disable-tcl-binding} \
	--with-linux-srcdir=%{_kernelsrcdir}

%if %{with userspace}
%{__make}
%endif

%if %{with kernel}
%{expand:%build_kernel_packages}
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}

%if %{with kernel}
%{expand:%install_kernel_packages}
cp -a drivers/gpib/installed/* $RPM_BUILD_ROOT
%endif

%if %{with userspace}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libgpib.la

%if %{with perl}
%{__make} -C language/perl pure_install \
	DESTDIR=$RPM_BUILD_ROOT
cp -pr language/perl/examples $RPM_BUILD_ROOT%{_examplesdir}/perl-gpib-%{version}
%{__rm} -f $RPM_BUILD_ROOT%{perl_vendorarch}/auto/LinuxGpib/.packlist
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

%if %{with docs}
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/linux-gpib/html
%endif
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%if %{with userspace}
%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ibterm
%attr(755,root,root) %{_bindir}/ibtest
%attr(755,root,root) %{_sbindir}/gpib_config
# TODO: move to /lib/udev/rules.d
/etc/udev/rules.d/99-agilent_82357a.rules
/etc/udev/rules.d/99-gpib-generic.rules
/etc/udev/rules.d/99-ni_usb_gpib.rules
# TODO: paths to fix (scripts used also in udev .rules)
%attr(755,root,root) /etc/hotplug/usb/agilent_82357a
%attr(755,root,root) /etc/hotplug/usb/ni_usb_gpib
/etc/hotplug/usb/agilent_82357a.usermap
/etc/hotplug/usb/ni_usb_gpib.usermap
# /lib/firmware/...; and where are the files?
%dir %{_datadir}/usb/agilent_82357a
%dir %{_datadir}/usb/ni_usb_gpib

%files libs
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README README.HAMEG README.hp82335 TODO
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

%if %{with perl}
%files -n perl-gpib
%defattr(644,root,root,755)
%doc language/perl/{Changes,README}
%{perl_vendorarch}/LinuxGpib.pm
%dir %{perl_vendorarch}/auto/LinuxGpib
%attr(755,root,root) %{perl_vendorarch}/auto/LinuxGpib/LinuxGpib.so
%{perl_vendorarch}/auto/LinuxGpib/autosplit.ix
%{_mandir}/man3/LinuxGpib.3pm*
%{_examplesdir}/perl-gpib-%{version}
%endif

%if %{with python}
%files -n python-gpib
%defattr(644,root,root,755)
%doc language/python/README
%attr(755,root,root) %{py_sitedir}/gpib.so
%{py_sitedir}/Gpib.py[co]
%{py_sitedir}/gpib-1.0-py*.egg-info
%endif

%if %{with tcl}
%files -n tcl-gpib
%defattr(644,root,root,755)
%doc language/tcl/README
%attr(755,root,root) %{_libdir}/libgpib_tcl-%{version}.so
%attr(755,root,root) %{_libdir}/libgpib_tcl.so
%{_examplesdir}/tcl-gpib-%{version}
%endif

%if %{with docs}
%files doc
%defattr(644,root,root,755)
%doc doc/doc_html/*
%endif
%endif
