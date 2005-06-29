#
# Replace MODULE_NAME with real module name and MODULE_DIR
# with required directory name.
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
# Source0-md5:	-
#Source1:	-
# Source1-md5:	-
#Patch0:		%{name}-what.patch
URL:		http://linux-gpib.sourceforge.net/
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel-module-build >= 2.6.7}
BuildRequires:	rpmbuild(macros) >= 1.153
%endif
BuildRequires:	kernel-headers >= 2.6.8
PreReq:		-
Requires(pre,post):	kernel >= 2.6.8
Requires(preun):	-
Requires(postun):	-
Requires:	kernel_up >=2.6.8
Provides:	-
Obsoletes:	-
Conflicts:	-
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description

%description -l pl

# kernel subpackages.
%prep

%build

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

	mv MODULE_NAME{,-$cfg}.ko
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

%post	-n kernel-MODULE_DIR-%{name}
%depmod %{_kernel_ver}

%postun	-n kernel-MODULE_DIR-%{name}
%depmod %{_kernel_ver}

%post	-n kernel-smp-MODULE_DIR-%{name}
%depmod %{_kernel_ver}smp

%postun	-n kernel-smp-MODULE_DIR-%{name}
%depmod %{_kernel_ver}smp

%if %{with kernel}
%files -n kernel-MODULE_DIR-%{name}
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/MODULE_DIR/*.ko*

%if %{with smp} && %{with dist_kernel}
%files -n kernel-smp-MODULE_DIR-%{name}
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/MODULE_DIR/*.ko*
%endif
%endif

%if %{with userspace}
%files
%defattr(644,root,root,755)

%endif
