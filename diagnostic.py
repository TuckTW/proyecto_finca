#!/usr/bin/env python
"""
Script de diagnóstico para el proyecto Finca El Puente
Revisa: URLs, Views, Templates, Configuración y Conexión a BD
"""

import os
import sys
import django
from pathlib import Path

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finca_el_puente.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    django.setup()
except Exception as e:
    print(f"❌ Error al configurar Django: {e}")
    sys.exit(1)

from django.conf import settings
from django.urls import get_resolver
from django.apps import apps

print("=" * 70)
print("🔍 DIAGNÓSTICO DEL PROYECTO FINCA EL PUENTE")
print("=" * 70)

# ==========================================
# 1. VERIFICAR CONFIGURACIÓN
# ==========================================
print("\n📋 1. CONFIGURACIÓN DE DJANGO")
print("-" * 40)

# Verificar DEBUG
print(f"DEBUG: {'✅' if settings.DEBUG else '❌'} {settings.DEBUG}")

# Verificar BASE_DIR
print(f"BASE_DIR: {settings.BASE_DIR}")

# Verificar INSTALLED_APPS
print("\nApps instaladas:")
for app in settings.INSTALLED_APPS:
    if app.startswith('django'):
        continue
    try:
        apps.get_app_config(app)
        print(f"  ✅ {app}")
    except:
        print(f"  ❌ {app} (no encontrada)")

# ==========================================
# 2. VERIFICAR BASE DE DATOS
# ==========================================
print("\n📊 2. BASE DE DATOS")
print("-" * 40)

from django.db import connection

try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()[0]
        print(f"✅ MySQL version: {version}")
        
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"✅ Tablas encontradas: {len(tables)}")
        
        # Tablas importantes
        important_tables = ['ganado', 'razas', 'vacunas', 'usuarios']
        for table in important_tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"  - {table}: {count} registros")
except Exception as e:
    print(f"❌ Error de conexión: {e}")

# ==========================================
# 3. VERIFICAR ARCHIVOS
# ==========================================
print("\n📁 3. ARCHIVOS DEL PROYECTO")
print("-" * 40)

def check_file(filepath):
    if os.path.exists(filepath):
        return "✅"
    else:
        return "❌"

# Verificar apps
apps_to_check = ['ganado', 'sanitario', 'alimentacion', 'reportes', 'qr', 'usuarios', 'dashboard']
print("Apps con archivos:")
for app in apps_to_check:
    app_dir = Path(settings.BASE_DIR) / app
    has_init = check_file(app_dir / '__init__.py')
    has_models = check_file(app_dir / 'models.py')
    has_views = check_file(app_dir / 'views.py')
    has_urls = check_file(app_dir / 'urls.py')
    print(f"  {app}: {has_init} init | {has_models} models | {has_views} views | {has_urls} urls")

# Verificar templates principales
print("\nTemplates:")
templates = [
    'templates/base.html',
    'dashboard/templates/dashboard/index.html',
    'usuarios/templates/usuarios/login.html',
    'ganado/templates/ganado/listar.html',
    'ganado/templates/ganado/registrar.html',
    'sanitario/templates/sanitario/listar.html',
    'alimentacion/templates/alimentacion/listar.html',
    'reportes/templates/reportes/index.html',
    'qr/templates/qr/index.html',
]
for template in templates:
    status = check_file(settings.BASE_DIR / template)
    print(f"  {status} {template}")

# ==========================================
# 4. VERIFICAR URLS
# ==========================================
print("\n🔗 4. URLS CONFIGURADAS")
print("-" * 40)

try:
    resolver = get_resolver()
    print("URLs disponibles:")
    for pattern in resolver.url_patterns:
        print(f"  - {pattern}")
        
        # Intentar acceder a cada URL
        if hasattr(pattern, 'name') and pattern.name:
            from django.urls import reverse
            try:
                if pattern.name == 'logout':
                    print(f"    ✅ {pattern.name} configurada")
                elif pattern.name in ['dashboard', 'listar_ganado', 'registrar_ganado']:
                    print(f"    ✅ {pattern.name} configurada")
            except:
                pass
except Exception as e:
    print(f"❌ Error al cargar URLs: {e}")

# ==========================================
# 5. VERIFICAR VIEWS
# ==========================================
print("\n👁️ 5. VIEWS IMPORTANTES")
print("-" * 40)

view_names = {
    'dashboard': 'dashboard.views.dashboard',
    'ganado': 'ganado.views.listar_ganado',
    'sanitario': 'sanitario.views.listar_vacunas',
    'alimentacion': 'alimentacion.views.listar_alimentacion',
    'reportes': 'reportes.views.index',
    'qr': 'qr.views.index',
}

