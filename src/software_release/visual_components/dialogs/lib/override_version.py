from PyInquirer import prompt
from ..interactive_dialog import Dialog


__all__ = ['RecommendedOrOverrideVersionDialog']


@Dialog.register_as_subclass('recommended-or-override-version')
class RecommendedOrOverrideVersionDialog(Dialog):

    def dialog(self, data):
        RECOMMENDED_VERSION_OPTION = data['recommended-version']
        CUSTOM_VERSION_OPTION = 'Input Custom Version'

        choices = [
            RECOMMENDED_VERSION_OPTION,
            CUSTOM_VERSION_OPTION
        ]
        questions = [
            {
                'type': 'list',  # navigate with arrows through choices
                'name': 'recommended-or-override',
                'message': 'Use the recommended version or use a custom version?',
                'choices': choices,
            },
            {
                'type': 'input',
                'name': 'custom-version',
                'message': 'Please input your desired release version in semver format (ie 0.5.0, 1.0.1)',
                'when': lambda answers: answers['recommended-or-override'] == CUSTOM_VERSION_OPTION,

            },
        ]
        answers = prompt(questions)
        if answers['recommended-or-override'] == CUSTOM_VERSION_OPTION:
            return answers['custom-version']
        return answers['recommended-or-override']
