from src.api_manual import handle_request

def test_ok_found():
    r = handle_request('{"iso3":" col ","year":1999}')
    assert r["ok"] is True
    assert r["status"] == 200
    assert r["data"]["iso3"] == "COL"
    assert r["data"]["year"] == 1999
    assert r["data"]["found"] is True

def test_invalid_iso3():
    r = handle_request('{"iso3":"CO","year":1999}')
    assert r["ok"] is False
    assert r["status"] == 422

def test_invalid_year():
    r = handle_request('{"iso3":"COL","year":"nope"}')
    assert r["ok"] is False
    assert r["status"] == 422

def test_extra_field_forbidden():
    r = handle_request('{"iso3":"COL","year":1999,"x":1}')
    assert r["ok"] is False
    assert r["status"] == 422

def test_invalid_json():
    r = handle_request("{bad json}")
    assert r["ok"] is False
    assert r["status"] == 400