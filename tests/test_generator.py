from core.context import ProjectContext
from core.default_templates import create_standard_project_template
from core.generator import ProjectGenerator
from pathlib import Path

# Test directory
test_dir = Path("C:/temp/test_projects")
test_dir.mkdir(parents=True, exist_ok=True)

# Maak context
ctx = ProjectContext(
    app_name="DemoAppWithVenv",
    version="1.0.0",
    author="John Doe",
    root_path=test_dir,
    description="Demo met virtuele omgeving",
    create_venv=True
)

# Maak template - ✅ GEEF ROOT_PATH MEE!
template = create_standard_project_template(
    name=ctx.app_name,
    version=ctx.version,
    author=ctx.author,
    description=ctx.description,
    create_venv=True,
    root_path=test_dir  # ✅ BELANGRIJK!
)

# Genereer project!
generator = ProjectGenerator(ctx, template)
success = generator.generate()

if success:
    print("\n🎉 PROJECT MET VENV SUCCESVOL AANGEMAAKT!")
    print(f"\n📂 Project: {ctx.project_root}")
    print(f"🐍 Venv: {ctx.venv_path}")
    print("\n📝 Activeer met:")
    print(f"   {ctx.venv_path / 'Scripts' / 'activate.bat'}")
    print("\n💡 Open in VS Code:")
    print(f"   code {ctx.project_root}")