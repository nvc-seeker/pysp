import os
import re
import subprocess
import shutil


class IZipApp(object):
    _folder_ignored = ['__pycache__', 'venv', 'tests', 'test', 'build']

    def __init__(self, config):
        """
        :param config: a dict with structure like below
            {
                "target":             # build path - exs: "./build/"
                "scripts":            # python scripts - exs: "venv/Scripts/"
                "name":               # src name will build - exs: "myApp"
                "src":                # src source path - exs: "./appSource/"
                "main":               # main class - exs: "main.py" or "package:main"
                "package":            # root package - exs: "myPackage"
                # "module":             # module using to zipapp - exs: "module1"
            }
        """
        target_path = (config.get('target') or f'./build/').removesuffix('/')
        self.scripts_path = config.get('scripts') or 'venv/Scripts/'
        self.app_name = config.get('name') or 'None'
        self.src_path = config.get('src') or './'
        self.main = config.get('main')
        self.build_target_path = config.get('target') or f'./{target_path}/{self.app_name}'
        self.packages = config.get('packages') or []
        # self.module = config.get('module') or None
        self.package_target_path = self.build_target_path
        self.requirements = config.get('reqs') or 'requirements.txt'

    def __get_files_ignored__(self, path, files):
        ls = re.split('[/\\\\]', path)
        exist_ignored = [i for i in self._folder_ignored if i in ls]
        if len(exist_ignored):
            return files
        return [f for f in files if f in self._folder_ignored]

    def __clone_src__(self):
        shutil.ignore_patterns([''])
        if os.path.exists(self.build_target_path):
            shutil.rmtree(self.build_target_path)
        # shutil.copytree(self.src_path, self.build_target_path, ignore=self._files_ignored, copy_function=shutil.copy2)
        shutil.copytree(self.src_path, self.package_target_path,
                        ignore=self.__get_files_ignored__,
                        copy_function=shutil.copy2)

    def __install_dependencies__(self):
        # venv/Scripts/pip install -r requirements.txt --target {build_target_path}
        cmd = [f'{self.scripts_path}pip', 'install', '-r', self.requirements, '--target', self.build_target_path]
        subprocess.run(cmd)

    def __make_zipapp__(self):
        # venv/Scripts/python -m zipapp {build_target_path}
        cmd = [f'{self.scripts_path}python', '-m', 'zipapp', '-p', '"interpreter"', f'{self.build_target_path}']
        if self.main:
            cmd += ['-m', self.main]
        subprocess.run(cmd)


def zipapp(config):
    zi = IZipApp(config)
    zi.__clone_src__()
    zi.__install_dependencies__()
    zi.__make_zipapp__()


if __name__ == '__main__':
    # zipapp({
    #     'name': 'pySetupApp1',
    #     'src': './pySetupApp1',
    # })
    zipapp({
        'name': 'pySetupApp',
        # 'src': './app',
        # 'reqs': './app/pysSetupApp/app1/requirements.txt',
        # 'package': 'pysSetupApp'
        # 'main': 'pysSetupApp:main'
    })
