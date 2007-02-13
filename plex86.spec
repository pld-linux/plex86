
# TODO: UP/SMP modules

%define		__year		2001
%define		__date		1015
#%define		__time		1707
%define		smpstr		%{?_with_smp:-smp}
%define		smp		%{?_with_smp:1}%{!?_with_smp:0}

Summary:	Virtual computer for x86
Summary(pl.UTF-8):	Wirtualny komputer dla x86
Name:		plex86
Version:	%{__year}%{__date}
Release:	1
License:	LGPL
Group:		Applications/Emulators
Source0:	%{name}-%{version}.tar.gz
# Source0-md5:	7369eb855ff6dd9bd6552785cc5128f3
# snapshots on ftp:
#Source0:	ftp://ftp.plex86.org/source-tarballs/current.tar.gz
# or
#Source0:	ftp://ftp.plex86.org/source-tarballs/plex86-%{__year}-%{__date}.tar.gz
#Patch0:		%{name}.patch
URL:		http://www.plex86.org/
BuildRequires:	XFree86-devel
BuildRequires:	libstdc++-devel
BuildRequires:	ncurses-devel
BuildRequires:	rpmbuild(macros) >= 1.118
Requires(post,postun):	fontpostinst
Requires:	kernel%{smpstr}-char-%{name}
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_kernel24	%(echo %{_kernel_ver} | grep -qv '2\.4\.' ; echo $?)

%description
Plex86 is an Open Source x86 PC virtualization program which let's you
concurrently run multiple x86 operating systems and corresponding
software on your x86 machine.

%description -l pl.UTF-8
Plex86 pozwala na uruchamianie wielu systemów operacyjnych na jednym
komputerze PC. Wykorzystywana jest tutaj metoda nazwana wirtualizacją,
która pozwala na dzielenie poszczególnych zasobów komputera między
pracujące systemy.

%package -n kernel%{smpstr}-char-plex86
Summary:	The kernel module necessary to use Plex86
Summary(pl.UTF-8):	Moduł jądra niezbędny do używania Plex86
Group:		Base/Kernel
Release:	%{release}@%{_kernel_ver_str}
Requires(post,postun):	/sbin/depmod
%{!?_without_dist_kernel:%{!?_with_smp:%requires_releq_kernel_up}}
%{!?_without_dist_kernel:%{?_with_smp:%requires_releq_kernel_smp}}
Obsoletes:	plex86-module

%description -n kernel%{smpstr}-char-plex86
Plex86 is an Open Source x86 PC virtualization program which let's you
concurrently run multiple x86 operating systems and corresponding
software on your x86 machine.

This package contains the kernel module necessary to run Plex86.

%description -n kernel%{smpstr}-char-plex86 -l pl.UTF-8
Plex86 pozwala na uruchamianie wielu systemów operacyjnych na jednym
komputerze PC. Wykorzystywana jest tutaj metoda nazwana wirtualizacją,
która pozwala na dzielenie poszczególnych zasobów komputera między
pracujące systemy.

Ten pakiet zawiera moduł jądra niezbędny do uruchomienia Plex86.

%prep
%setup -q -n %{name}
#%patch -p1

%build
CXXFLAGS="%{rpmcflags} -I/usr/include/ncurses"
%if %{smp}
CFLAGS="%{rpmcflags} -D__KERNEL_SMP=1"
%endif
%configure2_13 \
	--with-Linux \
	--with-linux-source=%{_kernelsrcdir} \
	--with-gui=x

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
# create necessary directories
install -d  $RPM_BUILD_ROOT%{_bindir} \
	$RPM_BUILD_ROOT%{_libdir}/plex86/{bios,conf,guest,misc,plugins} \
	$RPM_BUILD_ROOT%{_libdir}/plex86/guest/{cooperative,paging,preemptive,test,virtcode} \
	$RPM_BUILD_ROOT%{_libdir}/plex86/plugins/{bochs,ice,loader,misc,write-cache} \
	$RPM_BUILD_ROOT%{_fontsdir}/misc

%if %{_kernel24}
	install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/kernel/drivers/char
	cp kernel/plex86.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/kernel/drivers/char
%else
	install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc
	cp kernel/plex86.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc
%endif

