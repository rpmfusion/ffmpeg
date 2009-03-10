# TODO: add make test to %%check section

%define faad2min 1:2.6.1

Summary:        Digital VCR and streaming server
Name:           ffmpeg
Version:        0.5
Release:        1%{?dist}
License:        GPLv2+
Group:          Applications/Multimedia
URL:            http://ffmpeg.org/
Source0:        http://ffmpeg.org/releases/%{name}-%{version}.tar.bz2
# get rid of textrels on x86_64 in yasm code
Patch0:         %{name}-textrel.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%{?_with_amr:BuildRequires: amrnb-devel amrwb-devel}
BuildRequires:  bzip2-devel
BuildRequires:  faac-devel
BuildRequires:  faad2-devel >= %{faad2min}
BuildRequires:  gsm-devel
BuildRequires:  imlib2-devel
BuildRequires:  lame-devel
BuildRequires:  libdc1394-devel
BuildRequires:  libtheora-devel
BuildRequires:  libvorbis-devel
BuildRequires:  openjpeg-devel
BuildRequires:  schroedinger-devel
BuildRequires:  SDL-devel
BuildRequires:  speex-devel
BuildRequires:  texi2html
BuildRequires:  x264-devel >= 0.0.0-0.14.20080613
BuildRequires:  xvidcore-devel
BuildRequires:  zlib-devel
%ifarch %{ix86} x86_64
BuildRequires:  yasm
%endif

%description
FFMpeg is a complete and free Internet live audio and video
broadcasting solution for Linux/Unix. It also includes a digital
VCR. It can encode in real time in many formats including MPEG1 audio
and video, MPEG4, h263, ac3, asf, avi, real, mjpeg, and flash.

%package        libs
Summary:        Libraries for %{name}
Group:          System Environment/Libraries
Requires:       faad2-libs >= %{faad2min}
Obsoletes:      ffmpeg-libpostproc < 0.4.9-0.11
Obsoletes:      ffmpeg-compat < 0.4.9-0.49

%description    libs
FFMpeg is a complete and free Internet live audio and video
broadcasting solution for Linux/Unix. It also includes a digital
VCR. It can encode in real time in many formats including MPEG1 audio
and video, MPEG4, h263, ac3, asf, avi, real, mjpeg, and flash.
This package contains the libraries for %{name}

%package        devel
Summary:        Development package for %{name}
Group:          Development/Libraries
Requires:       %{name}-libs = %{version}-%{release}
Requires:       pkgconfig
Obsoletes:      ffmpeg-compat-devel < 0.4.9-0.49

%description    devel
FFMpeg is a complete and free Internet live audio and video
broadcasting solution for Linux/Unix. It also includes a digital
VCR. It can encode in real time in many formats including MPEG1 audio
and video, MPEG4, h263, ac3, asf, avi, real, mjpeg, and flash.
This package contains development files for %{name}

%define ff_configure \
../configure \\\
    --prefix=%{_prefix} \\\
    --bindir=%{_bindir} \\\
    --datadir=%{_datadir}/ffmpeg \\\
    --incdir=%{_includedir}/ffmpeg \\\
    --libdir=%{_libdir} \\\
    --mandir=%{_mandir} \\\
    --arch=%{_target_cpu} \\\
    --extra-cflags="$RPM_OPT_FLAGS -I%{_includedir}/openjpeg" \\\
    --extra-version=rpmfusion \\\
    %{?_with_amr:--enable-libamr-nb --enable-libamr-wb --enable-nonfree} \\\
    --enable-bzlib \\\
    --enable-libdc1394 \\\
    --enable-libfaac \\\
    --enable-libfaad \\\
    --enable-libgsm \\\
    --enable-libmp3lame \\\
    --enable-libopenjpeg \\\
    --enable-libschroedinger \\\
    --enable-libspeex \\\
    --enable-libtheora \\\
    --enable-libvorbis \\\
    --enable-libx264 \\\
    --enable-libxvid \\\
    --enable-x11grab \\\
    --enable-avfilter \\\
    --enable-avfilter-lavf \\\
    --enable-postproc \\\
    --enable-swscale \\\
    --enable-pthreads \\\
    --disable-static \\\
    --enable-shared \\\
    --enable-gpl \\\
    --disable-debug \\\
    --disable-stripping


%prep
%setup -q
%patch0 -p1 -b .textrel

%build
mkdir generic
pushd generic
%{ff_configure}\
    --shlibdir=%{_libdir} \
%ifarch %{ix86}
    --cpu=%{_target_cpu} \
    --disable-mmx2 \
    --disable-sse \
    --disable-ssse3 \
    --disable-yasm \
