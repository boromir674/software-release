
from software_release.nodes.node import Node
from software_release.version_class import VersionString


@Node.register_as_subclass('determine-new-version')
class DetermineNewVersionNode(Node):

    @classmethod
    def _handle(cls, request):
        
        # Automatically find previous release 
        command = cls.command('previous-release', request.repository)
        previous_version = cls.run(command)

        # Automatically recommend next semantic version
        command = cls.command('new-release', request.repository, VersionString(previous_version), force_version=None)
        # TODO fixate interface so it returns the same type and avoid doing if-else here!
        result = cls.run(command)
        if type(result) != tuple:  # version bump is None!
            proposed_new_version = result
            level_bump = None
        else:  # version bump is at least PATCH!
            proposed_new_version, level_bump = result

        # If no previous release found, show a message
        if previous_version == '0.0.0':
            command = cls.command('render', 'no-release-tag-found')
            cls.run(command)

            command = cls.command('render',
                f'\nIt seems this is the first ever semantic release we are about to make!\n',
                ' We assume that the previously release version is 0.0.0 for the purpose',
                'of automatically recommending the next release version.\n',
            )
            cls.run(command)
        else:  # previous release found, show a message
            command = cls.command('render', 'release-tag-found', previous_version)
            cls.run(command)

        # inform about how the next version suggestion is computed automatically
        cmd = cls.command('render',
            f'We examined the commits found in revision \'HEAD..master\' (using the',
            'Angular Parser to extract their messages\' contents) to understand',
            'what type (ie \'feature\', \'fix\', \'ci\') of changes they contain.\n',
            
            f'Based on the above:\n',

            f' Recommended version bump: {level_bump}\n',
            f' --> {previous_version} + {level_bump} bump = {proposed_new_version}'
            )

        cls.run(cmd)

        dialog = cls.dialog('recommended-or-override-version')
        input_new_version = dialog.dialog({
            'recommended-version': str(proposed_new_version),
        })
        import re
        build_version = r'[a-zA-Z]+(?:\.\d+)?'
        regex = fr'v?(\d+\.\d+\.\d+(?:[\.\-_]?{build_version}(?:\.{build_version})*)?)'
        
        cmd_1 = cls.command('render', 'Incorrect input version.\n',
                'Please make sure your input is a valid Semantic Version;\n',
                'MAJOR.MINOR.PATCH',
                f'Should match regex: {regex}'
            )
        match = re.match(regex, input_new_version)
        while not match:
            cls.run(cmd_1)
            input_new_version = dialog.dialog({
                'recommended-version': str(proposed_new_version),
            })
            match = re.match(regex, input_new_version)

        new_version = match.group(1)

        command = cls.command('render', 'new-release-version', new_version)
        cls.run(command)
        return previous_version, new_version


    def handle(self, request):
        previous_version, new_version = self._handle(request)
        request.previous_version = previous_version
        request.new_version = new_version
        return super().handle(request)
