%define svndate 20220119
%define sversion 9949
%define debug_package %{nil}

Summary:	Source port of Duke Nukem 3D
Name:		eduke32
Version:	2.0.4svn%{svndate}
Release:	1
License:	GPLv2+
Group:		Games/Arcade
Url:		http://www.eduke32.com/
Source0:	https://dukeworld.com/eduke32/synthesis/latest/eduke32_src_%{svndate}-%{sversion}-cba220b0d.tar.xz
Source1:	%{name}_32x32.png
Source2:	%{name}_48x48.png
Source3:	%{name}_64x64.png
Source4:	%{name}_128x128.png
Source5:	%{name}.desktop
Source6:	%{name}-demo-install.sh
#Patch0:		eduke32-libpng16.patch
BuildRequires:	nasm
BuildRequires:	libstdc++-static-devel
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(flac)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(sdl2)
BuildRequires:	pkgconfig(SDL2_mixer)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	pkgconfig(vpx)
BuildRequires:	pkgconfig(xrender)
Requires:	eduke32_engine = %{EVRD}

%description
EDuke32 is a source port of the classic PC first person shooter Duke Nukem 3D.

This game is non-free because it requires non-free data to function.

%files
%doc ChangeLog.html ChangeLog build/buildlic.txt
%{_gamesbindir}/%{name}-demo-install
%dir %{_gamesdatadir}/%{name}/
%{_gamesdatadir}/%{name}/m32help.hlp
%{_gamesdatadir}/%{name}/sehelp.hlp
%{_gamesdatadir}/%{name}/sthelp.hlp
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
%{_datadir}/icons/hicolor/64x64/apps/%{name}.png
%{_datadir}/icons/hicolor/128x128/apps/%{name}.png


#----------------------------------------------------------------------------

%package gui
Summary:	Eduke32 GUI game
Group:		Games/Arcade
Requires:	update-alternatives
Provides:	eduke32 = %{EVRD}
Provides:	eduke32_engine = %{EVRD}

%description gui
Eduke32 package with nice simple GTK loader.

%files gui
%ghost %{_gamesbindir}/%{name}
%{_gamesbindir}/%{name}-gui
%{_datadir}/applications/%{name}-gui.desktop

%preun gui
if [ "$1" = 0 ] ; then
	update-alternatives --remove %{name} %{_gamesbindir}/%{name}-gui
fi

%post gui
update-alternatives --install %{_gamesbindir}/%{name} %{name} %{_gamesbindir}/%{name}-gui 11

#----------------------------------------------------------------------------

%package console
Summary:	Eduke32 Console game
Group:		Games/Arcade
Requires:	update-alternatives
Provides:	eduke32 = %{EVRD}
Provides:	eduke32_engine = %{EVRD}

%description console
Classic console Eduke32 without GUI launcher.

%files console
%{_gamesbindir}/%{name}-console
%{_datadir}/applications/%{name}-console.desktop

%preun console
if [ "$1" = 0 ] ; then
	update-alternatives --remove %{name} %{_gamesbindir}/%{name}-console
fi

%post console
update-alternatives --install %{_gamesbindir}/%{name} %{name} %{_gamesbindir}/%{name}-console 11

#----------------------------------------------------------------------------

%package mapeditor
Summary:	Eduke32 map editor
Group:		Games/Arcade
Requires:	update-alternatives

%description mapeditor
Eduke32 maps editor based on BUILD engine.

# both versions of editor are packed but only GUI one is preffered but can be changed
# with use of update-alternatives
%files mapeditor
%ghost %{_gamesbindir}/mapster32
%{_gamesbindir}/mapster32-gui
%{_gamesbindir}/mapster32-console

%preun mapeditor
if [ "$1" = 0 ] ; then
	update-alternatives --remove mapster32 %{_gamesbindir}/mapster32-console
	update-alternatives --remove mapster32 %{_gamesbindir}/mapster32-gui
fi

%post mapeditor
update-alternatives --install %{_gamesbindir}/mapster32 mapster32 %{_gamesbindir}/mapster32-console 11
update-alternatives --install %{_gamesbindir}/mapster32 mapster32 %{_gamesbindir}/mapster32-gui 12

