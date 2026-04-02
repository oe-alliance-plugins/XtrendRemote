from setuptools import setup
import setup_translate

pkg = 'SystemPlugins.RemoteControlCode'
setup(name='enigma2-plugin-systemplugins-remotecontrolcode',
       version='3.0',
       description='Change Remote Control Code, Switch ET5000 ET9000 DMM remote',
       package_dir={pkg: 'RemoteControlCode'},
       packages=[pkg],
       package_data={pkg: ['images/*.png', '*.png', '*.xml', 'locale/*/LC_MESSAGES/*.mo']},
       cmdclass=setup_translate.cmdclass,  # for translation
      )
