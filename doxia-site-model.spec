Name:		doxia-site-model
Version:	2.0.0
Release:	1
Summary:	Doxia site model
Group:		Development/Java
License:	ASL 2.0
URL:		https://maven.apache.org/doxia/doxia-sitetools/
Source0:	https://repo1.maven.org/maven2/org/apache/maven/doxia/doxia-site-model/%{version}/doxia-site-model-%{version}-sources.jar
BuildArch:	noarch
BuildRequires:	python
BuildRequires:	mvn(javax.inject:javax.inject)
BuildRequires:	mvn(org.codehaus.plexus:plexus-utils)
# Literal, so the first rpmbuild -bs records them before sysjar is installed.
BuildRequires:	maven
BuildRequires:	java-current-devel
BuildSystem:	maven
BuildOption(install):	--file-name %{name}

%description
The Doxia site decoration model. The tag does not contain the
generated model classes, so this package builds the Maven Central
sources jar. XML classes come from plexus-utils.

%prep
%setup -q -c -T
# The builders' rpmuncompress passes a sources jar to tar.
python - %{SOURCE0} <<'PY'
import sys
import zipfile
zipfile.ZipFile(sys.argv[1]).extractall(".")
PY
python - <<'PY'
import os
import shutil
import xml.etree.ElementTree as ET

for name in ("LICENSE", "NOTICE"):
    src = os.path.join("META-INF", name)
    if os.path.exists(src):
        shutil.copy2(src, name)
os.makedirs("src/main/java", exist_ok=True)
shutil.move("org", "src/main/java/org")

NS = "http://maven.apache.org/POM/4.0.0"
ET.register_namespace("", NS)

def tag(name):
    return "{" + NS + "}" + name

def add(parent, name, text):
    node = ET.SubElement(parent, tag(name))
    node.text = text
    return node

root = ET.Element(tag("project"))
add(root, "modelVersion", "4.0.0")
add(root, "groupId", "org.apache.maven.doxia")
add(root, "artifactId", "doxia-site-model")
add(root, "version", "%{version}")
add(root, "name", "Doxia Sitetools :: Site model")
deps = ET.SubElement(root, tag("dependencies"))
for group, artifact, version in (
    ("javax.inject", "javax.inject", "1"),
    ("org.codehaus.plexus", "plexus-utils", "3.6.0"),
):
    dep = ET.SubElement(deps, tag("dependency"))
    add(dep, "groupId", group)
    add(dep, "artifactId", artifact)
    add(dep, "version", version)
ET.ElementTree(root).write("pom.xml", encoding="utf-8", xml_declaration=True)
PY

%files -f .mfiles
%doc LICENSE NOTICE