#----------------------------------------------------------------------------

%package utils
Summary:	Eduke32 build tools
Group:		Games/Arcade

%description utils
Eduke32 build tools.

%files utils
%{_bindir}/kextract
%{_bindir}/kgroup
%{_bindir}/transpal
%{_bindir}/wad2art
%{_bindir}/wad2map

#----------------------------------------------------------------------------

%prep
%setup -q -n %{name}_%{svndate}-%{sversion}-cba220b0d
cp %{SOURCE1} .
cp %{SOURCE2} .
cp %{SOURCE3} .
cp %{SOURCE4} .
cp %{SOURCE5} .
cp %{SOURCE6} .

%build
make veryclean
%make \
	SDL_TARGET=2 \
	HAVE_GTK2=1 \
	RELEASE=1 \
	BASECFLAGS="%{optflags}" \
	BASEASFLAGS="" \
	BASELDFLAGS="%{ldflags}"
mv %{name} %{name}-gui
mv mapster32 mapster32-gui
make veryclean

make \
	SDL_TARGET=2 \
	WITHOUT_GTK=1 \
	RELEASE=1 \
	BASECFLAGS="%{optflags}" \
	BASEASFLAGS="" \
	BASELDFLAGS="%{ldflags}"
mv %{name} %{name}-console
mv mapster32 mapster32-console

make veryclean
make utils \
	SDL_TARGET=2 \
	RELEASE=1 \
	BASECFLAGS="%{optflags}" \
	BASEASFLAGS="" \
	BASELDFLAGS="%{ldflags}"

touch %{name}
touch mapster32

%install
# ghost version of files...
install -Dm 0755 %{name} %{buildroot}%{_gamesbindir}/%{name}
install -Dm 0755 mapster32 %{buildroot}%{_gamesbindir}/mapster32
# shareware demo installer script
install -Dm 0755 %{name}-demo-install.sh %{buildroot}%{_gamesbindir}/%{name}-demo-install
# gui versions of game engine
install -Dm 0755 %{name}-gui %{buildroot}%{_gamesbindir}/%{name}-gui
install -Dm 0755 mapster32-gui %{buildroot}%{_gamesbindir}/mapster32-gui
# console versions of game engine
install -Dm 0755 mapster32-console %{buildroot}%{_gamesbindir}/mapster32-console
install -Dm 0755 %{name}-console %{buildroot}%{_gamesbindir}/%{name}-console
# data files and help files for editor
install -Dm 0644 package/sdk/SEHELP.HLP %{buildroot}%{_gamesdatadir}/%{name}/sehelp.hlp
install -Dm 0644 package/sdk/STHELP.HLP %{buildroot}%{_gamesdatadir}/%{name}/sthelp.hlp
install -Dm 0644 package/sdk/m32help.hlp %{buildroot}%{_gamesdatadir}/%{name}/m32help.hlp

install -Dm 0644 %{name}_32x32.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
install -Dm 0644 %{name}_48x48.png %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
install -Dm 0644 %{name}_64x64.png %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/%{name}.png
install -Dm 0644 %{name}_128x128.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{name}.png

# utils
install -Dm 0755 kextract %{buildroot}%{_bindir}/kextract
install -Dm 0755 kgroup %{buildroot}%{_bindir}/kgroup
install -Dm 0755 transpal %{buildroot}%{_bindir}/transpal
install -Dm 0755 wad2art %{buildroot}%{_bindir}/wad2art
install -Dm 0755 wad2map %{buildroot}%{_bindir}/wad2map

mkdir %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}-gui.desktop << EOF
[Desktop Entry]
Name=Duke Nukem 3D GUI
Comment=Eduke32 GUI game
Exec=%{_gamesbindir}/%{name}-gui
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=Game;ArcadeGame;
EOF

cat > %{buildroot}%{_datadir}/applications/%{name}-console.desktop << EOF
[Desktop Entry]
Name=Duke Nukem 3D Console
Comment=Eduke32 Console game
Exec=%{_gamesbindir}/%{name}-console
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=Game;ArcadeGame;
EOF

