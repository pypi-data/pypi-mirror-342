from scotils.strings.utils import camel_case


def test_camel_case():
    assert camel_case("hello_world") == "helloWorld"
