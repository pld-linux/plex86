
%define		__year		2001
%define		__date		0302
%define		__time		1106

Name: 		plex86
Version: 	%{__year}_%{__date}_%{__time}
Release: 	1
Summary: 	x86 CPU emulator
Summary(pl): 	x86 CPU emulator
Group: 		Applications/Emulators
Group(pl):	Aplikacje/Emulatory
License: 	LGPL
ExclusiveArch: 	i586 i686 i786 K5 K6 K7
Source: 	ftp://ftp.plex86.org/pub/%{name}-%{__year}-%{__date}-%{__time}.tar.gz
Patch0:		plex86.patch
BuildRequires:	libstdc++-devel
PreReq:		XFree86
Requires:	ncurses
BuildRoot: 	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_fontdir	/usr/share/fonts
%define		_kernel_ver	%(grep UTS_RELEASE /usr/src/linux/include/linux/version.h 2>/dev/null | cut -d'"' -f2)

%description
Plex86 is an Open Source x86 PC virtualization program which let's you
concurrently run multiple x86 operating systems and corresponding
software on your x86 machine. 

%description -l pl
Plex86 pozwala na uruchamianie wielu systemów operacyjnych na jednym komputerze
PC. Wykorzystywana jest tutaj metoda nazwana wirtualizacj±, ktora pozwala na 
dzielenie poszczególnych zasobów komputera miêdzy pracuj±ce systemy.

%prep
rm -rf $RPM_BUILD_ROOT
%setup -q -n %{name}
patch -s -p1 < %{PATCH0}

%build
CXXFLAGS="$RPM_OPT_FLAGS -I/usr/include/ncurses"
%configure --with-Linux --with-gui=curses

%{__make}

%install
# create necessary directories
install -d  $RPM_BUILD_ROOT%{_bindir} \
    $RPM_BUILD_ROOT%{_libdir}/plex86 \
    $RPM_BUILD_ROOT%{_libdir}/plex86/{bios,conf,guest,misc,plugins} \
    $RPM_BUILD_ROOT%{_libdir}/plex86/guest/{cooperative,paging,preemptive,test,virtcode} \
    $RPM_BUILD_ROOT%{_libdir}/plex86/plugins/{bochs,ice,loader,misc,write-cache} \
    $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc \
    $RPM_BUILD_ROOT%{_fontdir}/misc
    
# install the stuff
install kernel/plex86.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc
install user/plex86 $RPM_BUILD_ROOT%{_bindir}
install user/resetmod $RPM_BUILD_ROOT%{_bindir}
install bios/*BIOS* $RPM_BUILD_ROOT%{_libdir}/plex86/bios
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
gzip -9 misc/vga.pcf
cp -f misc/vga.pcf.gz $RPM_BUILD_ROOT%{_fontdir}/misc

%post
mkfontdir %{_fontdir}/misc
if [ ! -e /dev/plex86 ]; then
    mknod /dev/plex86 c 254 0
    chmod a+rw /dev/plex86
fi
/sbin/depmod -a

%postun
rm -f /dev/plex86
rm -f  %{_fontdir}/misc/vga.pcf.gz
mkfontdir %{_fontdir}/misc
/sbin/depmod -a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root)%{_bindir}/plex86
%attr(755,root,root)%{_bindir}/resetmod
%attr(600,root,root)/lib/modules/*/misc/plex86.o
%attr(755,root,root)%{_libdir}/plex86/guest/cooperative/kernel
%attr(755,root,root)%{_libdir}/plex86/guest/paging/kernel
%attr(755,root,root)%{_libdir}/plex86/guest/preemptive/kernel
%attr(755,root,root)%{_libdir}/plex86/guest/test/kernel
%attr(755,root,root)%{_libdir}/plex86/guest/virtcode/virtcode
%attr(755,root,root)%{_libdir}/plex86/plugins/bochs/plugin-bochs.so
%attr(755,root,root)%{_libdir}/plex86/plugins/loader/load-kernel.so
%attr(755,root,root)%{_libdir}/plex86/plugins/misc/replay_io.so
%attr(755,root,root)%{_libdir}/plex86/plugins/write-cache/write-cache.so
#%attr(755,root,root)%{_libdir}/plex86/plugins/ice/plugin-ice.so
%{_libdir}/plex86/misc/mbrdata
%{_libdir}/plex86/misc/vga.pcf
%{_libdir}/plex86/misc/vga_io.log
%attr(755,root,root)%{_libdir}/plex86/misc/createdisk.sh
%{_libdir}/plex86/misc/createdisk.README
%attr(755,root,root)%{_libdir}/plex86/misc/load_module.sh
%attr(755,root,root)%{_libdir}/plex86/misc/unload_module.sh
%attr(755,root,root)%{_libdir}/plex86/misc/netbsd_post.sh
%{_libdir}/plex86/bios/*BIOS*
%{_libdir}/plex86/conf/*

%doc README COPYING ChangeLog docs/{README,html,misc,sgml,xml,txt} README.DOS PERFORMANCE SBE-OFF-CONDITIONS TODO
