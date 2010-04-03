
%define plugin	mp3
%define name	vdr-plugin-%plugin
%define version	0.10.2
%define prever	0
%define rel	1
%if %prever
%define release	%mkrel 0.%prever.%rel
%else
%define release %mkrel %rel
%endif

Summary:	VDR plugin: A versatile audio player
Name:		%name
Version:	%version
Release:	%release
Group:		Video
License:	GPLv2+
URL:		http://www.muempf.de/
%if %prever
Source:		http://www.muempf.de/down/vdr-%plugin-%version%prever.tar.gz
%else
Source:		http://www.muempf.de/down/vdr-%plugin-%version.tar.gz
%endif
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	vdr-devel >= 1.6.0
BuildRequires:	libmad-devel libid3tag-devel libsndfile-devel libvorbis-devel
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
default=%_vdr_plugin_cachedir/mp3/id3
# search CDDB files in DIR
var=CDDB_DIR
param=--cddb=CDDB_DIR
default=%_vdr_plugin_cachedir/mp3/images/cddb
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
default=%_vdr_plugin_cachedir/mp3/images
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
rm -rf %{buildroot}
%vdr_plugin_install

install -d -m755 %buildroot%_vdr_plugin_cfgdir
for f in mp3sources.conf mplayersources.conf; do
cat > %buildroot%_vdr_plugin_cfgdir/$f <<EOF
# Please remove the line below when you add the correct configuration
/invalid/directory;Please configure;0
EOF
done

install -d -m755 %buildroot%_vdr_plugin_cachedir/mp3/images
install -d -m755 %buildroot%_vdr_plugin_cachedir/mp3/id3
install -d -m755 %buildroot%_vdr_plugin_cachedir/mp3/cddb

%clean
rm -rf %{buildroot}

%post
%vdr_plugin_post mp3

%postun
%vdr_plugin_postun mp3

%post -n vdr-plugin-mplayer
%vdr_plugin_post mplayer

%postun -n vdr-plugin-mplayer
%vdr_plugin_postun mplayer

%files -f mp3.vdr
%defattr(-,root,root)
%doc README COPYING HISTORY MANUAL examples
%config(noreplace) %_vdr_plugin_cfgdir/mp3sources.conf
%attr(-,vdr,vdr) %dir %_vdr_plugin_cachedir/mp3
%attr(-,vdr,vdr) %dir %_vdr_plugin_cachedir/mp3/images
%attr(-,vdr,vdr) %dir %_vdr_plugin_cachedir/mp3/id3
%attr(-,vdr,vdr) %dir %_vdr_plugin_cachedir/mp3/cddb

%files -n vdr-plugin-mplayer -f mplayer.vdr
%defattr(-,root,root)
%doc README COPYING HISTORY MANUAL examples
%config(noreplace) %_vdr_plugin_cfgdir/mplayersources.conf


