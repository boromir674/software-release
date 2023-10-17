from .release_wizard import ReleaseWizard
import yaml


class ReleaseWizardFactory:

    @staticmethod
    def from_yaml(repository, file_path):
        with open(file_path, 'r') as file_handle:
            config_data = yaml.safe_load(file_handle)
        return ReleaseWizard.create(
            repository,
            config_data['wizard_steps']
        )

    @staticmethod
    def create(repository, nodes):
        return ReleaseWizard.create(
            repository,
            nodes
        )
