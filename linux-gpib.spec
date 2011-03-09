#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	userspace	# don't build userspace module
%bcond_with	verbose		# verbose build (V=1)
#
# main package.
#

%define		mod_name	gpib

%define		_rel	0.1
Summary:	GPIB Linux Support
Summary(pl.UTF-8):	Sterowniki GPIB dla Linuksa
Name:		linux-gpib
Version:	3.2.15
Release:	%{_rel}
License:	GPL
Group:		Applications/System
Source0:	http://dl.sourceforge.net/linux-gpib/%{name}-%{version}.tar.gz
# Source0-md5:	cc90a7d6738953230bd24a18188ac2f5
Patch0:		%{name}-include_file.patch
URL:		http://linux-gpib.sourceforge.net/
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel-module-build >= 3:2.6.7}
BuildRequires:	rpmbuild(macros) >= 1.153
%endif
BuildRequires:	kernel-headers >= 2.6.8
BuildRequires:	python
Requires(pre,post):	kernel >= 2.6.8
Requires:	kernel-up >= 2.6.8
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Linux GPIB package provides support for GPIB (IEEE 488) hardware.

%description -l pl.UTF-8
Pakiet Linux GPIB służy do obsługi sprzętu GPIB (IEEE 488).

# kernel subpackages.

%package -n kernel-%{mod_name}
Summary:	Linux driver for %{name}
Summary(pl.UTF-8):	Sterownik dla Linuksa do %{name}
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

%description -n kernel-%{mod_name} -l pl.UTF-8
Sterownik dla Linuksa do %{name}.

Ten pakiet zawiera moduł jądra Linuksa.

%prep
%setup -q
%patch0 -p1

%build
%if %{with kernel}
%{__}
TOPDIR="`pwd`/drivers/gpib"
%build_kernel_modules -C drivers/gpib -m gpib_common,cec_gpib,ines_gpib,pc2_gpib \
	CFLAGS="%{rpmcflags} -I$TOPDIR/include -I$TOPDIR/o/include/asm/mach-default"
%endif

%if %{with userspace}
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

%{__make}
%endif

#for i in tms9914 agilent_82350b agilent_82357a cb7210 hp82335 hp_82341 nec7210 tnt4882 cec ines pc2 sys ; do

%install
rm -rf $RPM_BUILD_ROOT

%if %{with kernel}
%install_kernel_modules -d misc -m gpib_common,cec_gpib,ines_gpib,pc2_gpib
#for i in agilent_82350b agilent_82357a cb7210 hp82335 hp_82341 nec7210 tms9914 tnt4882 cec ines pc2 sys; do
%endif

%if %{with userspace}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	HOTPLUG_USB_CONF_DIR=$RPM_BUILD_ROOT$HOTPLUG_USB_CONF_DIR \
	USB_FIRMWARE_DIR=$RPM_BUILD_ROOT$USB_FIRMWARE_DIR
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post -n kernel%{_alt_kernel}-%{mod_name}
%depmod %{_kernel_ver}

%postun -n kernel%{_alt_kernel}-%{mod_name}
%depmod %{_kernel_ver}

%if %{with kernel}
%files -n kernel%{_alt_kernel}-%{mod_name}
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/*.ko*
%endif
