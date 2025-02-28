%global libliftoff_minver 0.4.1

%global _default_patch_fuzz 2
%global build_timestamp %(date +"%Y%m%d")
%global gamescope_tag 3.14.15

Name:           gamescope
Version:        100.%{gamescope_tag}
Release:        1.bazzite
Summary:        Micro-compositor for video games on Wayland

License:        BSD
URL:            https://github.com/ValveSoftware/gamescope

# Create stb.pc to satisfy dependency('stb')
Source0:        stb.pc

Patch0:         hardware.patch
Patch1:         720p.patch
Patch2:         disable-steam-touch-click-atom.patch
Patch3:         external-rotation.patch
Patch4:         panel-type.patch
Patch5:         deckhd.patch

# Until >= 3.14.16
Patch6:         input.patch

BuildRequires:  meson >= 0.54.0
BuildRequires:  ninja-build
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  glm-devel
BuildRequires:  google-benchmark-devel
BuildRequires:  libeis-devel
BuildRequires:  libXmu-devel
BuildRequires:  libXcursor-devel
BuildRequires:  pixman-devel
BuildRequires:  pkgconfig(libdisplay-info)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(libeis-1.0)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xdamage)
BuildRequires:  pkgconfig(xcomposite)
BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xfixes)
BuildRequires:  pkgconfig(xxf86vm)
BuildRequires:  pkgconfig(xtst)
BuildRequires:  pkgconfig(xres)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(wayland-protocols) >= 1.17
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(libavif)
BuildRequires:  (pkgconfig(wlroots) >= 0.18.0 with pkgconfig(wlroots) < 0.19.0)
BuildRequires:  (pkgconfig(libliftoff) >= 0.4.1 with pkgconfig(libliftoff) < 0.5)
BuildRequires:  pkgconfig(libcap)
BuildRequires:  pkgconfig(hwdata)
BuildRequires:  spirv-headers-devel
# Enforce the the minimum EVR to contain fixes for all of:
# CVE-2021-28021 CVE-2021-42715 CVE-2021-42716 CVE-2022-28041 CVE-2023-43898
# CVE-2023-45661 CVE-2023-45662 CVE-2023-45663 CVE-2023-45664 CVE-2023-45666
# CVE-2023-45667
BuildRequires:  stb_image-devel >= 2.28^20231011gitbeebb24-12
# Header-only library: -static is for tracking per guidelines
BuildRequires:  stb_image-static
BuildRequires:  stb_image_resize-devel
BuildRequires:  stb_image_resize-static
BuildRequires:  stb_image_write-devel
BuildRequires:  stb_image_write-static
BuildRequires:  /usr/bin/glslangValidator
BuildRequires:  libdecor-devel
BuildRequires:  libXdamage-devel
BuildRequires:  xorg-x11-server-Xwayland-devel
BuildRequires:  git

# libliftoff hasn't bumped soname, but API/ABI has changed for 0.2.0 release
Requires:       libliftoff%{?_isa} >= %{libliftoff_minver}
Requires:       xorg-x11-server-Xwayland
Requires:       gamescope-libs = %{version}
Recommends:     mesa-dri-drivers
Recommends:     mesa-vulkan-drivers

%description
%{name} is the micro-compositor optimized for running video games on Wayland.

%package libs
Summary:	libs for %{name}
%description libs
%summary

%prep
git clone --depth 1 --branch %{gamescope_tag} https://github.com/ValveSoftware/gamescope
cd gamescope
git submodule update --init --recursive
mkdir -p pkgconfig
cp %{SOURCE0} pkgconfig/stb.pc

# Replace spirv-headers include with the system directory
sed -i 's^../thirdparty/SPIRV-Headers/include/spirv/^/usr/include/spirv/^' src/meson.build

%autopatch -p1

%build
cd gamescope
export PKG_CONFIG_PATH=pkgconfig
%meson -Dpipewire=enabled -Ddrm_backend=enabled -Drt_cap=enabled -Davif_screenshots=enabled -Dinput_emulation=enabled -Dsdl2_backend=enabled -Dforce_fallback_for=vkroots -Dforce_fallback_for=wlroots
%meson_build

%install
cd gamescope
%meson_install --skip-subprojects

%files
%license gamescope/LICENSE
%doc gamescope/README.md
%attr(0755, root, root) %caps(cap_sys_nice=eip) %{_bindir}/gamescope

%files libs
%{_libdir}/libVkLayer_FROG_gamescope_wsi_*.so
%{_datadir}/vulkan/implicit_layer.d/VkLayer_FROG_gamescope_wsi.*.json

%changelog
{{{ git_dir_changelog }}}
