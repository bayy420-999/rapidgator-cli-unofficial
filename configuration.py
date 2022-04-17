from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

def configuration():
  return config['account']['email'], config['account']['password'], config['account']['token'], config['configuration']['download_path'], config.getboolean('configuration', 'is_batch_download'), config['configuration']['batch_file']

def write_token(args):
  for config['account']['token'] in config:
    config.set('account', 'token', args)
    with open('config.ini', 'w') as outfile:
      config.write(outfile)