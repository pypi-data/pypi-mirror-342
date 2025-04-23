from utils.defines import Scope


class InputProcessor:

    @staticmethod
    def process_input(data_view):

        scope = data_view["scope"]

        data_files = data_view['files']

        if scope != Scope.RUN:
            if 'runs' not in data_view:
                raise KeyError('Missing mandaroty field "runs"')
            # Merge all the run files under the proposal
            for run in data_view['runs']:
                data_files.extend(run['files'])
                run['files'] = []

            data_view['files'] = list(set(data_files))
            data_view['files'].sort()

            del data_view['runs']
        else:
            if 'files' in data_view:
                del data_view['files']

        match scope:
            case Scope.FILE:
                if data_files is not None:
                    data_files = [{'file': f, "parameters": {}} for f in data_files]
                    data_view.update({'files': data_files})
            case Scope.RUN:
                runs = data_view['runs'] if 'runs' in data_view else None
                if type(runs) is not list:
                    raise TypeError('List of runs is not well-formet')
                for run in runs:
                    run.update({'parameters': {}})
            case _:  # Scope.PROPOSAL
                data_view.update({'parameters': {}})

        return data_view