%endif
%ifarch ppc ppc64
    --disable-altivec \
%endif
%ifarch sparc sparc64
    --disable-vis \
%endif

make %{?_smp_mflags}
make documentation
popd

mkdir simd
pushd simd
%ifarch %{ix86}
%{ff_configure}\
    --shlibdir=%{_libdir}/i686 \
    --cpu=i686 \
    --disable-ffmpeg \
    --disable-ffserver \
    --disable-ffplay \

make %{?_smp_mflags}
%endif
%ifarch ppc
%{ff_configure}\
    --shlibdir=%{_libdir}/altivec \
    --cpu=g4 \
    --enable-altivec \
    --disable-ffmpeg \
    --disable-ffserver \
    --disable-ffplay \

make %{?_smp_mflags}
%endif
%ifarch ppc64
%{ff_configure}\
    --shlibdir=%{_libdir}/altivec \
    --cpu=g5 \
    --enable-altivec \
    --disable-ffmpeg \
    --disable-ffserver \
    --disable-ffplay \

make %{?_smp_mflags}
%endif
%ifarch sparc sparc64
%{ff_configure}\
    --shlibdir=%{_libdir}/v9 \
    --cpu=v9 \
    --enable-vis \
    --disable-ffmpeg \
    --disable-ffserver \
    --disable-ffplay \

make %{?_smp_mflags}
%endif
popd

%install
rm -rf $RPM_BUILD_ROOT
pushd generic
make install DESTDIR=$RPM_BUILD_ROOT
popd
pushd simd
%ifarch %{ix86} ppc ppc64 sparc sparc64
make install DESTDIR=$RPM_BUILD_ROOT
%endif
popd

%clean
rm -rf $RPM_BUILD_ROOT


%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING.GPL CREDITS Changelog README RELEASE doc/ffserver.conf
%{_bindir}/ffmpeg
%{_bindir}/ffplay
%{_bindir}/ffserver
%{_mandir}/man1/ffmpeg.1*
%{_mandir}/man1/ffplay.1*
%{_mandir}/man1/ffserver.1*
%{_datadir}/ffmpeg

%files libs
%defattr(-,root,root,-)
%{_libdir}/lib*.so.*
%{_libdir}/vhook/
%ifarch %{ix86}
%{_libdir}/i686/lib*.so.*
%{_libdir}/i686/vhook/
%endif
%ifarch ppc ppc64
%{_libdir}/altivec/lib*.so.*
%{_libdir}/altivec/vhook/
%endif
%ifarch sparc sparc64
%{_libdir}/v9/lib*.so.*
%{_libdir}/v9/vhook/
%endif

