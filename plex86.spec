
%define		__year		2001
%define		__date		0718
#%define		__time		1707

Name:		plex86
Version:	%{__year}%{__date}
Release:	1
Summary:	x86 CPU emulator
Summary(pl):	Emulator procesorów x86
Group:		Applications/Emulators
Group(de):	Applikationen/Emulators
Group(pl):	Aplikacje/Emulatory
License:	LGPL
ExclusiveArch:	i586 i686 i786 K5 K6 K7
Source0:	ftp://ftp.plex86.org/pub/%{name}-%{__year}-%{__date}.tar.gz
#Patch0:		%{name}.patch
BuildRequires:	libstdc++-devel
BuildRequires:	XFree86-devel
BuildRequires:	ncurses-devel
PreReq:		XFree86
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_kernel_ver	%(grep UTS_RELEASE /usr/src/linux/include/linux/version.h 2>/dev/null | cut -d'"' -f2)
%define		_kernel24	%(echo %{_kernel_ver} | grep -q '2\.[012]\.' ; echo $?)

%description
Plex86 is an Open Source x86 PC virtualization program which let's you
concurrently run multiple x86 operating systems and corresponding
software on your x86 machine.

%description -l pl
Plex86 pozwala na uruchamianie wielu systemów operacyjnych na jednym
komputerze PC. Wykorzystywana jest tutaj metoda nazwana wirtualizacj±,
ktora pozwala na dzielenie poszczególnych zasobów komputera miêdzy
pracuj±ce systemy.

%prep
%setup -q -n %{name}
#%patch -p1

%build
CXXFLAGS="%{rpmcflags} -I/usr/include/ncurses"
%configure --with-Linux --with-gui=x

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
	install kernel/plex86.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/kernel/drivers/char
%else
	install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc
	install kernel/plex86.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc
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
install guest/virtcode/virtcode $RPM_BUILD_ROOT/%{_libdir}/plex86/guest/virtcode

# added console fonts used by plex
gzip -9nf misc/vga.pcf
install misc/vga.pcf.gz $RPM_BUILD_ROOT%{_fontsdir}/misc

find docs -type d -name CVS | xargs rm -rf
find docs -type f -name .cvsignore -o -name Makefile\* | xargs rm -f
mv -f docs/README docs/README.docs

gzip -9nf README README.DOS ChangeLog PERFORMANCE SBE-OFF-CONDITIONS TODO
gzip -9nf docs/{README.docs,txt/*,xml/README}

%clean
rm -rf $RPM_BUILD_ROOT

%post
mkfontdir %{_fontsdir}/misc
if [ ! -e /dev/plex86 ]; then
    mknod /dev/plex86 c 254 0
    chmod a+rw /dev/plex86
fi
/sbin/depmod -a

%postun
rm -f /dev/plex86
mkfontdir %{_fontsdir}/misc
/sbin/depmod -a

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/plex86
%attr(755,root,root) %{_bindir}/resetmod
%if %{_kernel24}
/lib/modules/*/kernel/drivers/char/plex86.o
%else
/lib/modules/*/misc/plex86.o
%endif
%dir %{_libdir}/plex86
%dir %{_libdir}/plex86/guest
%dir %{_libdir}/plex86/guest/*
%attr(755,root,root)%{_libdir}/plex86/guest/cooperative/kernel
%attr(755,root,root)%{_libdir}/plex86/guest/paging/kernel
%attr(755,root,root)%{_libdir}/plex86/guest/preemptive/kernel
%attr(755,root,root)%{_libdir}/plex86/guest/test/kernel
%attr(755,root,root)%{_libdir}/plex86/guest/virtcode/virtcode
%dir %{_libdir}/plex86/plugins
%dir %{_libdir}/plex86/plugins/*
%attr(755,root,root)%{_libdir}/plex86/plugins/bochs/plugin-bochs.so
%attr(755,root,root)%{_libdir}/plex86/plugins/loader/load-kernel.so
%attr(755,root,root)%{_libdir}/plex86/plugins/misc/replay_io.so
%attr(755,root,root)%{_libdir}/plex86/plugins/write-cache/write-cache.so
#%attr(755,root,root)%{_libdir}/plex86/plugins/ice/plugin-ice.so
%dir %{_libdir}/plex86/misc
%{_libdir}/plex86/misc/mbrdata
%{_libdir}/plex86/misc/vga.pcf
%{_libdir}/plex86/misc/vga_io.log
%attr(755,root,root)%{_libdir}/plex86/misc/createdisk.sh
%{_libdir}/plex86/misc/createdisk.README
%attr(755,root,root)%{_libdir}/plex86/misc/load_module.sh
%attr(755,root,root)%{_libdir}/plex86/misc/unload_module.sh
%attr(755,root,root)%{_libdir}/plex86/misc/netbsd_post.sh
%dir %{_libdir}/plex86/bios
%{_libdir}/plex86/bios/*BIOS*
%{_libdir}/plex86/conf

%doc *.gz docs/{README*,html,misc,xml,txt}
