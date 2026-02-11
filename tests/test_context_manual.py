from core.context import ProjectContext
from core.default_templates import create_standard_project_template
from pathlib import Path

# Test template systeem
project_template = create_standard_project_template(
    name="MyTestApp",
    version="1.0.0",
    author="John Doe",
    description="Een test applicatie",
    create_venv=True
)

print("=" * 60)
print("PROJECT TEMPLATE")
print("=" * 60)
print(f"Naam: {project_template.name}")
print(f"Versie: {project_template.version}")
print(f"Auteur: {project_template.author}")
print(f"Venv: {project_template.create_venv}")
print()

print("ROOT FOLDERS:")
for folder in project_template.root_folders:
    print(f"  📁 {folder.name} (package: {folder.python_package})")
    for file in folder.files:
        print(f"      📄 {file.name}")
    for subfolder in folder.subfolders:
        print(f"      📁 {subfolder.name}")

print()
print("ROOT FILES:")
for file in project_template.root_files:
    print(f"  📄 {file.name}")

print()
print("=" * 60)
print("VOORBEELD: README.md CONTENT (eerste 500 chars)")
print("=" * 60)
readme = next(f for f in project_template.root_files if f.name == "README.md")
print(readme.template_body[:500])