from sarada import __version__
import sarada


def test_version():
	assert sarada.get_version() == __version__


def welcome_should_match(snapshot):
	message = sarada.welcome_message()
	assert message == snapshot
