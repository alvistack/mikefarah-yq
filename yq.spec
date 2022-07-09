%global debug_package %{nil}

Name: yq
Epoch: 100
Version: 4.25.3
Release: 1%{?dist}
Summary: Lightweight and portable command-line YAML processor
License: MIT
URL: https://github.com/mikefarah/yq/tags
Source0: %{name}_%{version}.orig.tar.gz
BuildRequires: go >= 1.18
BuildRequires: glibc-static

%description
yq is a lightweight and portable command-line YAML, JSON and XML
processor. yq uses jq like syntax but works with yaml files as well as
json and xml. It doesn't yet support everything jq does - but it does
support the most common operations and functions, and more is being
added continuously.

%prep
%autosetup -T -c -n %{name}_%{version}-%{release}
tar -zx -f %{S:0} --strip-components=1 -C .

%build
mkdir -p bin
set -ex && \
    export CGO_ENABLED=0 && \
    go build \
        -mod vendor -buildmode pie -v \
        -ldflags "-s -w -extldflags '-static -lm'" \
        -o ./bin/yq .

%install
install -Dpm755 -d %{buildroot}%{_bindir}
install -Dpm755 -d %{buildroot}%{_prefix}/share/bash-completion/completions
install -Dpm755 -t %{buildroot}%{_bindir}/ bin/yq
./bin/yq shell-completion bash > %{buildroot}%{_prefix}/share/bash-completion/completions/yq

%files
%license LICENSE
%{_bindir}/*
%{_prefix}/share/bash-completion/completions/*

%changelog
