%global upstreamname RCCL
%global rocm_release 5.7
%global rocm_patch 1
%global rocm_version %{rocm_release}.%{rocm_patch}

%global toolchain rocm
# hipcc does not support some clang flags
%global build_cxxflags %(echo %{optflags} | sed -e 's/-fstack-protector-strong/-Xarch_host -fstack-protector-strong/' -e 's/-fcf-protection/-Xarch_host -fcf-protection/')

Name:           rccl
Version:        %{rocm_version}
Release:        1%{?dist}
Summary:        ROCm Communication Collectives Library

Url:            https://github.com/ROCmSoftwarePlatform
License:        BSD-3-Clause
Source0:        %{url}/%{upstreamname}/archive/refs/tags/rocm-%{rocm_version}.tar.gz#/%{upstreamname}-%{rocm_version}.tar.gz
Patch0:         0001-prepare-rccl-cmake-for-fedora.patch
Patch1:         0002-rccl-fix-invalid-escape.patch

BuildRequires:  cmake
BuildRequires:  clang-devel
BuildRequires:  compiler-rt
BuildRequires:  hipify
BuildRequires:  lld
BuildRequires:  llvm-devel
BuildRequires:  ninja-build
BuildRequires:  rocm-cmake
BuildRequires:  rocm-comgr-devel
BuildRequires:  rocm-hip-devel
BuildRequires:  rocm-runtime-devel
BuildRequires:  rocm-rpm-macros
BuildRequires:  rocm-rpm-macros-modules
BuildRequires:  rocm-smi-devel

# Only x86_64 works right now:
ExclusiveArch:  x86_64

%description
RCCL (pronounced "Rickle") is a stand-alone library of standard
collective communication routines for GPUs, implementing all-reduce,
all-gather, reduce, broadcast, reduce-scatter, gather, scatter, and
all-to-all. There is also initial support for direct GPU-to-GPU
send and receive operations. It has been optimized to achieve high
bandwidth on platforms using PCIe, xGMI as well as networking using
InfiniBand Verbs or TCP/IP sockets. RCCL supports an arbitrary
number of GPUs installed in a single node or multiple nodes, and
can be used in either single- or multi-process (e.g., MPI)
applications.

The collective operations are implemented using ring and tree
algorithms and have been optimized for throughput and latency. For
best performance, small operations can be either batched into
larger operations or aggregated through the API.

%package devel
Summary:        Headers and libraries for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers and libraries for %{name}

%prep
%autosetup -p1 -n %{name}-rocm-%{version}

%build
%cmake %rocm_cmake_options

%install
%cmake_install

%check
%if %{with check}
%ctest
%endif

%files
%license LICENSE.txt
%{_libdir}/lib%{name}.so.1{,.*}
%exclude %{_docdir}/%{name}/LICENSE.txt

%files devel
%doc README.md
%{_datadir}/%{name}/
%{_includedir}/%{name}
%{_libdir}/cmake/%{name}
%{_libdir}/lib%{name}.so

%changelog
* Tue Oct 17 2023 Tom Rix <trix@redhat.com> - 5.7.1-1
- Update to 5.7.1

* Sun Oct 1 2023 Tom Rix <trix@redhat.com> - 5.7.0-1
- Initial package