%files devel
%defattr(-,root,root,-)
%doc MAINTAINERS doc/APIchanges doc/TODO doc/*.txt
%{_includedir}/ffmpeg
%{_libdir}/pkgconfig/lib*.pc
%{_libdir}/lib*.so
%ifarch %{ix86}
%{_libdir}/i686/lib*.so
%endif
%ifarch ppc ppc64
%{_libdir}/altivec/lib*.so
%endif
%ifarch sparc sparc64
%{_libdir}/v9/lib*.so
%endif


%changelog
* Tue Mar 10 2009 Dominik Mierzejewski <rpm at greysector.net> - 0.5-1
- 0.5 release
- enable yasm on x86_64, fix resulting textrels
- add missing obsoletes for ffmpeg-compat-devel (really fix bug #173)
- disable yasm and certain asm optimizations for generic ix86 builds
- %%{_bindir} is now usable
- include more docs
- specfile cleanups
- add JPEG2000 decoding support via openjpeg

* Sat Jan 31 2009 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.58.20090131
- 20090131 snapshot

* Wed Dec 17 2008 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.57.20081217
- 20081217 snapshot
- fix pkgconfig files again (broken in 0.4.9-0.55.20081214)

* Mon Dec 15 2008 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.56.20081214
- drop libdirac support for now

* Sun Dec 14 2008 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.55.20081214
- 20081214 snapshot
- change the lib split on x86, it doesn't work right for P3/AthlonXP
- specfile cleanups
- enable bzlib, dirac and speex support via external libs
- sort BR list alphabetically
- drop upstream'd patch

* Thu Dec 11 2008 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.54.20081202
- fix pkgconfig file generation

* Thu Dec 04 2008 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.53.20081202
- 20081202 snapshot
- drop upstreamed/obsolete patches

* Thu Nov 20 2008 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.52.20080908
- add obsoletes for -compat package (RPMFusion bug #173)

* Sat Nov 01 2008 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.51.20080908
- reworked build system
- build optimized versions where it makes sense
- specfile cleanups
- enable yasm for optimized asm routines on x86_32
- add obsoletes for Freshrpms' libpostproc subpackage

* Thu Sep 18 2008 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.50.20080908
- 20080908 snapshot (r25261), last before ABI change

* Fri Sep 05 2008 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.49.20080905
- 20080905 snapshot
- fix build --with amr
- update snapshot.sh
- drop liba52 support, native ac3 decoder is better in every way

* Mon Aug 25 2008 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.48.20080825
- 20080825 snapshot
- use CFLAGS more similar to upstream
- enable X11 grabbing input
- enable libavfilter

* Sun Aug 03 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 0.4.9-0.47.20080614
- rebuild

* Sat Jun 14 2008 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.46.20080614
- 20080614 snapshot
- no need to conditionalize swscaler anymore
- dropped obsolete pkgconfig patch
- BR latest x264

* Mon Mar 03 2008 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.45.20080113
- rebuild for new x264

* Sun Jan 13 2008 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.44.20080113
- 20080113 snapshot
- drop unnecessary patch
- enable libdc1394 support
- enable swscaler

* Mon Nov 12 2007 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.43.20071111
- ensure that we use the correct faad2 version

* Sun Nov 11 2007 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.42.20071111
- 20071111 snapshot
- current faad2 is good again

* Thu Oct 18 2007 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.41.20071011
- fix BRs and Requires for faad2

* Thu Oct 11 2007 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.40.20071011
- 20071011 snapshot
- don't link against faad2-2.5, it makes GPL'd binary non-distributable
- go back to normal linking instead of dlopen() of liba52

* Sun Sep 23 2007 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.39.20070923
- 20070923 snapshot
- use faad2 2.5
- optional AMR support
- dropped obsolete patch

* Thu Jun 07 2007 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.38.20070607
- 20070607 snapshot
- libdca BR dropped (no longer supported)
- drop gsm.h path hack, gsm in Fedora now provides a compatibility symlink
- remove arch hacks, ffmpeg's configure is smart enough
- enable cmov on x86_64

* Thu May 03 2007 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.37.20070503
- require older faad2 to prevent bugreports like #1388
- prepare for libdc1394 support
- enable pthreads
- 20070503 snapshot

* Thu Feb 08 2007 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.35.20070204
- libswscale.pc is necessary regardless of --enable-swscaler

* Sun Feb  4 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.4.9-0.34.20070204
- 2007-02-04 snapshot, enable libtheora.
- Make swscaler optional, disabled again by default (#1379).

* Fri Jan 05 2007 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.34.20061214
- move vhooks to -libs

* Wed Jan 03 2007 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.33.20061214
- split -libs subpackage for multilib installs

* Tue Dec 26 2006 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.32.20061214
- new kino works with swscaler, re-enabled

* Tue Dec 19 2006 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.31.20061214
- disable swscaler, it breaks kino

* Sun Dec 17 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.4.9-0.30.20061214
- fix pkgconfig patch

* Sat Dec 16 2006 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.29.20061214
- liba52 change broke build on 64bit
- resurrect lost URL changes

* Fri Dec 15 2006 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.28.20061214
- fixed build on x86
- change liba52 file-based dependency to provides-based
- resurrect and update pkgconfig patch

* Thu Dec 14 2006 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.27.20061214
- new snapshot URL
- new URL

* Thu Dec 14 2006 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.26.20061214
- 2006-12-14 snapshot
- added libdca support
- enabled swscaler
- dropped obsolete patches

* Mon Oct 30 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.4.9-0.25.20061030
- 2006-10-30 snapshot, fixes x86_64 build.
- Apply a less intrusive workaround for LAME detection issues.

* Sat Oct 28 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.4.9-0.25.20061028
- 2006-10-28 snapshot, build with x264.
- Clean up some pre-FC4 compat build dependency cruft.
- Quick and dirty workarounds for ./configure's libmp3lame test and asm
  register issues on ix86.

* Fri Oct 06 2006 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 0.4.9-25
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 26 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.4.9-0.24.20060817
- Drop SELinux fcontext settings, they're supposedly fixed upstream again.

* Thu Aug 17 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.4.9-0.23.20060817
- 2006-08-17 snapshot.
- Fix svn rev in "ffmpeg -version" etc.

* Wed Aug  9 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.4.9-0.23.20060804
- Reintroduce SELinux fcontext settings on ix86 (not needed on x86_64, ppc),
  they're not completely taken care of upstream (#1120).
- Split svn snapshot creator into a separate script.

* Fri Aug  4 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.4.9-0.22.20060804
- 2006-08-04 snapshot.
- Drop bogus version from SDL-devel build dependency.
- Drop no longer relevant libpostproc obsoletion.
- Prune pre-2005 changelog entries.
- Specfile cleanup.

* Sat Jun 17 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.4.9-0.22.20060617
- 2006-06-17 snapshot.

* Mon Jun 12 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.4.9-0.22.20060612
- 2006-06-12 snapshot, rgb.txt patch applied upstream.
- Patch to force linking vhook modules with their dependencies, --as-needed
  seems to drop needed things for some reason for drawtext and imlib2.
- Revert to dlopen()'ing liba52 and add file based dependency on it, it's
  easier this way again due to --as-needed linkage.

* Wed May 17 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.4.9-0.22.20060517
- 2006-05-17 snapshot.
- Link with faad2, don't dlopen() it.

* Sat May 13 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.4.9-0.22.20060513
- 2006-05-13 snapshot.
- Drop SELinux fixups, they're part of upstream policy now.

* Sat Apr 15 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.4.9-0.22.20060407
- SELinux file context fixups (mplayer, vdr-dxr3 etc) while waiting for #188358

* Sat Apr  8 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.4.9-0.21.20060407
- 2006-04-07 CVS snapshot.
- Move *.so to -devel, hopefully nothing needs them any more.

* Fri Mar 31 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.4.9-0.21.20051228
- Remove superfluous dependencies from pkgconfig files (#747).
- Re-enable MMX on x86_64.

* Thu Mar 09 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- switch to new release field

* Tue Feb 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- add dist

* Wed Dec 28 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.4.9-0.lvn.0.20.20051228
- 2005-12-28 CVS snapshot.
- Let upstream configure take care of PIC settings (patched for ppc).
- Own shared lib symlinks.

* Fri Dec 23 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.4.9-0.lvn.0.20.20050801
- Apply upstream fix for CVE-2005-4048.
- Patch to find rgb.txt in FC5 too.

* Thu Sep 29 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:0.4.9-0.lvn.0.19.20050801
- Clean up obsolete pre-FC3 stuff (FAAC is now unconditionally enabled).
- Drop zero Epochs.

* Tue Aug 16 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:0.4.9-0.lvn.0.18.20050801
- Apply some upstream and some mine (libdir) fixes to pkgconfig files.
- Add pkgconfig dependency to -devel.
- Include gsm support.

* Thu Aug 4 2005 David Woodhouse <dwmw2@infradead.org> - 0:0.4.9-0.lvn.0.17.20050801
- Update to 20050801 snapshot to make xine-lib happy
- Enable Altivec support by using --cpu=powerpc (not 'ppc')
- Enable theora
- Add pkgconfig files
- Undefine various things which might be macros before redefining them

* Sat Jul 23 2005 Dams <anvil[AT]livna.org> - 0:0.4.9-0.lvn.0.17.20050427
- Added patch from Marc Deslauriers to fix wmv2 distorsion

* Sun Jul 10 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:0.4.9-0.lvn.0.16.20050427
- Enable faac by default, rebuild with "--without faac" to disable.
- Clean up obsolete pre-FC2 and other stuff.

* Sun May 22 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:0.4.9-0.lvn.0.15.20050427
- PPC needs -fPIC too.

* Sat May 21 2005 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 0:0.4.9-0.lvn.0.14.20050427
- disable mmx for now on x86_64 to fix build

* Sat Apr 30 2005 Dams <anvil[AT]livna.org> - 0:0.4.9-0.lvn.0.13.20050427
- Removed bogus devel requires
- Re-added conditionnal a52dec buildreq

* Fri Apr 29 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:0.4.9-0.lvn.0.12.20050427
- Link avcodec with a52 when building with a52bin, remove unnecessary
  hardcoded liba52.so.0 dependency.

* Fri Apr 29 2005 Dams <anvil[AT]livna.org> - 0:0.4.9-0.lvn.0.11.20050427
- Fixed devel package deps

* Fri Apr 29 2005 Dams <anvil[AT]livna.org> - 0:0.4.9-0.lvn.0.10.20050427
- texi2html replaces tetex as build dependency (FC4 compliance)
- re-added man pages

* Thu Apr 28 2005 Dams <anvil[AT]livna.org> - 0:0.4.9-0.lvn.0.9.20050427
- Patch from Enrico to fix build on gcc4
- Missing BuildReq a52dec-devel when a52bin is defined
- Patch to fix a52 build

* Wed Apr 27 2005 Dams <anvil[AT]livna.org> - 0:0.4.9-0.lvn.0.8.20050427
- Updated tarball to cvs 20050427 snapshot
- Enabled libogg, xvid, a52bin
- Dropped Patch[0-3]
