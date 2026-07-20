from utils.storage import save_data, load_data


def test_save_load():
    data = [{"name": "Tabby"}]

    save_data("data/test.json", data)

    loaded = load_data("data/test.json")

    assert loaded == data