%define Werror_cflags %nil
%define	Summary	This is the port of Descent 2 Version 1.2, the famous 3D game for PC

Summary:	%{Summary}
Name:		d2x-xl
Version:	1.15.63
Release:	%mkrel 1
Source0:	http://www.descent2.de/resources/%{name}-%{version}.tar.bz2
Patch2:		d2x-xl-ogl.patch
URL:		http://www.descent2.de/
Group:		Games/Arcade
License:	GPL
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	automake SDL-devel dos2unix desktop-file-utils ImageMagick
BuildRequires:	SDL_mixer-devel	GL-devel
Requires:	TiMidity++

%description
This is the port of Descent 2 Version 1.2, the famous 3D game for PC.

D2X is based on source code that was released the 14 December 1999 by
Parallax Software Corporation.

To use this package you'll need the datafiles from the Retail version
of Descent 2 Version 1.2 installed in %{_gamesdatadir}/%{name}

%prep 
%setup -q
dos2unix -b -U * 

%build
aclocal
autoheader
autoconf
automake --add-missing
chmod +x configure
chmod +x config.sub
chmod +x missing
%configure --bindir=%{_gamesbindir} --enable-release --with-opengl
%make 

%install
rm -rf %{buildroot}
%makeinstall_std

install -d %{buildroot}%{_gamesdatadir}/%{name}

install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=D2X-XL
Comment=%{Summary}
Exec=%{_gamesbindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=Game;ArcadeGame;X-MandrivaLinux-MoreApplications-Games-Arcade;
EOF

# install -d %{buildroot}{%{_iconsdir},%{_miconsdir},%{_liconsdir}}
# convert -resize 16x16 d2x-xl-ico-32x32.gif %{buildroot}%{_miconsdir}/%{name}.png
# convert -resize 32x32 d2x-xl-ico-32x32.gif %{buildroot}%{_iconsdir}/%{name}.png
# convert -resize 48x48 d2x-xl-ico-64x64.gif %{buildroot}%{_liconsdir}/%{name}.png

%clean
rm -rf %{buildroot}

%files
%defattr (-,root,root)
%{_gamesbindir}/%{name}
%dir %{_gamesdatadir}/%{name}
%{_datadir}/applications/mandriva-%{name}.desktop
# %{_miconsdir}/%{name}.png
# %{_iconsdir}/%{name}.png
# %{_liconsdir}/%{name}.png




%changelog
* Wed Jul 23 2008 Thierry Vignaud <tvignaud@mandriva.com> 1.9.9-5mdv2009.0
+ Revision: 243885
- rebuild

* Wed Jan 02 2008 Olivier Blin <oblin@mandriva.com> 1.9.9-3mdv2008.1
+ Revision: 140717
- restore BuildRoot

  + Thierry Vignaud <tvignaud@mandriva.com>
    - kill re-definition of %%buildroot on Pixel's request
    - kill desktop-file-validate's 'warning: key "Encoding" in group "Desktop Entry" is deprecated'

* Sun May 27 2007 Bogdano Arendartchuk <bogdano@mandriva.com> 1.9.9-3mdv2008.0
+ Revision: 31718
- fixed TiMidity++ dep name


* Sun Mar 04 2007 Per Øyvind Karlsen <pkarlsen@mandriva.com> 1.9.9-2mdv2007.0
+ Revision: 132329
- bump
- use dos2unix on files only
- fix buildrequires
- fix buildrequires
-new package from Zombie
- Import d2x-xl

