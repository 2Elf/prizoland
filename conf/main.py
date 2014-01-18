class MainConfig(object):
    """
    Main configuration object
    """

    @classmethod
    def get_settings(cls):
        """
        Returns settings dictionary
        """
        return {
            key.lower(): getattr(cls, key)
            for key in filter(lambda s: s.isupper(), dir(cls))
        }

    HOST = 'viotest.local'
    PORT = 8000

    #  social network auth data
    LOGIN = "79670452475"
    PASSWORD = "C3NPWqjRe"
    SOCIAL_NETWORK = 'vk'

    STORAGE = 'achives_data.cfg'



