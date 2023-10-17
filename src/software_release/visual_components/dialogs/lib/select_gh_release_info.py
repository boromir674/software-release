from questionary import prompt
from ..interactive_dialog import Dialog


__all__ = ['SelectGithubReleaseInfoDialog']


@Dialog.register_as_subclass('select-gh-release-info')
class SelectGithubReleaseInfoDialog(Dialog):

    def dialog(self, data) -> str:
        questions = [
            {
                'type': 'list',  # navigate with arrows through choices
                'name': 'select-gh-release-is-draft',
                'message': 'Select whether this Github Relase should be marked as Draft',
                'choices': data['options'],
            },
        ]
        answers = prompt(questions)
        return answers['select-gh-release-is-draft']
