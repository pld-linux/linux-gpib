#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	smp		# don't build SMP module
%bcond_without	userspace	# don't build userspace module
%bcond_with	verbose		# verbose build (V=1)
#
# main package.
#

%define		mod_name	gpib

%define		_rel	0.1
Summary:	GPIB Linux Support
Summary(pl):	Sterowniki GPIB dla Linuksa
Name:		linux-gpib
Version:	3.2.05
Release:	%{_rel}
License:	GPL
Group:		Applications/System
Source0:	http://dl.sourceforge.net/linux-gpib/%{name}-%{version}.tar.gz
# Source0-md5:	65044161fe86a815c9c159fe301d85c4
#Patch0:		%{name}-Makefile.am.patch
URL:		http://linux-gpib.sourceforge.net/
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel-module-build >= 2.6.7}
BuildRequires:	rpmbuild(macros) >= 1.153
%endif
BuildRequires:	kernel-headers >= 2.6.8
BuildRequires:	python
Requires(pre,post):	kernel >= 2.6.8
Requires:	kernel-up >= 2.6.8
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Linux GPIB package provides support for GPIB (IEEE 488) hardware.

%description -l pl
Pakiet Linux GPIB s³u¿y do obs³ugi sprzêtu GPIB (IEEE 488).

# kernel subpackages.

%package -n kernel-%{mod_name}
Summary:	Linux driver for %{name}
Summary(pl):	Sterownik dla Linuksa do %{name}
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_up
Requires(postun):	%releq_kernel_up
%endif

%description -n kernel-%{mod_name}
This is driver for %{name} for Linux.

This package contains Linux module.

%description -n kernel-%{mod_name} -l pl
Sterownik dla Linuksa do %{name}.

Ten pakiet zawiera modu³ j±dra Linuksa.

%package -n kernel-smp-%{mod_name}
Summary:	Linux SMP driver for %{name}
Summary(pl):	Sterownik dla Linuksa SMP do %{name}
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_smp
Requires(postun):	%releq_kernel_smp
%endif

%description -n kernel-smp-%{mod_name}
This is driver for %{name} for Linux.

This package contains Linux SMP module.

%description -n kernel-smp-%{mod_name} -l pl
Sterownik dla Linuksa do %{name}.

Ten pakiet zawiera modu³ j±dra Linuksa SMP.

%prep
%setup -q
#patch0 -p1

%build
%{__aclocal} -I m4
%{__libtoolize}
%{__autoconf}
%{__automake}

%configure \
	--disable-guile-binding \
	--disable-perl-binding \
	--disable-php-binding \
	--disable-python-binding \
	--disable-tcl-binding \
	--disable-documentation

%if %{with userspace}
%{__make}
%endif

%if %{with kernel}
cd driver
for i in tms9914 agilent_82350b agilent_82357a cb7210 hp82335 hp_82341 nec7210 tnt4882 cec ines pc2 sys ; do

cd $i
# kernel module(s)
for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
	if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
		exit 1
	fi
	rm -rf include
	install -d include/{linux,config}
	ln -sf %{_kernelsrcdir}/config-$cfg .config
	ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h include/linux/autoconf.h
	ln -sf %{_kernelsrcdir}/include/asm-%{_target_base_arch} include/asm
	ln -sf %{_kernelsrcdir}/Module.symvers-$cfg Module.symvers
	touch include/config/MARKER

	cp -rdp ../include/* include
	install -d include/gpib
	cp -rdp include/gpib_user.h include/gpib
	cp -rdp ../../config.h include

	%{__make} -C %{_kernelsrcdir} clean \
		RCS_FIND_IGNORE="-name '*.ko' -o" \
		M=$PWD O=$PWD \
		%{?with_verbose:V=1}
	%{__make} -C %{_kernelsrcdir} modules \
		CC="%{__cc}" CPP="%{__cpp}" \
		M=$PWD O=$PWD \
		%{?with_verbose:V=1}

	if [ "$i" == "sys" ]; then
	    i=gpib_common
	fi
	if [ "$i" == "cec" ]; then
	    i=cec_gpib
	fi
	if [ "$i" == "ines" ]; then
	    i=ines_gpib
	fi
	if [ "$i" == "pc2" ]; then
	    i=pc2_gpib
	fi

	mv $i{,-$cfg}.ko
done
cd ..
done
%endif

%install
rm -rf $RPM_BUILD_ROOT
HOTPLUG_USB_CONF_DIR=/etc/hotplug/usb
USB_FIRMWARE_DIR=/usr/share/usb/

install -d $RPM_BUILD_ROOT{$HOTPLUG_USB_CONF_DIR,$USB_FIRMWARE_DIR}
%if %{with userspace}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	HOTPLUG_USB_CONF_DIR=$RPM_BUILD_ROOT$HOTPLUG_USB_CONF_DIR \
	USB_FIRMWARE_DIR=$RPM_BUILD_ROOT$USB_FIRMWARE_DIR
%endif

%if %{with kernel}
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/misc

cd driver
for i in agilent_82350b agilent_82357a cb7210 hp82335 hp_82341 nec7210 tms9914 tnt4882 cec ines pc2 sys; do
cd $i
	if [ "$i" == "sys" ]; then
	    i=gpib_common
	fi
	if [ "$i" == "cec" ]; then
	    i=cec_gpib
	fi
	if [ "$i" == "ines" ]; then
	    i=ines_gpib
	fi
	if [ "$i" == "pc2" ]; then
	    i=pc2_gpib
	fi

install $i-%{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/$i.ko
%if %{with smp} && %{with dist_kernel}
install $i-smp.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/$i.ko
cd ..
done
%endif
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post -n kernel-%{mod_name}
%depmod %{_kernel_ver}

%postun -n kernel-%{mod_name}
%depmod %{_kernel_ver}

%post	-n kernel-smp-%{mod_name}
%depmod %{_kernel_ver}smp

%postun	-n kernel-smp-%{mod_name}
%depmod %{_kernel_ver}smp

%if %{with kernel}
%files -n kernel-%{mod_name}
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/*.ko*

%if %{with smp} && %{with dist_kernel}
%files -n kernel-smp-%{mod_name}
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/misc/*.ko*
%endif
%endif
