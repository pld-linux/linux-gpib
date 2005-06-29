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

Summary:	GPIB Linux Support
Summary(pl):	Sterowniki GPIB dkla Linuksa
Name:		linux-gpib
Version:	3.2.05
%define		_rel	0.1
Release:	%{_rel}
#Epoch:		
License:	GPL
Group:		Unknown
Vendor:		PLD
#Icon:		-
Source0:	http://dl.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
# Source0-md5:	65044161fe86a815c9c159fe301d85c4
#Source1:	-
# Source1-md5:	-
#Patch0:		%{name}-what.patch
URL:		http://linux-gpib.sourceforge.net/
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel-module-build >= 2.6.7}
BuildRequires:	rpmbuild(macros) >= 1.153
%endif
BuildRequires:	kernel-headers >= 2.6.8
#PreReq:		-
Requires(pre,post):	kernel >= 2.6.8
#Requires(preun):	-
#Requires(postun):	-
Requires:	kernel-up >= 2.6.8
#Provides:	-
#Obsoletes:	-
#Conflicts:	-
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description

%description -l pl

# kernel subpackages.

%package -n kernel-%{mod_name}
Summary:        Linux driver for %{name}
Summary(pl):    Sterownik dla Linuksa do %{name}
Release:        %{_rel}@%{_kernel_ver_str}
Group:          Base/Kernel
Requires(post,postun):  /sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_up
Requires(postun):       %releq_kernel_up
%endif

%description -n kernel-%{mod_name}
This is driver for %{name} for Linux.

This package contains Linux module.

%description -n kernel-%{mod_name} -l pl
Sterownik dla Linuksa do %{name}.

Ten pakiet zawiera modu³ j±dra Linuksa.

%package -n kernel-smp-%{mod_name}
Summary:        Linux SMP driver for %{name}
Summary(pl):    Sterownik dla Linuksa SMP do %{name}
Release:        %{_rel}@%{_kernel_ver_str}
Group:          Base/Kernel
Requires(post,postun):  /sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_smp
Requires(postun):       %releq_kernel_smp
%endif

%description -n kernel-smp-%{mod_name}
This is driver for %{name} for Linux.

This package contains Linux SMP module.

%description -n kernel-smp-%{mod_name} -l pl
Sterownik dla Linuksa do %{name}.

Ten pakiet zawiera modu³ j±dra Linuksa SMP.


%prep

%setup -q

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

%{__make}	
%if %{with userspace}


%endif


%if %{with kernel}
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
	touch include/config/MARKER
#
#	patching/creating makefile(s) (optional)
#
	%{__make} -C %{_kernelsrcdir} clean \
		RCS_FIND_IGNORE="-name '*.ko' -o" \
		M=$PWD O=$PWD \
		%{?with_verbose:V=1}
	%{__make} -C %{_kernelsrcdir} modules \
		CC="%{__cc}" CPP="%{__cpp}" \
		M=$PWD O=$PWD \
		%{?with_verbose:V=1}

##	mv MODULE_NAME{,-$cfg}.ko
done
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with userspace}


%endif

%if %{with kernel}
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/MODULE_DIR
install MODULE_NAME-%{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/MODULE_DIR/MODULE_NAME.ko
%if %{with smp} && %{with dist_kernel}
install MODULE_NAME-smp.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/MODULE_DIR/MODULE_NAME.ko
%endif
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%depmod %{_kernel_ver}

%postun
%depmod %{_kernel_ver}

#%post	-n kernel-smp-MODULE_DIR-%{name}
#%depmod %{_kernel_ver}smp

#%postun	-n kernel-smp-MODULE_DIR-%{name}
#%depmod %{_kernel_ver}smp

%if %{with kernel}
%files 
#%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/MODULE_DIR/*.ko*

%endif
