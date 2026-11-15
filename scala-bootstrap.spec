Name:		scala-bootstrap
Version:	2.10.7
Release:	1
Summary:	Scala 2.10.7 compiler built from source for later Scala bootstraps
Group:		Development/Java
License:	Apache-2.0
URL:		https://github.com/vxtls/scala
Source0:	scala-bootstrap-%{version}.tar.gz
Patch0:		scala-bootstrap-resume.patch

BuildArch:	noarch
BuildRequires:	scala-bootstrap-part9 = 1
BuildRequires:	java-1.8.0-openjdk-devel
BuildRequires:	git-core
BuildRequires:	make
BuildRequires:	python
BuildRequires:	tar

%description
Scala 2.10.7 library, reflect, and compiler jars built from the vxtls
bootstrap sources. This build resumes from the scala-bootstrap-part9 seed
and compiles only v2.10.7. Later Scala releases use this compiler as their
starr. The jars are installed for build-time bootstraps.

%prep
%autosetup -n scala-bootstrap-%{version} -p1
find . -type f \( -name '*.jar' -o -name '*.class' -o -name '*.so' -o -name '*.node' -o -name '*.wasm' \) -print > binaries.list
if [ -s binaries.list ]; then
	cat binaries.list
	exit 1
fi
test -s LICENSE
test -s compile.sh
test -s check.sh
test -s scripts/buildit.sh
test -s scripts/pack-seed.sh
grep -q SCALA_BOOT_SEED compile.sh
grep -q resume_skip scripts/buildit.sh
test -d repo/.git
test -s vendor/apache-ant-1.9.16/bootstrap.sh

%build
set -eo pipefail
export JAVA_HOME=$(ls -d %{_jvmdir}/java-1.8.0-openjdk-* | head -n 1)
export PATH="$JAVA_HOME/bin:/usr/bin:/bin"
export SCALA_BOOT_SEED=%{_datadir}/scala-bootstrap-part9/seed
export SCALA_BOOT_FROM=v2.10.7-bootstrap
bash ./compile.sh

%install
set -eo pipefail
mkdir -p %{buildroot}%{_datadir}/scala-bootstrap
cp -a dist/lib dist/stubs %{buildroot}%{_datadir}/scala-bootstrap/
test -s %{buildroot}%{_datadir}/scala-bootstrap/lib/scala-compiler.jar
test -s %{buildroot}%{_datadir}/scala-bootstrap/lib/scala-library.jar
test -s %{buildroot}%{_datadir}/scala-bootstrap/lib/scala-reflect.jar
test -s %{buildroot}%{_datadir}/scala-bootstrap/stubs/java8-charbuffer-overrides.jar
test -s %{buildroot}%{_datadir}/scala-bootstrap/stubs/java8-legacy-stubs.jar
test -s %{buildroot}%{_datadir}/scala-bootstrap/stubs/java8-filtered-stubs.jar

%check
set -eo pipefail
export JAVA_HOME=$(ls -d %{_jvmdir}/java-1.8.0-openjdk-* | head -n 1)
export PATH="$JAVA_HOME/bin:/usr/bin:/bin"
bash ./check.sh %{buildroot}%{_datadir}/scala-bootstrap

%files
%{_datadir}/scala-bootstrap
%license LICENSE
