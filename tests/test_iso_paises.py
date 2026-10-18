import iso_paises


def test_resolver_iso_pais_nombres_conocidos():
    assert iso_paises.resolver_iso_pais("Spain") == "ES"
    assert iso_paises.resolver_iso_pais("Germany") == "DE"
    assert iso_paises.resolver_iso_pais("United Kingdom") == "GB"
    assert iso_paises.resolver_iso_pais("Australia") == "AU"
    assert iso_paises.resolver_iso_pais("Colombia") == "CO"


def test_resolver_iso_pais_insensible_a_mayusculas_y_espacios():
    assert iso_paises.resolver_iso_pais("  germany  ") == "DE"
    assert iso_paises.resolver_iso_pais("SPAIN") == "ES"


def test_resolver_iso_pais_desconocido_devuelve_none():
    assert iso_paises.resolver_iso_pais("Narnia") is None


def test_codigo_espana():
    assert iso_paises.CODIGO_ESPANA_ISO == "ES"
