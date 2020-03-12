from loguru import logger


def test_home_page(test_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    r = test_client.get("/")
    assert r.status_code == 200
    # assert b"Get Started" in r.data


def test_home_page_post(test_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (POST)
    THEN check the response is invalid
    """
    r = test_client.post("/")
    assert r.status_code == 405
    assert b"Recent Logs" not in r.data


def test_register_page(test_client):
    """
    GIVEN a Flask application
    WHEN the '/register' page is requested (GET)
    THEN check the response is valid
    """
    r = test_client.get("/register")
    assert r.status_code == 200


def test_login_page(test_client):
    """
    GIVEN a Flask application
    WHEN the '/login' page is requested (GET)
    THEN check the response is valid
    """
    r = test_client.get("/login")
    logger.debug(r.data)
    assert r.status_code == 200
    assert b"User Login" in r.data
    assert b"Email" in r.data
    assert b"Password" in r.data


def test_valid_login_logout(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/login' page is posted to (POST)
    THEN check the response is valid
    """
    r = test_client.post(
        "/login",
        data=dict(email="ryan.sheppard@gmail.com", password="strengthlog"),
        follow_redirects=True,
    )
    assert r.status_code == 200
    assert b"Recent Logs" in r.data
    assert b"Log In" not in r.data
    """
    GIVEN a Flask application
    WHEN the '/logout' page is requested (GET)
    THEN check the response is valid
    """
    r = test_client.get("/logout", follow_redirects=True)
    assert r.status_code == 200
    assert b"Log Out" not in r.data
    assert b"Log In" in r.data


def test_invalid_login(test_client, init_database):
    r = test_client.post(
        "/login",
        data=dict(email="ryan.sheppard@gmail.com", password="strengthnotlog"),
        follow_redirects=True,
    )
    assert r.status_code == 200
    assert b"Login" in r.data


def test_valid_registration(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/register' page is posted to (POST)
    THEN check the response is valid
    """
    r = test_client.post(
        "register",
        data=dict(email="foo@bar.com", password="foobar", confirm_password="foobar"),
        follow_redirects=True,
    )
    assert r.status_code == 200
    assert b"Register" in r.data
    assert b"Login" in r.data


def test_invalid_registration(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/register' page is posted to with invalid credentials (POST)
    THEN check an error message is returned to the user
    """
    r = test_client.post(
        "/register",
        data=dict(email="foo@bar.com", password="foobar", confirm_password="foonotbar"),
        follow_redirects=True,
    )
    assert r.status_code == 200
    assert b"Log Out" not in r.data
    assert b"Register" in r.data
