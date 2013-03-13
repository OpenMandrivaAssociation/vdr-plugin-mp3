%define plugin	mp3
%define prever	0
%define rel	3
%if %prever
%define release	%mkrel 0.%prever.%rel
%else
%define release %mkrel %rel
%endif

Summary:	VDR plugin: A versatile audio player
Name:		vdr-plugin-%plugin
Version:	0.10.2
Release:	%release
Group:		Video
License:	GPLv2+
URL:		http://www.muempf.de/
%if %prever
Source:		http://www.muempf.de/down/vdr-%plugin-%version%prever.tar.gz
%else
Source:		http://www.muempf.de/down/vdr-%plugin-%version.tar.gz
%endif
BuildRequires:	vdr-devel >= 1.6.0
BuildRequires:	libmad-devel libid3tag-devel sndfile-devel libvorbis-devel
Requires:	vdr-abi = %vdr_abi

%description
The "MP3-Plugin" allows playback of MP3 and other audio files.

%package -n vdr-plugin-mplayer
Summary:	VDR plugin: Media replay via MPlayer
Group:		Video
Requires:	vdr-abi = %vdr_abi
Requires:	mplayer

%description -n vdr-plugin-mplayer
The "MPlayer-Plugin" is used to call MPlayer for playback of video
files.

