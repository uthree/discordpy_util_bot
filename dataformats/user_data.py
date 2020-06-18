class UserData:
    def __init__(self):
        self._profile = "プロフィール未設定"

    @property
    def profile():
        return self_profile

    @profile.setter
    def set_profile(prof):
        self._profile = prof
