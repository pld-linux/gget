#
%define		epiphany_version	2.24
#
Summary:	Download manager for GNOME
Summary(pl.UTF-8):	Zarządca pobierania plików dla GNOME
Name:		gget
Version:	0.0.4
Release:	2
License:	GPL v2+
Group:		X11/Applications/Networking
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gget/0.0/%{name}-%{version}.tar.bz2
# Source0-md5:	fb997cac66287c18da74bb7b6d6a07e9
Patch0:		%{name}-desktop.patch
Patch1:		%{name}-dont-hardcode-python-version.patch
URL:		http://live.gnome.org/GGet
BuildRequires:	GConf2-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	epiphany-devel >= 2.24.0
BuildRequires:	gettext-devel
BuildRequires:	gtk+2-devel >= 2:2.12.0
BuildRequires:	intltool >= 0.33.0
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	python >= 1:2.5
BuildRequires:	python-dbus-devel >= 0.82
BuildRequires:	python-devel >= 1:2.5
BuildRequires:	python-gnome-devel >= 2.16.0
BuildRequires:	python-gnome-extras-devel >= 2.14.2
BuildRequires:	python-pygtk-devel >= 2:2.12.0
BuildRequires:	python-pynotify-devel >= 0.1.1
BuildRequires:	rpmbuild(macros) >= 1.311
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	gtk-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GGet is a download manager for GNOME.

%description -l pl.UTF-8
GGet jest zarządcą pobierania plików dla GNOME.

%package -n epiphany-extension-gget
Summary:	Epiphany extension - GGet
Summary(pl.UTF-8):	Rozszerzenie dla Epiphany - GGet
Group:		X11/Applications/Networking
Requires:	%{name} = %{version}-%{release}
Requires:	epiphany >= 2.24

%description -n epiphany-extension-gget
Epiphany extension that uses GGet to download files.

%description -n epiphany-extension-gget -l pl.UTF-8
Rozszerzenie dla Epiphany wykorzystujące GGet do pobierania plików.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-schemas-install
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%py_postclean
%py_postclean %{_libdir}/epiphany/%{epiphany_version}/extensions

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database
%update_icon_cache hicolor
%gconf_schema_install gget.schemas

%preun
%gconf_schema_uninstall gget.schemas

%postun
%update_desktop_database_postun
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc
%attr(755,root,root) %{_bindir}/gget
%{_desktopdir}/gget.desktop
%{_datadir}/dbus-1/services/org.gnome.gget.service
%{_datadir}/gget
%{_iconsdir}/hicolor/*/*/*.png
%{_iconsdir}/hicolor/*/*/*.svg
%{_sysconfdir}/gconf/schemas/gget.schemas
%dir %{py_sitescriptdir}/gget
%{py_sitescriptdir}/gget/*.py[co]

%files -n epiphany-extension-gget
%defattr(644,root,root,755)
%{_libdir}/epiphany/%{epiphany_version}/extensions/gget-epiphany.py[co]
%{_libdir}/epiphany/%{epiphany_version}/extensions/gget.ephy-extension
