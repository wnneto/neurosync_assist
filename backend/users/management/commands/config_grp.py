import json
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = 'Cria grupos e aplica permissões com base no JSON de configuração.'

    def handle(self, *args, **kwargs):
        try:
            with open('grupos_config.json', 'r') as f:
                config = json.load(f)
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR('Arquivo grupos_config.json não encontrado.'))
            return

        todas_permissoes = Permission.objects.all()
        permissoes_dict = {
            f"{p.content_type.app_label}.{p.codename}": p for p in todas_permissoes
        }

        for nome_grupo, permissoes in config.items():
            grupo, created = Group.objects.get_or_create(name=nome_grupo)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Grupo '{nome_grupo}' criado."))
            else:
                self.stdout.write(f"Grupo '{nome_grupo}' já existia. Permissões serão atualizadas.")

            grupo.permissions.clear()

            if "*" in permissoes:
                grupo.permissions.set(todas_permissoes)
                self.stdout.write(self.style.SUCCESS(f"Todas as permissões atribuídas ao grupo '{nome_grupo}'."))
                continue

            for cod in permissoes:
                perm = permissoes_dict.get(cod)
                if perm:
                    grupo.permissions.add(perm)
                else:
                    self.stderr.write(self.style.WARNING(f"Permissão '{cod}' não encontrada."))

            self.stdout.write(self.style.SUCCESS(f"Permissões aplicadas ao grupo '{nome_grupo}'."))

