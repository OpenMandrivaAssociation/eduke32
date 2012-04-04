License:	GPLv2
Name:		eduke32
Version:	2.0.3svn20120331
Release:	%mkrel 1
Group:		Games/Arcade
URL:	http://www.eduke32.com/
Source0:	%{name}-%{version}.tar.bz2
Source1:	%{name}_32x32.png
Source2:	%{name}_48x48.png
Source3:	%{name}_64x64.png
Source4:	%{name}_128x128.png
Source5:	%{name}.desktop
Source6:	%{name}-demo-install.sh
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
Summary:	Source port of Duke Nukem 3D
Requires:	eduke32_engine = %{version}-%{release}

BuildRequires:	SDL-devel SDL_mixer-devel nasm gcc-c++
BuildRequires:  libvorbis-devel gtk2-devel libstdc++
BuildRequires:  libstdc++-static-devel libvpx-devel


%description
EDuke32 is a source port of the classic PC first person shooter Duke Nukem 3D - Duke3D for short 
to Windows, Linux and OS X, which adds a ton of awesome features and 
upgrades for regular players and an arsenal of editing functions and
scripting extensions for mod authors and map makers.

This game is non-free because it requires non-free data to function.
%package gui
Group:		Games/Arcade
Summary:	Eduke32 GUI game
Requires:	update-alternatives
Provides:	eduke32 = %{version}-%{release}, eduke32_engine = %{version}-%{release}

%description gui
Eduke32 package with nice simple GTK loader

%package console
Group:		Games/Arcade
Summary:	Eduke32 Console game
Requires:	update-alternatives
Provides:	eduke32 = %{version}-%{release}, eduke32_engine = %{version}-%{release}

%description console
Classic console Eduke32 without GUI launcher

%package mapeditor
Group:		Games/Arcade
Summary:	Eduke32 map editor
Requires:	update-alternatives

%description mapeditor
Eduke32 maps editor based on BUILD engine

%package utils
Group:          Games/Arcade
Summary:        Eduke32 build tools
Requires:	SDL

%description utils
Eduke32 build tools

%prep
%setup -q
cp %{S:1} .
cp %{S:2} .
cp %{S:3} .
cp %{S:4} .
cp %{S:5} .
cp %{S:6} .

%build
make veryclean
make HAVE_GTK2=1 RELEASE=1 %{?jobs:-j%jobs}
mv %{name} %{name}-gui
mv mapster32 mapster32-gui
make veryclean
make HAVE_GTK2=0 RELEASE=1
mv %{name} %{name}-console
mv mapster32 mapster32-console
touch %{name}
touch mapster32
cd build
make veryclean
make utils
cd ..

%install 
rm -rf %{buildroot}
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
install -Dm 0644 SEHELP.HLP %{buildroot}%{_gamesdatadir}/%{name}/sehelp.hlp
install -Dm 0644 STHELP.HLP %{buildroot}%{_gamesdatadir}/%{name}/sthelp.hlp
install -Dm 0644 m32help.hlp %{buildroot}%{_gamesdatadir}/%{name}/m32help.hlp
# install -Dm 0644 tiles.cfg %{buildroot}%{_gamesdatadir}/%{name}/tiles.cfg
install -Dm 0644 %{name}_32x32.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
install -Dm 0644 %{name}_48x48.png %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
install -Dm 0644 %{name}_64x64.png %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/%{name}.png
install -Dm 0644 %{name}_128x128.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{name}.png
# utils
install -Dm 0755 build/kextract %{buildroot}%{_bindir}/kextract
install -Dm 0755 build/kgroup %{buildroot}%{_bindir}/kgroup
install -Dm 0755 build/transpal %{buildroot}%{_bindir}/transpal
install -Dm 0755 build/wad2art %{buildroot}%{_bindir}/wad2art
install -Dm 0755 build/wad2map %{buildroot}%{_bindir}/wad2map

mkdir %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}-gui.desktop << EOF
[Desktop Entry]
Name=Duke Nukem 3D GUI
Comment=Eduke32 GUI game
Exec=%{_gamesbindir}/%{name}-gui
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=Game;ArcadeGame;X-MandrivaLinux-MoreApplications-Games-Arcade;
EOF

cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}-console.desktop << EOF
[Desktop Entry]
Name=Duke Nukem 3D Console
Comment=Eduke32 Console game
Exec=%{_gamesbindir}/%{name}-console
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=Game;ArcadeGame;X-MandrivaLinux-MoreApplications-Games-Arcade;
EOF


%post gui
update-alternatives --install %{_gamesbindir}/%{name} %{name} %{_gamesbindir}/%{name}-gui 11

%post console
update-alternatives --install %{_gamesbindir}/%{name} %{name} %{_gamesbindir}/%{name}-console 11

%post mapeditor
update-alternatives --install %{_gamesbindir}/mapster32 mapster32 %{_gamesbindir}/mapster32-console 11
update-alternatives --install %{_gamesbindir}/mapster32 mapster32 %{_gamesbindir}/mapster32-gui 12


%preun console
if [ "$1" = 0 ] ; then
	update-alternatives --remove %{name} %{_gamesbindir}/%{name}-console
fi

%preun mapeditor
if [ "$1" = 0 ] ; then
	update-alternatives --remove mapster32 %{_gamesbindir}/mapster32-console
	update-alternatives --remove mapster32 %{_gamesbindir}/mapster32-gui
fi

%preun gui
if [ "$1" = 0 ] ; then
	update-alternatives --remove %{name} %{_gamesbindir}/%{name}-gui
fi


%files
%defattr(-,root,root,-)
%{_gamesbindir}/%{name}-demo-install
%dir %{_gamesdatadir}/%{name}/
%{_gamesdatadir}/%{name}/m32help.hlp
%{_gamesdatadir}/%{name}/sehelp.hlp
%{_gamesdatadir}/%{name}/sthelp.hlp
# %{_gamesdatadir}/%{name}/tiles.cfg
%doc ChangeLog.html ChangeLog buildlic.txt
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
%{_datadir}/icons/hicolor/64x64/apps/%{name}.png
%{_datadir}/icons/hicolor/128x128/apps/%{name}.png

%files console
%defattr(-,root,root,-)
%ghost %{_gamesbindir}/%{name}
%attr(-,root,root) %{_gamesbindir}/%{name}-console
%{_datadir}/applications/mandriva-%{name}-console.desktop

%files gui
%defattr(-,root,root,-)
%ghost %{_gamesbindir}/%{name}
%attr(-,root,root) %{_gamesbindir}/%{name}-gui
%{_datadir}/applications/mandriva-%{name}-gui.desktop

# both versions of editor are packed but only GUI one is preffered but can be changed
# with use of update-alternatives
%files mapeditor
%defattr(-,root,root,-)
%ghost %{_gamesbindir}/mapster32
%attr(-,root,root) %{_gamesbindir}/mapster32-gui
%attr(-,root,root) %{_gamesbindir}/mapster32-console

%files utils
%defattr(-,root,root,-)
%{_bindir}/kextract
%{_bindir}/kgroup
%{_bindir}/transpal
%{_bindir}/wad2art
%{_bindir}/wad2map

%clean
rm -rf %{buildroot}