%prep
%if %prever
%setup -q -n %plugin-%version%prever
%else
%setup -q -n %plugin-%version
%endif
chmod +x examples/*.sh.*
%vdr_plugin_prep

%vdr_plugin_params_begin mp3
# use CMD to mount/unmount/eject mp3 sources
var=MOUNT_CMD
param=--mount=MOUNT_CMD
# execute CMD before & after network access
var=NETWORK_CMD
param=--network=NETWORK_CMD
# store ID3 cache file in DIR
var=CACHE_DIR
param=--cache=CACHE_DIR
default=%vdr_plugin_cachedir/mp3/id3
# search CDDB files in DIR
var=CDDB_DIR
param=--cddb=CDDB_DIR
default=%vdr_plugin_cachedir/mp3/images/cddb
# device for OSS output
var=OSS_DEV
param=--dsp=OSS_DEV
# use CMD to convert background images
var=IMAGE_CMD
param=--iconv=IMAGE_CMD
# use IMG as default background image
var=IMAGE_IMG
param=--defimage=IMAGE_IMG
# cache converted images in DIR
var=IMAGE_DIR
param=--icache=IMAGE_DIR
default=%vdr_plugin_cachedir/mp3/images
# search sources config in SUB subdirectory
var=SOURCES_SUBDIR
param=--sources=SOURCES_SUBDIR
%vdr_plugin_params_end

%vdr_plugin_params_begin mplayer
# use CMD to mount/unmount/eject mplayer sources
var=MOUNT_CMD
param=--mount=MOUNT_CMD
# use CMD when calling MPlayer
var=MPLAYER_CMD
param=--mplayer=MPLAYER_CMD
# search sources config in SUB subdirectory
var=SOURCES_SUBDIR
param=--sources=SOURCES_SUBDIR
# store global resume file in DIR
var=RESUME_DIR
param=--resume=RESUME_DIR
%vdr_plugin_params_end

%build
%vdr_plugin_build

%install
%vdr_plugin_install

install -d -m755 %buildroot%vdr_plugin_cfgdir
for f in mp3sources.conf mplayersources.conf; do
cat > %buildroot%vdr_plugin_cfgdir/$f <<EOF
# Please remove the line below when you add the correct configuration
/invalid/directory;Please configure;0
EOF
done

install -d -m755 %buildroot%vdr_plugin_cachedir/mp3/images
install -d -m755 %buildroot%vdr_plugin_cachedir/mp3/id3
install -d -m755 %buildroot%vdr_plugin_cachedir/mp3/cddb

%files -f mp3.vdr
%defattr(-,root,root)
%doc README COPYING HISTORY MANUAL examples
%config(noreplace) %vdr_plugin_cfgdir/mp3sources.conf
%attr(-,vdr,vdr) %dir %vdr_plugin_cachedir/mp3
%attr(-,vdr,vdr) %dir %vdr_plugin_cachedir/mp3/images
%attr(-,vdr,vdr) %dir %vdr_plugin_cachedir/mp3/id3
%attr(-,vdr,vdr) %dir %vdr_plugin_cachedir/mp3/cddb

%files -n vdr-plugin-mplayer -f mplayer.vdr
%defattr(-,root,root)
%doc README COPYING HISTORY MANUAL examples
%config(noreplace) %vdr_plugin_cfgdir/mplayersources.conf


%changelog
* Sat Apr 03 2010 Anssi Hannula <anssi@mandriva.org> 0.10.2-1mdv2010.1
+ Revision: 530857
- new version
- drop gcc4.4.patch, fixed upstream

* Tue Jul 28 2009 Anssi Hannula <anssi@mandriva.org> 0.10.1-7mdv2010.0
+ Revision: 401088
- rebuild for new VDR
- fix build with gcc4.4 (const-char-gcc4.4.patch)

* Fri Mar 20 2009 Anssi Hannula <anssi@mandriva.org> 0.10.1-6mdv2009.1
+ Revision: 359339
- rebuild for new vdr

* Mon Apr 28 2008 Anssi Hannula <anssi@mandriva.org> 0.10.1-5mdv2009.0
+ Revision: 197951
- rebuild for new vdr

* Sat Apr 26 2008 Anssi Hannula <anssi@mandriva.org> 0.10.1-4mdv2009.0
+ Revision: 197693
- new version
- add vdr_plugin_prep
- bump buildrequires on vdr-devel
- re-enable gettext i18n

* Fri Jan 04 2008 Anssi Hannula <anssi@mandriva.org> 0.10.1-3mdv2008.1
+ Revision: 145137
- rebuild for new vdr

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Mon Oct 29 2007 Anssi Hannula <anssi@mandriva.org> 0.10.1-2mdv2008.1
+ Revision: 103160
- rebuild for new vdr

* Fri Sep 07 2007 Anssi Hannula <anssi@mandriva.org> 0.10.1-1mdv2008.0
+ Revision: 81782
- 0.10.1
- skip 1.5 i18n detection on build

* Thu Jul 19 2007 Anssi Hannula <anssi@mandriva.org> 0.10.0-1mdv2008.0
+ Revision: 53411
- 0.10.0
- drop mp3-closefd2.patch, applied upstream

* Sun Jul 08 2007 Anssi Hannula <anssi@mandriva.org> 0.9.15-6mdv2008.0
+ Revision: 50019
- rebuild for new vdr

* Thu Jun 21 2007 Anssi Hannula <anssi@mandriva.org> 0.9.15-5mdv2008.0
+ Revision: 42105
- rebuild for new vdr

* Sun Jun 10 2007 Anssi Hannula <anssi@mandriva.org> 0.9.15-4mdv2008.0
+ Revision: 37967
- close file descriptors when forking mplayer (patch0)

* Sat May 05 2007 Anssi Hannula <anssi@mandriva.org> 0.9.15-3mdv2008.0
+ Revision: 22757
- rebuild for new vdr


* Tue Dec 05 2006 Anssi Hannula <anssi@mandriva.org> 0.9.15-2mdv2007.0
+ Revision: 90943
- rebuild for new vdr

* Fri Nov 03 2006 Anssi Hannula <anssi@mandriva.org> 0.9.15-1mdv2007.1
+ Revision: 76326
- 0.9.15 final

* Tue Oct 31 2006 Anssi Hannula <anssi@mandriva.org> 0.9.15-0.pre14.5mdv2007.1
+ Revision: 74049
- rebuild for new vdr
- Import vdr-plugin-mp3

* Thu Sep 07 2006 Anssi Hannula <anssi@mandriva.org> 0.9.15-0.pre14.4mdv2007.0
- rebuild for new vdr

* Thu Aug 24 2006 Anssi Hannula <anssi@mandriva.org> 0.9.15-0.pre14.3mdv2007.0
- stricter abi requires

* Mon Aug 07 2006 Anssi Hannula <anssi@mandriva.org> 0.9.15-0.pre14.2mdv2007.0
- rebuild for new vdr

* Tue Aug 01 2006 Anssi Hannula <anssi@mandriva.org> 0.9.15-0.pre14.1mdv2007.0
- 0.9.15pre14

* Wed Jul 26 2006 Anssi Hannula <anssi@mandriva.org> 0.9.15-0.pre10.4mdv2007.0
- rebuild for new vdr

* Tue Jun 20 2006 Anssi Hannula <anssi@mandriva.org> 0.9.15-0.pre10.3mdv2007.0
- use _ prefix for system path macros

* Mon Jun 05 2006 Anssi Hannula <anssi@mandriva.org> 0.9.15-0.pre10.2mdv2007.0
- rebuild for new vdr

* Fri Jun 02 2006 Anssi Hannula <anssi@mandriva.org> 0.9.15-0.pre10.1mdv2007.0
- initial Mandriva release

