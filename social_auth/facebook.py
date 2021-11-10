
import facebook


class Facebook:
    """
    Facebook class to fetch the user info and return it
    """

    @staticmethod
    def validate(auth_token):
        """
        validate method Queries the facebook GraphAPI to fetch the user info
        """
        try:
            graph = facebook.GraphAPI(access_token=auth_token)
            profile = graph.request(
                '/me?fields=name,email,picture,friends,first_name,last_name,birthday,middle_name,cover')
            return profile
        except Exception as e:

            return "Error: "+str(e)+", The token is invalid or expired."
