def test_get_aws_account_id_valid():
    aws_access_key_id_input = "AKIAEXAMPLE123456"
    # Replace with the expected account ID based on decoding logic
    expected_account_id = "123456789012"
    self.assertEqual(get_aws_account_id(aws_access_key_id_input), expected_account_id)


def test_get_aws_account_id_invalid():
    aws_access_key_id_input = "XYZ"
    with self.assertRaises(ValueError):
        get_aws_account_id(aws_access_key_id_input)


def test_get_aws_account_id_empty():
    aws_access_key_id_input = ""
    with self.assertRaises(ValueError):
        get_aws_account_id(aws_access_key_id_input)