# install the stuff
install user/plex86 $RPM_BUILD_ROOT%{_bindir}
install user/resetmod $RPM_BUILD_ROOT%{_bindir}
install bios/*BIOS* $RPM_BUILD_ROOT%{_libdir}/plex86/bios
rm -rf conf/CVS
cp -R conf/* $RPM_BUILD_ROOT%{_libdir}/plex86/conf
cp -R misc/* $RPM_BUILD_ROOT%{_libdir}/plex86/misc
install user/plugins/bochs/plugin-bochs.so $RPM_BUILD_ROOT%{_libdir}/plex86/plugins/bochs
install user/plugins/loader/load-kernel.so $RPM_BUILD_ROOT%{_libdir}/plex86/plugins/loader
install user/plugins/misc/replay_io.so $RPM_BUILD_ROOT%{_libdir}/plex86/plugins/misc
install user/plugins/write-cache/write-cache.so $RPM_BUILD_ROOT%{_libdir}/plex86/plugins/write-cache
#install user/plugins/ice/plugin-ice.so $RPM_BUILD_ROOT%{_libdir}/plex86/plugins/ice
install guest/cooperative/kernel $RPM_BUILD_ROOT%{_libdir}/plex86/guest/cooperative
install guest/paging/kernel $RPM_BUILD_ROOT%{_libdir}/plex86/guest/paging
install guest/preemptive/kernel $RPM_BUILD_ROOT%{_libdir}/plex86/guest/preemptive
install guest/test/kernel $RPM_BUILD_ROOT%{_libdir}/plex86/guest/test
install guest/virtcode/virtcode $RPM_BUILD_ROOT%{_libdir}/plex86/guest/virtcode

# added console fonts used by plex
gzip -9nf misc/vga.pcf
install misc/vga.pcf.gz $RPM_BUILD_ROOT%{_fontsdir}/misc

find docs -type d -name CVS | xargs rm -rf
find docs -type f -name .cvsignore -o -name Makefile\* | xargs rm -f
mv -f docs/README docs/README.docs

%clean
rm -rf $RPM_BUILD_ROOT

%post
fontpostinst misc

%postun
fontpostinst misc

%post	-n kernel%{smpstr}-char-plex86
%depmod %{_kernel_ver}

%postun -n kernel%{smpstr}-char-plex86
%depmod %{_kernel_ver}

%files
%defattr(644,root,root,755)
%doc README README.DOS ChangeLog PERFORMANCE SBE-OFF-CONDITIONS TODO
%doc docs/{README*,html,misc,xml,txt}
%attr(755,root,root) %{_bindir}/plex86
%attr(755,root,root) %{_bindir}/resetmod
%dir %{_libdir}/plex86
%dir %{_libdir}/plex86/guest
%dir %{_libdir}/plex86/guest/*
%attr(755,root,root) %{_libdir}/plex86/guest/cooperative/kernel
%attr(755,root,root) %{_libdir}/plex86/guest/paging/kernel
%attr(755,root,root) %{_libdir}/plex86/guest/preemptive/kernel
%attr(755,root,root) %{_libdir}/plex86/guest/test/kernel
%attr(755,root,root) %{_libdir}/plex86/guest/virtcode/virtcode
%dir %{_libdir}/plex86/plugins
%dir %{_libdir}/plex86/plugins/*
%attr(755,root,root) %{_libdir}/plex86/plugins/bochs/plugin-bochs.so
%attr(755,root,root) %{_libdir}/plex86/plugins/loader/load-kernel.so
%attr(755,root,root) %{_libdir}/plex86/plugins/misc/replay_io.so
%attr(755,root,root) %{_libdir}/plex86/plugins/write-cache/write-cache.so
#%attr(755,root,root) %{_libdir}/plex86/plugins/ice/plugin-ice.so
%dir %{_libdir}/plex86/misc
%{_libdir}/plex86/misc/mbrdata
%{_libdir}/plex86/misc/vga.pcf
%{_libdir}/plex86/misc/vga_io.log
%attr(755,root,root) %{_libdir}/plex86/misc/createdisk.sh
%{_libdir}/plex86/misc/createdisk.README
%attr(755,root,root) %{_libdir}/plex86/misc/load_module.sh
%attr(755,root,root) %{_libdir}/plex86/misc/unload_module.sh
%attr(755,root,root) %{_libdir}/plex86/misc/netbsd_post.sh
%dir %{_libdir}/plex86/bios
%{_libdir}/plex86/bios/*BIOS*
%{_libdir}/plex86/conf
%attr(666,root,root) %dev(c,254,0) /dev/plex86

%files -n kernel%{smpstr}-char-plex86
%defattr(644,root,root,755)
%if %{_kernel24}
/lib/modules/*/kernel/drivers/char/plex86.o*
%else
/lib/modules/*/misc/plex86.o*
%endif