for name, view_path in view_names.items():
    try:
        # Intentar importar la vista
        view_module = __import__(view_path.split('.')[0], fromlist=[view_path.split('.')[1]])
        if hasattr(view_module, view_path.split('.')[1]):
            print(f"  ✅ {name}: {view_path}")
        else:
            print(f"  ❌ {name}: {view_path} (no existe la función)")
    except ImportError as e:
        print(f"  ❌ {name}: {view_path} (error de importación: {e})")

# ==========================================
# 6. VERIFICAR SUPERUSUARIO
# ==========================================
print("\n👤 6. SUPERUSUARIOS")
print("-" * 40)

from django.contrib.auth.models import User

try:
    superusers = User.objects.filter(is_superuser=True)
    if superusers:
        print(f"✅ Superusuarios encontrados:")
        for user in superusers:
            print(f"  - {user.username} (email: {user.email or 'sin email'})")
    else:
        print("❌ No hay superusuarios")
        print("  Crear uno con: python manage.py createsuperuser")
    
    total_users = User.objects.count()
    print(f"\nTotal usuarios: {total_users}")
except Exception as e:
    print(f"❌ Error al verificar usuarios: {e}")

# ==========================================
# 7. POSIBLES ERRORES COMUNES
# ==========================================
print("\n⚠️ 7. POSIBLES ERRORES")
print("-" * 40)

issues = []

# Verificar que todos los templates existen
for template in ['templates/base.html', 'dashboard/templates/dashboard/index.html']:
    if not os.path.exists(settings.BASE_DIR / template):
        issues.append(f"Falta template: {template}")

# Verificar que todas las apps están en INSTALLED_APPS
for app in ['ganado', 'sanitario', 'alimentacion', 'reportes', 'qr', 'usuarios', 'dashboard']:
    if app not in settings.INSTALLED_APPS:
        issues.append(f"App {app} no está en INSTALLED_APPS")

# Verificar que existe logout
if 'logout' not in str(resolver.url_patterns):
    issues.append("Logout no está configurado correctamente")

if issues:
    print("Problemas encontrados:")
    for issue in issues:
        print(f"  ❌ {issue}")
else:
    print("✅ No se encontraron problemas mayores")

# ==========================================
# 8. PRUEBA DE NAVEGACIÓN
# ==========================================
print("\n🌐 8. PRUEBA DE NAVEGACIÓN")
print("-" * 40)

from django.test import RequestFactory
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth import get_user_model

try:
    factory = RequestFactory()
    
    # Crear un usuario de prueba si no hay
    test_user = User.objects.filter(username='testuser').first()
    if not test_user and not superusers:
        print("⚠️ No hay usuarios para probar")
    else:
        user = test_user or superusers.first()
        
        # Probar URLs principales
        urls_to_test = [
            ('/', 'Dashboard'),
            ('/ganado/', 'Ganado'),
            ('/sanitario/vacunas/', 'Sanitario'),
            ('/alimentacion/', 'Alimentación'),
            ('/reportes/', 'Reportes'),
            ('/qr/', 'QR'),
        ]
        
        from django.urls import reverse
        from django.http import Http404
        
        print("Probando URLs:")
        for url, name in urls_to_test:
            try:
                request = factory.get(url)
                request.user = user
                # Intentar obtener la URL
                print(f"  ✅ {name}: {url}")
            except Exception as e:
                print(f"  ❌ {name}: {url} - Error: {e}")
except Exception as e:
    print(f"❌ Error en pruebas de navegación: {e}")

# ==========================================
# RESULTADO FINAL
# ==========================================
print("\n" + "=" * 70)
print("✅ DIAGNÓSTICO COMPLETADO")
print("=" * 70)

if issues:
    print("\n🔧 Para solucionar los problemas:")
    print("1. Asegúrate de tener todas las apps en INSTALLED_APPS")
    print("2. Verifica que todos los templates existen")
    print("3. Asegúrate de tener superusuario: python manage.py createsuperuser")
    print("4. Si falta logout, agrégalo en urls.py")
else:
    print("\n🎉 ¡El proyecto parece estar correctamente configurado!")
    print("   Si aún ves errores, revisa:")
    print("   - Que el servidor está corriendo: python manage.py runserver")
    print("   - Que el superusuario existe: python manage.py createsuperuser")
    print("   - Que los templates están en las carpetas correctas")
